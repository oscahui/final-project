import os
import pandas as pd
from pandas.io.sql import has_table
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR, DateTime

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '')

bitcoin_table = "bitcoin_data"
combine_table = "mix_data"

def init_table(drop=True):

    print("connection to databse: " + connection)
    engine = create_engine(connection)

    if drop:
        if engine.has_table(bitcoin_table):
            engine.execute(f"DROP table {bitcoin_table}")
        if engine.has_table(combine_table):
            engine.execute(f"DROP table {combine_table}")

    if not engine.has_table(bitcoin_table):
        print(f"Creating {bitcoin_table} Table")

        column_list = ['date', 'close', 'real',
            'ma_5', 'ma_10', 'ma_20', 'ma_30', 'ma_60',
            'ma_90', 'ma_180', 'ma_240', 'ma_360']
        new_table = Table(
            bitcoin_table, meta,
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

        df.to_sql(bitcoin_table, engine, if_exists="replace", index=False)

        print("Data Import Successful")
    else:
        
        print("Table Already Exists")

    if (not engine.has_table(combine_table)) or drop:
        print(f"Creating {combine_table} Table")
        column_list = ['date', 'close', 'real', 
            'gold', 'comp', 'spx', 'indu', 'oil', 
            'btc_diff', 'gold_diff', 'comp_diff', 'spx_diff', 'indu_diff', 'oil_diff',
            'btc_diffpct', 'gold_diffpct', 'comp_diffpct', 'spx_diffpct', 'indu_diffpct', 'oil_diffpct']
        new_table = Table(
            combine_table, meta,
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

        df.to_sql(combine_table, engine, if_exists="replace", index=False)

        print("Data Import Successful")
    else:
        print("Table Already Exists")

    print("initdb complete")

if __name__ == '__main__':
    init_table()