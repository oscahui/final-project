import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import os


# define how many days to use LSTM
table_name = "bitcoin_data"
n_days = 60
db = os.environ.get('DATABASE_URL', '')
default_suffix = "default"
engine = create_engine(db)

# create and train model
def create_model(suffix=None, rmse_limit = 10000):
    # Load data
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    # define data to use
    dataset = df[['close']].values
    training_len = int(len(dataset)*0.8)

    # scale the data
    scaler = MinMaxScaler().fit(dataset)
    data_scaled = scaler.transform(dataset)

    # get the training data
    train_data = data_scaled[:training_len, :]
    X_train = []
    y_train = []

    for i in range(n_days, len(train_data)):
        X_train.append(train_data[i-n_days:i, 0])
        y_train.append(train_data[i, 0])

    # reshape the data for LSTM
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    stop = False

    # make sure RMSE < rmselimit
    while(not stop):
        # define model and compile
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(optimizer="adam", loss="mean_squared_error")

        # train the model
        model.fit(X_train, y_train, batch_size=1, epochs=1)

        # get test data
        test_data = data_scaled[training_len - n_days: , :]
        X_test = []
        y_test = dataset[training_len: , :]

        for i in range(n_days, len(test_data)):
            X_test.append(test_data[i-n_days:i, 0])

        # reshape the data for LSTM
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

        prediction = model.predict(X_test)
        prediction = scaler.inverse_transform(prediction)

        # calculate the rmse, 
        rmse = np.sqrt(np.square(np.subtract(y_test, prediction)).mean())
        print(f"RMSE: {rmse}")
        if rmse < rmse_limit:
            suf = None
            if suffix is None:
                suf = default_suffix
            else:
                suf = suffix
            joblib.dump(scaler, f"model/scaler_{suf}.scl")
            model.save(f"model/good_trained_{suf}.h5")
            stop = True

# predict next day
def predict_nextday(df_source, suffix=None):
    #Load Data
    #df = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
    #df["date"] = pd.to_datetime(df['date']).dt.date

    model_file = None
    scaler_file = None
    #Load Model
    if suffix is None:
        model_file = f"model/good_trained_{default_suffix}.h5"
        scaler_file =f"model/scaler_{default_suffix}.scl"
    else:
        model_file = f"model/good_trained_{suffix}.h5"
        scaler_file =f"model/scaler_{suffix}.scl"
    
    model = load_model(model_file)
    scaler = joblib.load(scaler_file)
    new_df = df_source.filter(["close"])
    last_n_days = new_df[-n_days:].values
    last_n_days_scaled = scaler.transform(last_n_days)
    X_test = []
    X_test.append(last_n_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predict = model.predict(X_test)
    predict = scaler.inverse_transform(predict)
    return predict[0,0]

def predict_date(date, suffix=None):
    # Load data
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df=df[["date", "close", "real"]]
    initial_date = max(df["date"])
    current_date = initial_date
    if date < initial_date:
        return None
    while(current_date < date):
        current_date = current_date + timedelta(days=1)
        if suffix is None:
            current_predict = predict_nextday(df)
        else:
            current_predict = predict_nextday(df, suffix)
        columns = df.columns
        df = df.append({
            columns[0] : current_date,
            columns[1] : current_predict,
            columns[2] : 0
        }, ignore_index=True)
    predict = None
    if suffix is None:
        predict = predict_nextday(df)
    else:
        predict = predict_nextday(df, suffix)
    print(df.loc[df["date"]>initial_date])
    return predict

def predict_date_df(date, suffix=None):
    # Load data
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df=df[["date", "close", "real"]]
    initial_date = max(df["date"])
    current_date = initial_date
    if date < initial_date:
        return None
    while(current_date <= date):
        current_date = current_date + timedelta(days=1)
        if suffix is None:
            current_predict = predict_nextday(df)
        else:
            current_predict = predict_nextday(df, suffix)
        columns = df.columns
        df = df.append({
            columns[0] : current_date,
            columns[1] : current_predict,
            columns[2] : 0
        }, ignore_index=True)
    return df
