"""
Rule-based Symptom Advice Logic Module
Provides symptom analysis and health recommendations
"""

from typing import List, Dict, Tuple
import re
from fuzzywuzzy import fuzz

class SymptomChecker:
    """Rule-based symptom analysis engine"""
    
    def __init__(self):
        """Initialize symptom database and rules"""
        self.symptom_database = self._initialize_symptoms()
        self.emergency_keywords = self._initialize_emergency_keywords()
        
    def _initialize_symptoms(self) -> Dict:
        """Initialize common symptoms and related conditions"""
        return {
            "headache": {
                "possible_causes": ["Tension", "Migraine", "Dehydration", "Stress"],
                "recommendations": ["Rest", "Hydration", "Pain reliever"],
                "when_to_seek_help": ["Severe sudden onset", "With fever", "After head injury"]
            },
            "fever": {
                "possible_causes": ["Infection", "Inflammation", "Heat exhaustion"],
                "recommendations": ["Rest", "Fluids", "Antipyretics"],
                "when_to_seek_help": ["Above 103°F", "Lasting >3 days", "With confusion"]
            },
            "cough": {
                "possible_causes": ["Cold", "Flu", "Allergies", "Bronchitis"],
                "recommendations": ["Rest", "Warm fluids", "Humidifier"],
                "when_to_seek_help": ["Blood in sputum", "Difficulty breathing", "Lasting >2 weeks"]
            },
            "nausea": {
                "possible_causes": ["Food poisoning", "Motion sickness", "Medication side effect"],
                "recommendations": ["Small sips of water", "BRAT diet", "Rest"],
                "when_to_seek_help": ["Severe dehydration", "Blood in vomit", "High fever"]
            }
        }
    
    def _initialize_emergency_keywords(self) -> List[str]:
        """Initialize emergency symptom keywords"""
        return [
            "chest pain", "difficulty breathing", "unconscious", "severe bleeding",
            "stroke", "heart attack", "seizure", "severe allergic reaction",
            "suicidal thoughts", "severe trauma"
        ]
    
    def analyze(self, symptom_description: str) -> Dict:
        """
        Analyze symptoms and provide recommendations
        
        Args:
            symptom_description: User's description of symptoms
        
        Returns:
            Analysis results with recommendations
        """
        result = {
            "emergency": False,
            "symptoms_detected": [],
            "possible_conditions": [],
            "recommendations": [],
            "seek_immediate_help": False
        }
        
        # Check for emergency symptoms
        description_lower = symptom_description.lower()
        for emergency in self.emergency_keywords:
            if emergency in description_lower:
                result["emergency"] = True
                result["seek_immediate_help"] = True
                result["recommendations"].append("⚠️ SEEK IMMEDIATE MEDICAL ATTENTION")
                break
        
        # Detect mentioned symptoms
        for symptom, info in self.symptom_database.items():
            if symptom in description_lower or fuzz.partial_ratio(symptom, description_lower) > 80:
                result["symptoms_detected"].append(symptom)
                result["possible_conditions"].extend(info["possible_causes"])
                result["recommendations"].extend(info["recommendations"])
        
        # Remove duplicates
        result["possible_conditions"] = list(set(result["possible_conditions"]))
        result["recommendations"] = list(set(result["recommendations"]))
        
        # Add general advice if no specific symptoms detected
        if not result["symptoms_detected"] and not result["emergency"]:
            result["recommendations"] = [
                "Monitor your symptoms",
                "Rest and stay hydrated",
                "Consult a healthcare provider if symptoms persist"
            ]
        
        return result
    
    def get_symptom_info(self, symptom: str) -> Dict:
        """Get detailed information about a specific symptom"""
        symptom_lower = symptom.lower()
        
        # Direct lookup
        if symptom_lower in self.symptom_database:
            return self.symptom_database[symptom_lower]
        
        # Fuzzy matching
        for key, value in self.symptom_database.items():
            if fuzz.ratio(symptom_lower, key) > 80:
                return value
        
        return {
            "message": "Symptom not found in database",
            "recommendation": "Please consult a healthcare provider"
        }