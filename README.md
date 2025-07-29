# Stevia FastAPI Project

## Overview
This project provides a FastAPI backend for interacting with a neural network and activating rules.

## Features
- Predict values using a neural network.
- Activate rules based on input data.
- JWT-based authentication.

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd stevia-fastapi-2
```

## Generate a JWT Token
To generate a JWT token for testing or manual use, run the following command:

```bash
python app/utils/generate_token.py
```

## Running with Gunicorn

To run the FastAPI app with Gunicorn (using Uvicorn workers):

```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

You can adjust the number of workers as needed.