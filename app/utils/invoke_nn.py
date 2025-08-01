import torch
import os
import json
import numpy as np
from datetime import datetime, timedelta
from app.utils import lstm_model
import urllib.request
from dateutil.parser import parse

def retrieve_closest_indexes(data, previous_samples_num):
    minDistanceDate = datetime.today()
    indexes = []
    dates = []
    for predSample in range(0, previous_samples_num):
        minDistanceDateTest = minDistanceDate + timedelta(hours=-3 * predSample)
        dates.append(minDistanceDateTest)
        bestCost = timedelta.max
        bestI = -1
        for i in range(len(data) - 1, len(data) - 1 - 20, -1):
            date = datetime.fromtimestamp(data[f'{i}']['timestamp'] / 1e3)
            if (minDistanceDateTest - date) < bestCost:
                bestCost = (minDistanceDateTest - date)
                bestI = i
        indexes.append(bestI)
    indexes.reverse()
    return indexes, dates

def load_model(what_to_predict):
    model = lstm_model.LSTMModel(10, 256, 64, 4)
    model_path = os.path.join(os.path.dirname(__file__), "data", f"stevia_{what_to_predict}_nn.pth")
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    return model

def get_weather_data():
    try:
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/38.9125%2C22.4280?unitGroup=metric&key=DZENVN3LSWYNLL5F2BJWKUX8P&contentType=json"
        result_bytes = urllib.request.urlopen(url)
        json_data = json.load(result_bytes)
        json_str = json.dumps(json_data, indent=4)
        with open(os.path.join(os.path.dirname(__file__), "data", "weather_data.json"), "w") as f:
            f.write(json_str)
        return json_data
    except urllib.error.HTTPError as e:
        error_info = e.read().decode()
        print('Error code: ', e.code, error_info)
        with open(os.path.join(os.path.dirname(__file__), "data", "weather_data.json"), "r") as f:
            json_data = json.load(f)
            return json_data
    except urllib.error.URLError as e:
        error_info = e.read().decode()
        print('Error code: ', e.code, error_info)
        with open(os.path.join(os.path.dirname(__file__), "data", "weather_data.json"), "r") as f:
            json_data = json.load(f)
            return json_data

# def construct_previous_samples(indexes, dates, d, minmax, weather_json):
#     variables_path = os.path.join(os.path.dirname(__file__), "data", "variables_to_train_on.txt")
#     weather_variables_path = os.path.join(os.path.dirname(__file__), "data", "weather_variables_to_train_on.txt")

#     with open(variables_path, "r") as f:
#         variables_to_train_on = [s.strip() for s in f.readlines()]
#     with open(weather_variables_path, "r") as f:
#         weather_variables_to_train_on = [s.strip() for s in f.readlines()]

#     testX = []
#     for ind, i in enumerate(indexes):
#         date = datetime.fromtimestamp(d[f'{i}']['timestamp'] / 1e3)
#         sampleX = []
#         for variable_name in variables_to_train_on:
#             if variable_name in ['timestamp', 'month', 'day']:
#                 variable_name1 = 'hour' if variable_name == 'timestamp' else variable_name
#                 sampleX.append((getattr(dates[ind], variable_name1) - minmax[f'{variable_name}_data'][0]) /
#                                (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))
#             else:
#                 sampleX.append((d[f'{i}'][variable_name] - minmax[f'{variable_name}_data'][0]) /
#                                (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))
#         testX.append(sampleX)

#     sampleX1 = []
#     for variable_name in weather_variables_to_train_on:
#         sampleX1.append((weather_json["days"][0][variable_name] - minmax[f'{variable_name}_data'][0]) /
#                         (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))

#     testX = np.array(testX).astype(float)
#     testX1 = np.array(sampleX1).astype(float)
#     return testX, testX1

def construct_previous_samples(indexes, dates, d, minmax, weather_json):
    variables_path = os.path.join(os.path.dirname(__file__), "data", "variables_to_train_on.txt")
    weather_variables_path = os.path.join(os.path.dirname(__file__), "data", "weather_variables_to_train_on.txt")

    with open(variables_path, "r") as f:
        variables_to_train_on = [s.strip() for s in f.readlines()]
    with open(weather_variables_path, "r") as f:
        weather_variables_to_train_on = [s.strip() for s in f.readlines()]

    testX = []
    for ind, i in enumerate(indexes):
        # Fix: parse ISO string to datetime
        if isinstance(d[f'{i}']['timestamp'], str):
            date = parse(d[f'{i}']['timestamp'])
        else:
            date = datetime.fromtimestamp(d[f'{i}']['timestamp'] / 1e3)
        sampleX = []
        for variable_name in variables_to_train_on:
            if variable_name in ['timestamp', 'month', 'day']:
                variable_name1 = 'hour' if variable_name == 'timestamp' else variable_name
                sampleX.append((getattr(dates[ind], variable_name1) - minmax[f'{variable_name}_data'][0]) /
                               (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))
            else:
                sampleX.append((d[f'{i}'][variable_name] - minmax[f'{variable_name}_data'][0]) /
                               (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))
        testX.append(sampleX)

    sampleX1 = []
    for variable_name in weather_variables_to_train_on:
        sampleX1.append((weather_json["days"][0][variable_name] - minmax[f'{variable_name}_data'][0]) /
                        (minmax[f'{variable_name}_data'][1] - minmax[f'{variable_name}_data'][0]))

    testX = np.array(testX).astype(float)
    testX1 = np.array(sampleX1).astype(float)
    return testX, testX1

# Test invoke with predated data
# def invoke(what_to_predict: str, previous_samples_num: int):
#     model = load_model(what_to_predict)
#     data_path = os.path.join(os.path.dirname(__file__), "data")
#     with open(os.path.join(data_path, "sample.json")) as f:
#         minmax = json.load(f)
#     weather_json = get_weather_data()
#     with open(os.path.join(data_path, "record_data.json")) as f:
#         d = json.load(f)
#         indexes, dates = retrieve_closest_indexes(d, previous_samples_num)
#         testX, testX1 = construct_previous_samples(indexes, dates, d, minmax, weather_json)
#         predictions_tensor = lstm_model.infer(model, testX, testX1) * (
#             minmax[f'{what_to_predict}_data'][1] - minmax[f'{what_to_predict}_data'][0]
#         ) + minmax[f'{what_to_predict}_data'][0]
#         # print(predictions_tensor)
#         return predictions_tensor

def invoke(what_to_predict: str, samples_or_list):
    model = load_model(what_to_predict)
    data_path = os.path.join(os.path.dirname(__file__), "data")
    with open(os.path.join(data_path, "sample.json")) as f:
        minmax = json.load(f)
    weather_json = get_weather_data()
    previous_samples_num = 4

    if isinstance(samples_or_list, list):
        client_samples = samples_or_list
        n_client = len(client_samples)
        if n_client == 0:
            raise ValueError("At least one sample is required for prediction.")

        if n_client < previous_samples_num:
            # Fill with closest from record_data.json
            with open(os.path.join(data_path, "record_data.json")) as f:
                record_data = json.load(f)
            # Find the closest samples in record_data.json for each missing sample
            needed = previous_samples_num - n_client
            # Use the timestamp of the oldest client sample as reference
            ref_time = parse(client_samples[0]['timestamp'])
            # Use retrieve_closest_indexes to get the right indexes/dates
            indexes, dates = retrieve_closest_indexes(record_data, needed)
            # Build the combined sample list: records first, then client samples
            d = {}
            for idx, i in enumerate(indexes):
                d[str(idx)] = record_data[str(i)]
            for idx, sample in enumerate(client_samples):
                d[str(needed + idx)] = sample
            # Dates: records first, then client sample dates
            record_dates = dates
            client_dates = [parse(s['timestamp']) for s in client_samples]
            all_dates = record_dates + client_dates
            all_indexes = list(range(previous_samples_num))
        else:
            # Use only client samples
            d = {str(i): sample for i, sample in enumerate(client_samples[-previous_samples_num:])}
            all_indexes = list(range(previous_samples_num))
            all_dates = [parse(s['timestamp']) for s in client_samples[-previous_samples_num:]]
    else:
        # Fallback: use record_data.json for the last N samples
        with open(os.path.join(data_path, "record_data.json")) as f:
            d = json.load(f)
        all_indexes, all_dates = retrieve_closest_indexes(d, samples_or_list)

    testX, testX1 = construct_previous_samples(all_indexes, all_dates, d, minmax, weather_json)
    predictions_tensor = lstm_model.infer(model, testX, testX1) * (
        minmax[f'{what_to_predict}_data'][1] - minmax[f'{what_to_predict}_data'][0]
    ) + minmax[f'{what_to_predict}_data'][0]
    return predictions_tensor