# Multimodal Construction Intelligence Platform

Skill Wallet Capstone Project 1 — AI-assisted construction decision support built with Python and Streamlit.

## Features mapped to the project brief
- **Secure optional Gemini API key** in a password input; demo fallback when absent.
- **Site Safety & PPE Audit:** JPG/PNG upload, multimodal review prompt, structured JSON fields for safety score, status, PPE checklist, hazards/severity/remedies, metrics and JSON download.
- **Crack Diagnostics & Structural Integrity:** surface image upload, defect classification, optional width estimate only when a scale is available, severity/urgency, possible causes and next steps.
- **Planning & Real Estate Valuation:** structure, area, Indian city tier and completion inputs; budget, expenditure proxy, valuation, milestone progress, steel/cement planning allowances and JSON download.
- **Conceptual 3D render integration:** creates an architectural prompt and opens the Pollinations image endpoint. Treat output as concept art, not approved construction documentation.
- **Daily Site Assistant & Weather-Aware Advisory:** high wind, heavy rain, extreme heat and normal-weather checklists plus multi-turn construction assistant.
- **JSON data contracts:** reports can be downloaded for safety, cracks and planning.
- **No external database required.**

## Run locally
Python 3.9+ recommended.
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Optional Gemini setup
Create a Gemini API key in Google AI Studio and paste it into the app sidebar at runtime. The key is not stored in this repository. Without a key, the app provides transparent demo guidance and does not claim to perform AI image inference.

## Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Choose **Create app**.
3. Repository: `rakshitworking-ai/multimodal-construction-intelligence`
4. Branch: `main`
5. Main file path: `app.py`
6. Select **Deploy** and wait for the build to complete.
7. Submit the actual HTTPS app URL in Skill Wallet using **Add Demo Link**. Submit this repository URL using **Add Github Link**.

## Limitations and safety
This educational prototype is not a certified OSHA/IS-code compliance inspection, structural assessment, bill of quantities or professional real-estate appraisal. Vision models can miss or misinterpret details. Steel/cement allowances are rough thumb rules only. Confirm all safety-critical decisions with qualified site professionals.
