import model1
import model2
from datetime import datetime

# testing
model1.create_model()
dt = datetime.strptime("20210523", "%Y%m%d").date()
print(f"Model1 Predict Date {dt}: {model1.predict_date(dt)}")
print(f"Model1 Predict Date {dt}: {(model1.predict_date_df(dt)).tail()}")

