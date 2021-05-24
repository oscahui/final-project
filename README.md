# Project Objectives
The purpose of this project is to predict the future price of Bitcoin. Also, using other variables (e.g. NASDAQ Composite Index, S&P 500 and Gold) within the financial industry to help determine if bitcoin’s price has any impact on other variables. 


<p align="center">
  <img width="1000" height="584" src="https://fortraders.info/wp-content/uploads/2021/02/shutterstock_658232353.jpg">
</p>

# Instructions

1. Git pull the project folder. 

## Data Preparation
2. Download the following datasets copy the files into ..\final-project\data: 
    
- Bitcoin Jan 2012 to March 2021 - https://www.kaggle.com/mczielinski/bitcoin-historical-data/download.

- Bitcoin history after March 2021 - https://www.nasdaq.com/market-activity/cryptocurrency/btc/historical. Rename to HistoricalData_BTC. 

- Dow Industrials (INDU) - https://www.nasdaq.com/market-activity/index/indu/historical. Rename to HistoricalData_INDU.

- NASDAQ Composite Index (COMP) - https://www.nasdaq.com/market-activity/index/comp/historical. Rename to HistoricalData_Comp.

- S&P 500 (SPX) - https://www.nasdaq.com/market-activity/index/spx/historical. Rename to HistoricalData_SPX. 

- Gold - https://www.nasdaq.com/market-activity/stocks/gold/historical. Rename to HistoricalData_Gold. 

- Oil - https://www.nasdaq.com/market-activity/funds-and-etfs/oil/historical. Rename to HistoricalData_Oil.
   
   
## ETL
3. Use \notebooks\DataProcess.ipynb to obtain the following:
- Bitcoin close price and ma price. Save findings to bitcoin.csv.
- Bitcoin close price and other index prices. Save to combine.csv.
   
4. Open \final-project\etl_func.py and use init_table() function to load the following to postgresql:
- Bitcoin.csv data to bitcoin_data table.
- Combine.csv data to mix_data table.


## Model Training 
5. LSTM model (model1.py):
- Use create_model() function to train the LSTM model by using the bitcoin_data table. By default, it will generate "good_train_default.h5" and "scale_default.scl"             files so the model can be reused. They can be used with parameters "suffix=<str>" and "rmse_limit=<int>".
- Use predict_date(date) function to predict and the close price for a specific date.
- Use predict_date(date) function to predict all the close price from the last date in the database to the specific date, and return a dataframe for visualization.

 6. Features model (model2.py):
- Use create_model() function to train the model using different features (default: gold, oil, comp, spx, indu and timestamp), and generate "svc.h5" and "svc.scl"             files so the model can be reused. They can be used with parameter "feature_list=<list>" to specify the features to train the model.
- Use predict(list_data) function to predict if the price goes up, down or no change for the input timestamp.

    
7. There are 3 files etl_test.py / model1_testing.py /model2_testing.py to test the etl and model functions

    
8. Web service route:
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
