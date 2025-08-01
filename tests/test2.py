import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"
TMP_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3NTY0MzM1NTJ9.g4vm4jJA18FTAglvp5bZKpIj5kh_WaA_JmycowbkyQE"
HEADERS = {"Authorization": f"Bearer {TMP_TOKEN}"}

def make_samples(start_time, n):
    samples = []
    for i in range(n):
        ts = (start_time + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        samples.append({
            "timestamp": ts,
            "air_temp": 10.0 + (30.0 * i / max(1, n-1)),            # 10 to 40
            "air_humidity": 20.0 + (80.0 * i / max(1, n-1)),        # 20 to 100
            "air_pressure": 98000.0 + (6000.0 * i / max(1, n-1)),   # 98000 to 104000
            "soil_temp": 5.0 + (30.0 * i / max(1, n-1)),            # 5 to 35
            "soil_moisture": 10.0 + (40.0 * i / max(1, n-1)),       # 10 to 50
            "leaf_wetness_upper": 0.0 + (50.0 * i / max(1, n-1)),   # 0 to 50
            "leaf_wetness_lower": 0.0 + (50.0 * i / max(1, n-1))    # 0 to 50
        })
    return samples

def test_predict_dual_mode():
    start_time = datetime(2025, 7, 15, 6, 0, 0)  # Summer morning

    # Case 1: 4 samples (should use payload)
    payload_4 = {"samples": make_samples(start_time, 4)}
    resp_4 = requests.post(f"{BASE_URL}/predict", json=payload_4, headers=HEADERS)
    assert resp_4.status_code == 200, resp_4.text
    data_4 = resp_4.json()
    print("4-sample (in-range) mode output:", data_4)

    # Case 2: 2 samples (should combine input and record_data.json)
    payload_2 = {"samples": make_samples(start_time, 2)}
    resp_2 = requests.post(f"{BASE_URL}/predict", json=payload_2, headers=HEADERS)
    assert resp_2.status_code == 200, resp_2.text
    data_2 = resp_2.json()
    print("Combined mode output (input + record_data.json):", data_2)

if __name__ == "__main__":
    test_predict_dual_mode()