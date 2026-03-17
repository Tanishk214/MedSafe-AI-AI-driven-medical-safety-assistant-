"""
Activity 4.3 - MedSafe AI: Deployment Preparation Script
==========================================================
Run this script to verify your environment is ready for deployment.
Supports: Local Server | Streamlit Cloud
"""

import subprocess
import sys
import os
import shutil

REQUIRED_PACKAGES = [
    "streamlit",
    "google-generativeai",
    "Pillow",
    "pytesseract",
    "opencv-python-headless",
    "numpy",
]

REQUIRED_FILES = [
    "streamlit_app.py",
    "symptom.py",
    "risk_engine.py",
    "med_db.py",
    "ocr_utils.py",
    "requirements.txt",
    ".gitignore",
    "README.md",
]


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def check_python_version():
    print_header("1. Python Version Check")
    v = sys.version_info
    print(f"  Python {v.major}.{v.minor}.{v.micro}")
    if v.major == 3 and v.minor >= 9:
        print("  ✅ Python version OK (3.9+)")
    else:
        print("  ⚠️  Recommend Python 3.9 or higher for Streamlit Cloud compatibility")


def check_packages():
    print_header("2. Package Installation Check")
    missing = []
    for pkg in REQUIRED_PACKAGES:
        import_name = pkg.split("-")[0].replace("-", "_")
        # Handle special cases
        if pkg == "Pillow":
            import_name = "PIL"
        elif pkg == "opencv-python-headless":
            import_name = "cv2"
        elif pkg == "google-generativeai":
            import_name = "google.generativeai"
        try:
            __import__(import_name)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} — NOT INSTALLED")
            missing.append(pkg)
    if missing:
        print(f"\n  ⚠️  Install missing packages:")
        print(f"     pip install {' '.join(missing)}")
    return missing


def check_files():
    print_header("3. Required File Check")
    all_ok = True
    for f in REQUIRED_FILES:
        if os.path.exists(f):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} — MISSING")
            all_ok = False
    return all_ok


def check_streamlit_config():
    print_header("4. Streamlit Configuration")
    config_path = os.path.join(".streamlit", "config.toml")
    secrets_template = os.path.join(".streamlit", "secrets.toml.template")
    secrets_actual = os.path.join(".streamlit", "secrets.toml")

    if os.path.exists(config_path):
        print(f"  ✅ .streamlit/config.toml found")
    else:
        print(f"  ❌ .streamlit/config.toml missing — creating it...")
        os.makedirs(".streamlit", exist_ok=True)
        with open(config_path, "w") as f:
            f.write('[server]\nheadless = true\nport = 8501\nenableCORS = false\n')
        print(f"  ✅ Created .streamlit/config.toml")

    if os.path.exists(secrets_actual):
        print(f"  ✅ .streamlit/secrets.toml found (local dev)")
    elif os.path.exists(secrets_template):
        print(f"  ⚠️  secrets.toml.template found — copy and fill in your API keys:")
        print(f"     cp .streamlit/secrets.toml.template .streamlit/secrets.toml")
    else:
        print(f"  ⚠️  No secrets.toml found. For Streamlit Cloud: add secrets via the dashboard.")


def check_gitignore():
    print_header("5. .gitignore Security Check")
    if not os.path.exists(".gitignore"):
        print("  ❌ .gitignore missing! Creating one...")
        create_gitignore()
    else:
        with open(".gitignore") as f:
            content = f.read()
        if "secrets.toml" not in content:
            print("  ⚠️  secrets.toml not in .gitignore — adding it to protect your API keys...")
            with open(".gitignore", "a") as f:
                f.write("\n# Streamlit secrets\n.streamlit/secrets.toml\n")
            print("  ✅ Added .streamlit/secrets.toml to .gitignore")
        else:
            print("  ✅ .gitignore properly excludes secrets.toml")


def create_gitignore():
    content = """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
.env
*.egg-info/
dist/
build/

# Streamlit secrets
.streamlit/secrets.toml

# Logs
*.log
validation_report_*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
"""
    with open(".gitignore", "w") as f:
        f.write(content)
    print("  ✅ Created .gitignore")


def print_deployment_instructions():
    print_header("6. Deployment Instructions")

    print("""
  ── LOCAL DEPLOYMENT ──────────────────────────────────────
  1. Make sure all packages are installed:
       pip install -r requirements.txt

  2. Set up your API key (choose one method):
     a) Environment variable:
          export GEMINI_API_KEY="your-key-here"       (Mac/Linux)
          set GEMINI_API_KEY=your-key-here            (Windows)
     b) .streamlit/secrets.toml:
          GEMINI_API_KEY = "your-key-here"

  3. Run the app:
       streamlit run streamlit_app.py

  ── STREAMLIT CLOUD DEPLOYMENT ────────────────────────────
  1. Push your code to GitHub (ensure secrets.toml is in .gitignore)

  2. Go to https://share.streamlit.io and sign in with GitHub

  3. Click "New app" → select your repo → set:
       Main file path: streamlit_app.py
       Branch: main

  4. In "Advanced settings" → "Secrets", add:
       GEMINI_API_KEY = "your-key-here"
       (or GOOGLE_CLOUD_PROJECT = "your-project-id")

  5. Click "Deploy!" — your app will be live in ~2 minutes

  ── GITHUB COMMIT CHECKLIST ───────────────────────────────
  Before pushing, verify:
  ✅ secrets.toml is NOT committed (check .gitignore)
  ✅ requirements.txt is up to date
  ✅ README.md has usage instructions
  ✅ All .py files are working (run validate_deployment.py)
""")


def main():
    print("\n🏥 MedSafe AI — Activity 4.3 Deployment Preparation")
    print("=" * 60)

    check_python_version()
    missing_pkgs = check_packages()
    files_ok = check_files()
    check_streamlit_config()
    check_gitignore()
    print_deployment_instructions()

    print_header("SUMMARY")
    if not missing_pkgs and files_ok:
        print("  🎉 All checks passed! Run validate_deployment.py for full E2E validation.")
        print("  📦 Ready to deploy!")
    else:
        if missing_pkgs:
            print(f"  ❌ {len(missing_pkgs)} package(s) missing — install before deploying")
        if not files_ok:
            print("  ❌ Some required files are missing")
        print("\n  Fix the issues above, then re-run this script.")


if __name__ == "__main__":
    main()