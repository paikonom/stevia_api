from pydantic import BaseModel
from typing import List, Dict

class NeuralNetInputSample(BaseModel):
    timestamp: str
    air_temp: float
    air_humidity: float
    air_pressure: float
    soil_temp: float
    soil_moisture: float
    leaf_wetness_upper: float
    leaf_wetness_lower: float

# Input model for Neural Network
class NeuralNetInput(BaseModel):
    # timestamp: str
    # air_temp: float
    # air_humidity: float
    # air_pressure: float
    # soil_temp: float
    # soil_moisture: float
    # leaf_wetness_upper: float
    # leaf_wetness_lower: float
    samples: List[NeuralNetInputSample]

# Output model for NN
class NeuralNetOutput(BaseModel):
    leaf_wetness_upper: List[float]
    leaf_wetness_lower: List[float]
    soil_moisture: List[float]
    soil_temp: List[float]

# Input model for Rule Activation
class RuleActivationInput(BaseModel):
    rule_id: str
    parameters: List[Dict]