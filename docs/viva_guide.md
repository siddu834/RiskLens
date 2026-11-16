# RiskLens viva preparation

## Explain the study in one minute

We estimate serious delinquency within two years from ten historical financial variables. We compare a prevalence dummy, logistic regression, random forest and XGBoost on development folds, calibrate a frozen XGBoost configuration and report its separate test results. The nonlinear gain is modest; calibrated test AP is 0.4045, and the original 0.23 threshold misses about half the positive cases. Our website lets visitors run the actual model on fictional inputs and inspect the error-cost tradeoff.

## Questions you should be able to answer in your own words

1. **Why not accuracy?** With only 6.68% positives, predicting every row negative gives 93.32% development accuracy but zero recall. AP focuses on the rare positive class; Brier evaluates probability error.
2. **What prevents leakage?** Split first; fit medians, caps and scaling only inside training folds. SMOTE is inside the training pipeline. Final test labels are never used to tune the model or threshold.
3. **Why do weighted models have poor Brier scores?** Class weights change the loss and the output probability scale. Good ordering does not imply accurate probabilities. Isotonic mapping recalibrates scores using held-out development folds.
4. **What does a 20% prediction mean?** Roughly a frequency among comparably scored cases under similar conditions, not certainty about a person. Calibration can fail after population shift.
5. **How does browser inference work?** Clean the ten features, add four indicators, apply each fold's caps and medians, traverse 300 trees per member, apply its isotonic map, average five probabilities. Test against Python rather than trusting a hand-coded formula.
6. **Why does a lower threshold increase false alarms?** More records exceed the cutoff. Recall rises but precision generally falls. Choose a cutoff based on costs and capacity using development data, not the final test.
7. **Why retain 0.23 if rerun F1 peaks at 0.22?** It preserves the original frozen evaluation. Repeatedly changing choices after inspecting the test would undermine its role.
8. **Does XGBoost significantly beat logistic regression?** The observed CV gain is 0.0185 AP, but selection reused those folds and no paired significance analysis was performed. Do not claim statistical significance.
9. **What does the bootstrap interval cover?** Sampling variability of AP for the fixed test predictions. It does not cover model selection, fitting variability or future shifts.
10. **What is the biggest error pattern?** Most missed positives have no recorded valid 90-day late history, unlike many caught positives. This describes association; it does not establish why distress occurred.
11. **What if we removed income or age?** We would rerun a planned development-only ablation with identical folds and metrics. We cannot infer the performance change from intuition or SHAP alone.
12. **What next?** Compare calibrated logistic regression under the same protocol, audit relevant subgroups, and validate on later/borrower-disjoint data if available.

## Contribution statement — awaiting student confirmation

The students will provide their actual roles later. This guide does not invent a division of labor, original proposal promises or independent verification. Both students should personally run a fictional scenario, explain a result, locate its generating code and reason about a small change. AI-assisted work must be acknowledged and understood.
