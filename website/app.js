/* Static educational interface; entered profiles are kept only in memory. */
'use strict';
const $ = id => document.getElementById(id);
const pct = (v, digits = 1) => (v * 100).toFixed(digits) + '%';
const num = v => Number(v).toLocaleString('en-US', {maximumFractionDigits: 3});
async function getJSON(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
  return response.json();
}
const fields = [
 ['RevolvingUtilizationOfUnsecuredLines','Revolving credit utilization','Balance / available revolving credit. 0.5 = 50%.',0,100000,.01],
 ['age','Age','Years; 18–110 for this fictional demo.',18,110,1],
 ['NumberOfTime30-59DaysPastDueNotWorse','30–59 days late','Count in the previous two years.',0,98,1],
 ['DebtRatio','Debt-to-income ratio','Monthly debt and living costs / monthly income.',0,100000,.01],
 ['MonthlyIncome','Monthly income','Original dataset units. Leave blank if unknown.',0,10000000,1,true],
 ['NumberOfOpenCreditLinesAndLoans','Open credit lines & loans','Number of open loans and credit lines.',0,100,1],
 ['NumberOfTimes90DaysLate','90+ days late','Count in the previous two years.',0,98,1],
 ['NumberRealEstateLoansOrLines','Real-estate loans','Number of mortgage / real-estate lines.',0,100,1],
 ['NumberOfTime60-89DaysPastDueNotWorse','60–89 days late','Count in the previous two years.',0,98,1],
 ['NumberOfDependents','Dependents','Number of dependents. Blank means unknown.',0,50,1,true]
];
for (const [key, label, help, min, max, step, optional] of fields) {
 const wrap = document.createElement('div'); wrap.className = 'field';
 const lab = document.createElement('label'); lab.htmlFor = key; lab.textContent = label;
 const input = document.createElement('input'); Object.assign(input,{id:key,name:key,type:'number',min:String(min),max:String(max),step:String(step),required:!optional});
 input.setAttribute('aria-describedby', key+'Help');
 const hint = document.createElement('small'); hint.id = key+'Help'; hint.textContent = help;
 wrap.append(lab,input,hint); $('inputFields').append(wrap);
}
const presets = {steady:[.12,52,0,.28,6500,8,0,1,0,2], strained:[.95,38,2,.65,3500,7,1,1,1,2], unknown:[.45,45,1,.4,null,6,0,1,0,null]};
let model, lastPrediction = null, savedScenario = null;
function fillPreset(key) { fields.forEach((f,i) => $(f[0]).value = presets[key][i] ?? ''); document.querySelectorAll('[data-preset]').forEach(b => b.classList.toggle('active',b.dataset.preset===key)); if(model) estimate(); }
function estimate() {
 if (!model || !$('profileForm').reportValidity()) return;
 const input = Object.fromEntries(fields.map(([key]) => [key,$(key).value===''?null:Number($(key).value)]));
 const probability = RiskLens.predict(model,input);
 if (!Number.isFinite(probability)) { $('modelStatus').textContent='Prediction failed. Check the inputs or reload the model.'; return; }
 lastPrediction = {probability,input};
 $('predictionValue').innerHTML = (probability*100).toFixed(1)+'<span>%</span>';
 $('probabilityFill').style.width = probability*100+'%';
 $('predictionDescription').textContent = `Estimated probability for this fictional profile: ${pct(probability)}. This is a model estimate, not an observed outcome.`;
 $('predictionFlag').textContent = probability >= .23 ? 'Flagged for this demonstration' : 'Below the flag threshold';
 $('saveScenario').disabled=false;
 const notes=[];
 for (const key of ['MonthlyIncome', 'NumberOfDependents']) {
   if (input[key] !== null) continue;
   const index = model.features.indexOf(key);
   const medians = model.members.map(member => member.medians[index]);
   const label = fields.find(field => field[0] === key)[1];
   notes.push(label + ' was blank. Its missingness indicator is 1. The five stored fold medians used here are ' + medians.map(num).join(', ') + '.');
 }

 if (fields.filter(f=>f[0].includes('Days')).some(f=>[96,98].includes(input[f[0]]))) notes.push('Late-payment codes 96/98 are treated as missing, with a combined sentinel flag.');
 for(const key of ['RevolvingUtilizationOfUnsecuredLines','DebtRatio']) if(model.members.some(m=>input[key]>m.caps[key])) notes.push(`${fields.find(f=>f[0]===key)[1]} is capped at stored training-fold limits.`);
 notes.push('Changing one field while holding others fixed may create an unrealistic profile; the difference is not a causal effect.');
 $('inputNotes').textContent=notes.join(' ');
 if(savedScenario) {
   const changed=fields.filter(([key])=>input[key]!==savedScenario.input[key]).map(f=>f[1]);
   const delta=(probability-savedScenario.probability)*100;
   $('comparison').textContent=`Saved: ${pct(savedScenario.probability)} → current: ${pct(probability)} (${delta>=0?'+':''}${delta.toFixed(1)} percentage points). ${changed.length?'Changed: '+changed.join(', ')+'.':'Same input profile.'}`;
 }
 $('modelStatus').textContent='Estimate complete. Inputs stay in this browser session.';
 return true;
}
$('profileForm').addEventListener('submit', event => {
 event.preventDefault();
 if (estimate()) {
   $('predictionValue').scrollIntoView({
     block: 'center',
     behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'
   });
 }
});
$('profileForm').addEventListener('input',()=>{lastPrediction=null;$('saveScenario').disabled=true;$('predictionValue').innerHTML='—<span>%</span>';$('predictionFlag').textContent='Estimate again';$('probabilityFill').style.width='0%';$('predictionDescription').textContent='Inputs changed. Select “Estimate probability” to update the result.';document.querySelectorAll('[data-preset]').forEach(b=>b.classList.remove('active'));});
document.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>fillPreset(b.dataset.preset)));
$('saveScenario').addEventListener('click',()=>{if(!lastPrediction)return;savedScenario=structuredClone(lastPrediction);$('comparison').textContent=`Saved ${pct(savedScenario.probability)}. Change an input and estimate again to compare.`;});
fillPreset('steady');
getJSON('data/model.json').then(async data=>{
 if(data.schema_version!==2)throw new Error('Unsupported model schema');
 await Promise.all(data.members.map(async member=>{
   member.trees=(await Promise.all(member.tree_files.map(file=>{
     if(!/^model\/member-[0-4]-part-[0-2]\.json$/.test(file))throw new Error('Invalid model part');
     return getJSON('data/'+file);
   }))).flat();
 }));
 model=data;$('predictButton').disabled=false;$('modelStatus').textContent='Trained model ready. Choose a fictional profile or edit the inputs.';estimate();
}).catch(error=>{$('modelStatus').textContent='Model unavailable. Please reload; no predictions are being generated. '+error.message;});
let thresholds=[];
function updateMetrics() {
 if(!thresholds.length)return;
 const result=thresholds.reduce((best,row)=>Math.abs(row.threshold-Number($('thresholdSlider').value))<Math.abs(best.threshold-Number($('thresholdSlider').value))?row:best);
 $('thresholdValue').textContent=result.threshold.toFixed(2);
 $('precision').textContent=result.tp+result.fp===0?'Undefined':pct(result.precision,2);
 $('recall').textContent=pct(result.recall,2);
 $('f1').textContent=(result.precision+result.recall?2*result.precision*result.recall/(result.precision+result.recall):0).toFixed(4);
 $('flagRate').textContent=pct(result.flag_rate,2);
 for(const key of ['tp','fp','fn','tn'])$(key).textContent=num(result[key]);
 const total=result.tp+result.fp+result.fn+result.tn;
 const caughtPerHundred = Math.round(result.recall * 100);
 const flagExplanation = result.tp + result.fp
   ? 'Of every 100 flagged, about ' + Math.round(result.precision * 100) + ' experienced serious delinquency.'
   : 'No records were flagged, so precision is undefined.';
 $('tradeoff').textContent = 'On development predictions, about ' + caughtPerHundred + ' of every 100 actual cases were caught. ' + flagExplanation;

 if($('costRatio').validity.valid && $('costRatio').value!=='') {
   const ratio=Number($('costRatio').value), cost=r=>ratio*r.fn+r.fp;
   const optimum=thresholds.reduce((a,b)=>cost(b)<cost(a)?b:a);
   $('cost').textContent=(cost(result)/total*1000).toFixed(1);
   $('costOptimum').textContent=`For this assumed ${ratio}:1 ratio, the lowest-cost grid threshold is ${optimum.threshold.toFixed(2)}.`;
 } else { $('cost').textContent='—'; $('costOptimum').textContent='Enter a whole-number cost ratio from 1 to 1,000.'; }
}
$('thresholdSlider').addEventListener('input',updateMetrics);$('costRatio').addEventListener('input',updateMetrics);
document.querySelectorAll('[data-threshold]').forEach(b=>b.addEventListener('click',()=>{$('thresholdSlider').value=b.dataset.threshold;updateMetrics();}));
getJSON('data/threshold_metrics.json').then(data=>{if(!Array.isArray(data)||!data.length)throw new Error('Empty threshold table');thresholds=data;$('thresholdSlider').disabled=false;$('status').textContent='Development OOF data loaded · 101 thresholds · original test reporting stays fixed.';updateMetrics();}).catch(error=>{$('status').textContent=error.message;});
const addRow=(target,values)=>{const row=document.createElement('tr');for(const value of values){const cell=document.createElement('td');cell.textContent=value;row.append(cell);}$(target).append(row);};
getJSON('data/evidence.json').then(data=>{

 data.features.forEach(f=>addRow('featureRows',[fields.find(x=>x[0]===f.feature)?.[1]||f.feature,num(f.missing),num(f.median),num(f.p01),num(f.p99)]));
 Object.entries(data.errors).forEach(([name,g])=>addRow('errorRows',[name,num(g.n),pct(g.median_probability),num(g.median_utilization),pct(g.prior_90day_late_rate)]));
 $('uncertainty').textContent=`95% conditional bootstrap interval for test AP: ${data.test_ap_interval.map(x=>x.toFixed(4)).join('–')} (${data.bootstrap_repetitions} resamples).`;
}).catch(error=>{$('errorRows').textContent='Evidence table unavailable: '+error.message;});
let chartData;
const chartInfo={pr:['Precision–recall','Recall','Precision','At higher recall, precision falls: catching more positive cases brings more false alarms. The dashed baseline is the development prevalence, 6.68%.'],roc:['ROC','False-positive rate','True-positive rate','The model ranks positive cases above negative cases more often than chance. With many negatives, even a small false-positive rate can create many false alarms. The diagonal is chance ranking.'],calibration:['Calibration','Mean predicted probability','Observed positive fraction','Each point groups OOF predictions into one of ten quantile bins. Near the diagonal, predicted probabilities agree with observed frequencies. This is aggregate agreement, not certainty for an individual.']};
function drawChart(kind){
 if(!chartData)return;
 const [title,xLabel,yLabel,explanation]=chartInfo[kind];
 const points=chartData[kind].map(r=>kind==='pr'?[r.recall,r.precision]:kind==='roc'?[r.fpr,r.tpr]:[r.mean_predicted_probability,r.fraction_of_positives]);
 const x=v=>65+v*470,y=v=>300-v*265;
 let svg=`<svg viewBox="0 0 570 360" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">`;
 for(let i=0;i<=5;i++){const t=i/5;svg+=`<path d="M65 ${y(t)}H535 M${x(t)} 35V300" fill="none" stroke="#d9dfd7"/><text x="${x(t)}" y="320" text-anchor="middle">${t.toFixed(1)}</text><text x="52" y="${y(t)+4}" text-anchor="end">${t.toFixed(1)}</text>`;}
 svg+=kind==='pr'?`<path d="M65 ${y(.0668416667)}H535" stroke="#bb542e" stroke-dasharray="6 5"/>`:`<path d="M65 300L535 35" stroke="#bb542e" stroke-dasharray="6 5"/>`;
 svg+=`<polyline points="${points.map(([a,b])=>`${x(a).toFixed(2)},${y(b).toFixed(2)}`).join(' ')}" fill="none" stroke="#17685b" stroke-width="2.5"/>`;
 if(kind==='calibration')for(const[a,b]of points)svg+=`<circle cx="${x(a)}" cy="${y(b)}" r="4" fill="#17685b"/>`;
 svg+=`<text x="300" y="350" text-anchor="middle">${xLabel}</text><text transform="translate(16 170) rotate(-90)" text-anchor="middle">${yLabel}</text></svg>`;
 $('evaluationChart').innerHTML=svg;$('evaluationChart').setAttribute('aria-label',`${title}, development out-of-fold predictions. ${explanation}`);$('chartTitle').textContent=title;$('chartExplanation').textContent=explanation;
 document.querySelectorAll('[data-chart]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.chart===kind)));
}
document.querySelectorAll('[data-chart]').forEach(b=>b.addEventListener('click',()=>drawChart(b.dataset.chart)));
getJSON('data/chart_data.json').then(data=>{chartData=data;drawChart('pr');}).catch(error=>{$('evaluationChart').textContent=error.message;});

getJSON('data/review_capacity.json').then(data => {
  const control = $('reviewBudget');
  function showBudget() {
    const models = data.budgets[control.value];
    $('budgetRows').replaceChildren();
    for (const [name, row] of Object.entries(models)) {
      addRow('budgetRows', [name, ...['reviewed', 'caught', 'missed', 'false_alarms'].map(key => num(row[key]))]);
    }
    const gain = models.XGBoost.caught - models['Logistic regression'].caught;
    const comparison = gain === 0 ? 'Both models catch the same number of cases'
      : (gain > 0 ? 'XGBoost' : 'Logistic regression') + ' catches ' + num(Math.abs(gain)) + ' more cases';
    $('budgetFinding').textContent = comparison + ' with ' + num(models.XGBoost.reviewed) + ' reviews each.';
  }
  control.addEventListener('change', showBudget);
  control.disabled = false;
  showBudget();
}).catch(() => { $('budgetFinding').textContent = 'Review counts could not load. Reload to try again.'; });
