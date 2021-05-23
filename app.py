import pandas as pd
from flask import (Flask, render_template, jsonify, request, redirect)
import simplejson
from flask_sqlalchemy import SQLAlchemy
from joblib import load
from datetime import datetime
import os
import model.model1 as model1
import model.model2 as model2
from model.models import create_bitcoin_data_classes, create_mix_data_classes
import etl_func


app = Flask(__name__)

# setup DB connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '')

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create db connection
db = SQLAlchemy(app)

# create a reference to the CRIME_LGA class
bitcoin_data = create_bitcoin_data_classes(db)
mix_data = create_mix_data_classes(db)

@app.route('/')
def index():
    """
    Display the main webpage where users can enter their details
    which we will then pass to the prediction endpoint
    """
    return render_template("index.html")

# route to do the initial data load to database


@app.route("/loaddata")
def load_data():
    etl_func.init_table()
    return render_template("index.html")


# use model2, json format as follow
# can define a function to convert date to timestamp
# {
#     "gold":         [40],
#     "comp":         [14000],
#     "spx" :       [43000],
#     "indu" :        [35000],
#     "oil" :         [20],
#     "timestamp" :   [1621555200000000000]
# }
@app.route("/predict/feature", methods=["POST"])
def predict_feature():
    data = request.json
    columns = list(data.keys())

    # model2.create_model(columns)

    # create dataframe from received data
    # rename columns and sort as per the
    # order columns were trained on
    try:
        df = pd.DataFrame([data])
    except Exception as e:
        print("Error Parsing Input Data")
        print(e)
        return "Error"

    predict = model2.predict(df)
    print(f"predicted Value: {predict}")
    return jsonify({
        "predict": predict
    })


# use model2, json format as follow:
# {
#     "type": "price",
#     "date": "24/05/2021"
# }
# change the orient="split" to get different json format for the dataframe
@app.route("/predict/date", methods=["POST"])
def predict_date():
    data = request.json
    p_type = data["type"]
    date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    result = {}

    # to return just the predict price for the date
    result["predict"] = float(model1.predict_date(date))
    #result["trend"] = (model1.predict_date_df(date)).to_json(orient="split")

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
