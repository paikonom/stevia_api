import requests

BASE_URL = "http://127.0.0.1:8000/api/v1"
TMP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTY0MTQzNzF9.ROTkB6YsgHKieSnLdS2mkalWiJQ2M2-uOpo10FZ9wUI"

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
            {
                "timestamp": "2025-01-09T00:00:00Z",
                "air_temp": 14,
                "air_humidity": 62,
                "soil_temp": -37.052307,
                "leaf_wetness_upper": 41.227947,
                "dpd": 6.112051
            },
            {
                "timestamp": "2025-01-12T00:00:00Z",
                "air_temp": 4,
                "air_humidity": 93,
                "soil_temp": -37.67322,
                "leaf_wetness_upper": 39.25424,
                "dpd": 2.8415253
            }
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
    print("Running test_predict...")
    test_predict()
    print("\nRunning test_activate_rule...")
    test_activate_rule()