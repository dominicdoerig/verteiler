# 03_Forecasting_LightGBM #

### What is this folder for? ###

Folder contains all files used to compute forecasts using boosted trees (LightGBM).

### Description of the Files ###

#### 1) Boosted-Trees.ipynb
Here we use one LightGBM model for all articles.

#### 2) Boosted-Trees_v2.ipynb
First all articles are classified into high-, medium- & low seller.  
Afterwards, one model for each class is fitted.

### Performance Comparison ####

Approach | RMSE (Turnover)
--- | --- | 
Boosted-Trees.ipynb | 113.33
Boosted-Trees_v2.ipynb | 107.60 