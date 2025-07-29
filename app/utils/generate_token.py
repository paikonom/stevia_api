import os
import sys
from datetime import timedelta
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.auth import create_access_token

load_dotenv()

# Load secret key and token expiration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 43800))  # Default: 1 month

def main():
    # Replace with the user data you want to encode in the token
    user_data = {"sub": "test_user"}

    # Set token expiration
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Generate the token
    token = create_access_token(user_data, expires_delta)

    print(f"Generated Token: {token}")

if __name__ == "__main__":
    main()