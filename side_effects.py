"""
Side Effect Monitoring Module
Analyzes user reported side effects with medicine usage
"""

from typing import Dict, List


class SideEffectAnalyzer:

    def __init__(self):
        self.side_effect_db = self._initialize_db()

    def _initialize_db(self):
        return {
            "paracetamol": {
                "common": ["nausea", "rash"],
                "serious": ["liver damage"]
            },
            "ibuprofen": {
                "common": ["stomach pain", "heartburn"],
                "serious": ["bleeding", "kidney damage"]
            },
            "amoxicillin": {
                "common": ["diarrhea", "nausea"],
                "serious": ["allergic reaction"]
            }
        }

    def analyze(
        self,
        medicine: str,
        side_effects: List[str],
        age: int,
        gender: str,
        dosage: str
    ) -> Dict:

        result = {
            "medicine": medicine,
            "reported_effects": side_effects,
            "severity": "low",
            "warnings": []
        }

        med = medicine.lower()

        if med in self.side_effect_db:

            serious = self.side_effect_db[med]["serious"]

            for effect in side_effects:
                if effect.lower() in serious:
                    result["severity"] = "high"
                    result["warnings"].append(
                        f"Serious side effect detected: {effect}"
                    )

        if age > 65:
            result["warnings"].append("Higher sensitivity due to age")

        if dosage.lower() == "high":
            result["warnings"].append("High dosage may increase risk")

        return result