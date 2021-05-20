import model1
import model2
from datetime import datetime
# testing
#create_model()
dt = datetime.strptime("20210520", "%Y%m%d").date()
print(f"Model1 Predict Date {dt}: {model1.predict_date(dt)}")

input_list = ["oil_diff", "gold_diff"]
in_dict = {
    input_list[0] : [-10000],
    input_list[1] : [-200000]
}

print(f"Model2 Predict Price: {model2.predict(in_dict)}")