# <YOUR_IMPORTS>
import datetime
import os
import dill
import json
import glob
import pandas as pd
from pydantic import BaseModel
from datetime import datetime


path = os.environ.get('PROJECT_PATH', '.')

list_of_files = os.listdir(f'{path}/data/models/')


def file_date(x):
    return x[-12:]


latest_file = sorted(list_of_files, key=file_date)[-1]
print(f'Latest Model: {latest_file}')
with open(f'{path}/data/models/{latest_file}', 'rb') as file:
    model = dill.load(file)


class Form(BaseModel):
    description: str
    fuel: str
    id: str
    image_url: str
    lat: float
    long: float
    manufacturer: str
    model: str
    odometer: int
    posting_date: str
    price: int
    region: str
    region_url: str
    state: str
    title_status: str
    transmission: str
    url: str
    year: int


class Prediction(BaseModel):
    car_id: str
    pred: str


def predict():
    def get_dict():
        file_path = path + '/data/test'
        predict_list = []
        for r, d, f in os.walk(file_path):
            for file in f:
                with open(file_path + '/' + file) as f1:
                    predict_list.append(json.load(f1))
        return predict_list

    def make_prediction(form: Form):
        import pandas as pd
        df = pd.DataFrame(form, index=[0])
        y = model.predict(df)
        return [form['id'], y[0]]

    pred_list = get_dict()
    pred_df = pd.DataFrame(columns=['car_id', 'pred'], index=[0])

    for i, item in enumerate(pred_list):
        pred_df.loc[i] = make_prediction(item)

    csv_filename = f'{path}/data/predictions/pred_{datetime.now().strftime("%Y%m%d%H%M")}.csv'
    pred_df.to_csv(csv_filename, index=False)


if __name__ == '__main__':
    predict()
