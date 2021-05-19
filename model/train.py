import pandas as pd
import numpy as np
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# load data
df = pd.read_csv("../data/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv")
df1 = pd.read_csv("../data/HistoricalData20210517.csv", parse_dates=["Date"])

df = df.dropna()
df = df[["Timestamp", "Close"]]

df["DateTime"] = pd.to_datetime(df['Timestamp'],unit='s')
df["Date"] = df["DateTime"].dt.date
df["Time"] = df["DateTime"].dt.time

df = df[["Date","Time", "Close"]]
df["real"] = 1

df =df.reset_index(drop=True)
df = df.groupby("Date").max("Time")
df = df.reset_index()

df1 = df1.sort_values(by="Date")
df1 = df1.reset_index(drop=True)
df1 = df1[["Date", "Close/Last"]]
df1.columns = ["Date", "Close"]
df1["Date"] = df1["Date"].dt.date
df1["real"] = 1
max_date_df = max(df["Date"])
df1.loc[df1["Date"]>max_date_df]


df = pd.concat([df, df1.loc[df1["Date"]>max_date_df]])
df = df.reset_index(drop=True)

# change here
dataset = df[['Close']].values

training_len = int(len(dataset)*0.8)

scaler = MinMaxScaler().fit(dataset)
data_scaled = scaler.transform(dataset)
train_data = data_scaled[:training_len, :]

X_train = []
y_train = []
n_days = 60

for i in range(n_days, len(train_data)):
    X_train.append(train_data[i-n_days:i, 0])
    y_train.append(train_data[i, 0])

X_train = np.array(X_train)
y_train = np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

model = Sequential()

model.add(LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer="adam", loss="mean_squared_error")

model.fit(X_train, y_train, batch_size=1, epochs=1)

test_data = data_scaled[training_len - n_days: , :]

X_test = []
y_test = dataset[training_len: , :]


for i in range(n_days, len(test_data)):
    X_test.append(test_data[i-n_days:i, 0])

X_test = np.array(X_test)

X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

prediction = model.predict(X_test)

prediction = scaler.inverse_transform(prediction)
prediction

rmse = np.sqrt(np.mean(prediction - y_test) ** 2)

print(rmse)



train_df = df[:training_len]
predict_df = df[training_len:]
predict_df["Prediction"] = prediction

predict_df.plot.line(x="Date", y=["Close", "Prediction"])

predict_df = predict_df.reset_index(drop=True)
predict_df.tail()

# to predict next day price
def predict_nextday(df_source):
    new_df = df_source.filter(["Close"])
    last_n_days = new_df[-60:].values
    last_n_days_scaled = scaler.transform(last_n_days)
    X_test = []
    X_test.append(last_n_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predict = model.predict(X_test)
    predict = scaler.inverse_transform(predict)
    return predict

def predict_nextday_dict(df_source):
    max_date = max(df_source["Date"])
    new_df = df_source.filter(["Close"])
    last_n_days = new_df[-60:].values
    last_n_days_scaled = scaler.transform(last_n_days)
    X_test = []
    X_test.append(last_n_days_scaled)
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predict = model.predict(X_test)
    predict = scaler.inverse_transform(predict)
    return {max_date, predict[0,0]}

predict_nextday_dict(df)

model.save("trained_model.h5")



