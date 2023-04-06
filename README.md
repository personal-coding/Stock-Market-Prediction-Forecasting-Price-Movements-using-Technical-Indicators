# Forecasting Stock Market Movements using Technical Indicators: Investigating the Impact of Varying Input Window Length

## Introduction
In this project, I aim to replicate the results presented in the paper ["Forecasting Price Movements using Technical Indicators: Investigating the Impact of Varying Input Window Length."](https://github.com/ScrapeWithYuri/Stock-Market-Predicition-Forecasting-Price-Movements-using-Technical-Indicators/blob/master/PDF/2017Forecastingpricemovementsusingtechnicalindicators-Investigatingtheimpactofvaryinginputwindowlength.pdf)  My analysis focuses on predicting stock price movements using technical indicators and explores the impact of varying input window length on prediction accuracy. I use Support Vector Machine (SVM) as the machine learning technique and compare my results with those presented in the paper.

This project includes three main codes: GrabYahoo, SVM - Cross Validation, and SVM - Best Accuracy. I also provide a detailed explanation of my testing terminology, including "pred step" and "input step." My results, which are saved in the results and best results folders, indicate that accuracy rates are lower than those presented in the paper, particularly for shorter prediction horizons. However, I do find promising results for longer prediction horizons with longer input windows for technical indicators.

While I acknowledge that k-fold cross validation may not be realistic in time series analysis, our aim is to replicate the paper's results using the same method.

# Conclusion
My results use the terminology "pred step" and "input step." Pred step is the prediction horizon (i.e. predict if a stock is going up / down *t* days from now). Input step is the number of historical days used to create the technical indicators.

The absolute best results I could obtain when looping the ten technical indicators used in the paper to train / test, the sigmoid kernel, and all values for C (-5 to 15) and gamma (-15 to 3) - these results are much lower than those presented in the paper, especially in the shorter prediction horizons. However, longer prediction horizons, with longer input windows for the technical indicators, show potentially promising results.:

```
Pred step 1, input step 3, acc 53.8%
Pred step 15, input step 15, acc 60.9%
Pred step 30, input step 30, acc 64.9%
```

# Codes
There are three main codes in the repo.

*GrabYahoo* - Grabs data from Yahoo finance into the data folder. 40 stock data files are already downloaded for data from 1/29/2002 - 7/20/2012, which is the same date ranges used in the paper. The paper used 50 stocks, but I excluded 10 of the stocks from the paper due to either incomplete information or downloading data errors.

*SVM - Cross Validation* - This uses a five-fold cross validation against the ten technical indicators used in the paper to train, then tests the prediction accuracy. The SVM is using the sigmoid kernel and a grid search for C (-5 to 15) and gamma (-15 to 3). Again, this matches the paper parameters.

*SVM - Best Accuracy* - This loops the SVM across the sigmoid kernel and all values for C (-5 to 15) and gamma (-15 to 3) to see what the best possible accuracies are.
