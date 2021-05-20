import os
import csv
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

table_name = "bitcoin_data"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table(table_name):
    print("Creating Table")

    new_table = Table(
        table_name, meta,
        Column('date', String),
        Column('close', Float),
        Column('real', Boolean)   
    )

    meta.create_all(engine)
    
    # seed_data = list()

    # with open('./data/combine.csv', newline='') as input_file:
    #     reader = csv.DictReader(input_file)       #csv.reader is used to read a file
    #     for row in reader:
    #         seed_data.append(row)
            
    # with engine.connect() as conn:
    #     conn.execute(new_table.insert(), seed_data)

    # load data
    df = pd.read_csv("./data/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv")
    df1 = pd.read_csv("./data/HistoricalData20210517.csv", parse_dates=["Date"])

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

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")