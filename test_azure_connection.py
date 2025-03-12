"""
Simple script to test Azure OpenAI API connection.
"""
import requests
import json
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Azure OpenAI configuration
AZURE_ENDPOINT = "https://andras018923456332.services.ai.azure.com/"  # Make sure there's no "models" at the end
AZURE_API_KEY = "FCU89qWazU9ZkYGmtC3g41e1EKNFsbtkiOULeWahSW4lQ84xsbP1JQQJ99BBACYeBjFXJ3w3AAAAACOGlZgA"
AZURE_API_VERSION = "2024-08-01-preview"
AZURE_DEPLOYMENT = "DeepSeek-R1"

def test_azure_connection():
    """Test the Azure OpenAI API connection."""
    logger.info("Testing Azure OpenAI API connection...")
    logger.info(f"Endpoint: {AZURE_ENDPOINT}")
    logger.info(f"API Key: {'*' * 5 + AZURE_API_KEY[-4:] if len(AZURE_API_KEY) > 9 else 'Not set properly'}")
    logger.info(f"API Version: {AZURE_API_VERSION}")
    logger.info(f"Deployment: {AZURE_DEPLOYMENT}")
    
    # Construct the API URL
    api_url = f"{AZURE_ENDPOINT}openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version={AZURE_API_VERSION}"
    logger.info(f"API URL: {api_url}")
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY
    }
    
    # Prepare request body
    body = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, this is a test message. Please respond with a simple confirmation."}
        ],
        "temperature": 0.1,
        "max_tokens": 100,
        "model": "DeepSeek-R1"  # Added model name parameter
    }
    
    try:
        # Send the request
        logger.info("Sending request to Azure OpenAI API...")
        response = requests.post(api_url, headers=headers, json=body)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "No content")
            logger.info("API connection successful!")
            logger.info(f"Response: {message}")
            return True
        else:
            logger.error(f"API request failed: {response.status_code} {response.reason}")
            logger.error(f"Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error connecting to Azure OpenAI API: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_azure_connection()
    sys.exit(0 if success else 1)
