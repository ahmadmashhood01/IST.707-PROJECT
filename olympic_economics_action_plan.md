# Olympic Economics: Final Project Action Plan

This plan builds on the existing notebook and incorporates the final report and presentation rubric. The proposal has not yet been incorporated. Experimental rigor, evaluation, and discussion account for 65% of both the report and presentation scores.

The five checkpoints specify what to send back for review before proceeding.

## Step 1: Organize the project and incorporate midterm feedback

- Keep the existing midterm report structure.
- Create a checklist of instructor comments and the action needed for each.
- Assign an owner and reviewer to each major task.
- Ensure every member makes meaningful repository contributions weekly.
- Start an experiment log with these columns: experiment, question, features, model, tuning space, validation, metrics, and finding.

**Finish when:** Every instructor comment has an assigned action and the team has a shared task list.

## Step 2: Define the final prediction task

**Primary question:** Which economic factors help predict Olympic medal totals beyond national wealth and population?

Use total medals as the primary target. Keep any-medal versus no-medal classification as a secondary task if time permits.

Confirm:

- Whether the primary analysis covers Summer Olympics only, consistent with the 2016 benchmark.
- The country-edition observation unit.
- How team medals are counted.
- How historical countries are handled.
- Which columns contain economic scores and how they were calculated.
- Whether the intended use is forecasting before the Games or explaining completed Games.

Keep athlete count and event entries outside the primary economics-only model. Add them in a separate experiment because they change the question to performance conditional on participation.

**Finish when:** The target, eligible observations, predictors, and intended use are documented.

## Step 3: Audit the data and summarize EDA

Check duplicates, country mappings, missing targets, economic coverage, and score ranges. Distinguish zero medals from missing outcomes and nonparticipation.

Fix two notebook issues:

- GDP-per-capita group labels use a $30,000 boundary while the code uses $40,000.
- The substring filter for GDP and population removes indicators beyond size measures, including health expenditure expressed as a percentage of GDP. Replace it with an explicit variable list.

### Existing EDA summary

The notebook's saved outputs report:

- 13,584 merged rows and 74 original columns.
- Economic data spanning 1960-2025; 2,715 Olympic observations spanning 1960-2016.
- 1,824 Olympic observations in the 1990-2016 window.
- Eight economic indicators removed below 10% coverage, leaving 54.
- Fifteen retained indicators missing for more than half of the 1990-2016 Olympic panel.
- Only 39% of Olympic observations have medals; the median medal count is zero.
- Athlete count and medals have a Pearson correlation of approximately 0.887 in the 1990+ observations.
- In the eligible 2016 sample, medal correlations are approximately 0.864 with GDP, 0.394 with population, and 0.186 with GDP per capita.

These are descriptive associations. Confirm that final analyses use your scored economic columns: the supplied notebook displays raw indicators, including mortality and inflation.

### Five statistical analyses for the report

1. Medal distribution and zero-medal share.
2. Economic missingness by indicator and country group.
3. Economic-score correlation heatmap.
4. Economic associations with medals, including wealth and population.
5. Participation versus medals and why participation is analyzed separately.

Introduce every analysis with what it shows and why it matters. Prefer the final analysis sample and clearly label broader historical EDA.

### Checkpoint 1: Before finalizing the modeling dataset

**Send back:**

- Updated notebook.
- Dataset shape, edition list, and duplicate-check results.
- Score definitions or scoring code.
- Missingness table.
- Five selected EDA outputs.
- Midterm report and instructor feedback, if available.

**Review focus:** Sample selection, score consistency, missingness decisions, EDA interpretation, and alignment between the question and available data.

## Step 4: Lock validation and baselines

Use earlier Summer editions to train and later editions to validate with expanding training windows. Keep all countries from an edition together.

Within each outer training window, tune using earlier-to-later inner validation splits. Fit imputation, scaling, feature screening, data-estimated score transformations, and PCA within training folds.

Since 2016 outcomes have already been examined, describe 2016 as an existing benchmark rather than an untouched final test.

Use:

- **RMSE:** Primary metric if large medal-count errors matter most.
- **MAE:** Typical absolute error in medals.
- **R-squared:** Performance relative to variation in the target.

Report fold-level results and their mean and spread. Do not randomly split pooled country-year rows for the main future-edition evaluation.

Baselines:

- Training mean.
- Training median.
- Previous same-season Olympic medal total, where available.

For incomplete historical records, document a persistence-baseline fallback or compare all models on the same eligible subset.

**Finish when:** Saved split assignments and baseline scores are available for reuse.

## Step 5: Define shared feature sets

| Set | Predictors | Purpose |
|---|---|---|
| A | Wealth and population | Establish the economic-size benchmark |
| B | Other economic scores | Assess broader conditions alone |
| C | A + B | Measure added value beyond wealth and population |
| D | C + participation measures | Assess delegation-size information |

Exclude country IDs, medal components, and outcome-derived predictors. Use C for the primary family comparison. Keep groups mainly descriptive or use them in a sensitivity analysis; groups retain indirect wealth/population information.

### Checkpoint 2: Before large tuning runs

**Send back:** Validation code, counts per fold, baseline results, explicit feature lists, preprocessing pipeline, and proposed tuning ranges.

**Review focus:** Leakage, temporal consistency, baseline strength, comparable samples, and feasible tuning with the available editions.

## Step 6: Tune Ridge

1. Impute and standardize inside training folds.
2. Search alpha over a broad logarithmic range.
3. Expand the range if the optimum lies at an edge.
4. Compare feature sets A, B, and C.
5. Inspect training and validation errors.
6. Examine residuals for zero-medal countries and major medal winners.
7. Record coefficient signs and rankings across outer folds.

The earlier all-factor Ridge result (R-squared 0.673, MAE 3.708, RMSE 6.968) is a historical reference from a 2016 country split. Do not directly compare it with scores from another evaluation design.

**Finish when:** A tuned benchmark, tuning plot, residual diagnostics, and coefficient stability summary are available.

## Step 7: Build Lasso and PCA comparisons

### Lasso

- Reuse Ridge's preprocessing and validation folds.
- Tune alpha systematically and check convergence.
- Record retained variables, signs, and selection frequency across folds.
- Explain when correlated indicators substitute for one another.

### PCA

- Fit PCA on imputed, standardized scores inside the pipeline.
- Inspect the scree plot, explained variance, and component loadings.
- Tune component count and Ridge alpha jointly for PCA + Ridge.
- Compare with Ridge on original scores.
- Consider retaining wealth/population controls outside PCA while reducing the other scores.

High explained variance does not establish predictive value. Validate component count using prediction performance. Component signs are arbitrary, even when all input scores have higher-is-better orientation.

### Checkpoint 3: After Ridge, Lasso, and PCA

**Send back:** Search ranges and selected parameters; fold results; Ridge coefficients; Lasso selection frequencies; PCA scree plot and loadings; prediction/residual plots; warnings.

**Review focus:** Regularization strength, unstable predictors, PCA usefulness, and justified revisions.

## Step 8: Tune trees, forests, and SVR

Use identical observations, folds, feature set C, and metrics.

| Model | Main tuning parameters | Evidence to retain |
|---|---|---|
| Decision tree | Depth, minimum leaf size, pruning strength | Training/validation gap and shallow tree |
| Random forest | Features per split, leaf size, depth; enough trees for stability | Validation errors and permutation importance |
| RBF support vector regression | C, epsilon, gamma | Tuning results and comparison with other families |

Scale for SVR; trees generally do not require scaling. Document search spaces, budgets, and final settings. Retain underperforming results when they teach something.

**Why SVR is included:** Ridge and Lasso are one broad family, PCA is a transformation, and decision trees and forests are related. SVR gives a clearly distinct kernel-based family to support the rubric's three-family guideline.

## Step 9: Complete the experiment matrix

The rubric suggests approximately 8-12 documented experiments, with quality more important than a quota.

| Run | Experiment | Question |
|---|---|---|
| 1 | Ridge, A | How much does size explain? |
| 2 | Ridge, B | How informative are other scores alone? |
| 3 | Ridge, C | What do other scores add beyond size? |
| 4 | Lasso, C | Can fewer predictors perform similarly? |
| 5 | PCA + Ridge | Does dimension reduction help? |
| 6 | Decision tree, C | Are simple thresholds useful? |
| 7 | Random forest, C | Do nonlinear interactions improve prediction? |
| 8 | SVR, C | Does a kernel-based model help? |
| 9 | Leading model, transformed target | Does target skew explain errors? |
| 10 | Leading model, D | What does participation add? |

Each row is a documented experiment with appropriate tuning, not one arbitrary parameter setting. Baselines are additional. Evaluate transformed targets back in medal units and inspect inverse-transformation bias.

## Step 10: Diagnose leading models

- Compare results across editions.
- Check zero-medal and high-medal country errors.
- Examine error across wealth/population strata.
- Test sensitivity to dominant medal-winning countries without automatically dropping them.
- Compare coefficient stability, Lasso selection, and forest permutation importance.
- Check whether differences are consistent across folds.
- If estimating uncertainty, respect repeated observations rather than treating country-edition rows as independent.

If classification remains in scope, compare tuned logistic regression, decision-tree, and random-forest classifiers on identical classification folds. Report precision, recall, F1, balanced accuracy, PR-AUC, and confusion matrices; tune thresholds on validation data.

### Checkpoint 4: Before declaring the final model

**Send back:** Complete experiment table, fold metrics, out-of-fold predictions, subgroup errors, importance/coefficient outputs, and your proposed winner with an explanation.

**Review focus:** Whether the winner is defensible, whether another targeted experiment is necessary, and which economic conclusions are supported.

## Step 11: Write the discussion

For every major finding, explain:

1. What happened?
2. What evidence supports it?
3. Why might it have happened?
4. What alternative explanation remains?
5. What does it mean for stakeholders?

Hypotheses to investigate, not assume:

- Ridge may benefit from correlated predictors and limited sample size.
- Forests may capture interactions but struggle with rare extreme medal totals.
- Group models may lose continuous information and have too little training data.
- Participation may improve prediction while absorbing part of the economic relationship.

Distinguish prediction from causation. Report dead ends and surprises honestly. Explain whether the model is useful, for whom, and under what conditions.

## Step 12: Assemble report and presentation separately

### Report

Revise existing midterm sections rather than restarting:

- Problem and stakeholders.
- Related work with GitHub Markdown footnotes.
- Dataset provenance and preprocessing.
- Five explained statistical analyses.
- Null baselines and best-model evaluation.
- Problems and challenges.

Add experiments, discussion, limitations, and future work. Explain changes of course and visibly address instructor feedback.

### Presentation

Suggested 12-slide structure:

1. Context and changes since midterm.
2. Dataset and baseline recap.
3. Validation design.
4-6. Experiments and model comparisons.
7. Best-model performance.
8-10. Why it worked, errors, and economic findings.
11. Limitations and future work.
12. Takeaways and Q&A.

Target 10-12 minutes of speaking, leaving Q&A within the required 12-15 minutes. Every member must present a meaningful portion. Keep detailed EDA and related work in the report; emphasize results and discussion in the talk.

### Checkpoint 5: Before submission

**Send back:** Draft final_report.md, exported report PDF, slide deck, supporting notebooks, instructor-feedback checklist, speaking assignments, and rehearsal timing.

**Review focus:** Rubric coverage, unsupported claims, figure clarity, consistency, discussion depth, and presentation pacing.

## Step 13: Submission checklist

- [ ] Save final_report.md at the project repository root.
- [ ] Export final_report.pdf.
- [ ] Include supporting Jupyter notebooks.
- [ ] Link to the data or explain access; do not submit data directly.
- [ ] Commit the slide copy, such as final_slides.pdf.
- [ ] Have the point of contact upload required files to Blackboard.
- [ ] Confirm attendance and meaningful speaking roles for every member.
- [ ] Prepare answers about validation, tuning, baselines, model behavior, and limitations.
- [ ] Each student prepares to ask at least one question of another group.

**Start with Steps 1-3 and return at Checkpoint 1.** Resolve data and scoring issues before they affect every model.
