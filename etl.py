import os
import csv
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, VARCHAR, DATETIME

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

table_name = "bitcoin_data"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table(table_name):
    print("Creating Table")

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

print("initdb complete")