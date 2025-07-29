from pydantic import BaseModel
from typing import List, Dict

# Input model for Neural Network
class NeuralNetInput(BaseModel):
    timestamp: str
    air_temp: float
    air_humidity: float
    air_pressure: float
    soil_temp: float
    soil_moisture: float
    leaf_wetness_upper: float
    leaf_wetness_lower: float

# Output model for NN
class NeuralNetOutput(BaseModel):
    predictions: List[float]

# Input model for Rule Activation
class RuleActivationInput(BaseModel):
    rule_id: str
    parameters: List[Dict]