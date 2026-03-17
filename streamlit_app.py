import streamlit as st
import pandas as pd
from PIL import Image

from med_db import MedicineDatabase
from symptom import SymptomChecker
from ocr_utils import PrescriptionOCR
from risk_engine import RiskAssessment
from side_effects import SideEffectAnalyzer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MedSafe AI ",
    page_icon="🧠",
    layout="wide"
)


# ---------------- SESSION STATE ----------------
def init_session():
    defaults = {
        "prescription_text": "",
        "interaction_result": None,
        "symptom_result": None,
        "side_effect_log": None,
        "risk_result": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------- INITIALIZE MODULES ----------------
@st.cache_resource
def init_components():
    return (
        MedicineDatabase(),
        SymptomChecker(),
        PrescriptionOCR(),
        RiskAssessment(),
        SideEffectAnalyzer()
    )


# ---------------- MAIN APP ----------------
def main():

    init_session()

    # -------- HEADER --------
    st.title("🧠 MedSafe AI")
    st.markdown("### Your Smart Medical Safety Assistant")
    st.markdown("---")

    med_db, symptom_checker, ocr_processor, risk_assessor, side_effect_engine = init_components()

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2966/2966481.png", width=80)
        st.header("Navigation")

        page = st.radio(
            "Choose Feature",
            [
                "🏠 Home",
                "💊 Medicine Checker",
                "🔍 Symptom Analyzer",
                "📄 Prescription Scanner",
                "⚠️ Side Effects",
                "🚨 Risk Predictor"
            ]
        )

        st.markdown("---")
        st.info("💡 Tip: Always consult a doctor for serious conditions.")

    # ---------------- HOME ----------------
    if page == "🏠 Home":
        st.success("Welcome to MedSafe AI 🚀")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🩺 What You Can Do:
            - Check medicine interactions  
            - Analyze symptoms  
            - Scan prescriptions  
            - Monitor side-effects  
            - Predict health risks  
            """)

        with col2:
            st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png")

    # ---------------- MEDICINE CHECKER ----------------
    elif page == "💊 Medicine Checker":

        st.subheader("💊 Medicine Interaction Checker")

        medicines = st.text_input("Enter medicines (comma separated)")

        if st.button("🔍 Check Interactions"):

            if medicines.strip() == "":
                st.warning("⚠️ Please enter at least one medicine.")
            else:
                med_list = [m.strip() for m in medicines.split(",")]
                result = med_db.check_interactions(med_list)
                st.session_state.interaction_result = result

        if st.session_state.interaction_result:
            st.success("✅ Result")
            st.write(st.session_state.interaction_result)

    # ---------------- SYMPTOM ANALYSIS ----------------
    elif page == "🔍 Symptom Analyzer":

        st.subheader("🔍 Symptom Analysis")

        symptoms = st.text_area("Describe your symptoms")

        if st.button("🧠 Analyze"):

            if symptoms.strip() == "":
                st.warning("⚠️ Please enter symptoms.")
            else:
                analysis = symptom_checker.analyze(symptoms)
                st.session_state.symptom_result = analysis

        if st.session_state.symptom_result:

            result = st.session_state.symptom_result

            col1, col2 = st.columns(2)

            with col1:
                st.info("🧾 Detected Symptoms")
                st.write(result["symptoms_detected"])

                st.warning("⚠️ Possible Conditions")
                st.write(result["possible_conditions"])

            with col2:
                st.success("💡 Recommendations")
                st.write(result["recommendations"])

                if result["seek_immediate_help"]:
                    st.error("🚨 Seek Immediate Medical Attention!")

    # ---------------- OCR ----------------
    elif page == "📄 Prescription Scanner":

        st.subheader("📄 Upload Prescription")

        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            if st.button("📖 Extract Text"):
                text = ocr_processor.extract_text(image)
                st.session_state.prescription_text = text

        if st.session_state.prescription_text:
            st.text_area("Extracted Text", st.session_state.prescription_text, height=200)

    # ---------------- SIDE EFFECT ----------------
    elif page == "⚠️ Side Effects":

        st.subheader("⚠️ Side Effect Monitor")

        age = st.slider("Age", 1, 100, 25)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        medicine = st.text_input("Medicine")
        dosage = st.selectbox("Dosage", ["Low", "Normal", "High"])
        effects = st.text_input("Side effects (comma separated)")

        if st.button("Analyze Effects"):

            if medicine == "" or effects == "":
                st.warning("⚠️ Fill all fields")
            else:
                effects_list = [e.strip() for e in effects.split(",")]
                result = side_effect_engine.analyze(
                    medicine, effects_list, age, gender, dosage
                )
                st.session_state.side_effect_log = result

        if st.session_state.side_effect_log:
            st.write(st.session_state.side_effect_log)

    # ---------------- RISK ----------------
    elif page == "🚨 Risk Predictor":

        st.subheader("🚨 Emergency Risk Predictor")

        age = st.slider("Age", 1, 100, 30)
        conditions = st.multiselect(
            "Existing Conditions",
            ["Diabetes", "Hypertension", "Heart Disease", "Asthma"]
        )
        symptoms = st.text_input("Symptoms (comma separated)")

        if st.button("⚡ Predict Risk"):

            symptom_list = [s.strip() for s in symptoms.split(",") if s]

            score = risk_assessor.calculate_risk(age, conditions, symptom_list)
            assessment = risk_assessor.assess_emergency(score, symptom_list)

            st.session_state.risk_result = {"score": score, "assessment": assessment}

        if st.session_state.risk_result:
            st.metric("Risk Score", f"{st.session_state.risk_result['score']}/100")

            if st.session_state.risk_result["score"] > 70:
                st.error(st.session_state.risk_result["assessment"])
            else:
                st.success(st.session_state.risk_result["assessment"])


if __name__ == "__main__":
    main()