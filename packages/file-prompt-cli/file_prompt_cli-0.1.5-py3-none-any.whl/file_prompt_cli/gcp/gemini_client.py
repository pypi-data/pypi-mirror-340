import os
import logging
import base64
from typing import Dict, Any
import google.generativeai as genai
from PIL import Image
import re
import json
from io import BytesIO
from google.cloud import secretmanager

logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Gemini models."""
    
    def __init__(self, project_id: str = None):
        """Initialize the Gemini client."""
        # Configure the API key
        api_key = os.getenv("GOOGLE_API_KEY")
        logger.debug(f"GOOGLE_API_KEY from env: {api_key[:5] if api_key else None}...")  # Log first 5 chars for security
        
        if not api_key:
            # Try to get from Secret Manager if not in env
            try:

                client = secretmanager.SecretManagerServiceClient()
                name = f"projects/{project_id}/secrets/google-api-key/versions/latest"
                response = client.access_secret_version(request={"name": name})
                api_key = response.payload.data.decode("UTF-8")
                logger.debug("Retrieved API key from Secret Manager")
            except Exception as e:
                logger.error(f"Failed to get API key from Secret Manager: {str(e)}")
                raise ValueError("GOOGLE_API_KEY must be set in environment variables or Secret Manager")
        
        try:
            genai.configure(api_key=api_key)
            logger.info("Successfully configured Gemini API")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise
        
        # Initialize model
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite-001')
    
    
    def analyze_content(self, content: str, prompt: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze content using Gemini models.
        
        Args:
            content: The content to analyze (text or base64-encoded image)
            prompt: The prompt to use for analysis
            metadata: Optional metadata about the content (e.g., file type, stats)
            
        Returns:
            Dict containing analysis results
        """
        try:
            logger.info("Starting Gemini analysis")
            logger.debug(f"Content length: {len(content)} characters")
            logger.debug(f"Prompt: {prompt}")
            
            # Handle different content types
            if metadata and metadata.get('file_type') == 'image':
                # For images, create a Part object with the base64 content
                image_part = {
                    "mime_type": f"image/{metadata['image_metadata']['format'].lower()}",
                    "data": content
                }
                # Create a list of parts for the content
                parts = [
                    {"text": f"{prompt}\n\nPlease analyze this image and provide insights:"},
                    image_part
                ]

                response = self.model.generate_content(parts)
            elif metadata and metadata.get('file_type') in ['csv', 'excel']:
                # Enhance prompt for structured data
                enhanced_prompt = f"""Analyze this structured data:

{content}

Consider the following metadata:
- File type: {metadata['file_type']}
- Statistics: {json.dumps(metadata.get('stats', {}), indent=2)}
- Sheets: {metadata.get('sheets', ['N/A'])}

{prompt}"""
                response = self.model.generate_content(enhanced_prompt)
            else:
                # For text content
                enhanced_prompt = f"{prompt}\n\nContent to analyze:\n{content}"
                response = self.model.generate_content(enhanced_prompt)
            
            logger.info("Received response from Gemini")
            
            # Get the response text
            response_text = response.text
            logger.info(f"Response text: {response_text}")
            logger.debug(f"Response text length: {len(response_text)} characters")
            
            # Get prompt feedback
            prompt_feedback = response.prompt_feedback
            logger.debug(f"Prompt feedback: {prompt_feedback}")
            
            # Get safety ratings
            safety_ratings = response.candidates[0].safety_ratings
            logger.debug(f"Safety ratings: {safety_ratings}")
            
            # Get usage metadata
            usage_metadata = response.usage_metadata
            logger.debug(f"Usage metadata: {usage_metadata}")
            
            # Prepare the analysis result
            analysis = {
                "model": self.model._model_name,
                "response": response_text,
                "prompt_feedback": {
                    "block_reason": prompt_feedback.block_reason.name if prompt_feedback.block_reason else None,
                    "safety_ratings": [
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name
                        }
                        for rating in safety_ratings
                    ]
                },
                "usage_metadata": {
                    "prompt_token_count": usage_metadata.prompt_token_count,
                    "candidates_token_count": usage_metadata.candidates_token_count,
                    "total_token_count": usage_metadata.total_token_count
                }
            }
            
            # Add structured data insights if available
            if metadata and metadata.get('file_type') in ['csv', 'excel']:
                analysis['structured_data'] = {
                    "file_type": metadata['file_type'],
                    "stats": metadata.get('stats', {}),
                    "sheets": metadata.get('sheets', [])
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            logger.exception("Full traceback:")
            return {
                "error": str(e),
                "response": "Error analyzing content"
            }
