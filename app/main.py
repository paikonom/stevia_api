"""
TODO: 
    2. RULES RETURN STATUS, NO TIMESTAMP, 
        ALERTS MIA LISTA APO TEXTS (REMOVE TIMESTAMPS)
        MESO ORO APO TA POST REQUESTS KAI META KANONES
    3. printscrenns apo docs gia to paradoteo 10
"""

from fastapi import FastAPI
from app.routes import neural_net, rules

app = FastAPI()

# Include routes
app.include_router(neural_net.router, prefix="/api/v1")
app.include_router(rules.router, prefix="/api/v1")