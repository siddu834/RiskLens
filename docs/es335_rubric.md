# ES335 evidence map

Based on the two course guide/submission PDFs supplied by the student on 16 November 2026. These documents define the rubric; they are not authorization to submit a course form or expose private student information. The user's request adds a real input-based predictor, which the rubric does not explicitly require.

| Criterion | Points | Concrete evidence |
|---|---:|---|
| Problem formulation and scope | 10 | Website question: row unit, two-year target, baseline snapshot assumption, historical-data scope |
| Data understanding | 10 | Dataset size, class prevalence, feature table, missingness, sentinel values, duplicate-profile audit |
| Preprocessing and statistical reasoning | 10 | Training-fold caps and medians, missingness flags, pipeline scaling, leakage tests |
| Baselines and method selection | 15 | Dummy, logistic, RF, XGBoost; objectives and tradeoffs; calibration and imbalance experiments |
| Evaluation design and metrics | 20 | Seed-42 stratified 80/20 split, five-fold development CV, frozen test, AP definition, Brier and confusion metrics, selection caveat |
| Results, errors and limitations | 10 | Numerical comparison, all-test error audit, conditional bootstrap interval, temporal/duplicate/fairness limits |
| Reproducibility and integrity | 5 | README, pinned dependencies, exporter, tests, source hash, raw-data exclusion; fresh final-model reproduction |
| Published interactive website | 10 | Responsive GitHub Pages research site, clear navigation, evidence charts and reproduction links |
| Useful interaction | 5 | Actual browser model, fictional profiles, scenario comparison, threshold and cost explorer, chart switching |
| Individual understanding and defense | 5 | Viva guide prepared; each student's genuine contribution and understanding must be supplied/demonstrated |

## Remaining student-owned items

- Confirm how the final question matches the submitted proposal; the original proposal has not been supplied.
- Provide an accurate contribution statement for both students. Do not claim someone performed an analysis solely because it appears in the repository.
- Review the AI disclosure and verify important outputs independently; be ready to explain preprocessing, calibration, evaluation, errors and a small change.
- Submit the two final links through the course portal before the PDF's deadline: 17 November 2026, 11:59 PM IST. A working deployment does not itself submit the assignment.

No grade is guaranteed. The ES678 LaTeX paper requirement does not apply to ES335. Deep learning is not required. A backend prediction API is not required; this site's real model runs statically in the browser.
