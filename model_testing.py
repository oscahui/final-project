import model1
import model2
import etl_func
from datetime import datetime

etl_func.init_table()

# testing
model1.create_model()
dt = datetime.strptime("20210523", "%Y%m%d").date()
print(f"Model1 Predict Date {dt}: {model1.predict_date(dt)}")



# test model2
column_list = ['date', 'close', 'real', 
        'gold', 'comp', 'spx', 'indu', 'oil', 
        'btc_diff', 'gold_diff', 'comp_diff', 'spx_diff', 'indu_diff', 'oil_diff',
        'btc_diffpct', 'gold_diffpct', 'comp_diffpct', 'spx_diffpct', 'indu_diffpct', 'oil_diffpct',
        'timestamp']

input_list = column_list[3:8] # ['gold', 'comp', 'sp500', 'indu', 'oil', 'timestamp']
input_list.append('timestamp')
print(input_list)
in_dict = {
    input_list[0] : [40],
    input_list[1] : [14000],
    input_list[2] : [43000],
    input_list[3] : [35000],
    input_list[4] : [20],
    input_list[5] : [1621555200000000000]
}
model2.create_model()
print(f"Model2 Predict Price: {model2.predict(in_dict)}")