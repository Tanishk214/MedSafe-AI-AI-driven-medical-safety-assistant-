🏥 MedSafe AI — AI-Driven Medical Safety Assistant
An AI-powered medical safety assistant that helps users analyze symptoms, check medication safety, and get AI-generated health guidance using Google Gemini.

📋 Project Structure
MedSafe-AI/
├── streamlit_app.py          # Main Streamlit UI application
├── app.py                    # Main Integration Entry for MedSafe AI
├── symptom.py                # Symptom analysis module
├── risk_engine.py            # Risk level assessment engine
├── side_effects.py           # Analyzes user-reported side effects
├── ai_explainer.py           # Provides educational AI explanations
├── med_db.py                 # Medication database & lookup
├── ocr_utils.py              # OCR for prescription image reading
├── utils.py                  # OCR for prescription image reading
├── requirements.txt          # Python dependencies
├── test_setup.py             # Environment setup tests
├── validate_deployment.py    # Activity 4.3: E2E validation script
├── prepare_deployment.py     # Activity 4.3: Deployment prep script
├── .gitignore                # Excludes secrets and cache files
├── .streamlit/
│   ├── config.toml           # Streamlit server configuration
│   └── secrets.toml.template # Template for API key configuration
└── README.md                 # This file
🚀 Local Setup & Running
1. Clone the Repository
git clone https://github.com/RishitaPandey2327/MedSafe-AI.git
cd MedSafe-AI
2. Install Dependencies
pip install -r requirements.txt
3. Configure API Keys
Create .streamlit/secrets.toml (do NOT commit this file):

GEMINI_API_KEY = "your-gemini-api-key-here"
Or use environment variables:

export GEMINI_API_KEY="your-gemini-api-key-here"   # Mac/Linux
set GEMINI_API_KEY=your-gemini-api-key-here        # Windows
4. Run the App
streamlit run streamlit_app.py
App will open at http://localhost:8501

☁️ Streamlit Cloud Deployment
Push your code to GitHub (ensure .streamlit/secrets.toml is in .gitignore)
Go to share.streamlit.io
Connect your GitHub account → Select the MedSafe-AI repo
Set Main file: streamlit_app.py | Branch: main
In Advanced settings → Secrets, add:
GEMINI_API_KEY = "your-key-here"
Click Deploy 🚀
✅ Activity 4.3 Validation
Run the deployment preparation and validation scripts:

# Step 1: Check environment and file structure
python prepare_deployment.py

# Step 2: Run full end-to-end validation
python validate_deployment.py
🔄 Core Workflow
User Input (symptoms / prescription image)
       ↓
symptom.py → Symptom Analysis
       ↓
risk_engine.py → Risk Level Assessment (Low / Medium / High)
       ↓
med_db.py → Medication Safety Check
       ↓
Google Gemini AI → Natural Language Explanation
       ↓
streamlit_app.py → UI Output (risk badge, recommendations, warnings)
⚠️ Disclaimer
MedSafe AI is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

👥 Contributors
Tanishk Sahu
Tanu Mourya
Team Members
Milestone 4 — Activity 4.3: Deployment Preparation and Final Validation
