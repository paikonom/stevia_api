from fastapi import APIRouter, Depends
from app.models import NeuralNetInput, NeuralNetOutput
from app.auth import get_current_user

from app.utils.invoke_nn import invoke

router = APIRouter()

@router.post("/predict", response_model=NeuralNetOutput)
async def predict(input_data: NeuralNetInput, user: str = Depends(get_current_user)):
    # Prepare input for the NN
    previous_samples_num = 4  # Number of previous samples to use

    # Predict leaf_wetness_upper
    predictions_upper = invoke("leaf_wetness_upper", previous_samples_num)
    predictions_upper = predictions_upper.flatten().tolist() if predictions_upper is not None else []

    # Predict leaf_wetness_lower
    predictions_lower = invoke("leaf_wetness_lower", previous_samples_num)
    predictions_lower = predictions_lower.flatten().tolist() if predictions_lower is not None else []

    # Predict soil_moisture
    predictions_soil = invoke("soil_moisture", previous_samples_num)
    predictions_soil = predictions_soil.flatten().tolist() if predictions_soil is not None else []

    # Return predictions
    return {
        "leaf_wetness_upper": predictions_upper,
        "leaf_wetness_lower": predictions_lower,
        "soil_moisture": predictions_soil
    }