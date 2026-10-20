
# Midterm Report: Predicting Olympic Success from National Economic Conditions

**Team:**  
**Course:** IST 707  
**Repository:** https://github.com/ahmadmashhood01/IST.707-PROJECT  
**Notebook:** `notebooks/olympic_economics_split_models.ipynb` (EDA Sections 1 to 10; modeling Sections 12 to 20)  
**Slides:** `notebooks/Olympic Economics - Project Progress.pptx`

---

## Problem

Countries do not compete at the Olympics with the same resources. Factors such as GDP, population, healthcare, and employment can all influence how many athletes a country can develop and how many medals it can win. Our project looks at whether we can use economic indicators from the World Bank to predict how many medals a country will win at the Olympics.

We also want to understand which economic factors are most closely related to Olympic success. Rather than just ranking countries by total medals, our goal is to see how well countries perform compared to what their economic conditions would suggest. This could help countries set more realistic expectations and better understand how their resources relate to Olympic performance.

---

## Stakeholders and Significance

Several groups could benefit from the results of our project.

**National Olympic Committees (NOCs)** could use our predictions to set realistic medal expectations when planning budgets and requesting funding from their governments. **Sports ministries** could use our findings to better understand how economic conditions relate to Olympic performance and whether countries are making effective use of their resources. Measures such as medals per athlete or medals relative to GDP and population could be useful for these comparisons.

**The International Olympic Committee (IOC) and Olympic Solidarity** provide financial support to countries that may not have the same resources as wealthier nations. Our analysis could help identify countries that are performing below expectations and may benefit from further evaluation or additional support.[^5]

**Sports researchers, media, and analysts** typically compare countries using total medal counts. However, this does not account for differences in population, wealth, or other resources. Comparing actual medal totals to predicted totals could provide another way to evaluate Olympic performance.

**Athletes and coaches in developing countries** could also use these findings when seeking funding, grants, or additional support from their national Olympic committees.

GDP and population have already been studied extensively as predictors of Olympic success. If we only use these two variables, we would be repeating much of the existing research without providing many new insights. Our project expands on this work by including a wider range of World Development Indicators (WDI) and using machine learning to determine which other economic factors may help predict Olympic success.

We are particularly interested in whether indicators outside of GDP, GDP per capita, and population can improve predictions, especially when evaluating participation and medals relative to a country's resources.

---

## Related Work

Previous research has shown that GDP and population are two of the most important factors associated with Olympic medal counts.

Bernard and Busse examined how economic resources relate to Olympic performance, focusing on GDP and population. Their research also used statistical methods to account for countries that do not win any medals.[^1]

Johnson and Ali looked at Olympic participation and success from two perspectives: whether a country wins a medal at all and how many medals it wins. This is similar to our approach of using both classification and regression models.[^2]

Vagenas and Vlachokyriakou expanded on earlier research by looking at additional factors, including team size, healthcare spending, and unemployment. Their work suggests that Olympic success is influenced by more than just the overall size of a country's economy.[^3]

More recent studies have started using machine learning and deep learning models to predict medal counts. These models often combine GDP, population, athlete participation, and previous Olympic results. Some have also found that total GDP can be a stronger predictor than GDP per capita.[^4]

Our project builds on this research by combining historical Olympic data with 62 economic indicators from the World Bank. We are comparing different machine learning models and feature sets to see whether using a wider range of economic factors can improve predictions.

---

## Dataset

We combined historical Olympic results with economic data from the World Bank to create a dataset that connects each country's Olympic performance to its economic conditions.

The Olympic data includes medal counts and athlete participation by country and year. The economic data comes from the World Bank's World Development Indicators, which cover areas such as GDP, population, healthcare, employment, and other development measures.

| Item | Detail |
| --- | --- |
| Olympic outcomes | Olympedia-derived medal counts by country and year (`Dataset/olympics_data.csv` and merged file).[^olymp] |
| Economic data | World Development Indicators from the World Bank, stored in `Dataset/WDI_raw_data.csv`.[^wdi] |
| Merged dataset | `Dataset/olympic_economics.csv`, containing 13,584 rows and 74 columns covering 1960 to 2025. |
| Features | 62 numeric economic indicators after initial cleaning, along with medal counts, athlete counts, and country information. |
| Data reliability | WDI is widely used for international economic research. We removed indicators with very limited coverage and reviewed the available economic data. Olympic results can also be checked against published records. |

One of the biggest challenges with the dataset was missing economic information. Not every country reports every indicator, and some variables have very little data available.

During our initial cleaning, we preserved the rows in the merged dataset and removed economic columns with less than 10% data coverage. For exploratory analysis, we also created a more complete subset of the data. Additional filtering was then applied for modeling.

We also worked on making historical country information more consistent and created additional economic variables, including measures related to child mortality, number of children, trade openness, and climate-related conditions.

For our initial modeling, we focused on the **2016 Rio Olympics**. This allowed us to compare countries from the same Olympic year without having to account for differences between Games.

### 2016 Modeling Dataset

| Item | Value |
| --- | --- |
| Countries | 201 |
| Economic indicators with at least 80% coverage | 33 |
| Indicators in reduced feature set | 9 |
| Training data | 75% |
| Testing data | 25% |
| Countries in test set | 51 |
| Random state | 42 |

We used the same training and testing split for our model comparisons to keep the results consistent. Missing training features were filled using median imputation, and features were standardized for Ridge and logistic regression.

All model results reported below come from the executed notebook, primarily Sections 19 and 20.

---

## Exploratory Data Analysis

Before building our models, we explored the dataset to understand the relationships between economic conditions and Olympic performance. We also looked for missing data, unusual distributions, and potential problems that could affect our models.

We focused on five main analyses.

### 1. Missing Economic Data (Section 3)

We first calculated the percentage of missing values for each economic indicator.

Some indicators were missing data for a large number of countries, which could make them less useful for prediction. This was especially important because countries with fewer economic resources may also have less complete reporting.

After our initial cleaning, we decided to use indicators with at least 80% coverage among the countries in our 2016 modeling dataset.

### 2. GDP and Population Distributions (Section 4)

We examined the distributions of GDP and population to see how much they varied between countries.

Both variables were heavily skewed, with a small number of countries having much larger economies or populations than the rest. We used logarithmic scales to make these differences easier to visualize.

These distributions also showed why feature scaling is useful when working with models such as Ridge regression.

### 3. Team Size vs. Total Medals (Section 6)

We compared the number of athletes each country sent to the Olympics with the number of medals it won.

We found a strong positive correlation, with a Pearson correlation coefficient of approximately **0.89** for recent Olympic Games.

This result makes sense because countries that send more athletes generally have more opportunities to win medals. However, it also suggests that some of the relationship between economic conditions and medal counts may be explained by wealthier countries being able to send larger teams.

### 4. Economic Indicators and Medal Counts Over Time (Section 8)

We looked at correlations between selected economic indicators and medal counts from 1990 to 2016.

Several indicators showed relationships with medal totals that were consistent with previous research on wealth and economic development. However, these relationships were not always consistent from one Olympic year to another.

In our 2016 analysis, **GDP had the strongest positive correlation with total medals (r = 0.864)** among the selected indicators. International tourism arrivals also showed a relatively strong correlation (r = 0.707), while total population had a weaker correlation (r = 0.394).

Other indicators, including private-sector credit, healthcare spending, internet usage, and life expectancy, also showed positive relationships with medal counts. Fertility rate showed a negative correlation.

These results suggest that economic conditions are important, but they do not fully explain Olympic success. It is also important to recognize that correlation does not necessarily mean one factor directly causes another.

### 5. Olympic Performance Relative to Resources (Section 9)

We also examined Olympic performance from a stakeholder perspective using data from the 2016 Rio Olympics.

Instead of only comparing total medal counts, we looked at measures such as medals per athlete and compared performance across economic groups.

This allowed us to identify countries that performed relatively well or poorly compared to their team sizes and economic conditions.

We believe these types of comparisons could be useful for understanding how effectively countries use their available resources.

---

## Null and Random Baselines

Before evaluating our machine learning models, we created baseline predictions to see how well a model could perform without learning relationships between economic indicators and medal counts.

For regression, our target variable was the total number of medals won by each country.

Our first baseline predicted the average medal count from the training set for every country in the test set. We also tested a random baseline that generated medal predictions between the minimum and maximum values in the training data.

### Regression Baselines

| Baseline | R² | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Predict training-set mean | -0.004 | 6.78 | 12.21 |
| Random uniform prediction | -29.31 | 58.62 | 67.07 |

The training-set mean performed much better than the random baseline, but its R² was still slightly negative. This means it did not explain the variation in medal counts among the test countries.

For classification, we wanted to predict whether a country would win at least one medal.

Our baseline always predicted that a country would win no medals, since that was the most common outcome in the test set.

### Classification Baseline

| Baseline | Accuracy | F1 |
| --- | ---: | ---: |
| Always predict no medal | 0.608 | 0.000 |

This baseline achieved an accuracy of 60.8%, but its F1 score was zero because it never correctly predicted a country that won a medal.

These baselines gave us a starting point for determining whether our machine learning models were actually improving predictions.

---

## Best Models So Far

We tested several machine learning models to predict Olympic performance. We approached the problem in two ways:

1. **Regression:** Predicting the total number of medals a country wins.
2. **Classification:** Predicting whether a country wins at least one medal.

All results were evaluated on the same 2016 test set containing 51 countries.

### Regression: Predicting Total Medals

For regression, we tested Ridge regression, decision trees, random forests, and XGBoost.

We also compared two different approaches to selecting economic indicators. The first used all 33 well-covered economic indicators, including GDP and population. The second removed direct GDP and population-related inputs and instead used nine other economic indicators along with country groups based on GDP per capita and population.

| Model | R² | MAE | RMSE |
| --- | ---: | ---: | ---: |
| Null: training mean | -0.004 | 6.78 | 12.21 |
| Ridge (33 economic indicators) | **0.673** | **3.71** | **6.97** |
| Ridge (reduced indicators + country groups) | 0.171 | 5.87 | 11.10 |
| Random forest (reduced indicators + group) | 0.479 | 4.37 | 8.80 |
| XGBoost (reduced indicators + group) | 0.347 | 4.31 | 9.84 |
| Decision tree (depth 6) | -0.526 | 5.73 | 15.05 |

Our best-performing regression model was **Ridge regression using all 33 well-covered economic indicators**.

This model achieved an R² of **0.673**, an MAE of **3.71**, and an RMSE of **6.97**.

The R² value means the model explained approximately 67.3% of the variation in medal counts among the test countries. The MAE means that its predictions were off by about 3.7 medals per country on average.

Compared to the mean-only baseline, the full Ridge model reduced MAE by approximately **45%**.

One of the most interesting results was the difference between the two Ridge models. When we replaced direct GDP and population-related indicators with our reduced feature set and country groups, the R² dropped from 0.673 to 0.171.

This suggests that direct economic scale information provides a large amount of useful information when predicting Olympic medal counts. However, the country groups still contain some information about GDP per capita and population, so this comparison does not completely remove their influence.

The random forest performed relatively well with the reduced feature set, achieving an R² of 0.479. XGBoost also performed better than the baseline, but it did not outperform the random forest.

The decision tree performed the worst, with a negative R² of -0.526. This suggests that the model did not generalize well to the test data, even after limiting its maximum depth to six.

It is important to note that not all models used the same features. Because of this, we cannot say that Ridge regression is always better than the other algorithms. However, it was the best-performing model among the versions we tested.

The notebook includes predicted-versus-actual plots for both Ridge models in Sections 19C and 19D, along with random forest feature importance in Section 20D.

### Classification: Predicting Whether a Country Wins a Medal

For classification, we used logistic regression to predict whether a country would win at least one medal.

The model used our reduced economic indicators along with country groups and balanced class weights.

| Model | Accuracy | F1 |
| --- | ---: | ---: |
| Null: always predict no medal | 0.608 | 0.000 |
| Logistic regression | **0.902** | **0.872** |

Our logistic regression model achieved an accuracy of **90.2%** and an F1 score of **0.872**.

This was a major improvement over the baseline and suggests that economic indicators can be useful for predicting whether a country will win a medal.

We also looked at the confusion matrix to see where the model made correct and incorrect predictions.

#### Confusion Matrix

| Actual / Predicted | No Medal | Any Medal |
| --- | ---: | ---: |
| No medal | 29 | 2 |
| Any medal | 3 | 17 |

Out of the 51 countries in the test set, the model correctly classified **46 countries**.

It incorrectly predicted that two countries would win medals when they did not, and it failed to identify three countries that actually won medals.

Overall, these results suggest that predicting whether a country wins any medals may be easier than predicting the exact number of medals it will win. The F1 score is also important because accuracy alone can be misleading when one class is more common than the other.

The confusion matrix is also displayed in Section 20B of the notebook.

---

## Future Work

We have made progress with our initial models, but there are several areas we want to improve before the final project.

- **Additional models and tuning:** We plan to test LightGBM and tune the hyperparameters of our random forest, XGBoost, and LightGBM models. We also want to train these models using multiple Olympic years instead of only 2016.

- **PCA and clustering:** We want to use Principal Component Analysis (PCA) and clustering to group countries based on similarities in their economic conditions. This could help us determine whether different types of countries follow different patterns of Olympic success.

- **Stakeholder-focused analysis:** We plan to compare actual medal totals with predicted totals to identify countries that are performing above or below expectations. We also want to explore measures such as medals per GDP and examples of countries that could benefit from further evaluation for Olympic funding.

- **Temporal validation:** We want to train models using earlier Olympic Games and test them on later Games. This should give us a better understanding of how well our models could predict future Olympic results.

- **Alternative models and targets:** We want to compare our models against a simpler GDP-and-population-only model and explore transformations of medal counts or models designed specifically for count data. If time allows, we may also build separate models for gold medals and examine whether hosting the Olympics affects medal performance.

---

## Problems and Challenges

We faced several challenges while preparing the data and building our models.

- **Missing economic data:** Many countries, especially lower-income countries, do not have complete data for every World Bank indicator. We addressed this by setting coverage thresholds and using median imputation, but missing data could still affect our results.

- **Small sample size:** Our initial models only used the 2016 Olympics, giving us 201 countries and 51 test observations. Because of this, our results could change depending on which countries are included in the training and testing sets.

- **Correlated economic indicators:** Variables such as GDP, trade, and other development measures are often closely related. This makes it harder to determine the individual importance of each factor, especially in linear models. Our country groups also retain some GDP and population information.

- **Decision tree performance:** Our decision tree had a negative test R², suggesting that it did not generalize well. We limited its depth, but Ridge regression and random forest still performed better in our initial testing.

- **Ensemble model performance:** Random forest and XGBoost did not outperform our full-feature Ridge model. We plan to explore hyperparameter tuning and training on multiple Olympic years to see whether their performance improves.

- **Differences between countries:** A small number of countries win a large share of Olympic medals, which can have a major influence on our models. We also recognize that finding correlations and making accurate predictions does not necessarily explain what causes a country to win more medals.

These challenges have helped us identify where we need to focus during the second half of the project.

---

## Conclusion

Our results so far suggest that economic conditions can help predict Olympic performance.

Our best regression model, Ridge regression with 33 economic indicators, explained approximately **67% of the variation in medal counts** among our 2016 test countries. Our logistic regression model also performed well, correctly predicting whether a country would win a medal for approximately **90% of the test countries**.

One of our biggest findings was how much prediction accuracy decreased when direct GDP and population-related indicators were replaced with country groups and other economic indicators. This supports previous research showing that the size and economic strength of a country are important factors in Olympic success.

However, our analysis also identified relationships between medal counts and other indicators, including tourism, healthcare, and financial development. We want to explore whether these factors can provide additional predictive value beyond GDP and population.

We still need to test our models across multiple Olympic years before making stronger conclusions. Our current results show useful relationships, but they do not establish that changing a particular economic factor would directly improve Olympic performance.

For the remainder of the project, we want to focus on improving our models, testing how well they predict future Olympic results, and creating comparisons that stakeholders could use to evaluate Olympic performance relative to economic resources.

Ultimately, we hope this project provides a more useful way to compare Olympic success than simply ranking countries by medal count.

## Use of AI
We hereby acknowledge that we used ChatGPT to help aid sentence structure and improve language throughout this project. We used AI to generate language when deciding on challenges and stakeholders. We also used AI to help decide the structure of our future work. Last we used chatGPT to help fix our GitHub markdown formatting whereever we felt it was necessary[^chatGPT].

---

## References

[^1]: Andrew B. Bernard and Meghan R. Busse, "Who Wins the Olympic Games: Economic Resources and Medal Totals," *Review of Economics and Statistics* 86 (2004): 413–417. https://direct.mit.edu/rest/article-abstract/86/1/413/57461/

[^2]: Daniel K. N. Johnson and Ayfer H. Ali, "Coming to Play or Coming to Win: Participation and Success at the Olympic Games," *SSRN* (2000). https://papers.ssrn.com/sol3/papers.cfm

[^3]: George Vagenas and Eleni Vlachokyriakou, "Olympic Medals and Demo-Economic Factors," *Sport Management Review* 15 (2012): 211–217. https://ideas.repec.org/a/eee/spomar/v15y2012i2p211-217.html

[^4]: "STGCN-LSTM for Olympic Medal Prediction," *arXiv* (2025). https://arxiv.org/abs/2501.17711

[^5]: International Olympic Committee, Olympic Solidarity. https://www.olympics.com/ioc/olympic-solidarity

[^olymp]: Olympedia / CRAN olympicAthletes package: https://cran.r-project.org/web/packages/olympicAthletes/index.html

[^wdi]: World Development Indicators: https://databank.worldbank.org/source/world-development-indicators

[^chatGPT]: ChatGPT: https://chatgpt.com/
