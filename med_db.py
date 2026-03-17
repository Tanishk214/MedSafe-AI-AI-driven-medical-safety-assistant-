"""
Medicine Database and Interaction Metadata Module
Handles medicine information storage and drug interaction checking
"""

import json
from typing import Dict, List, Optional
from fuzzywuzzy import fuzz, process

class MedicineDatabase:
    """Medicine database manager with interaction checking capabilities"""
    
    def __init__(self):
        """Initialize medicine database with sample data"""
        self.medicines = self._load_medicine_data()
        self.interactions = self._load_interaction_data()
    
    def _load_medicine_data(self) -> Dict:
        """Load medicine information database"""
        # Sample medicine data - in production, load from external database
        return {
            "aspirin": {
                "name": "Aspirin",
                "category": "Pain reliever",
                "common_uses": ["Pain relief", "Fever reduction", "Anti-inflammatory"],
                "side_effects": ["Stomach upset", "Bleeding risk"],
                "dosage": "325-650mg every 4-6 hours"
            },
            "ibuprofen": {
                "name": "Ibuprofen",
                "category": "NSAID",
                "common_uses": ["Pain relief", "Fever reduction", "Anti-inflammatory"],
                "side_effects": ["Stomach upset", "Dizziness"],
                "dosage": "200-400mg every 4-6 hours"
            },
            "paracetamol": {
                "name": "Paracetamol/Acetaminophen",
                "category": "Pain reliever",
                "common_uses": ["Pain relief", "Fever reduction"],
                "side_effects": ["Liver damage (high doses)", "Allergic reaction"],
                "dosage": "500-1000mg every 4-6 hours"
            }
        }
    
    def _load_interaction_data(self) -> Dict:
        """Load drug interaction database"""
        return {
            "aspirin": ["warfarin", "methotrexate", "alcohol"],
            "ibuprofen": ["aspirin", "warfarin", "lithium"],
            "paracetamol": ["warfarin", "alcohol", "isoniazid"]
        }
    
    def search_medicine(self, query: str, threshold: int = 80) -> Optional[Dict]:
        """
        Fuzzy search for medicine in database
        
        Args:
            query: Medicine name to search
            threshold: Minimum matching score (0-100)
        
        Returns:
            Medicine information if found
        """
        if not query:
            return None
            
        # Use fuzzy matching to find best match
        medicine_names = list(self.medicines.keys())
        best_match = process.extractOne(query.lower(), medicine_names, 
                                       scorer=fuzz.ratio)
        
        if best_match and best_match[1] >= threshold:
            return self.medicines[best_match[0]]
        
        return None
    
    def check_interactions(self, medicine: str, 
                         other_medicines: List[str] = None) -> Dict:
        """
        Check for drug interactions
        
        Args:
            medicine: Primary medicine name
            other_medicines: List of other medicines to check against
        
        Returns:
            Dictionary containing interaction warnings and details
        """
        result = {
            "medicine": medicine,
            "found": False,
            "interactions": [],
            "warnings": []
        }
        
        # Search for medicine
        med_info = self.search_medicine(medicine)
        if not med_info:
            result["warnings"].append(f"Medicine '{medicine}' not found in database")
            return result
        
        result["found"] = True
        result["medicine_info"] = med_info
        
        # Check interactions
        medicine_key = medicine.lower()
        if medicine_key in self.interactions:
            known_interactions = self.interactions[medicine_key]
            
            if other_medicines:
                for other_med in other_medicines:
                    if other_med.lower() in known_interactions:
                        result["interactions"].append({
                            "drug": other_med,
                            "severity": "Moderate",
                            "description": f"Potential interaction between {medicine} and {other_med}"
                        })
            
            result["all_known_interactions"] = known_interactions
        
        return result
    
    def get_medicine_info(self, medicine_name: str) -> Optional[Dict]:
        """Get detailed medicine information"""
        return self.search_medicine(medicine_name)