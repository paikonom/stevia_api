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


@router.post("/activate-rule")
async def activate_rule(rule_data: RuleActivationInput, user: str = Depends(get_current_user)):
    data = rule_data.parameters  # Expecting a list of dicts with values

    # Validate input format 
    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="Invalid input format. Expected a list of values.")

    # Calculate averages for each parameter across all data
    averages = {}
    for param in RULES.keys():
        if param == "timestamp":
            continue  # Skip timestamp
        values = [entry[param] for entry in data if param in entry]
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        if numeric_values:
            averages[param] = sum(numeric_values) / len(numeric_values)
        else:
            averages[param] = None

    # Evaluate rules
    alerts = []
    for param, value in averages.items():
        if param in RULES and value is not None:
            rule = RULES[param]
            if "min" in rule and value < rule["min"]:
                alerts.append(rule["alert"])
            if "max" in rule and value > rule["max"]:
                alerts.append(rule["alert"])

    # Return response
    if alerts:
        return {"status": "alert", "alerts": alerts}
    return {"status": "ok", "message": "All values (avg) are within acceptable ranges."}
