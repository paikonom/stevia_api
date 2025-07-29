from fastapi import APIRouter, Depends
from app.models import NeuralNetInput, NeuralNetOutput
from app.auth import get_current_user

from app.utils.invoke_nn import invoke

router = APIRouter()

@router.post("/predict", response_model=NeuralNetOutput)
async def predict(input_data: NeuralNetInput, user: str = Depends(get_current_user)):
    # Prepare input for the Neural Network
    what_to_predict = "leaf_wetness_upper"  # Example: Predicting leaf wetness upper
    previous_samples_num = 4  # Example: Number of previous samples to use

    # Invoke the Neural Network
    predictions_tensor = invoke(what_to_predict, previous_samples_num)

    # Flatten the tensor to a list of floats
    predictions = predictions_tensor.flatten().tolist() if predictions_tensor is not None else []

    # Return predictions
    return {"predictions": predictions}