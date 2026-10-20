# Midterm Report: Predicting Olympic Success from National Economic Conditions

**Team:** Ahmad Mashhood (ahmadmashhood01), Ethan Westfall (ecwestfa)  
**Course:** IST 707  
**Repository:** https://github.com/ahmadmashhood01/IST.707-PROJECT  
**Notebook:** `notebooks/olympic_economics_split_models.ipynb` (EDA Sections 1 to 11; modeling Sections 19 and 20)  
**Slides:** `notebooks/Olympic Economics - Project Progress.pptx`

---

## Problem

Countries do not compete at the Olympics on equal footing. Wealth, population, health systems, and education all shape how many athletes a nation can develop and how many medals they can win. We ask: given World Bank economic indicators for a country in an Olympic year, how well can we predict that country's medal performance? The answer supports realistic target setting and funding decisions, not just ranking who won the most medals.

---

## Stakeholders and significance

**National Olympic Committees (NOCs)** need defensible medal expectations when negotiating budgets with governments. **Sports ministries** must justify public spending with evidence that links economic capacity to outcomes (including efficiency measures such as medals per athlete or per GDP). **The IOC and Olympic Solidarity** allocate hundreds of millions of dollars per cycle to nations where economic constraints, not lack of talent, limit success[^5]. **Media and analysts** often rank raw medal tables; adjusted views highlight over- and under-performance relative to resources. **Athletes and coaches in developing nations** can use quantitative trends when applying for grants or solidarity support.

If we only predict medals from GDP and population, we repeat decades of economics literature but give policymakers little nuance. Our project adds a broad WDI feature set and machine learning models so stakeholders can see which non-obvious indicators matter alongside classic size and wealth effects.

---

## Related work

Classic work treats Olympic medal totals as a function of population and GDP, often with Tobit or similar models to handle the mass of zero-medal countries[^1]. Johnson and Ali separate participation (winning any medal) from intensity (how many medals)[^2]. Vagenas and Vlachokyriakou emphasize team size as a mediator and add health spending and unemployment[^3]. Recent studies apply ensembles and deep learning, combining GDP, population, team size, and past performance; tree models often favor total GDP over GDP per capita alone[^4].

Our contribution at midterm is a reproducible merge of Olympedia-style medal history with 62 curated WDI indicators, exploratory views aligned to stakeholder questions, and baseline-to-ensemble model comparisons on a fixed 2016 snapshot with held-out countries.

---

## Dataset

| Item | Detail |
| --- | --- |
| Olympic outcomes | Olympedia-derived medal counts by country and year (`Dataset/olympics_data.csv` and merged file)[^olymp]. |
| Economics | World Development Indicators via World Bank DataBank; scraped to `Dataset/WDI_raw_data.csv` with country-year keys[^wdi]. |
| Merged panel | `Dataset/olympic_economics.csv`: 13,584 rows and 74 columns, years 1960 to 2025 in the merge (modeling uses years with WDI coverage and Olympic participation through 2016). |
| Features | After cleaning low-coverage WDI fields, 62 numeric economic indicators plus Olympic fields (medals, athlete counts, codes). |
| Trust | WDI is the standard cross-country source used by governments and researchers; we drop indicators with unreliable reporting flags and exclude columns with very low coverage in our modeling slice. Olympic counts are cross-checkable against official summaries. |

[^olymp]: Olympedia / CRAN olympicAthletes package: https://cran.r-project.org/web/packages/olympicAthletes/index.html  
[^wdi]: World Development Indicators: https://databank.worldbank.org/source/world-development-indicators

**2016 modeling snapshot:** 201 countries in the modeling table (Section 19A), 33 well-covered economic indicators (at least 80% non-missing among those countries), 9 indicators after removing GDP and population columns for the reduced specification. Train/test split: 75% / 25% by country (`random_state=42`), 51 countries in the test set.

All metrics below match the executed notebook outputs (Section 20).

---

## Exploratory data analysis (five statistical analyses)

Each analysis is in `olympic_economics_split_models.ipynb` with plots and tables.

1. **WDI missingness by indicator (Section 3).** Percent missing per economic column after merging shows which indicators are safe for modeling versus which would need heavy imputation that could bias results for low-income countries. This supports requiring at least 80% coverage among 2016 countries before an indicator enters the medal models.

2. **Log-scale distributions of GDP and population (Section 4).** Histograms on log axes show the heavy right tail of global GDP and population, which explains why we scale features for linear models.

3. **Team size vs total medals (Section 6).** Athlete counts correlate strongly with medal totals across the panel (Pearson r about 0.89 on recent Games), consistent with Vagenas et al.[^3] and motivating careful interpretation when attributing success only to economics.

4. **Panel correlations between economics and medals, 1990 to 2016 (Section 8).** Selected WDI variables move with medal counts over time in ways that align with wealth and development literature, though year-to-year noise remains.

5. **2016 stakeholder efficiency snapshot (Section 9).** Medals per athlete and group-level summaries for Rio 2016 highlight over- and under-performers relative to team size and economic tier.

---

## Null / random baseline

Floors on the **same 2016 test countries** as Section 19 (notebook Section 20A).

**Regression (target: total medals)**

| Baseline | R2 | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Predict training-set mean for every test country | -0.004 | 6.78 | 12.21 |
| Random uniform draw between train min and max | -29.31 | 58.62 | 67.07 |

**Classification (target: won any medal, total greater than 0)**

| Baseline | Accuracy | F1 |
| --- | ---: | ---: |
| Always predict no medal (majority class) | 0.608 | 0.000 |

---

## Best models so far

Metrics are on the held-out 2016 test set (51 countries). Source: notebook Section 19E and Section 20C.

### Regression (total medals)

| Model | R2 | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Null: train mean | -0.004 | 6.78 | 12.21 |
| Ridge, all well-covered factors (33 indicators) | 0.673 | 3.71 | 6.97 |
| Ridge, country groups without GDP/population (9 indicators) | 0.171 | 5.87 | 11.10 |
| Random forest (reduced indicators plus group) | 0.479 | 4.37 | 8.80 |
| XGBoost (reduced indicators plus group) | 0.347 | 4.31 | 9.84 |
| Decision tree (depth 6, same features) | -0.526 | 5.73 | 15.05 |

**Best regression model at midterm:** **Ridge regression with all well-covered economic factors** (R2 0.673, MAE 3.71, RMSE 6.97). It beats the null mean baseline and the tree ensembles on this split. Random forest is second among nonlinear models. Section 19C and 19D show predicted-vs-actual plots for the two Ridge setups; Section 20D shows random forest feature importance.

### Classification (any medal)

| Model | Accuracy | F1 |
| --- | ---: | ---: |
| Null: always no medal | 0.608 | 0.000 |
| Logistic regression (reduced factors plus group, balanced classes) | 0.902 | 0.872 |

Confusion matrix on the test set (rows = actual, columns = predicted):

|  | Predicted: no medal | Predicted: any medal |
| --- | ---: | ---: |
| Actual: no medal | 29 | 2 |
| Actual: any medal | 3 | 17 |

Section 20B plots this matrix in the notebook.

---

## Future work

- LightGBM and hyperparameter tuning for RF, XGBoost, and LightGBM on multiple Olympic years, not only 2016.
- PCA and clustering of countries by economic profiles, then cluster-aware models or stratified evaluation.
- Stakeholder deliverables: medals-per-GDP rankings, over/under-performance vs model prediction, and examples for Solidarity-style funding cases.
- Temporal validation: train on earlier Games, test on later ones.
- Optional: separate models for gold count vs total medals and host-nation indicators where data allow.

---

## Problems and challenges

- Missing WDI data for many lower-income countries forced coverage thresholds and median imputation.
- Small effective sample size when using one Olympic year and a 25% holdout; metrics should be interpreted with that limitation.
- Collinearity among GDP, trade, and development indicators complicates linear interpretation; country groups and tree models add complexity.
- Single decision tree overfit (negative test R2); we cap depth and rely more on Ridge and random forest for midterm results.
- Ensembles (XGBoost on this split) did not yet beat the full-factor Ridge model; tuning and multi-year training are planned for the final phase.

---

## References

[^1]: Andrew B. Bernard and Meghan R. Busse, "Who Wins the Olympic Games: Economic Resources and Medal Totals," *Review of Economics and Statistics* 86 (2004): 413-417. https://direct.mit.edu/rest/article-abstract/86/1/413/57461/

[^2]: Daniel K. N. Johnson and Ayfer H. Ali, "Coming to Play or Coming to Win: Participation and Success at the Olympic Games," *SSRN* (2000). https://papers.ssrn.com/sol3/papers.cfm

[^3]: George Vagenas and Eleni Vlachokyriakou, "Olympic Medals and Demo-Economic Factors," *Sport Management Review* 15 (2012): 211-217. https://ideas.repec.org/a/eee/spomar/v15y2012i2p211-217.html

[^4]: "STGCN-LSTM for Olympic Medal Prediction," arXiv (2025). https://arxiv.org/abs/2501.17711

[^5]: International Olympic Committee, Olympic Solidarity. https://www.olympics.com/ioc/olympic-solidarity
