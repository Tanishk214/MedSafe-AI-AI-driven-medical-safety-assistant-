"""
Main Integration Entry for MedSafe AI
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from symptom import SymptomChecker
from risk_engine import RiskAssessment
from side_effects import SideEffectAnalyzer
from ai_explainer import AIExplainer
from utils import setup_logger, log_event


def main():

    # ---------------- Setup ----------------
    setup_logger()

    st.set_page_config(
        page_title="MedSafe AI",
        page_icon="💊",
        layout="wide"
    )

    st.title("💊 MedSafe AI Health Assistant")

    # ---------------- Initialize Engines ----------------
    try:
        symptom_checker = SymptomChecker()
        risk_engine = RiskAssessment()
        side_effect_engine = SideEffectAnalyzer()
        ai_explainer = AIExplainer()
    except Exception as e:
        st.error(f"System initialization error: {e}")
        return

    # ---------------- Session State ----------------
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False

    # ---------------- User Information ----------------
    st.header("User Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    with col2:
        medicine = st.text_input("Medicine Name")
        dosage = st.selectbox("Dosage Level", ["low", "normal", "high"])

    # ---------------- Symptoms ----------------
    st.header("Symptoms")

    symptoms = st.text_area(
        "Describe your symptoms",
        placeholder="Example: headache, fever, nausea"
    )

    # ---------------- Side Effects ----------------
    st.header("Side Effects")

    side_effects = st.text_input(
        "Side effects experienced (comma separated)",
        placeholder="Example: dizziness, rash"
    )

    # ---------------- Analyze Button ----------------
    if st.button("Analyze Health"):

        log_event("Analysis started")

        try:

            # ---------- Symptom Analysis ----------
            symptom_result = symptom_checker.analyze(symptoms)

            # ---------- Side Effect Parsing ----------
            side_effect_list = [
                s.strip()
                for s in side_effects.split(",")
                if s.strip()
            ]

            # ---------- Side Effect Analysis ----------
            side_effect_result = side_effect_engine.analyze(
                medicine,
                side_effect_list,
                age,
                gender,
                dosage
            )

            # ---------- Risk Calculation ----------
            risk_score = risk_engine.calculate_risk(
                age,
                symptoms=symptom_result["symptoms_detected"],
                medications=[medicine]
            )

            risk_assessment = risk_engine.assess_emergency(
                risk_score,
                symptom_result["symptoms_detected"]
            )

            # ---------- AI Explanation ----------
            ai_help = ai_explainer.generate_explanation(symptom_result)

            st.session_state.analysis_complete = True

        except Exception as e:
            st.error(f"Analysis failed: {e}")
            return

        # ---------------- Results ----------------
        st.divider()
        st.header("Analysis Results")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Symptom Analysis")
            st.json(symptom_result)

        with col2:
            st.subheader("Side Effect Analysis")
            st.json(side_effect_result)

        # ---------- Risk Score ----------
        st.subheader("Risk Score")

        st.metric(
            label="Risk Score",
            value=risk_score
        )

        # ---------- Emergency Assessment ----------
        st.subheader("Emergency Assessment")
        st.write(risk_assessment)

        # ---------- AI Explanation ----------
        st.subheader("Educational Explanation")
        st.write(ai_help)

        # =================================================
        # MEDICINE SAFETY DATA + VISUALIZATION (MERGED PART)
        # =================================================

        st.divider()
        st.header("Medicine Safety Analysis")

        data = {
            "Medicine": ["Paracetamol", "Ibuprofen", "Aspirin"],
            "Safety Score": [85, 70, 60]
        }

        df = pd.DataFrame(data)

        st.subheader("Safety Data")
        st.write(df)

        st.subheader("Safety Score Visualization")

        fig, ax = plt.subplots()

        ax.bar(df["Medicine"], df["Safety Score"])

        ax.set_xlabel("Medicine")
        ax.set_ylabel("Safety Score")
        ax.set_title("Medicine Safety Analysis")

        st.pyplot(fig)

        log_event("Analysis completed successfully")


if __name__ == "__main__":
    main()