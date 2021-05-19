import os
import csv
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.sql.sqltypes import VARCHAR

meta = MetaData()

connection = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

print("connection to databse: " + connection)
engine = create_engine(connection)

if not engine.has_table("bitcoin_data"):
    print("Creating Table")

    new_table = Table(
        'bitcoin_data', meta,Column('date', String),
        Column('close', Float),
        Column('ma_5', Float),
        Column('ma_10', Float),
        Column('ma_20', Float),
        Column('ma_30', Float),
        Column('ma_60', Float),
        Column('ma_90', Float),
        Column('ma_180', Float),
        Column('ma_240', Float),
        Column('ma_360', Float),
        Column('gold', Float),
        Column('nasdaq_comp', Float),
        Column('sp500', Float),
        Column('indu', Float),
        Column('oil', Float),
        Column('btc_diff', Float),
        Column('gold_diff', Float),
        Column('nasdaq_diff', Float),
        Column('sp500_diff', Float),
        Column('indu_diff', Float),
        Column('oil_diff', Float),
        Column('btc_diffpct', Float),
        Column('gold_diffpct', Float),
        Column('nasdaq_diffpct', Float),
        Column('sp500_diffpct', Float),
        Column('indu_diffpct', Float),
        Column('oil_diffpct', Float),       
    )

    meta.create_all(engine)
    
    seed_data = list()

    with open('./data/combine.csv', newline='') as input_file:
        reader = csv.DictReader(input_file)       #csv.reader is used to read a file
        for row in reader:
            seed_data.append(row)
            
    with engine.connect() as conn:
        conn.execute(new_table.insert(), seed_data)

    print("Data Import Successful")
else:
    print("Table already exists")

print("initdb complete")