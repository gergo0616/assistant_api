"""
Configuration settings for the Azure Email Assistant.
"""
from dataclasses import dataclass


@dataclass
class AzureConfig:
    """Azure OpenAI API configuration."""
    endpoint: str = "https://bek-openai-dev.openai.azure.com/"
    api_key: str = "your-api-key-here"
    api_version: str = "2024-08-01-preview"
    deployment: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 4096
    top_p: float = 0.9
    frequency_penalty: float = 0
    presence_penalty: float = 0


@dataclass
class APIConfig:
    """API server configuration."""
    host: str = "0.0.0.0"
    port: int = 5000
    secret_key: str = "your-secret-key-here"


@dataclass
class EmailConfig:
    """Email configuration."""
    smtp_server: str = "smtp.example.com"
    smtp_port: int = 587
    username: str = "your-email@example.com"
    password: str = "your-email-password"


# Create default configuration instances
azure_config = AzureConfig()
api_config = APIConfig()
email_config = EmailConfig()
