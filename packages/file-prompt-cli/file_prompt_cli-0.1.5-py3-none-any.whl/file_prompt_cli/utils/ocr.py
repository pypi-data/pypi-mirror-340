import pytesseract
from PIL import Image
import io
from typing import Optional, Tuple
import numpy as np
from pathlib import Path

class OCRUtils:
    """Utility class for OCR operations."""
    
    @staticmethod
    def extract_text_from_image(image_data: bytes, lang: str = 'eng') -> str:
        """Extract text from image bytes."""
        image = Image.open(io.BytesIO(image_data))
        return pytesseract.image_to_string(image, lang=lang)
    
    @staticmethod
    def extract_text_from_image_file(file_path: Path, lang: str = 'eng') -> str:
        """Extract text from image file."""
        return pytesseract.image_to_string(str(file_path), lang=lang)
    
    @staticmethod
    def get_image_confidence(image_data: bytes) -> float:
        """Get OCR confidence score for image."""
        image = Image.open(io.BytesIO(image_data))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence for non-empty text
        confidences = [conf for conf in data['conf'] if conf > 0]
        return sum(confidences) / len(confidences) if confidences else 0.0
    
    @staticmethod
    def preprocess_image(image_data: bytes) -> bytes:
        """Preprocess image for better OCR results."""
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        image = image.point(lambda x: 0 if x < 128 else 255, '1')
        
        # Save processed image to bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        return output.getvalue()
    
    @staticmethod
    def detect_text_regions(image_data: bytes) -> list:
        """Detect regions containing text in image."""
        image = Image.open(io.BytesIO(image_data))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        
        regions = []
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                regions.append({
                    'text': data['text'][i],
                    'confidence': data['conf'][i],
                    'bbox': (
                        data['left'][i],
                        data['top'][i],
                        data['left'][i] + data['width'][i],
                        data['top'][i] + data['height'][i]
                    )
                })
        
        return regions
    
    @staticmethod
    def is_text_dominant(image_data: bytes, threshold: float = 0.3) -> bool:
        """Check if image is likely to contain significant text."""
        regions = OCRUtils.detect_text_regions(image_data)
        if not regions:
            return False
            
        # Calculate total area of text regions
        total_text_area = sum(
            (r['bbox'][2] - r['bbox'][0]) * (r['bbox'][3] - r['bbox'][1])
            for r in regions
        )
        
        # Calculate total image area
        image = Image.open(io.BytesIO(image_data))
        total_image_area = image.width * image.height
        
        # Check if text area exceeds threshold
        return (total_text_area / total_image_area) > threshold
    
    @staticmethod
    def get_supported_languages() -> list:
        """Get list of supported OCR languages."""
        return pytesseract.get_languages() 