"""
Prescription OCR and Text Extraction Utilities Module
Handles optical character recognition for prescription images
"""

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from typing import Dict, List, Optional
import numpy as np

class PrescriptionOCR:
    """OCR processor for prescription images"""
    
    def __init__(self):
        """Initialize OCR configuration"""
        self.config = '--oem 3 --psm 6'
        self.medicine_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict:
        """Initialize regex patterns for prescription parsing"""
        return {
            'medicine': r'(?i)(?:rx|med[s]?|drug[s]?)[:\s]+([a-zA-Z\s]+)',
            'dosage': r'(\d+\.?\d*)\s*(mg|ml|mcg|g|units?)',
            'frequency': r'(?i)(?:take|use)?\s*(\d+)\s*(?:time[s]?|tablet[s]?|pill[s]?)\s*(?:a|per)?\s*day',
            'duration': r'(?i)for\s+(\d+)\s+(day[s]?|week[s]?|month[s]?)',
            'date': r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'doctor': r'(?i)dr\.?\s+([a-zA-Z\s]+)',
        }
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: PIL Image object
        
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Apply sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        # Resize if too small
        width, height = image.size
        if width < 1000:
            ratio = 1000 / width
            new_size = (int(width * ratio), int(height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def extract_text(self, image: Image.Image) -> str:
        """
        Extract text from prescription image
        
        Args:
            image: PIL Image object
        
        Returns:
            Extracted text
        """
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Perform OCR
        try:
            text = pytesseract.image_to_string(processed_image, config=self.config)
            return text.strip()
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def parse_prescription(self, text: str) -> Dict:
        """
        Parse prescription text to extract structured information
        
        Args:
            text: Extracted prescription text
        
        Returns:
            Structured prescription data
        """
        prescription_data = {
            'raw_text': text,
            'medicines': [],
            'dosages': [],
            'frequencies': [],
            'duration': None,
            'date': None,
            'doctor': None,
            'warnings': []
        }
        
        # Extract medicines
        medicine_matches = re.findall(self.medicine_patterns['medicine'], text)
        prescription_data['medicines'] = [m.strip() for m in medicine_matches]
        
        # Extract dosages
        dosage_matches = re.findall(self.medicine_patterns['dosage'], text)
        prescription_data['dosages'] = [f"{amount} {unit}" for amount, unit in dosage_matches]
        
        # Extract frequency
        frequency_matches = re.findall(self.medicine_patterns['frequency'], text)
        prescription_data['frequencies'] = frequency_matches
        
        # Extract duration
        duration_match = re.search(self.medicine_patterns['duration'], text)
        if duration_match:
            prescription_data['duration'] = f"{duration_match.group(1)} {duration_match.group(2)}"
        
        # Extract date
        date_match = re.search(self.medicine_patterns['date'], text)
        if date_match:
            prescription_data['date'] = date_match.group(0)
        
        # Extract doctor name
        doctor_match = re.search(self.medicine_patterns['doctor'], text)
        if doctor_match:
            prescription_data['doctor'] = doctor_match.group(1).strip()
        
        # Add warnings if critical information is missing
        if not prescription_data['medicines']:
            prescription_data['warnings'].append("No medicines detected")
        if not prescription_data['dosages']:
            prescription_data['warnings'].append("No dosage information found")
        
        return prescription_data
    
    def validate_prescription(self, prescription_data: Dict) -> Dict:
        """
        Validate extracted prescription data
        
        Args:
            prescription_data: Parsed prescription data
        
        Returns:
            Validation results
        """
        validation = {
            'is_valid': True,
            'missing_fields': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['medicines', 'dosages']
        for field in required_fields:
            if not prescription_data.get(field):
                validation['missing_fields'].append(field)
                validation['is_valid'] = False
        
        # Check dosage safety
        for dosage in prescription_data.get('dosages', []):
            # Simple validation - in production, check against medicine database
            if 'mg' in dosage:
                amount = float(re.search(r'(\d+\.?\d*)', dosage).group(1))
                if amount > 1000:
                    validation['warnings'].append(f"High dosage detected: {dosage}")
        
        return validation