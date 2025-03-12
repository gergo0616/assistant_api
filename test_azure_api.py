"""
Test script to verify the Azure OpenAI API key is working correctly.
"""
import logging
import sys
from azure_email_assistant.core.assistant import AzureAssistant, EmailContent
from azure_email_assistant.core.config import azure_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_azure_api():
    """Test the Azure OpenAI API with a specific use case."""
    # Display current configuration
    logger.info("Current Azure OpenAI Configuration:")
    logger.info(f"Endpoint: {azure_config.endpoint}")
    logger.info(f"API Key: {'*' * 5 + azure_config.api_key[-4:] if len(azure_config.api_key) > 9 else 'Not set properly'}")
    logger.info(f"API Version: {azure_config.api_version}")
    logger.info(f"Deployment: {azure_config.deployment}")
    
    # Check if API key is set to a non-default value
    if azure_config.api_key == "your-api-key-here" or azure_config.api_key == "your-actual-api-key-here":
        logger.error("API key is set to a placeholder value. Please update with a real API key.")
        return False
    
    # Create an instance of the Azure Assistant
    logger.info("Creating Azure Assistant instance...")
    assistant = AzureAssistant()
    
    # Create a test email
    test_email = EmailContent(
        from_email="test@example.com",
        subject="API Key Test",
        body="This is a test to verify if the Azure OpenAI API key is working correctly. Please respond with a confirmation."
    )
    
    # Process the email
    try:
        logger.info("Sending test request to Azure OpenAI API...")
        response = assistant.process_email(test_email)
        
        # Check if response was successful
        if response.status == "success" and response.response:
            logger.info("API key is working correctly!")
            logger.info(f"Response: {response.response}")
            return True
        else:
            logger.error(f"API request failed: {response.error}")
            return False
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_azure_api()
    sys.exit(0 if success else 1)
