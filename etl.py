import os
import csv
import pandas as pd
from pandas.io.sql import has_table
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR, DateTime

meta = MetaData()

#os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:168168@localhost:5432/bitcoin_db"
connection = os.environ.get('DATABASE_URL', '')

table_name = "bitcoin_data"
table_name2 = "mix_data"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table(table_name):
    print(f"Creating {table_name} Table")

    column_list = ['date', 'close', 'real', 'ma_5', 'ma_10', 'ma_20', 'ma_30', 'ma_60',
       'ma_90', 'ma_180', 'ma_240', 'ma_360']
    new_table = Table(
        table_name, meta,
        Column(column_list[0], DateTime),
        Column(column_list[1], Float),
        Column(column_list[2], Boolean),
        Column(column_list[3], Float),
        Column(column_list[4], Float),
        Column(column_list[5], Float),
        Column(column_list[6], Float),
        Column(column_list[7], Float),
        Column(column_list[8], Float),
        Column(column_list[9], Float),
        Column(column_list[10], Float),
        Column(column_list[11], Float) 
    )

    meta.create_all(engine)

    # load data
    df = pd.read_csv("./data/bitcoin.csv")
    df = df.reset_index(drop=True)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

if not engine.has_table(table_name2):
    print(f"Creating {table_name2} Table")
    column_list = ['date', 'close', 'real', 
        'gold', 'comp', 'spx', 'indu', 'oil', 
        'btc_diff', 'gold_diff', 'comp_diff', 'spx_diff', 'indu_diff', 'oil_diff',
        'btc_diffpct', 'gold_diffpct', 'comp_diffpct', 'spx_diffpct', 'indu_diffpct', 'oil_diffpct']
    new_table = Table(
        table_name2, meta,
        Column(column_list[0], DateTime),
        Column(column_list[1], Float),
        Column(column_list[2], Boolean),
        Column(column_list[3], Float),
        Column(column_list[4], Float),
        Column(column_list[5], Float),
        Column(column_list[6], Float), 
        Column(column_list[7], Float), #"oil"
        Column(column_list[8], Float),
        Column(column_list[9], Float),
        Column(column_list[10], Float),
        Column(column_list[11], Float),
        Column(column_list[12], Float), 
        Column(column_list[13], Float), # oil_diff
        Column(column_list[14], Float), 
        Column(column_list[15], Float),
        Column(column_list[16], Float),
        Column(column_list[17], Float),
        Column(column_list[18], Float),
        Column(column_list[19], Float) # oil_diffpct
    )

    meta.create_all(engine)

    df = pd.read_csv("./data/combine.csv")

    df.to_sql(table_name2, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")