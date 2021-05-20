import pandas as pd
from sqlalchemy import create_engine

# load datafrom csv
df = pd.read_csv("../data/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv")
df1 = pd.read_csv("../data/HistoricalData20210517.csv", parse_dates=["Date"])

# process dataframe from kaggle
df = df.dropna()

# timestamp to datetime
df["DateTime"] = pd.to_datetime(df['Timestamp'],unit='s')
df["Date"] = df["DateTime"].dt.date
df["Time"] = df["DateTime"].dt.time

# keep only useful columns and add a column indicate weather the close value is acctual or predict
df = df[["Date","Time", "Close"]]
df["Real"] = True

# get the date closing price then sort and reset index
df = df.groupby("Date").max("Time")
df = df.reset_index()
df = df.sort_values(by="Date")
df = df.reset_index(drop=True)

# process dataframe from nasdaq
df1 = df1.sort_values(by="Date")
df1 = df1.reset_index(drop=True)
df1 = df1[["Date", "Close/Last"]]
df1.columns = ["Date", "Close"]
df1["Date"] = df1["Date"].dt.date
df1["Real"] = True

# concat two dataset 
df_max_date = max(df["Date"])
df = pd.concat([df, df1.loc[df1["Date"]>df_max_date]])

# reset index again
df = df.reset_index(drop=True)

# load to sqlite
engine = create_engine('sqlite:///../data/bitcoin.sqlite', echo=True)
connection = engine.connect()
df.to_sql("bitcoin", connection, if_exists="replace", index=False)