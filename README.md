# GetRichQuick
Know how rich you will be if you invest in BitCoin!

Some shortcuts were taken:


# Overview

# data preparation

1. download files:
    (1) download  bitcoin Jan 2012 to March 2021  data from kaggle:
        https://www.kaggle.com/mczielinski/bitcoin-historical-data/download

    (2) download other data from nasdaq:
        Bitcoin history (for later than March 2021): 
        https://www.nasdaq.com/market-activity/cryptocurrency/btc/historical
        Rename to HistoricalData_BTC

        Dow Industrials (INDU):
        https://www.nasdaq.com/market-activity/index/indu/historical
        Rename to HistoricalData_INDU

        NASDAQ Composite Index (COMP)
        https://www.nasdaq.com/market-activity/index/comp/historical
        Rename to HistoricalData_Comp

        S&P 500 (SPX)
        https://www.nasdaq.com/market-activity/index/spx/historical
        Rename to HistoricalData_SPX

        Gold
        https://www.nasdaq.com/market-activity/stocks/gold/historical
        Rename to HistoricalData_Gold

        Oil
        https://www.nasdaq.com/market-activity/funds-and-etfs/oil/historical
        Rename to HistoricalData_Oil

2. ETL
    Use notebooks/DataProcess.py to do the following:
    (1) Get the bitcoin close price and ma price then save to bitcoin.csv
    (2) Get the bitcoin close price and other index price and save to combine.csv

    In etl_func.py use init_table() function to load the data to postgresql
    (3) Load the bitcoin.csv data to bitcoin_data table
    (4) Load the combine.csv data to mix_data table

4. Model training
    (1) LSTM model (model1.py):
        use create_model() function to train the LSTM model by using the bitcoin_data table, by default it will generate "good_train_default.h5" and "scale_default.scl" file so we can reuse the model.
        use predict_date(date) function to predict and the close price for a specific date
        use predict_date(date) function to predict all the close price from the last date in the database to the specific date, and return a dataframe for visualization.

    (2) Features model (model2.py):
        use create_model() function to train the model using different features (default: gold, oil, comp, spx, indu and timestamp), and i will generate a "svc.h5" and "svc.scl" file so we can reuse the model.
        use predict(list_data) function to predict will the price go up, down or nochange for the input timestamp

5. Web service route:




* `notebooks/00_Preprocessing.ipynb` loads in the source data and preprocesses it
* `model/train.py` can be called from the root directory to train and save the model e.g. `python train/model.py`
* `app.py` houses the flask app that will a guest can check their ticket for potential peril

# Potential Improvements

## Back End
- [ ] Impute the missing values in the `age` column

## Front End
