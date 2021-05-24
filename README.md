# Project Objectives
The purpose of this project is to predict the future price of Bitcoin. Also, using other variables (e.g. NASDAQ Composite Index, S&P 500 and Gold) within the financial industry to help determine if bitcoin’s price has any impact on other variables. 


<p align="center">
  <img width="700" height="408" src="https://fortraders.info/wp-content/uploads/2021/02/shutterstock_658232353.jpg">
</p>

# Instructions

1. Git pull the project folder. 

### Data Preparation
2. Download the following datasets copy the files into **..\final-project\data**: 
    
- Bitcoin Jan 2012 to March 2021 - https://www.kaggle.com/mczielinski/bitcoin-historical-data/download.

- Bitcoin history after March 2021 - https://www.nasdaq.com/market-activity/cryptocurrency/btc/historical. Rename to HistoricalData_BTC. 

- Dow Industrials (INDU) - https://www.nasdaq.com/market-activity/index/indu/historical. Rename to HistoricalData_INDU.

- NASDAQ Composite Index (COMP) - https://www.nasdaq.com/market-activity/index/comp/historical. Rename to HistoricalData_Comp.

- S&P 500 (SPX) - https://www.nasdaq.com/market-activity/index/spx/historical. Rename to HistoricalData_SPX. 

- Gold - https://www.nasdaq.com/market-activity/stocks/gold/historical. Rename to HistoricalData_Gold. 

- Oil - https://www.nasdaq.com/market-activity/funds-and-etfs/oil/historical. Rename to HistoricalData_Oil.
   
   
### ETL
3. Use **..\notebooks\DataProcess.ipynb** to obtain the following:
- Bitcoin close price and ma price. Save findings to bitcoin.csv.
- Bitcoin close price and other index prices. Save to combine.csv.
   
4. Open **..\final-project\etl_func.py** and use init_table() function to load the following to postgresql:
- Bitcoin.csv data to bitcoin_data table.
- Combine.csv data to mix_data table.


### Model Training 
5. LSTM model (**..\model\model1.py**):
- Use create_model() function to train the LSTM model by using the bitcoin_data table. By default, it will generate "good_train_default.h5" and "scale_default.scl"             files so the model can be reused. They can be used with parameters "suffix=<str>" and "rmse_limit=<int>".
- Use predict_date(date) function to predict and the close price for a specific date.
- Use predict_date(date) function to predict all the close price from the last date in the database to the specific date, and return a dataframe for visualization.

 6. Features model (**..\model\model2.py**):
- Use create_model() function to train the model using different features (default: gold, oil, comp, spx, indu and timestamp), and generate "svc.h5" and "svc.scl"             files so the model can be reused. They can be used with parameter "feature_list=<list>" to specify the features to train the model.
- Use predict(list_data) function to predict if the price goes up, down or no change for the input timestamp.

    
7. There are 3 files to test the ETL and model functions:
  - ..\prototypes\etl_test.py
  - ..\prototypes\model1_testing.py
  - ..\prototypes\model2_testing.py
  

### Running the project on your local machine

1. Enter this environment variable in gitbash: 

  **export DATABASE_URL="postgresql+psycopg2://postgres:putyourpasswordhere@localhost:5432"**
2. Ensure to update your postgre username and password in the command.
3. Ensure postgre server is running.
4. Run **python etl_func.py** to load data to PG database.
5. Run **python app.py**.
6. Open **https://getrichquick.herokuapp.com/** in chrome.


# Potential Improvements
1. Bulletproof code to prevent entering invalid data.
2. Add a feature to upload and save new data for retraining the model.
3. Utilise more models and elaborate the differences for each model.


# Back End
Python, Tensorfolow and Scikit-Learn have been utilised to build the models. Please ensure to uninstall Tensorflow-CPU if you do not have a CUDA-eanbled (Nvidia) video card.
Data was loaded on a postgre DB and SQLAlchemy was utilised to interact with the DB.
 

# Front End
HTML, CSS and Javascript have been utilised to build the webpage. JS Plotly was also used for plotting graphs and bootstrap for styling. 
