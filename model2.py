import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import joblib

def create_model():
    df = pd.read_csv("./data/combine.csv")

    df["trend"] = df.apply(lambda x: 1 if x["btc_diff"] > 0 else (-1 if x["btc_diff"] <0 else 0), axis=1)

    ind_train_start = 360
    ind_test_start = int((len(df) - 360) * 0.8)

    X = df[["oil", "gold"]]
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

    joblib.dump(grid, "svc.h5")
    joblib.dump(X_scaler, "svc.scl")

def predict(oil_price, gold_price):
    model = joblib.load("svc.h5")
    scaler = joblib.load("svc.scl")
    X = pd.DataFrame({
        "oil": [oil_price],
        "gold": [gold_price]
    })
    X_scaled = scaler.transform(X)
    print(X.head())
    print(model.predict(X_scaled))

#create_model()
# predict(140000,1200000)