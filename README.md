# What factors affect Oscar nominations?

## Data story:
[https://anfindsen.github.io/CorrelationEqCausation/](https://anfindsen.github.io/CorrelationEqCausation/)

## Note:
In results.ipynb, our plotly plots are not correctly displayed in Github. The correct plots can be seen in our data story.

## Abstract
The Oscar Academy Awards are some of the most renowned movie awards in the world. 
Experts and critics carefully select nominees, and reward a few of them with the award. 
In this project we aim to examine how various factors affect Oscar nominations in categories for specific actors (such as best actress, best supporting actor). 
What drives the Oscar Academy Awards' decisions to nominate actors? Do Oscar nominations align with the popular opinion?
To answer these questions, we will explore movie revenue and IMDB ratings in relation to Oscar nominations. 
To explore other factors affecting Oscar nominations, we look at properties such as actor ethnicity, theme/genre of the movies and actor history.  
We will explore this topic based on the CMU Movie Summary Corpus dataset, and [others](#datasets).

## Research Questions
### Main question: What factors affect Oscar nominations?

### Subquestions:
1. Do Oscar nominations align with popular opinion?
2. To what degree are Oscar nominations affected by the origin country of the movie?
3. To what degree are Oscar winnings and nominations representative of ethnicity statistics (for the world and United States)?
4. To what degree do personal actor features such as height and age correlate with Oscar nominations?

## Datasets
### CMU Movie Summary Corpus
Our main dataset is the CMU Movie Summary Corpus, which contains information about movies (such as release date, revenue, run time, etc.), actors involved in the movies and plot summaries.
<br>
The CMU dataset contains information about the country of origin of the movie, languages used, etc. We intend to use these in our investigation of RQ2. Additionally, personal information about actors such as ethnicity, height and age in the CMU character dataset allow us to examine RQs 3 and 4.
### Oscars
In addition to the CMU Movie Summary Corpus dataset, we will be using a [dataset of Oscar awards](https://www.kaggle.com/datasets/unanimad/the-oscar-award). We joined it to the CMU dataset using movie title, release year and actor name as a combined primary key. Combining with the CMU dataset resulted in 952 out of 63968 distinct movies who were nominated for Oscars and 801 out of 134907 actors.
### IMDB
[Datasets from IMDB](https://datasets.imdbws.com/) named title.basics.tsv.gz and title.ratings.tsv.gz  will also be utilized. These describe movies in IMDB with their ratings on the website. The movie scores were joined to the movies using movie name and release year as the primary key. In combination with the previous datasets 36760 movies had ratings, 939 of which were nominated for Oscars.
<br>
We intend to use ratings from the IMDb dataset to gauge popular opinion for RQ1.

For full documentation of joining and transforming data see the data processing pipeline [data_pipeline.ipynb](data_pipeline.ipynb).

## Methods (Also explained on a separate page of the data story):
Preliminary implementations of these methods can be found in [results.ipynb](results.ipynb).
### Correlation
No correlation implies that there is no causation. Hence this makes for a good starting point of our analysis.
### Kolmogorov-Smirnoff Test
For different single dimensional, continuous empirical distributions, the KS test tells us if they come from the same underlying distribution. 
Hence we can use it to see if for instance the underlying distributions of ratings of Oscar nominated and non-Oscar nominated movies is the same.
### Binomial test
Binomial test can be used to assess the similarity between binary distributions (e.g. series of coin flips using different coins). We can use this to assess the differences between ethnicities and nationalities. For example, it can be used to check whether the nomination rates we observe for American and non-American actors are likely to have come from the same distribution.
### Logistic Regression/classification model
Logistic regression is used to model a binary prediction from data. It can be implemented to assess the predictive power of actor features on Oscar nominations. This analysis can be useful for answering all our research questions. 
<br>
Logistic regression learns coefficients for input features (normalized for numerical values and one-hot encoded for categorical features). 
We interpret these coefficients as the effect of each feature on Oscar nomination odds.

## Contributions:
We worked as a team, so there is of course overlap between our contributions due to helping each other, proofreading etc. That being said, here are our main contribution areas:

- Rasmus: Modelling for prediction, compiling main results.ipynb file
- Erik: Data preprocessing pipeline, career analysis
- Melker: Genre analysis, actor network analysis
- Tejas: Clustering for analysis in different areas of analysis (high-level, actor, movie)
- John: Setting up the data story website, nationality analysis


## Other notes:
- Examining actor gender differences would also be interesting, but the Oscars are already split in male/female so it's not relevant.
- We chose to analyze nominees and not only winners, because only using the winners would be a too small dataset for drawing proper conclusions.
