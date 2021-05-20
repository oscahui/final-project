import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

# define how many days to use LSTM

n_days = 60
db = "sqlite:///../data/bitcoin.sqlite"
default_suffix = "default"
engine = create_engine("sqlite:///../data/bitcoin.sqlite")

# create and train model
def create_model(suffix=None):
    # Load data
    df = pd.read_sql_query("SELECT * FROM bitcoin", engine)
    df["Date"] = pd.to_datetime(df['Date']).dt.date
    # define data to use
    dataset = df[['Close']].values
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
    rmse_limit = 2000

    # make sure RMSE < 2000
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
            joblib.dump(scaler, f"scaler_{suf}.scl")
            model.save(f"good_trained_{suf}.h5")
            stop = True

# predict next day
def predict_nextday(df_source, model_file=None, scaler_file=None):
    #Load Data
    df = pd.read_sql_query("SELECT * FROM bitcoin", engine)
    df["Date"] = pd.to_datetime(df['Date']).dt.date

    #Load Model
    if model_file is None:
        model_file = f"good_trained_{default_suffix}.h5"

    if scaler_file is None:
        scaler_file =f"scaler_{default_suffix}.scl"
    
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

def predict_date(date, model_file=None, scaler_file=None):
    # Load data
    df = pd.read_sql_query("SELECT * FROM bitcoin", engine)
    df["Date"] = pd.to_datetime(df['Date']).dt.date
    initial_date = max(df["Date"])
    current_date = initial_date
    if date < initial_date:
        return None
    while(current_date < date):
        current_date = current_date + timedelta(days=1)
        current_predict = predict_nextday(df, model_file, scaler_file)
        columns = df.columns
        df = df.append({
            columns[0] : current_date,
            columns[1] : current_predict,
            columns[2] : 0
        }, ignore_index=True)
    predict = predict_nextday(df, model_file, scaler_file)
    print(df.loc[df["Date"]>initial_date])
    return predict


# testing
create_model()
dt = datetime.strptime("20210520", "%Y%m%d").date()
print(f"Predict Date {dt}: {predict_date(dt)}")