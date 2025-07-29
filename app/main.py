from fastapi import FastAPI
from app.routes import neural_net, rules

app = FastAPI()

# Include routes
app.include_router(neural_net.router, prefix="/api/v1")
app.include_router(rules.router, prefix="/api/v1")