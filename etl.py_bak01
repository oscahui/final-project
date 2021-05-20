import os
import csv
import pandas as pd
from pandas.io.sql import has_table
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR, DATETIME

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

table_name = "bitcoin_data"
table_name2 = "mix_data"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table(table_name):
    print(f"Creating {table_name} Table")

    new_table = Table(
        table_name, meta,
        Column('date', DATETIME),
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
    df = pd.read_csv("./data/bitcoin.csv")
    df = df.reset_index(drop=True)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

if not engine.has_table(table_name2):
    print(f"Creating {table_name} Table")
    column_list = ['date', 'close', 'ma_5', 'ma_10', 'ma_20', 'ma_30', 'ma_60', 'ma_90',
       'ma_180', 'ma_240', 'ma_360', 'gold', 'nasdaq_comp', 'sp500', 'indu',
       'oil', 'btc_diff', 'gold_diff', 'nasdaq_diff', 'sp500_diff',
       'indu_diff', 'oil_diff', 'btc_diffpct', 'gold_diffpct',
       'nasdaq_diffpct', 'sp500_diffpct', 'indu_diffpct', 'oil_diffpct']
    new_table = Table(
        table_name2, meta,
        Column(column_list[0], DATETIME),
        Column(column_list[1], Float),
        Column(column_list[2], Float),
        Column(column_list[3], Float),
        Column(column_list[4], Float),
        Column(column_list[5], Float),
        Column(column_list[6], Float),
        Column(column_list[7], Float),
        Column(column_list[8], Float),
        Column(column_list[9], Float),
        Column(column_list[10], Float),
        Column(column_list[11], Float),
        Column(column_list[12], Float),
        Column(column_list[13], Float),
        Column(column_list[14], Float),
        Column(column_list[15], Float),
        Column(column_list[16], Float),
        Column(column_list[17], Float),
        Column(column_list[18], Float),
        Column(column_list[19], Float),
        Column(column_list[20], Float),
        Column(column_list[21], Float),
        Column(column_list[22], Float),
        Column(column_list[23], Float),
        Column(column_list[24], Float),
        Column(column_list[25], Float),
        Column(column_list[26], Float),
        Column(column_list[27], Float)
    )

    meta.create_all(engine)

    df = pd.read_csv("./data/combine.csv")

    df.to_sql(table_name2, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")