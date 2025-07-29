from fastapi import APIRouter, Depends, HTTPException
from app.models import RuleActivationInput
from app.auth import get_current_user
from datetime import datetime
from collections import defaultdict
import requests

router = APIRouter()

# Define rules
RULES = {
    "timestamp": "2025-01-09 00:00:00",
    "air_temp": {"min": 20, "max": 30, "alert": "Out of range air temperature (<20°C or >30°C)"},
    "air_humidity": {"min": 65, "max": 80, "alert": "Out of range air humidity (<65% or >80%)"},
    "soil_temp": {"min": 15, "alert": "Low soil temperature (<15°C)"},
    "leaf_wetness_upper": {"max": 50, "alert": "Excessive leaf wetness (>50%)"},
    "dpd": {"min": 2, "alert": "Low dew point depression (<2°C)"}
}


# OLD TEST CODE
# @router.post("/activate-rule")
# async def activate_rule(rule_data: RuleActivationInput, user: str = Depends(get_current_user)):
#     # Simulate rule activation
#     # Replace this with actual rule activation logic
#     return {"message": f"Rule {rule_data.rule_id} activated with parameters {rule_data.parameters}"}

# Version 2 old
# @router.post("/activate-rule")
# async def activate_rule(rule_data: RuleActivationInput, user: str = Depends(get_current_user)):
#     parameters = rule_data.parameters
#     timestamp = parameters.get("timestamp")

#     # Validate timestamp
#     try:
#         timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid timestamp format. Use 'YYYY-MM-DD HH:MM:SS'.")

#     # Evaluate rules
#     alerts = []
#     for param, value in parameters.items():
#         if param in RULES:
#             rule = RULES[param]
#             if "min" in rule and value < rule["min"]:
#                 alerts.append(rule["alert"])
#             if "max" in rule and value > rule["max"]:
#                 alerts.append(rule["alert"])

#     # Return response
#     if alerts:
#         return {"status": "alert", "alerts": alerts, "timestamp": timestamp}
#     return {"status": "ok", "message": "All parameters are within acceptable ranges.", "timestamp": timestamp}

@router.post("/activate-rule")
async def activate_rule(rule_data: RuleActivationInput, user: str = Depends(get_current_user)):
    data = rule_data.parameters  # Expecting a list of timestamps with values

    # Validate input format 
    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Invalid input format. Expected a list of timestamped values.")

    # Group data by hour
    hourly_data = defaultdict(list)
    for entry in data:
        try:
            timestamp = entry["timestamp"]
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")  # ISO 8601 format
            hour = timestamp_dt.strftime("%Y-%m-%d %H:00:00")  # Group by hour
            hourly_data[hour].append(entry)
        except (KeyError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid timestamp format or missing timestamp.")
        
    # Calculate hourly averages
    hourly_averages = {}
    for hour, entries in hourly_data.items():
        averages = {}
        for param in RULES.keys():
            values = [entry[param] for entry in entries if param in entry]
            numeric_values = [v for v in values if isinstance(v, (int, float))]
            if numeric_values:  # Ensure the list is not empty
                averages[param] = sum(numeric_values) / len(numeric_values)
            else:
                averages[param] = None  # Or handle this case as needed
        hourly_averages[hour] = averages

    # Evaluate rules
    alerts = []
    for hour, averages in hourly_averages.items():
        for param, value in averages.items():
            if param in RULES:
                rule = RULES[param]
                if "min" in rule and value < rule["min"]:
                    alerts.append(f"{hour}: {rule['alert']}")
                if "max" in rule and value > rule["max"]:
                    alerts.append(f"{hour}: {rule['alert']}")

    # Return response
    if alerts:
        return {"status": "alert", "alerts": alerts}
    return {"status": "ok", "message": "All hourly averages are within acceptable ranges."}
