# Phases 12–14: delivery and verification

## Website

The source is `website/`; `python scripts/build_site.py` produces the self-contained `site/` deployment bundle with figures and saved final-test results. The build also refreshes `metrics_summary.json`, `roc_pr.json` and `calibration.json` from notebook exports. `threshold_metrics.json` contains 101 development out-of-fold threshold rows. Legacy filenames remain for notebook compatibility.

The page follows the requested section order. The slider reports TP, FP, FN, TN, precision, recall, F1, flag rate and illustrative relative cost per 1,000 records. Its range is 0–1 in steps of 0.01, using the nearest saved row. It is disabled until data loads, announces updates for assistive technology, and reports loading failures.

## GitHub Pages deployment

GitHub write access was confirmed on 16 November 2026 after reconnecting the repository owner account. The review branch is improve/resume-readiness. Deployment and live verification are pending.

Deployment steps:

1. Publish the prepared changes on a review branch and review the diff.
2. In repository Settings → Pages, select **GitHub Actions** as the source.
3. Merge the reviewed changes to `main`, or manually run the Deploy RiskLens Website workflow from the reviewed branch if the environment permits it.
4. Wait for successful deployment. The workflow builds and uploads `site/`; no `/website` branch-folder selection is needed.
5. Open https://siddu834.github.io/RiskLens/ in a private browser window. Check all sections, images, links, and slider values at 0, 0.23, 0.50 and 1. Verify requests have no missing assets.

The live URL and private-window checks remain incomplete until deployment succeeds. Do not present the intended address as a working demo on a resume yet.

## Reproducibility and narrative

README documents data access, Python setup, split, seed, notebook order, metric definition and results. The conclusion distinguishes CV selection, calibration and frozen-model test evaluation. It labels modest lift, errors, untested calibrated logistic regression, dataset overlap and fairness limitations. Codex assistance is disclosed.

The supplied phase list is the alignment reference. The original proposal was not supplied separately, so exact promise-by-promise alignment with that document has not been verified.

## Local checks on 15 November 2026

- Seven preprocessing/reporting tests passed; site build validated strict JSON and referenced assets; JavaScript syntax and Git whitespace checks passed.
- Browser interaction verified thresholds 0, 0.23, 0.24, 0.50 and 1. At 0: TP 8,021, FN 0, FP 111,979. At 0.50: TP 1,455, FN 6,566, FP 931. At 1: TP 2, FN 8,019, FP 0. An isotonic probability can equal 1, so the endpoint need not flag zero records.
- All five figures loaded. At a 390-pixel mobile viewport the page did not overflow horizontally. Keyboard interaction and status updates worked.
- A targeted scan of 55 tracked/publishable source files found no personal absolute paths, credential filenames, private-key headers, or recognizable GitHub/AWS token patterns. This is not a comprehensive secret-history audit.
- Seed review confirmed the stratified split, shuffled CV, randomized search, SMOTE and stochastic model fits use 42 (directly or via `RANDOM_SEED`). Deterministic inner calibration folds do not require a seed.
- Local `git clone` failed in the Windows Git helper with access denied. A source snapshot was extracted into a clean directory, with raw source data copied separately. This is a clean-copy test, not verification of cloning the unpublished changes from GitHub.
- In that clean copy, notebooks 00, 02 and 07 completed with the existing validated environment and the runner exited 0. All final numeric metrics matched within `1e-8`. A nonfatal joblib cleanup warning was observed; details and scope are in the reproduction report.
- A new Python 3.13 environment was created. Installation from `requirements.txt` and `requirements-checks.txt` was attempted twice: the first failed on package-host DNS lookup, and the second resolved dependencies and downloaded most packages before a remote connection reset. Installation did not complete. Consequently, fresh-install execution and the full fresh-clone checkpoint remain **incomplete**, despite the successful clean-copy check. Retry the documented installation on a working connection; do not treat this as a verified fresh-environment run.

## Checkpoint status

| Phase | Completed | Still incomplete |
|---|---|---|
| 12 | Website, requested data files, useful interaction, mobile/browser checks, GitHub link, deployment workflow | Remote publication, live URL and private-window live test |
| 13 | README, seed review, targeted secret/path scan, clean-source reproduction of final metrics | Successful fresh dependency installation and remote fresh-clone test |
| 14 | Quantitative conclusion, errors and limitations, cautious claims, rubric section alignment, AI disclosure | Exact alignment with an original proposal not supplied to this task |

GitHub supports branch publishing from root or `/docs`, not an arbitrary `/website` folder. This project uses the Actions workflow instead. See [GitHub’s publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
