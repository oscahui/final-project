import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import joblib
from sqlalchemy import create_engine
import os

table_name = "mix_data"
db = os.environ.get('DATABASE_URL', '')
engine = create_engine(db)


column_list = ['date', 'close', 'real', 
        'gold', 'comp', 'spx', 'indu', 'oil', 
        'btc_diff', 'gold_diff', 'comp_diff', 'spx_diff', 'indu_diff', 'oil_diff',
        'btc_diffpct', 'gold_diffpct', 'comp_diffpct', 'spx_diffpct', 'indu_diffpct', 'oil_diffpct',
        'timestamp']

input_list = column_list[3:8]
input_list.append("timestamp")

def output(number):
    if number == -1:
        return "down"
    elif number == 1:
        return "up"
    else:
        return "nochange"

def create_model(feature_list=input_list):
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", engine)
 #   df = pd.read_csv("./data/combine.csv")

    df["trend"] = df.apply(lambda x: 1 if x["btc_diff"] > 0 else (-1 if x["btc_diff"] <0 else 0), axis=1)
    df["timestamp"] = pd.to_datetime(df["date"]).astype('int64')
    
    # to set ma days so the training data will start from the +1 day
    # only to use when use ma as feature
    ma_days = 0
    ind_train_start = ma_days
    ind_test_start = int((len(df) - ma_days) * 0.8)

    X = df[feature_list]
    y = df["trend"]

    X_train = X.iloc[ind_train_start:ind_test_start]
    X_test = X.iloc[ind_test_start:]
    X_test = X_test.iloc[:len(X_test)-1]
    X_test.iloc[0]

    y_train = y.iloc[ind_train_start+1:ind_test_start+1]
    y_test = y.iloc[ind_test_start+1:]

    X_scaler = MinMaxScaler().fit(X)
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)

    model = SVC(kernel='linear')

    param_grid = {'C': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 1000],
                  'gamma': [0.00001, 0.0005, 0.0001, 0.0005, 0.0001]}
    grid = GridSearchCV(model, param_grid, verbose=3)

    grid.fit(X_train_scaled, y_train)

    joblib.dump(grid, "model/svc.h5")
    joblib.dump(X_scaler, "model/svc.scl")

def predict(price_dict):
    model = joblib.load("model/svc.h5")
    scaler = joblib.load("model/svc.scl")
    input = {}
    for i in input_list:
        input[i] = price_dict[i]
    print(input)
    X = pd.DataFrame.from_dict(input)
    X_scaled = scaler.transform(X)
    return  output(model.predict(X_scaled)[0])
