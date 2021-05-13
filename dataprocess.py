import pandas as pd

# moving avarage calculation function
def ma(df_source, date, n_days):
    index = df_source.index[df_source["Date"] == date][0]
    df = None
    if index == 0:
        df = df_source.iloc[0]
    elif index - n_days >= 0:
        df = df_source.iloc[index - n_days + 1 : index+1]
    else:
        df = df_source.iloc[0 : index + 1]
    return df["Close"].mean()

# compare close price function
def closediff(df_source, col, date):
    index = df_source.index[df_source["Date"] == date][0]
    diff = 0
    if index == 0:
        diff = 0
    else:
        diff = df_source.iloc[index][col] - df_source.iloc[index - 1][col]
    return diff

# calculate percentage of close different 
def diffpct(df_source, col, date):
    index = df_source.index[df_source["Date"] == date][0]
    diff = 0
    if index == 0:
        diff = 0
    else:
        diff = (df_source.iloc[index][col] - df_source.iloc[index - 1][col])/df_source.iloc[index - 1][col]
    return diff

# process bitcoin data
# load data
df_btc = pd.read_csv("./data/bitstampUSD_1-min_data_2012-01-01_to_2021-03-31.csv")

# drop na rows
df_btc = df_btc.dropna()

# leave only timestamp and close columns
df_btc_clean = df_btc[["Timestamp", "Close"]]

# convert timestamp to date and time
df_btc_clean["DateTime"] = pd.to_datetime(df_btc_clean['Timestamp'],unit='s')
df_btc_clean["Date"] = df_btc_clean["DateTime"].dt.date
df_btc_clean["Time"] = df_btc_clean["DateTime"].dt.time

# delete not used columns
df_btc_clean = df_btc_clean[["Date","Time", "Close"]]

# reset index
df_btc_clean = df_btc_clean.reset_index(drop=True)

# get the close value by using the max time of a date 
df_btc_close = df_btc_clean.groupby("Date").max("Time")

# reset index again
df_btc_close = df_btc_close.reset_index()

# sort by date
df_btc_close.sort_values(by="Date")

# reset index again
df_btc_close = df_btc_close.reset_index()

# make a copy of btc df
df_btc_close_ma = df_btc_close.copy()

# add different ma point to each date
ma_days = [5, 10, 20, 30, 60, 180, 240, 360]
for ma_day in ma_days:
    column_name = f"ma_{ma_day}"
    df_btc_close_ma[column_name] = df_btc_close_ma.apply(lambda x: ma(df_btc_close_ma, x["Date"], ma_day), axis=1)

# load and process other dataset
# process gold
df_gold = pd.read_csv("./data/All/Gold.csv", parse_dates=["Date"])
df_gold["Date"] = df_gold["Date"].dt.date
df_gold_clean = df_gold[["Date", "Close/Last"]]
df_gold_clean.columns = ["Date", "Gold"]
df_gold_clean["Gold"] = df_gold_clean["Gold"].str[1:]
df_gold_clean["Gold"] = df_gold_clean["Gold"].astype("float")
# merge with gold, first merge
df_combine = df_btc_close_ma.merge(df_gold_clean, on="Date")

# process NASDAQ Composite Index
df_nasdaq = pd.read_csv("./data/All/Nasdaq_COMP.csv", parse_dates=["Date"])
df_nasdaq["Date"] = df_nasdaq["Date"].dt.date
df_nasdaq_clean = df_nasdaq[["Date", "Close/Last"]]
df_nasdaq_clean.columns = ["Date", "Nasdaq_Comp"]
# merge with nsadaq
df_combine = df_combine.merge(df_nasdaq_clean, on="Date")

# process SP500
df_sp500 = pd.read_csv("./data/All/SP500.csv", parse_dates=["Date"])
df_sp500["Date"] = df_sp500["Date"].dt.date
df_sp500_clean = df_sp500[["Date", "Close/Last"]]
df_sp500_clean.columns = ["Date", "SP500"]
# merge with sp500
df_combine = df_combine.merge(df_sp500_clean, on="Date")

# process Dow Industrials
df_indu = pd.read_csv("./data/All/DowIndu.csv", parse_dates=["Date"])
df_indu["Date"] = df_indu["Date"].dt.date
df_indu_clean = df_indu[["Date", "Close/Last"]]
df_indu_clean.columns=["Date", "INDU"]
# merge with INDU
df_combine = df_combine.merge(df_indu_clean, on="Date")

# process Oil
df_oil = pd.read_csv("./data/All/Oil.csv", parse_dates=["Date"])
df_oil["Date"] = df_oil["Date"].dt.date
df_oil_clean = df_oil[["Date", "Close/Last"]]
df_oil_clean.columns = ["Date", "Oil"]
# merge with Oil
df_combine = df_combine.merge(df_oil_clean, on="Date")

# calculate day diff
df_combine_diff = df_combine.copy()
df_combine_diff["Btc_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "Close", x["Date"]), axis=1)
df_combine_diff["Gold_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "Gold", x["Date"]), axis=1)
df_combine_diff["Nasdaq_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "Nasdaq_Comp", x["Date"]), axis=1)
df_combine_diff["SP500_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "SP500", x["Date"]), axis=1)
df_combine_diff["INDU_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "INDU", x["Date"]), axis=1)
df_combine_diff["Oil_diff"] = df_combine_diff.apply(lambda x: closediff(df_combine_diff, "Oil", x["Date"]), axis=1)

# calculate day diff percentage
df_combine_diff["Btc_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "Close", x["Date"]), axis=1)
df_combine_diff["Gold_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "Gold", x["Date"]), axis=1)
df_combine_diff["Nasdaq_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "Nasdaq_Comp", x["Date"]), axis=1)
df_combine_diff["SP500_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "SP500", x["Date"]), axis=1)
df_combine_diff["INDU_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "INDU", x["Date"]), axis=1)
df_combine_diff["Oil_diffpct"] = df_combine_diff.apply(lambda x: diffpct(df_combine_diff, "Oil", x["Date"]), axis=1)

# save the df to csv
df_combine_diff.to_csv("./combine.csv")