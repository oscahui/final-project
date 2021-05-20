# GetRichQuick
Know how rich you will be if you invest in BitCoin!

Some shortcuts were taken:


# Overview

# data preparation

1. download  bitcoin Jan 2012 to March 2021  data from kaggle:
    https://www.kaggle.com/mczielinski/bitcoin-historical-data/download

2. download other data from nasdaq:
    Bitcoin history (for later than March 2021): 
    https://www.nasdaq.com/market-activity/cryptocurrency/btc/historical

    Dow Industrials (INDU):
    https://www.nasdaq.com/market-activity/index/indu/historical

    NASDAQ Composite Index (COMP)
    https://www.nasdaq.com/market-activity/index/comp/historical

    S&P 500 (SPX)
    https://www.nasdaq.com/market-activity/index/spx/historical

    Gold
    https://www.nasdaq.com/market-activity/stocks/gold/historical

    Oil
    https://www.nasdaq.com/market-activity/funds-and-etfs/oil/historical

3. ETL
    (1) Get the bitcoin close price and save to bitcoin.csv
    (2) Get the bitcoin close price/ma and other index price and save to combine.csv
    (3) Load the bitcoin.csv data to bitcoin_data table
    (4) Load the combine.csv data to mix_data table




* `notebooks/00_Preprocessing.ipynb` loads in the source data and preprocesses it
* `model/train.py` can be called from the root directory to train and save the model e.g. `python train/model.py`
* `app.py` houses the flask app that will a guest can check their ticket for potential peril

# Potential Improvements

## Back End
- [ ] Impute the missing values in the `age` column

## Front End
