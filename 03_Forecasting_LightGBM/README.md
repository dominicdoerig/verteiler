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

### Performance Comparison ####

Approach | RMSE (Turnover)
--- | --- | 
Boosted-Trees.ipynb | 113.33
Boosted-Trees_v2.ipynb | 107.60 
Boosted-Trees_v3.ipynb | 96.18 
