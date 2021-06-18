# 03_Forecasting_LightGBM #

### What is this folder for? ###

Folder contains all files used to compute forecasts using boosted trees (LightGBM).

### Description of the Files ###

#### 1) Boosted-Trees.ipynb
Here we use one LightGBM model for all articles.

#### 2) Boosted-Trees_v2.ipynb
First all articles are classified into high-, medium- & low seller.  
Afterwards, one model for each class is fitted.


#### 3) Boosted-Trees_v3.ipynb
First all articles are classified into high-, medium- & low seller.  
Afterwards, one model for each class (high-, medium- & low seller) and for each article category is fitted.  
The article's category is retrieved from its master data (dt. Stammdaten).  
Best results are achieved when using the Censhare Category Level 1. 


#### 4) Boosted-Trees_v4.ipynb
Here we use a Top-Down approach. We first aggregate the bottom level time series based on the article category, forecast the aggregated time series and obtain the bottom level time series by disaggregating the aggregated forecast.


### Best Performing Model ###
Boosted-Trees_v3.ipynb with following performance:

Class | RMSE (Turnover)
--- | --- | 
A | 66.82
B | 63.09 
C | 84.92 
 



