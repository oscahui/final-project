#from numpy.lib.npyio import load
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import globalvar
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import joblib
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

engine = create_engine("sqlite:///../data/bitcoin.sqlite")
df = pd.read_sql_query("SELECT * FROM bitcoin", engine)
df["Date"] = pd.to_datetime(df['Date']).dt.date
model_file = "good_trained_20210520_173302.h5"
scaler_file = "scaler_20210520_173302.scl"

n_days = globalvar.lstm_days

def predict_nextday(df_source, model_file, scaler_file):
    model = load_model(model_file)
    scaler = joblib.load(scaler_file)
    new_df = df_source.filter(["Close"])
    last_n_days = new_df[-n_days:].values
    last_n_days_scaled = scaler.transform(last_n_days)
    X_test = []
    X_test.append(last_n_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predict = model.predict(X_test)
    predict = scaler.inverse_transform(predict)
    return predict[0,0]

def predict_date(df_source, model_file, scaler_file, date):
    df_copy = df_source.copy()
    initial_date = max(df_copy["Date"])
    current_date = initial_date
    if date < initial_date:
        return None
    while(current_date < date):
        current_date = current_date + timedelta(days=1)
        current_predict = predict_nextday(df_copy, model_file, scaler_file)
        columns = df_copy.columns
        df_copy = df_copy.append({
            columns[0] : current_date,
            columns[1] : current_predict,
            columns[2] : 0
        }, ignore_index=True)
    predict = predict_nextday(df_copy, model_file, scaler_file)
    print(df_copy.loc[df_copy["Date"]>initial_date])
    return predict


# for testing purpose
dt = datetime.strptime("20210520", "%Y%m%d").date()
print(f"Predict Next Day: {predict_nextday(df, model_file, scaler_file)}")
print(f"Predict Date {dt}: {predict_date(df, model_file, scaler_file, dt)}")
