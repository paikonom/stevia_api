from fastapi import APIRouter, Depends
from app.models import NeuralNetInput, NeuralNetOutput
from app.auth import get_current_user

from app.utils.invoke_nn import invoke

router = APIRouter()

# @router.post("/predict", response_model=NeuralNetOutput)
# async def predict(input_data: NeuralNetInput, user: str = Depends(get_current_user)):
#     # Prepare input for the NN
#     previous_samples_num = 4  # Number of previous samples to use

#     # Predict leaf_wetness_upper
#     predictions_upper = invoke("leaf_wetness_upper", previous_samples_num)
#     predictions_upper = predictions_upper.flatten().tolist() if predictions_upper is not None else []

#     # Predict leaf_wetness_lower
#     predictions_lower = invoke("leaf_wetness_lower", previous_samples_num)
#     predictions_lower = predictions_lower.flatten().tolist() if predictions_lower is not None else []

#     # Predict soil_moisture
#     predictions_soil = invoke("soil_moisture", previous_samples_num)
#     predictions_soil = predictions_soil.flatten().tolist() if predictions_soil is not None else []

#     # Predict soil_temp
#     predictions_soil_temp = invoke("soil_temp", previous_samples_num)
#     predictions_soil_temp = predictions_soil_temp.flatten().tolist() if predictions_soil_temp is not None else []

#     # Return predictions
#     return {
#         "leaf_wetness_upper": predictions_upper,
#         "leaf_wetness_lower": predictions_lower,
#         "soil_moisture": predictions_soil,
#         "soil_temp": predictions_soil_temp
#     }

@router.post("/predict", response_model=NeuralNetOutput)
async def predict(input_data: NeuralNetInput, user: str = Depends(get_current_user)):
    previous_samples_num = 4
    client_samples = [s.dict() for s in input_data.samples]
    n_client = len(client_samples)

    if n_client >= previous_samples_num:
        # Use only the last 4 client samples
        samples = client_samples[-previous_samples_num:]
        predictions_upper = invoke("leaf_wetness_upper", samples)
        predictions_lower = invoke("leaf_wetness_lower", samples)
        predictions_soil = invoke("soil_moisture", samples)
        predictions_soil_temp = invoke("soil_temp", samples)
    else:
        # Use all client samples, fill the rest from records
        predictions_upper = invoke("leaf_wetness_upper", client_samples)
        predictions_lower = invoke("leaf_wetness_lower", client_samples)
        predictions_soil = invoke("soil_moisture", client_samples)
        predictions_soil_temp = invoke("soil_temp", client_samples)

    return {
        "leaf_wetness_upper": predictions_upper.flatten().tolist() if predictions_upper is not None else [],
        "leaf_wetness_lower": predictions_lower.flatten().tolist() if predictions_lower is not None else [],
        "soil_moisture": predictions_soil.flatten().tolist() if predictions_soil is not None else [],
        "soil_temp": predictions_soil_temp.flatten().tolist() if predictions_soil_temp is not None else [],
    }