from fastapi import FastAPI
from app.routes import neural_net, rules
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stevia.codeinu.gr"],  # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(neural_net.router, prefix="/api/v1")
app.include_router(rules.router, prefix="/api/v1")