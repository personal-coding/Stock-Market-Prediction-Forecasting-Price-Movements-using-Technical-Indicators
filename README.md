# Stock-Market-Predicition-Forecasting-Price-Movements-using-Technical-Indicators
Trying to replicate the results in the paper ["Forecasting Price Movements using Technical Indicators: Investigating the Impact of Varying Input Window Length."](https://github.com/ScrapeWithYuri/Stock-Market-Predicition-Forecasting-Price-Movements-using-Technical-Indicators/blob/master/PDF/2017Forecastingpricemovementsusingtechnicalindicators-Investigatingtheimpactofvaryinginputwindowlength.pdf) My general results show much lower prediction accuracies than those noted in the paper, especially when it comes to short prediction horizons. Longer prediction horizons, with longer input windows for the technical indicators show potentially promising results.

My results use the terminology "pred step" and "input step." Pred step is the prediction horizon (i.e. predict if a stock is going up / down *t* days from now). Input step is the number of days used to create the technical indicators.

My tests only used Support Vector Machine (SVM), as this was noted as the best performing machine learning technique in the paper.

# Best Results
The absolule best results I could obtain when looping the ten technical indicators used in the paper to train / test, the sigmoid kernel, and all values for C (-5 to 15) and gamma (-15 to 3) - these results are much lower than those presented in the paper, especially in the short prediction horizons:

```
Pred step 1, input step 3, acc 53.8%
Pred step 15, input step 15, acc 60.9%
Pred step 30, input step 30, acc 64.9%
```

# Codes
There are three main codes in the repo.

GrabYahoo - Grabs data from Yahoo finance into the data folder. 40 stock data files are already downloaded for data from 1/29/2002 - 7/20/2012, which is the same date ranges used in the paper. The paper used 50 stocks, but I excluded 10 of the stocks from the paper due to either incomplete information or downloading data errors.

SVM - Cross Validation - This uses a five-fold cross validation against the ten technical indicators used in the paper to train, then tests the prediciton accuracy. The SVM is using the sigmoid kernel and a grid search for C (-5 to 15) and gamma (-15 to 3). Again, this matches the paper paramters.

SVM - Best Accuracy - This loops the SVM across the sigmoid kernel and all values for C (-5 to 15) and gamma (-15 to 3) to see what the best possible accuracies are.

# Results Files
All of my results are noted in the results folders (cross validation files are saved here) and best results folders (absolute best results are saved here).

# K-Fold Cross Validation
Yes, I am aware k-fold cross validation is not realistic in the context of time series analysis, but this repo is trying to attempt to confirm the results of the paper which uses k-fold cross validation.
