"""
Emergency Risk Scoring and Safety Rules Module
Calculates health risk scores and provides safety recommendations
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import numpy as np

class RiskAssessment:
    """Health risk assessment and emergency detection engine"""
    
    def __init__(self):
        """Initialize risk scoring parameters and thresholds"""
        self.risk_factors = self._initialize_risk_factors()
        self.emergency_thresholds = self._initialize_emergency_thresholds()
        self.safety_rules = self._initialize_safety_rules()
    
    def _initialize_risk_factors(self) -> Dict:
        """Define risk factors and their weights"""
        return {
            'age': {
                'ranges': [(0, 18, 'low'), (18, 40, 'low'), 
                          (40, 60, 'moderate'), (60, 80, 'high'), 
                          (80, 120, 'very_high')],
                'weights': {'low': 1, 'moderate': 2, 'high': 3, 'very_high': 4}
            },
            'conditions': {
                'diabetes': 3,
                'hypertension': 3,
                'heart_disease': 4,
                'asthma': 2,
                'kidney_disease': 4,
                'cancer': 5,
                'copd': 3,
                'stroke_history': 4
            },
            'symptoms': {
                'chest_pain': 5,
                'difficulty_breathing': 5,
                'severe_headache': 3,
                'confusion': 4,
                'persistent_fever': 2,
                'severe_pain': 3
            },
            'medications': {
                'anticoagulants': 2,
                'immunosuppressants': 3,
                'chemotherapy': 4,
                'insulin': 2,
                'multiple_medications': 2
            }
        }
    
    def _initialize_emergency_thresholds(self) -> Dict:
        """Define emergency condition thresholds"""
        return {
            'vital_signs': {
                'heart_rate': {'low': 40, 'high': 120},
                'blood_pressure_systolic': {'low': 90, 'high': 180},
                'blood_pressure_diastolic': {'low': 60, 'high': 120},
                'oxygen_saturation': {'low': 92, 'normal': 100},
                'temperature': {'low': 95, 'high': 103}
            },
            'risk_score_threshold': 70  # Above this requires immediate attention
        }
    
    def _initialize_safety_rules(self) -> List[Dict]:
        """Define safety rules and recommendations"""
        return [
            {
                'condition': 'chest_pain',
                'rule': 'Seek immediate medical attention',
                'priority': 'critical'
            },
            {
                'condition': 'difficulty_breathing',
                'rule': 'Call emergency services',
                'priority': 'critical'
            },
            {
                'condition': 'high_fever_persistent',
                'rule': 'Consult healthcare provider within 24 hours',
                'priority': 'high'
            },
            {
                'condition': 'medication_interaction',
                'rule': 'Consult pharmacist before taking',
                'priority': 'moderate'
            }
        ]
    
    def calculate_risk(self, age: int, 
                      conditions: List[str] = None,
                      symptoms: List[str] = None,
                      medications: List[str] = None,
                      vital_signs: Dict = None) -> int:
        """
        Calculate overall health risk score
        
        Args:
            age: Patient age
            conditions: List of existing health conditions
            symptoms: Current symptoms
            medications: Current medications
            vital_signs: Dictionary of vital signs
        
        Returns:
            Risk score (0-100)
        """
        risk_score = 0
        max_possible_score = 100
        
        # Age-based risk
        age_risk = self._calculate_age_risk(age)
        risk_score += age_risk * 10
        
        # Condition-based risk
        if conditions:
            condition_score = sum(self.risk_factors['conditions'].get(
                condition.lower(), 0) for condition in conditions)
            risk_score += min(condition_score * 5, 30)
        
        # Symptom-based risk
        if symptoms:
            symptom_score = sum(self.risk_factors['symptoms'].get(
                symptom.lower(), 0) for symptom in symptoms)
            risk_score += min(symptom_score * 5, 30)
        
        # Medication-based risk
        if medications:
            med_score = len(medications) * 2
            risk_score += min(med_score, 15)
        
        # Vital signs risk
        if vital_signs:
            vital_risk = self._calculate_vital_signs_risk(vital_signs)
            risk_score += vital_risk
        
        # Normalize to 0-100 scale
        return min(int(risk_score), 100)
    
    def _calculate_age_risk(self, age: int) -> int:
        """Calculate age-based risk factor"""
        for age_range in self.risk_factors['age']['ranges']:
            if age_range[0] <= age <= age_range[1]:
                return self.risk_factors['age']['weights'][age_range[2]]
        return 1
    
    def _calculate_vital_signs_risk(self, vital_signs: Dict) -> int:
        """Calculate risk based on vital signs"""
        risk = 0
        thresholds = self.emergency_thresholds['vital_signs']
        
        for sign, value in vital_signs.items():
            if sign in thresholds:
                limits = thresholds[sign]
                if 'low' in limits and value < limits['low']:
                    risk += 10
                if 'high' in limits and value > limits['high']:
                    risk += 10
        
        return risk
    
    def assess_emergency(self, risk_score: int, 
                        symptoms: List[str] = None) -> Dict:
        """
        Assess if emergency intervention is needed
        
        Args:
            risk_score: Calculated risk score
            symptoms: List of current symptoms
        
        Returns:
            Emergency assessment results
        """
        assessment = {
            'is_emergency': False,
            'urgency_level': 'low',
            'recommendations': [],
            'action_required': None
        }
        
        # Check risk score threshold
        if risk_score >= self.emergency_thresholds['risk_score_threshold']:
            assessment['is_emergency'] = True
            assessment['urgency_level'] = 'critical'
            assessment['action_required'] = 'Seek immediate medical attention'
        elif risk_score >= 50:
            assessment['urgency_level'] = 'high'
            assessment['action_required'] = 'Schedule medical consultation soon'
        elif risk_score >= 30:
            assessment['urgency_level'] = 'moderate'
            assessment['action_required'] = 'Monitor symptoms closely'
        
        # Check for emergency symptoms
        if symptoms:
            emergency_symptoms = ['chest_pain', 'difficulty_breathing', 
                                 'unconscious', 'severe_bleeding']
            for symptom in symptoms:
                if any(emerg in symptom.lower() for emerg in emergency_symptoms):
                    assessment['is_emergency'] = True
                    assessment['urgency_level'] = 'critical'
                    assessment['recommendations'].append('Call 911 immediately')
                    break
        
        # Add general recommendations based on urgency
        if assessment['urgency_level'] == 'critical':
            assessment['recommendations'].extend([
                'Do not drive yourself to the hospital',
                'Have someone stay with you',
                'Bring all current medications'
            ])
        elif assessment['urgency_level'] == 'high':
            assessment['recommendations'].extend([
                'Contact your healthcare provider',
                'Keep emergency contacts ready',
                'Document your symptoms'
            ])
        
        return assessment
    
    def generate_safety_report(self, risk_score: int, 
                              assessment: Dict) -> Dict:
        """
        Generate comprehensive safety report
        
        Args:
            risk_score: Calculated risk score
            assessment: Emergency assessment results
        
        Returns:
            Safety report with recommendations
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'risk_score': risk_score,
            'risk_level': self._get_risk_level(risk_score),
            'emergency_status': assessment['is_emergency'],
            'urgency': assessment['urgency_level'],
            'immediate_actions': assessment.get('recommendations', []),
            'follow_up': [],
            'preventive_measures': []
        }
        
        # Add follow-up recommendations
        if risk_score < 30:
            report['follow_up'] = ['Regular check-ups', 'Maintain healthy lifestyle']
        elif risk_score < 70:
            report['follow_up'] = ['Schedule doctor appointment', 
                                   'Monitor symptoms daily']
        else:
            report['follow_up'] = ['Immediate medical consultation required']
        
        # Add preventive measures
        report['preventive_measures'] = [
            'Maintain medication compliance',
            'Regular vital sign monitoring',
            'Keep emergency contacts updated',
            'Document symptoms and changes'
        ]
        
        return report
    
    def _get_risk_level(self, score: int) -> str:
        """Convert risk score to risk level category"""
        if score < 20:
            return 'Low'
        elif score < 40:
            return 'Moderate'
        elif score < 70:
            return 'High'
        else:
            return 'Critical'