import requests
from datetime import datetime, timedelta


BASE_URL = "http://127.0.0.1:8000/api/v1"
TMP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTY0MzM1NTJ9.g4vm4jJA18FTAglvp5bZKpIj5kh_WaA_JmycowbkyQE"

HEADERS = {"Authorization": f"Bearer {TMP_TOKEN}"}

def test_predict():
    payload = {
        "samples": [
            {
                "timestamp": "2025-07-15T12:00:00Z",
                "air_temp": 25.0,              # between -5.0 and 58.0
                "air_humidity": 50.0,          # between 4.0 and 100.0
                "air_pressure": 100500.0,      # between 99111.0 and 103295.0
                "soil_temp": 20.0,             # between 7.76 and 33.04
                "soil_moisture": 15.0,         # between 7.47 and 24.73
                "leaf_wetness_upper": 43.0,    # between 41.89 and 44.11
                "leaf_wetness_lower": 35.0
            }#,
            # {
            #     "timestamp": "2025-01-09T01:00:00Z",
            #     "air_temp": 21.0,
            #     "air_humidity": 71.0,
            #     "air_pressure": 100010.0,
            #     "soil_temp": 15.5,
            #     "soil_moisture": 1.6,
            #     "leaf_wetness_upper": 41.0,
            #     "leaf_wetness_lower": 38.5
            # },
            # {
            #     "timestamp": "2025-01-09T02:00:00Z",
            #     "air_temp": 22.0,
            #     "air_humidity": 72.0,
            #     "air_pressure": 100020.0,
            #     "soil_temp": 16.0,
            #     "soil_moisture": 1.7,
            #     "leaf_wetness_upper": 42.0,
            #     "leaf_wetness_lower": 38.0
            # },
            # {
            #     "timestamp": "2025-01-09T03:00:00Z",
            #     "air_temp": 23.0,
            #     "air_humidity": 73.0,
            #     "air_pressure": 100030.0,
            #     "soil_temp": 16.5,
            #     "soil_moisture": 1.8,
            #     "leaf_wetness_upper": 43.0,
            #     "leaf_wetness_lower": 37.5
            # }
        ]
    }
    response = requests.post(f"{BASE_URL}/predict", json=payload, headers=HEADERS)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "leaf_wetness_upper" in data
    assert "leaf_wetness_lower" in data
    assert "soil_moisture" in data
    assert "soil_temp" in data
    print("Test passed:", data)

def test_activate_rule():
    """Test the /activate-rule endpoint."""
    url = f"{BASE_URL}/activate-rule"
    payload = {
        "rule_id": "environment_check",
        "parameters": [
        {"timestamp": "2025-01-09T00:00:00Z", "air_temp": 19, "air_humidity": 70, "soil_temp": 14, "leaf_wetness_upper": 51, "dpd": 1.5},
        {"timestamp": "2025-01-10T00:00:00Z", "air_temp": 21, "air_humidity": 75, "soil_temp": 16, "leaf_wetness_upper": 49, "dpd": 2.5},
        {"timestamp": "2025-01-11T00:00:00Z", "air_temp": 22, "air_humidity": 72, "soil_temp": 17, "leaf_wetness_upper": 48, "dpd": 2.0},
        {"timestamp": "2025-01-12T00:00:00Z", "air_temp": 18, "air_humidity": 68, "soil_temp": 13, "leaf_wetness_upper": 52, "dpd": 1.8},
        {"timestamp": "2025-01-13T00:00:00Z", "air_temp": 23, "air_humidity": 77, "soil_temp": 18, "leaf_wetness_upper": 47, "dpd": 2.2},
        {"timestamp": "2025-01-14T00:00:00Z", "air_temp": 20, "air_humidity": 80, "soil_temp": 15, "leaf_wetness_upper": 50, "dpd": 2.1},
        {"timestamp": "2025-01-15T00:00:00Z", "air_temp": 24, "air_humidity": 65, "soil_temp": 19, "leaf_wetness_upper": 46, "dpd": 2.3},
        {"timestamp": "2025-01-16T00:00:00Z", "air_temp": 25, "air_humidity": 78, "soil_temp": 20, "leaf_wetness_upper": 45, "dpd": 2.4},
        {"timestamp": "2025-01-17T00:00:00Z", "air_temp": 26, "air_humidity": 79, "soil_temp": 21, "leaf_wetness_upper": 44, "dpd": 2.6},
        {"timestamp": "2025-01-18T00:00:00Z", "air_temp": 27, "air_humidity": 66, "soil_temp": 22, "leaf_wetness_upper": 43, "dpd": 2.7}
        ]
    }
    print(f"Testing /activate-rule with payload: {payload}")
    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Non-JSON Response: {response.text}")

def make_samples(start_time, n):
    samples = []
    for i in range(n):
        ts = (start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        samples.append({
            "timestamp": ts,
            "air_temp": 20.0 + i,
            "air_humidity": 70.0 + i,
            "air_pressure": 100000.0 + i,
            "soil_temp": 15.0 + i * 0.5,
            "soil_moisture": 1.5 + i * 0.1,
            "leaf_wetness_upper": 40.0 + i,
            "leaf_wetness_lower": 39.0 + i
        })
    return samples

def test_predict_batch():
    start_time = datetime(2025, 1, 9, 0, 0, 0)
    for call in range(3):
        payload = {"samples": make_samples(start_time + timedelta(days=call), 10)}
        response = requests.post(f"{BASE_URL}/predict", json=payload, headers=HEADERS)
        assert response.status_code == 200, f"Call {call+1} failed: {response.text}"
        data = response.json()
        assert "leaf_wetness_upper" in data
        assert "leaf_wetness_lower" in data
        assert "soil_moisture" in data
        assert "soil_temp" in data
        print(f"Call {call+1} passed:", {k: v[:2] for k, v in data.items()})  # print only first 2 values for brevity

def make_samples2(start_time, n):
    samples = []
    for i in range(n):
        ts = (start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        samples.append({
            "timestamp": ts,
            "air_temp": 20.0 + i * 0.1,
            "air_humidity": 70.0 + i * 0.2,
            "air_pressure": 100000.0 + i,
            "soil_temp": 15.0 + i * 0.05,
            "soil_moisture": 1.5 + i * 0.01,
            "leaf_wetness_upper": 40.0 + i * 0.1,
            "leaf_wetness_lower": 39.0 + i * 0.1
        })
    return samples

# def test_predict_100():
#     start_time = datetime(2025, 1, 9, 0, 0, 0)
#     payload = {"samples": make_samples2(start_time, 100)}
#     response = requests.post(f"{BASE_URL}/predict", json=payload, headers=HEADERS)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert "leaf_wetness_upper" in data
#     assert "leaf_wetness_lower" in data
#     assert "soil_moisture" in data
#     assert "soil_temp" in data
#     print("Test passed. First 2 values of each output:", {k: v[:2] for k, v in data.items()})

def make_samples_100(start_time, n=100):
    samples = []
    for i in range(n):
        ts = (start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        samples.append({
            "timestamp": ts,
            "air_temp": 20.0 + i * 0.1,
            "air_humidity": 70.0 + i * 0.2,
            "air_pressure": 100000.0 + i,
            "soil_temp": 15.0 + i * 0.05,
            "soil_moisture": 1.5 + i * 0.01,
            "leaf_wetness_upper": 40.0 + i * 0.1,
            "leaf_wetness_lower": 39.0 + i * 0.1
        })
    return samples

def test_predict_100():
    start_time = datetime(2025, 1, 9, 0, 0, 0)
    payload = {"samples": make_samples2(start_time, 100)}
    response = requests.post(f"{BASE_URL}/predict", json=payload, headers=HEADERS)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "leaf_wetness_upper" in data
    assert "leaf_wetness_lower" in data
    assert "soil_moisture" in data
    assert "soil_temp" in data
    print("Test passed. Prediction output:", data)

if __name__ == "__main__":
    # print("Running test_predict...")
    test_predict()
    # print("\nRunning test_activate_rule...")
    # test_activate_rule()
    # test_predict_batch()
    # test_predict_100()