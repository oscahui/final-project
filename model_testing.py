import model1
from datetime import datetime
# testing
#create_model()
dt = datetime.strptime("20210520", "%Y%m%d").date()
print(f"Predict Date {dt}: {model1.predict_date(dt)}")