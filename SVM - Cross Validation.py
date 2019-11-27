#Import scikit-learn dataset library
from sklearn import svm, metrics
from sklearn.model_selection import GridSearchCV
from itertools import islice
import pandas as pd, codecs, talib, numpy as np

def svc_param_selection(X, y, nfolds, score):
    Cs = []
    gammas = []
    for i in range(-5, 16):
        Cs.append(2 ** i)
    for i in range(-15, 4):
        gammas.append(2 ** i)
    param_grid = {'C': Cs, 'gamma': gammas}
    grid_search = GridSearchCV(svm.SVC(kernel='sigmoid', cache_size=1200), param_grid, cv=nfolds, iid=False, n_jobs=-3, scoring=score)
    grid_search.fit(X, y)

    return grid_search.best_params_

def create_targets(predictionstep):
    df['Target2'] = 0
    for i in range(len(df['Close'])-predictionstep):
        if df['Close'][i+predictionstep] > df['Close'][i]:
            df['Target2'][i] = 1

stocks = list()
pd.options.mode.chained_assignment = None

with codecs.open('.\\data\\symbols.txt', mode='r', encoding='utf-8') as f:
    while True:
        lines = list(islice(f, 1000))

        if not lines:
            break


        for qm in lines:
            try:
                hold = qm.replace('\r', '')
                hold = hold.replace('\n', '')
                stocks.append(hold)
            except:
                pass

for stock in stocks:
    #Load dataset
    df = pd.read_csv('.\\data\\{0}.csv'.format(stock), index_col=False)

    timestep = 15
    predictionstep = 15
    startingpoint = timestep*2 #times 2 because adx needs to calculate atr first
    endtrainperiod = 1740
    endtestperiod = None

    create_targets(predictionstep)

    xdata = df.drop(columns=['Unnamed: 0', 'Target2', 'Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Adj Close'], axis=1)
    ydata = df['Target2']
    high, low, close, open = df['High'], df['Low'], df['Close'], df['Open']

    columns = ['sma', 'ema', 'atr', 'adx', 'cci', 'roc', 'rsi', 'willr', 'fastk', 'fastd']

    sma = talib.SMA(close, timeperiod=timestep)
    ema = talib.EMA(close, timeperiod=timestep)
    atr = talib.ATR(high,low, close, timeperiod=timestep)
    adx = talib.ADX(high,low, close, timeperiod=timestep)
    cci = talib.CCI(high,low, close, timeperiod=timestep)
    roc = talib.ROC(close, timeperiod=timestep)
    rsi = talib.RSI(close, timeperiod=timestep)
    willr = talib.WILLR(high,low, close, timeperiod=timestep)
    fastk, fastd = talib.STOCHF(high,low, close, fastk_period=timestep, fastd_period=3, fastd_matype=0)

    xdata['sma'] = sma
    xdata['ema'] = ema
    xdata['atr'] = atr
    xdata['adx'] = adx
    xdata['cci'] = cci
    xdata['roc'] = roc
    xdata['rsi'] = rsi
    xdata['willr'] = willr
    xdata['fastk'] = fastk
    xdata['fastd'] = fastd

    for m in columns:
        #normalize train and test data to zero mean and unit variance
        meanSeq = np.mean(xdata[m][startingpoint:endtrainperiod])
        stdSeq = np.std(xdata[m][startingpoint:endtrainperiod])

        xdata[m][startingpoint:(endtestperiod if not endtestperiod is None else 0)-predictionstep] = \
            (xdata[m][startingpoint:(endtestperiod if not endtestperiod is None else 0)-predictionstep] - meanSeq) / stdSeq

    x_train, x_test, y_train, y_test = xdata[startingpoint:endtrainperiod], xdata[endtrainperiod:(endtestperiod if not endtestperiod is None else 0)-predictionstep], \
                                       ydata[startingpoint:endtrainperiod], ydata[endtrainperiod:(endtestperiod if not endtestperiod is None else 0)-predictionstep]

    best = svc_param_selection(x_train, y_train, 5, 'accuracy')

    print(best)

    #Create a svm Classifier
    clf = svm.SVC(kernel='sigmoid', C=best['C'], gamma=best['gamma'], cache_size=1200)

    #Train the model using the training sets
    clf.fit(x_train, y_train)

    #Predict the response for test dataset
    y_pred = clf.predict(x_test)

    acc = metrics.accuracy_score(y_test, y_pred)

    # Model Accuracy: how often is the classifier correct?
    print("Accuracy:",acc)
    print(metrics.confusion_matrix(y_test,y_pred))
    print(metrics.classification_report(y_test,y_pred))

    l = [None] * endtrainperiod
    for m in y_pred:
        l.append(m)
    for m in range(timestep):
        l.append(None)
    xdata['Target'] = ydata
    xdata['Predict']= None
    xdata['Predict'] = pd.DataFrame(l)

    acc = '{:.1%}'.format(acc)

    xdata = pd.concat([df.drop(columns=['Unnamed: 0', 'Target2'], axis=1), xdata], axis=1)

    xdata.to_csv('.\\results\\{0} results - pred step {1}, input step {2}, acc {3}.csv'.format(stock, predictionstep, timestep, acc), \
                 sep=',', index=False)