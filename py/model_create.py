import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import globalvar
from datetime import datetime
import joblib

# Load data
engine = create_engine("sqlite:///../data/bitcoin.sqlite")
df = pd.read_sql_query("SELECT * FROM bitcoin", engine)

# print(df.head())

# define data to use
dataset = df[['Close']].values
training_len = int(len(dataset)*0.8)

# scale the data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler().fit(dataset)
data_scaled = scaler.transform(dataset)

# get the training data
train_data = data_scaled[:training_len, :]
X_train = []
y_train = []

# define how many days to use LSTM
n_days = globalvar.lstm_days

for i in range(n_days, len(train_data)):
    X_train.append(train_data[i-n_days:i, 0])
    y_train.append(train_data[i, 0])

# reshape the data for LSTM
X_train = np.array(X_train)
y_train = np.array(y_train)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

stop = False
rmse_limit = 2000
while(not stop):

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, LSTM

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
        dt = datetime.now().strftime('%Y%m%d_%H%M%S')
        joblib.dump(scaler, f'scaler_{dt}.scl')
        model.save(f"good_trained_{dt}.h5")
        stop = True