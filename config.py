# server.py
from dotenv import dotenv_values

# Load environment variables from .env file
config = dotenv_values('.env')
print(config)
