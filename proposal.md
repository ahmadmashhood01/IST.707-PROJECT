# Predicting Olympic Success from National Economic Conditions


## Contributors

Point of Contact?
Ethan Westfall, GitHub: ecwestfa, ecwestfa@syr.edu; Ahmad Mashhood, GitHub: ahmadmashhood01, ahmashho@syr.edu


## Introduction

We want to find out whether a country's wealth and economic health help predict how many Olympic medals its athletes win, by matching year-by-year medal records for about 150 countries with World Bank indicators from 1960 to 2025 covering income, poverty, health, education, and labor. Unlike prior studies that rely on simple models using only population and GDP, we will apply machine learning to 62 economic indicators paired with our year-by-year medal dataset (medal_table_summary.csv), which can capture complex patterns and rank which factors matter most. 

Prior work shows GDP and population already explain much of medal variation[^1], so we expect a broader indicator set and more flexible models to improve on that baseline. The results can help Olympic committees and sports ministries set realistic medal targets, guide IOC funding to countries limited by economic constraints rather than talent, and give developing nations evidence to support sports investment.


## Literature Review

Research consistently links national economic strength to Olympic success. Members of the National Bureau of Economic Research, Bernard and Busse (2004) modeled medal share from 1960 to 1996 as a function of population and GDP per capita using Tobit regression (a statistical model with a 0 limit), finding that total GDP is the strongest predictor of Olympic success. Their model accurately forecast the 2000 Sydney Games using the sample from their prior research[^1]. Doctors of Economics, Johnson and Ali (2000) showed that economic factors affect both whether a country wins any medals and how many it wins[^2]. Researchers from the University of Athens, Vagenas and Vlachokyriakou (2012) found that team size mediates much of the GDP-medals relationship, while health spending, unemployment, and GDP growth also contribute[^3]. Later studies add host-nation status and past performance as key predictors, with prior medal counts often the strongest signal of future success.

Recent work has begun applying machine learning. Ensemble models (XGBoost, LightGBM) and deep learning architectures (CNN-LSTM, STGCN-LSTM) integrate GDP, population, team size, and historical performance to predict medal totals. Applied studies using World Bank indicators report R² values of 75 to 79% for recent Games, with total GDP outperforming GDP per capita alone in tree-based models[^4].

Three gaps motivate our project. First, most studies rely on simple linear models that miss nonlinear effects and interactions. Second, few combine a wide set of economic indicators (health, education, poverty, inflation) in one framework. Third, results are rarely presented in a form useful to policymakers who need interpretable, country-level predictions. We address these by merging year-by-year medal data with 62 World Bank indicators and applying interpretable machine learning models that report both accuracy and feature importance.


### Stakeholders and Their Needs

*National Olympic Committees (NOCs)* - target and allocate budgets. Depend on government funding; must set medal and adjusted medal expectations based on economic capacity.

*Government sports ministries* - Must justify public sports spending to legislatures and voters using evidence linking economic investment to Olympic outcomes; efficiency metrics (e.g., medals per GDP).  

*IOC / Olympic Solidarity* - Distributes around 590M to 650M USD per cycle to support athlete development in economically or athletically deprived nations[^5]. They also identify countries where economic constraints, not talent, are the primary barrier to success.

*Sports media and analysts* - Rank countries by raw medal counts without economic context. Adjusted rankings will highlight over- and under-performers relative to economic resources.
                           
*Athletes and coaches (developing nations)* - Countries are lacking access to training infrastructure and international competition. Quantitative evidence links economic development to Olympic improvement for grant applications.


## Data and Methods

Both data sources can be found through the GitHub link:
https://github.com/ahmadmashhood01/IST.707-PROJECT.


### Data Source 1

Two main data sources were obtained as prerequisites to starting this research project. The first source is the primary measure for determining Olympic success. It contains a historical archive of all countries’ medals from 1896 to the present day.

**Dataset 1**: https://cran.r-project.org/web/packages/olympicAthletes/index.html.

This dataset comes from Olympedia.org, the official online archive for past Olympic events. It has been peer-reviewed and can be cross-referenced with other datasets. The dataset includes 11 columns and 1930 rows, and it is well labeled with metadata. This dataset includes medal counts for each country that has won a medal in any modern Olympics. The rows are well marked with the year and Olympic edition/season that a country’s medals are from.


### Data Source 2

The second data source compiles economic measures into counts, scores and indexes, monetary totals, percentages, and rates. The dataset is compiled using these measures for each country and each individual year that country has been monitored in the dataset, from 1960 to the present. The dataset can be found from the World Bank Group:

**Dataset 2**: https://databank.worldbank.org/source/world-development-indicators.

This link connects to the World Bank Group’s Data Bank, where the World Development Indicators database is listed. This database is how we will measure economic success and growth/decline. We need to sort individual countries, necessary columns, and years by scraping the data. While scraping, we used Python to combine results with countries by year and give them a primary ID. The CSV file from the web scrape is on GitHub, linked at the top of the Data section above.

The data is trusted by national governments, economists, and researchers to track economic development. This does not come without any concerns. Many variables come directly from a country's interpretation of reported numbers that may be falsified. However, the dataset uses expanded metadata with information blocks to mark these instances. As a safety precaution for research reliability, we will be leaving out these variables. 

We still needed to cut down the economic measures, so we factored in the specific variables we researched from similar economic analysis projects[^6][^7][^18]. We decided on 62 integer/float variables, paired up with each country/country code by year. This leaves our dataset with 66 columns and 9381 rows. All individual columns and categories are in our Data Index, listed in our GitHub.


## Methods

The first step to run this project will be data cleaning. To do this, we merged the data on country code and year. Once the data is clean, we will progress to the next phase of our project, exploratory data analysis. Here we will preprocess and transform the variables in the economic dataset. This will also include removing variables that may be irrelevant to the rest of our research. Transformed variables will be scaled or binned. 

After completing our preprocessing step, we will start our machine learning process.  The training process will combine the improvement of countries both on the Olympic and economic levels. We will try a couple of different training models (Logistic Regression and Clusters, Decision Trees, etc.). We will then evaluate and improve our model, attempting to not overfit our model. We will try to use multiple models and compare scores instead of just looking at accuracy, which can be a false predictor of a model’s success.

Lastly, we will use our models to predict key interests of our stakeholders. We will need to understand why countries are actually performing poorly or well based on economic factors. This cannot just predict the more successful countries, as many stakeholders will want to know what is holding them back, not what factors stakeholders are doing right. These measures might be unattainable for smaller, less wealthy stakeholders. The Olympic Committees need to know how different economic factors affect performance to confirm they are donating to the right institutions/projects.


## Project Plan

| **Period** | **Activity** | **Milestone** |
| --- | --- | --- |
| 9/16 - 9/22 | Row 1, Col 2 | Row 1, Col 3 |
| 9-23, 9-29 | Row 2, Col 2 | Row 2, Col 3 |
| 9/16 - 9/22 | Row 1, Col 2 | Row 1, Col 3 |
| 9-23, 9-29 | Row 2, Col 2 | Row 2, Col 3 |
| 9/16 - 9/22 | Row 1, Col 2 | Row 1, Col 3 |
| 9-23, 9-29 | Row 2, Col 2 | Row 2, Col 3 |
| 9/16 - 9/22 | Row 1, Col 2 | Row 1, Col 3 |
| 9-23, 9-29 | Row 2, Col 2 | Row 2, Col 3 |
| 9/16 - 9/22 | Row 1, Col 2 | Row 1, Col 3 |
| 9-23, 9-29 | Row 2, Col 2 | Row 2, Col 3 |

## Risks

A large risk comes with handling missing data in the economics dataset. Since there are so many nulls, we will have to carefully decide where it makes sense to drop and fill in data. Since many third-world countries are missing data, we do not want to misinterpret the results for a large group of countries. 

Another concern is not properly representing our data due to overfitting or underfitting. Since the Olympic dataset is limited, we must be very careful to accurately predict growth and declines. Moreover, we don't want to misinterpret years negatively affecting a country, such as years with wars, global crises, etc. Our data is vast in terms of information but lacks longevity; not overfitting will be very difficult when analyzing trends over time in a limited timeframe. 

### Sources

[^1]: Andrew B. Bernard and Meghan R. Busse, "Who Wins the Olympic Games: Economic
Resources and Medal Totals," *Review of Economics and Statistics 86* (2004): 413-417. 
https://direct.mit.edu/rest/article-abstract/86/1/413/57461/Who-Wins-the-Olympic-Games-Economic-Resources.

[^2]: Daniel K. N. Johnson and Ayfer H. Ali, "Coming to Play or Coming to Win: Participation
And Success at the Olympic Games," *SSRN* (2000). https://papers.ssrn.com/sol3/papers.cfm?

[^3]: George Vagenas and Eleni Vlachokyriakou, "Olympic Medals and Demo-Economic
Factors: Novel Predictors, the Ex-Host Effect, the Exact Role of Team Size, and the
'Population- GDP' Model Revisited," *Sport Management Review 15* (2012): 211-217. 
https://ideas.repec.org/a/eee/spomar/v15y2012i2p211-217.html.

[^4]: "STGCN-LSTM for Olympic Medal Prediction: Dynamic Power Modeling and Causal
Policy Optimization," arXiv (2025). https://arxiv.org/abs/2501.17711.

[^5]: *International Olympic Committee*, "Olympic Solidarity" and "Funding." 
https://www.olympics.com/ioc/olympic-solidarity.

[^6]: Konstantin M. Wacker et al., “Leveraging Growth Regressions for Country Analysis”,
*Policy Research Working Paper*. (2024) https://documents1.worldbank.org/curated/
en/.pdf.

[^7]: Alin Mirestean and Charalambos Tsangarides, “Growth Determinants Revisited,” *IMF
Working Paper* (2009). https://www.imf.org/-/media/websites/imf/imported-full-text-
pdf/external/pubs/ft/wp/2009/_wp09268.pdf.

[^8]: Gernot Doppelhofer et al., “Determinants of Long-Term Growth: A Bayesian Averaging
of Classical Estimates (BACE) Approach,” *National Bureau of Economic Research*
(2000)

