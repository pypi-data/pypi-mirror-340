from google.cloud import secretmanager
from typing import Optional
import os
import json

class SecretsManager:
    """Utility class for managing GCP secrets."""
    
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv('GCP_PROJECT_ID')
        if not self.project_id:
            raise ValueError("GCP project ID must be provided or set in environment variables")
        self.client = secretmanager.SecretManagerServiceClient()
    
    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        """Get a secret value from Secret Manager."""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    
    def get_secret_json(self, secret_id: str, version_id: str = "latest") -> dict:
        """Get a secret value as JSON from Secret Manager."""
        secret_value = self.get_secret(secret_id, version_id)
        return json.loads(secret_value)
    
    def create_secret(self, secret_id: str, secret_value: str) -> None:
        """Create a new secret in Secret Manager."""
        parent = f"projects/{self.project_id}"
        
        # Create the secret
        secret = self.client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )
        
        # Add the secret version
        self.client.add_secret_version(
            request={
                "parent": secret.name,
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )
    
    def update_secret(self, secret_id: str, secret_value: str) -> None:
        """Update an existing secret in Secret Manager."""
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": secret_value.encode("UTF-8")},
            }
        )
    
    def delete_secret(self, secret_id: str) -> None:
        """Delete a secret from Secret Manager."""
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        self.client.delete_secret(request={"name": name})
    
    @staticmethod
    def get_secret_env(secret_id: str) -> str:
        """Get a secret value from environment variables or Secret Manager."""
        # First try environment variable
        env_value = os.getenv(secret_id)
        if env_value:
            return env_value
            
        # If not in env, try Secret Manager
        try:
            secrets_manager = SecretsManager()
            return secrets_manager.get_secret(secret_id)
        except Exception as e:
            raise ValueError(f"Secret {secret_id} not found in environment or Secret Manager: {str(e)}") 