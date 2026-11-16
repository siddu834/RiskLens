# Improvement log

The project now has verified rerun results, repaired notebooks, explicit evaluation boundaries, a complete website build and seven regression checks. These changes improve reliability and presentation; they do not establish a predictive improvement.

| Change | Interview value | Evidence |
|---|---|---|
| Repair sentinel checks and preprocessing descriptions | Explain the exact feature transformation | Full preprocessing notebook rerun plus regression tests |
| Separate original reporting threshold from new development optimum | Defend threshold policy without test-driven tuning | Original reporting 0.23; rerun F1 optimum 0.22; illustrative cost optimum 0.09 |
| Export computed metrics and CV tables | Reduce stale or manually copied results | Final metrics regenerated; new CV export cells checked with recovered run summaries |
| Clarify base-model SHAP scope | Avoid explaining the wrong fitted predictor | SHAP notebook rerun; final ensemble distinction documented |
| Package all figures and strict JSON | Deliver a usable evaluation demo | Build validation and browser image checks |
| Generate website test summary from saved metrics | Keep displayed results consistent | Build reads final_test_metrics.json |
| Add tests and automated-check configuration | Demonstrate maintainability | Seven local regression checks; remote CI remains unverified |
| Add notebook runner and bound CPU workers | Make reproduction easier on a laptop | Nine notebooks completed; shipped Windows runner smoke test exits 0 |
| Audit duplicate feature profiles | Discuss validation limitations honestly | 173 overlapping test profiles; subset sensitivity metrics recorded |
| Preserve original results and document rerun differences | Distinguish replication from claimed improvement | Reproduction report, source hashes and timings |
| Add quantitative website comparison and conclusion | Explain modest ranking lift separately from calibration | CV gain 0.0185; fixed-model test AP 0.4045; evaluation boundaries stated |
| Add accessible threshold feedback and relative-cost illustration | Demonstrate a useful interaction rather than a decorative control | Keyboard/browser checks at five thresholds; mobile layout check |
| Add requested JSON exports and download links | Make the displayed analysis inspectable | Build refreshes public schemas and verifies their paths |
| Reproduce from a clean source directory | Detect dependence on hidden generated state | Split, preprocessing and final evaluation rerun; metrics match within 1e-8 |
| Reconcile stale notebook prose and remove personal paths from saved outputs | Keep the story consistent with computed evidence | Updated XGBoost results and test-selection wording; targeted source scan |

## Remaining work

GitHub write access was confirmed on 16 November 2026 and the review branch was created. Live Pages and remote CI remain unverified until the prepared changes are published and deployed.

Further experiments should use development data only: compare weighted/unweighted XGBoost, sigmoid/isotonic calibration, uncertainty intervals, and representative error slices. For an ML engineering application, add a saved final pipeline with input validation and a tested inference interface. None of these extensions is claimed as complete.

## ES335 redesign — 16 November 2026

Replaced the generic dark report with a responsive research site and real browser-side prediction lab. Exported the frozen five-model XGBoost/isotonic ensemble with all preprocessing; validated 200 synthetic and 30,000 test predictions against Python. Added fictional presets, missing-value handling, saved-scenario comparisons, cost-sensitive threshold exploration, ROC/PR/calibration chart selection, full test-error summaries and a conditional AP bootstrap interval. Added rubric mapping, source citations, updated reproduction evidence and viva questions. No new model or threshold was chosen using test outcomes. Student contributions and original-proposal alignment remain for the students to confirm.
