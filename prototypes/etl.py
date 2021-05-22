import os
import csv
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Date, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR, DATETIME

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

table_name = "bitcoin_data"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table(table_name):
    print("Creating Table")

    if connection == "sqlite:///db.sqlite":
        new_table = Table(
            table_name, meta,
            Column('date', DateTime),
            Column('close', Float),
            Column('real', Boolean)   
        )
    else:
            new_table = Table(
            table_name, meta,
            Column('date', Date),
            Column('close', Float),
            Column('real', Boolean)   
        )

    meta.create_all(engine)
    
    df = pd.read_csv("./data/bitcoin.csv")
    df = df.reset_index(drop=True)

    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")