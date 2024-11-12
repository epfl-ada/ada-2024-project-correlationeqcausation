# What factors affect Oscar nomiations?

## Abstract
The Oscar Academy Awards are some of the most renowned movie awards in the world. Experts and critics carefully select nominees, and reward a few of them with the awards. In this project we aim to examine how various factors affect Oscar nominations in categories for specific actors (Such as best actress, best supporting actor). What drives the Oscar Academy Awards' decisions to nominate movies? Do Oscar nominations align with the popular opinion?
To see if public opinion aligns with Oscar nominations, we will explore movie revenue and IMDB ratings in relation to Oscar nominations. To explore other factors affecting Oscar nominations, we look at properties such as actor ethnicity, theme/genre of the movies and actor history.  
We will explore this topic based on the CMU Movie Summary Corpus dataset, and [others](#additional-datasets). This study will be limited to American movies, as there is likely a skew towards American movies being nominated for the Oscars (TODO: show this).

## Research Questions
- Do Oscar nominations align with popular opinion?
- To what degree are Oscar winnings and nominations representative of the US population ethnicity statistics?
- To what degree do personal actor features such as height and age correlate with Oscar nominations?

## Datsets
### CMU Movie Summary Corpus
Our main datset is the CMU Movie Summary Corpus, which contains infomration about movies (such as release date, revenue, run time, etc.), actors involved in the movies and plot summaries.
### Oscars
In addition to the CMU Movie Summary Corpus dataset, we will be using a dataset of Oscar awards (https://www.kaggle.com/datasets/unanimad/the-oscar-award).
### IMDB
Datasets from IMDB named title.basics.tsv.gz and title.ratings.tsv.gz  will also be utilized (https://datasets.imdbws.com/). These describe movies in IMDB with their ratings on the website.
Note: In the title.basics dataset, there is a problem with some values being within double quotes, which initially caused some data corruption. We fixed this by using quoting=3 in our read_csv call.

We join these with our main dataset for analysis, see the data processing pipeline [data.ipynb](data.ipynb).

## Methods
- Regression/classification model
- Propensity score
- Correlation significance analysis
-

## Proposed timeline, organization within the team
### Timeline
??

### Milestones:
-a  
-b  
-c  

## Questions for TAs


## General notes:
- Examining actor gender differences would also be interesting, but the Oscars are already split in male/female so it's not relevant.
- We chose to analyze nominees and not only winners, because only winners would be a too small dataset for drawing proper conclusions.