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

    In etl_func.py use init_table() function ls -lto load the data to postgresql
    (3) Load the bitcoin.csv data to bitcoin_data table
    (4) Load the combine.csv data to mix_data table

4. Model training
    (1) LSTM model (model1.py):
        use create_model() function to train the LSTM model by using the bitcoin_data table, by default it will generate "good_train_default.h5" and "scale_default.scl" file so we can reuse the model. Can be used with parameter "suffix=<str>" and "rmse_limit=<int>".
        use predict_date(date) function to predict and the close price for a specific date
        use predict_date(date) function to predict all the close price from the last date in the database to the specific date, and return a dataframe for visualization.

    (2) Features model (model2.py):
        use create_model() function to train the model using different features (default: gold, oil, comp, spx, indu and timestamp), and i will generate a "svc.h5" and "svc.scl" file so we can reuse the model. Can be used with parameter "feature_list=<list>" to specify the features to train the model.
        use predict(list_data) function to predict will the price go up, down or nochange for the input timestamp

5. There are 3 files etl_test.py / model1_testing.py /model2_testing.py to test the etl and model functions

6. Web service route:
    Thoughts:
    (1) 1 route to do the etl
    Direct access with an <a> element

    (2) 1 route to implement the model1.predict_date function, and return a predict price to show
    (3) 1 route to implement the model1.predict_date function, and return a dataframe so we can draw a predict trend to the future
    For the these 2, front end should have an input of date to send to the route

    (4) 1 route to implement the model2.create_model and model2.predict together, and return a predict trend of "up", "down", "nochange" for a given dict of feature values
    For this one, the front end should have some inputs for different features to send to the route


* `notebooks/00_Preprocessing.ipynb` loads in the source data and preprocesses it
* `model/train.py` can be called from the root directory to train and save the model e.g. `python train/model.py`
* `app.py` houses the flask app that will a guest can check their ticket for potential peril


# How to Run on Your Local Machine

1. enter this environment variable in gitbash: export DATABASE_URL="postgresql+psycopg2://postgres:putyourpasswordhere@localhost:5432"
2. Ensure to update the Postgre username and password in the command
3. Ensure Postgre server is running
4. run -> python etl_func.py to load data to PG database
5. run -> python app.py
6. copy the link for the app and open in chrome


# Link for deployed code in Heroku

https://getrichquick.herokuapp.com/


# Potential Improvements

1. Bulletproofing code to prevent entering invalid data
2. Feature to upload and save new data for retraining the model
3. Utilise more models and elaborating the differences for each model


## Back End

Utilised Python, Tensorfolow and Scikit-Learn to build models. Please ensure to unstall Tensorflow-CPU instead if you don't have a CUDA-eanbled (Nvidia) video card.

Data was loaded on a postgre DB and SQLAlchemy was uitlised to interact with the DB.

## Front End

Utilised HTML, CSS and Javascript. JS Plotly was also used for plotting graphs and bootstrap for styling. 
