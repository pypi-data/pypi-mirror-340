"""Configuration module for file-prompt-cli."""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the application."""
    
    # GCP Configuration
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "")
    
    # Pub/Sub Configuration
    PUBSUB_TOPIC: str = os.getenv("PUBSUB_TOPIC", "")
    PUBSUB_SUBSCRIPTION: str = os.getenv("PUBSUB_SUBSCRIPTION", "")
    PUBSUB_RESULTS_TOPIC: str = os.getenv("PUBSUB_RESULTS_TOPIC", "")
    PUBSUB_RESULTS_SUBSCRIPTION: str = os.getenv("PUBSUB_RESULTS_SUBSCRIPTION", "")
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate that all required environment variables are set."""
        required_vars = [
            "GCP_PROJECT_ID",
            "GCS_BUCKET_NAME",
            "PUBSUB_TOPIC",
            "PUBSUB_SUBSCRIPTION",
            "PUBSUB_RESULTS_TOPIC",
            "PUBSUB_RESULTS_SUBSCRIPTION",
            "GOOGLE_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Please set them in your .env file or environment."
            )
    
    @classmethod
    def get_pubsub_topic_path(cls) -> str:
        """Get the full Pub/Sub topic path."""
        if not cls.GCP_PROJECT_ID or not cls.PUBSUB_TOPIC:
            raise ValueError("GCP_PROJECT_ID and PUBSUB_TOPIC must be set")
        return f"projects/{cls.GCP_PROJECT_ID}/topics/{cls.PUBSUB_TOPIC}"
    
    @classmethod
    def get_results_topic_path(cls) -> str:
        """Get the full Pub/Sub results topic path."""
        if not cls.GCP_PROJECT_ID or not cls.PUBSUB_RESULTS_TOPIC:
            raise ValueError("GCP_PROJECT_ID and PUBSUB_RESULTS_TOPIC must be set")
        return f"projects/{cls.GCP_PROJECT_ID}/topics/{cls.PUBSUB_RESULTS_TOPIC}"
    
    @classmethod
    def get_gcs_bucket_path(cls) -> str:
        """Get the full GCS bucket path."""
        if not cls.GCS_BUCKET_NAME:
            raise ValueError("GCS_BUCKET_NAME must be set")
        return f"gs://{cls.GCS_BUCKET_NAME}" 