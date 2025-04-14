import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
FIREFLY_HOST = os.getenv("FIREFLY_HOST", "localhost")
FIREFLY_PORT = int(os.getenv("FIREFLY_PORT", 6379))
FIREFLY_PASSWORD = os.getenv("FIREFLY_PASSWORD", None)

# Debug configuration
DEBUG = os.getenv("FIREFLY_DEBUG", "false").lower() == "true"