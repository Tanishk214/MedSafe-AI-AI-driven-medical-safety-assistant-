"""
AI Explanation Generator
Creates educational explanations for symptoms
"""

from typing import Dict


class AIExplainer:

    def generate_explanation(self, symptom_result: Dict) -> Dict:

        explanation = {
            "education": [],
            "home_remedies": [],
            "lifestyle": [],
            "warning_signs": []
        }

        detected = symptom_result.get("symptoms_detected", [])

        if "headache" in detected:

            explanation["education"].append(
                "Headaches are often caused by dehydration, stress or fatigue."
            )

            explanation["home_remedies"].extend([
                "Drink water",
                "Rest in a quiet dark room",
                "Apply cold compress"
            ])

            explanation["lifestyle"].extend([
                "Reduce screen time",
                "Improve sleep schedule"
            ])

        if "fever" in detected:

            explanation["education"].append(
                "Fever is usually the body's response to infection."
            )

            explanation["home_remedies"].extend([
                "Stay hydrated",
                "Take adequate rest"
            ])

            explanation["warning_signs"].extend([
                "Temperature above 103°F",
                "Persistent fever > 3 days"
            ])

        return explanation