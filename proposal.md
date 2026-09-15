#Predicting Olympic Success from National Economic Conditions

##Contributors

Point of Contact?
Ethan Westfall, GitHub: ecwestfa, ecwestfa@syr.edu
Ahmad Mashhood, GitHub: ahmadmashhood01, ahmashho@syr.edu

##Introduction

We want to find out whether a country's wealth and economic health help predict how many Olympic medals its athletes win, by matching year-by-year medal records for about 150 countries with World Bank indicators from 1960 to 2025 covering income, poverty, health, education, and labor. Unlike prior studies that rely on simple models using only population and GDP, we will apply machine learning to 62 economic indicators paired with our year-by-year medal dataset (medal_table_summary.csv), which can capture complex patterns and rank which factors matter most. 

Prior work shows GDP and population already explain much of medal variation[^1][^2], so we expect a broader indicator set and more flexible models to improve on that baseline. The results can help Olympic committees and sports ministries set realistic medal targets, guide IOC funding to countries limited by economic constraints rather than talent, and give developing nations evidence to support sports investment.


##Literature Review

Research consistently links national economic strength to Olympic success. Members of the National Bureau of Economic Research, Bernard and Busse (2004) modeled medal share from 1960 to 1996 as a function of population and GDP per capita using Tobit regression (a statistical model with a 0 limit), finding that total GDP is the strongest predictor of Olympic success. Their model had an accurate forecast for the 2000 Sydney Games using the sample from their prior research[^1]. Doctors of Economics, Johnson and Ali (2000) showed that economic factors affect both whether a country wins any medals and how many it wins[^3]. Researchers from the University of Athens, Vagenas and Vlachokyriakou (2012) found that team size mediates much of the GDP-medals relationship, while health spending, unemployment, and GDP growth also contribute[^4]. Later studies add host-nation status and past performance as key predictors, with prior medal counts often the strongest signal of future success[^5][^6].

Recent work has begun applying machine learning. Ensemble models (XGBoost, LightGBM) and deep learning architectures (CNN-LSTM, STGCN-LSTM) integrate GDP, population, team size, and historical performance to predict medal totals[^7]. Applied studies using World Bank indicators report R² values of 75 to 79% for recent Games, with total GDP outperforming GDP per capita alone in tree-based models[^8].

Three gaps motivate our project. First, most studies rely on simple linear models that miss nonlinear effects and interactions. Second, few combine a wide set of economic indicators (health, education, poverty, inflation) in one framework. Third, results are rarely presented in a form useful to policymakers who need interpretable, country-level predictions. We address these by merging year-by-year medal data with 62 World Bank indicators and applying interpretable machine learning models that report both accuracy and feature importance.


###Stakeholders and Their Needs

*National Olympic Committees (NOCs)* - target and allocate budgets[^9]. Depend on government funding; must set medal and adjusted medal expectations based on economic capacity.

*Government sports ministries* - Must justify public sports spending to legislatures and voters using evidence linking economic investment to Olympic outcomes; efficiency metrics (e.g., medals per GDP).  

*IOC / Olympic Solidarity* - Distributes around 590M to 650M USD per cycle to support athlete development in economically or athletically deprived nations[^10]. They also identify countries where economic constraints, not talent, are the primary barrier to success.

*Sports media and analysts* - Rank countries by raw medal counts without economic context.                                   Using adjusted rankings will highlight over- and under-performers relative to economic resources.
                           
*Athletes and coaches (developing nations)* - Countries are lacking access to training infrastructure and international competition. Quantitative evidence links economic development to Olympic improvement for grant applications.

*Small neighborhoods and communities* – Small-scale economic improvement for local sports based on controllable economic factors; deciding the focus to develop aspiring athletes.


##Data and Methods

Both data sources can be found through the GitHub link:
https://github.com/ahmadmashhood01/IST.707-PROJECT.

###Data Source 1

Two main data sources were obtained as prerequisites to starting this research project. The first source is the primary measure for determining Olympic success. It contains a historical archive of all countries’ medals from 1896 to the present day (LINKED BELOW).

https://cran.r-project.org/web/packages/olympicAthletes/index.html.

This dataset comes from Olympedia.org, the official online archive for past Olympic events. It has been peer-reviewed and can be cross-referenced with other datasets from sports-reference.com and Wikipedia’s Olympic medal page, which both source from a different site. 

The dataset includes 11 columns and 1930 rows, and it is well labeled with metadata. Each column holds only one data type, making the cleaning of the data very easy. There are no official primary keys, but there are surrogate keys. However, we will work to create our own primary key that will match our other dataset. We will also need to cut the dataset down, since the other dataset starts in 1960. It has not been determined if we want to use any additional years to test on pre-1960.

This dataset includes medal counts (gold, silver, bronze, and total) for each country that won a medal in any of the modern Olympics. The rows are well marked with the year and Olympic edition/season that a country’s medals are from. The countries’ full names and National Olympic Committee(NOC) codes are both listed; we will be using the NOC code to match the keys from our other dataset. Another important column we will be using is the notes column; this tells us where countries are competing under a new name, or they have split or joined a new country. This is important for countries like Russia, which have had 5 different Olympic NOC codes since 1960.

Datatypes by columns:

editon_id – int
games – int
year – int
season – char(6)
noc – char(3)
country – string
gold – int
silver – int
bronze – int
total – int
notes – string

###Data Source 2

The second data source brings the project together. The dataset compiles economic measures into counts of people, scores and indexes, monetary totals, percentages, and rates. The dataset is compiled using these measures for each country and each individual year that country has been monitored in the dataset, from 1960 to the present. The dataset can be found from the World Bank Group:

https://databank.worldbank.org/source/world-development-indicators.

This link is the main link to the World Bank Group’s Data Bank, where we are using their World Development Indicators database. This database is how we will be measuring economic success and economic growth and decline. We will then compare our results to the results from the Olympic Medals dataset. To do so, we will need to sort out individual countries, necessary columns, and years. To get the specific data we wanted, we were forced to scrape the data from an Api call to the World Bank. There, we were able to use Python to combine results with countries by year and give them their NOC codes, with the last two digits of the year as a primary ID. The CSV file from the web scrape can be found in our GitHub linked at the top of the Data and Methods section above.

This dataset is the most accurate at the overarching level. It is trusted by national governments, economists, researchers, and more as one of the best sources to track economic development. This does not come without any concerns. Many variables come directly from a country's own interpretation or reported numbers that could be falsified or flat-out inaccurate. However, the dataset uses expanded metadata with information blocks and long column names to mark out all of these instances. As a safety precaution for research reliability, we will be leaving out all of these variables in our research. 

After this step, we still needed to cut down the economic measures. To do this, we factored in our own variables along with those who have researched three similar economic analysis projects[^11][^12][^13]. We then matched what variables we could to the variables in the World Bank data base. Resultantly, we decided on 62 integer/float variables, paired up with each country by year. This leaves our dataset with 66 columns and 9381 rows after pairing up the countries from the World Bank dataset with the Olympic dataset. All individual columns and categories can be found in our Data Index, also listed on GitHub.


##Methods

The first step to run this project will be data cleaning. To do this, the datasets need to be merged on country code and year. We will also have to determine where countries have changed, merged, or split since 1960. Where applicable, we will have to give them a common code to be matched on. There are also over 200,000 null cells in the World Bank dataset, which we will have to deal with. Other cleaning methods will need to be applied that are not yet conclusive.

Once the data is clean, we will be progressing to the next phase of our project, exploratory data analysis. Here we will preprocess and transform the necessary variables in the economic dataset. This will also include the removal of some variables that may be irrelevant to the rest of our research. Variables that need to be transformed will mostly be scaled to a score or binned in a way that can help aid our research. Potentially finding more data on countries that participate but do not win medals could also be very informative to our preprocessing step and further research.

After completing our preprocessing step, we will start our machine learning process. This is where we will select and train our model. The training process will combine the improvement of countries both on the Olympic and economic levels, and then on a combined scale as well. We will try a couple of different training models (Logistic Regressions and Clusters, Decision Trees, Random Forests, etc.), including ones where economic growth and increased medal counts are trained using older data to predict newer data. We will also train on how individual factors and factors compared against each other will predict medal success.
We will then evaluate and improve our model, attempting to not overfit or underfit our model. Due to so many economic variables, this will be one of the greatest challenges during this project. We will try to use multiple models and compare scores instead of just looking at accuracy, which can be a false predictor of a model’s success.

Lastly, we will use our models to predict key interests of our stakeholders. We will need to understand why countries are actually performing poorly or well based on economic factors. This cannot just predict the more successful countries, as many stakeholders will want to know what is holding them back, not what factors others are doing right, since these measures might be unattainable for smaller, less wealthy stakeholders. The Olympic Committees are going to need to know how different economic factors affect performances so they can be more careful about their donations and make sure they are donating to the right institutions/projects.





##Risks

The largest risk of this project can easily be not properly handling missing data in the economics dataset. Since there are so many null cells, we will have to carefully decide where it makes sense to drop data and fill in data. Since many of the third-world countries are the ones missing data, we do not want to misinterpret the results for a large group of countries by removing too much data. We might also want to consider cutting down the years, since the data from the earlier years is more likely to be missing or misrepresentative, as new factors may have become better predictors.

Another risk was discussed earlier with aligning countries by country code. We must make sure to find where countries have merged, split, changed, or gained freedom, as these factors can give false interpretations of economic growth and decline. Similarly, it can also affect the increase or decrease in medals, as huge changes in political freedoms or population changes can heavily affect this number.

Our personal biggest concern is not properly representing our data due to overfitting or underfitting. Since the Olympic dataset is limited and countries’ economies change all the time, we must be very careful to accurately predict growth and declines. Moreover, we do not want to misinterpret years that can negatively affect a country, such as years with wars, global crises, and other major world events. Our data is vast in terms of information but lacks longevity; not overfitting will be very difficult when analyzing trends over time in a limited timeframe. 

###Sources

[^1]: Andrew B. Bernard and Meghan R. Busse, "Who Wins the Olympic Games: Economic
Resources and Medal Totals," Review of Economics and Statistics 86(1) (2004): 413-417. https://direct.mit.edu/rest/article-abstract/86/1/413/57461/Who-Wins-the-Olympic-Games-Economic-Resources.

[^2]: Andrew B. Bernard and Meghan R. Busse, "Who Wins the Olympic Games: Economic
Development and Medal Totals," NBER Working Paper 7998 (2000). 
https://www.nber.org/system/files/working_papers/w7998/w7998.pdf.

[^3]: Daniel K. N. Johnson and Ayfer H. Ali, "Coming to Play or Coming to Win: Participation
And Success at the Olympic Games," SSRN (2000). https://papers.ssrn.com/sol3/papers.cfm?

[^4]: George Vagenas and Eleni Vlachokyriakou, "Olympic Medals and Demo-Economic
Factors: Novel Predictors, the Ex-Host Effect, the Exact Role of Team Size, and the
'Population- GDP' Model Revisited," Sport Management Review 15 (2012): 211-217. 
https://ideas.repec.org/a/eee/spomar/v15y2012i2p211-217.html.


[^5]: William J. Kelly and Paul H. Rubin, "A Socioeconomic Model of National Olympic
Performance," Journal of Sports Economics (2016).
https://doi.org/10.1177/1527002515626166.

[^6]: "What Contributes to Winning Gold? A Cross-Section Analysis of Olympic Success," 
Bryant University Economics Working Paper (2017). https://digitalcommons.bryant.edu/eeb.

[^7]: "STGCN-LSTM for Olympic Medal Prediction: Dynamic Power Modeling and Causal
Policy Optimization," arXiv (2025). https://arxiv.org/abs/2501.17711.

[^8]: Anand Writes, "Macro-economic Indicators and Olympic Medals: A Point-of-View Using
ML Libraries in Python" (2024). https://anandwrites.com/2024/10/02/macro-economic-
indicators-and-olympic-medals-a-point-of-view-using-ml-libraries-in-python.

[^9]: RINGS Project, *Road towards Innovative Governance of NOCs and Grassroots Sport
Organisations: Handbook* (2022). https://www.sportoekonomie.unimainz.de/files
/2022/12/RINGS-Handbook.pdf.

[^10]: International Olympic Committee, "Olympic Solidarity" and "Funding." 
https://www.olympics.com/ioc/olympic-solidarity.

[^11]: Konstantin M. Wacker et al., “Leveraging Growth Regressions for Country Analysis”,
*Policy Research Working Paper*. (2024) https://documents1.worldbank.org/curated/
en/ 099217304102412750/pdf/IDU141f597b31c20114fa718cac1466610c36a27.pdf.

[^12]: Alin Mirestean and Charalambos Tsangarides, “Growth Determinants Revisited,” *IMF
Working Paper* (2009). https://www.imf.org/-/media/websites/imf/imported-full-text-
pdf/external/pubs/ft/wp/2009/_wp09268.pdf.

[^13]: Gernot Doppelhofer et al., “Determinants of Long-Term Growth: A Bayesian Averaging
of Classical Estimates (BACE) Approach,” *National Bureau of Economic Research*
(2000)

