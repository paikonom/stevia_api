import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"
TMP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTY0MzM1NTJ9.g4vm4jJA18FTAglvp5bZKpIj5kh_WaA_JmycowbkyQE"

HEADERS = {"Authorization": f"Bearer {TMP_TOKEN}"}

def test_predict():
    """Test the /predict endpoint."""
    url = f"{BASE_URL}/predict"
    payload = {
        "timestamp": "2025-01-09T00:00:00Z",
        "air_temp": 14,
        "air_humidity": 62,
        "air_pressure": 100329,
        "soil_temp": -37.052307,
        "soil_moisture": 1.5028205,
        "leaf_wetness_upper": 41.227947,
        "leaf_wetness_lower": 41.438976
        }
    print(f"Testing /predict with payload: {payload}")
    response = requests.post(url, json=payload, headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except ValueError:
        print(f"Non-JSON Response: {response.text}")

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

if __name__ == "__main__":
    # print("Running test_predict...")
    # test_predict()
    print("\nRunning test_activate_rule...")
    test_activate_rule()