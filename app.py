import json
from datetime import datetime
import streamlit as st
from PIL import Image

st.set_page_config(page_title="BuildSight AI", page_icon="🏗️", layout="wide")
st.title("🏗️ BuildSight AI")
st.subheader("Multimodal Construction Intelligence Platform")
st.caption("Site safety • Crack diagnostics • Planning & valuation • Site assistant")

with st.sidebar:
    st.header("Project Settings")
    api_key = st.text_input("Gemini API key (optional)", type="password")
    st.info("Demo mode works without a key. AI outputs are advisory only.")

def ask_gemini(prompt, image=None):
    if not api_key:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model.generate_content([prompt, image] if image else prompt).text
    except Exception as exc:
        st.error(f"AI request failed: {exc}")
        return None

def export_report(data, filename):
    st.download_button("Download JSON report", json.dumps(data, indent=2), filename, "application/json")

page = st.sidebar.radio("Modules", ["Overview", "Site Safety & PPE Audit", "Crack Diagnostics", "Planning & Valuation", "Site Assistant"])

if page == "Overview":
    st.markdown("### Your construction project workspace")
    a,b,c,d = st.columns(4)
    a.metric("Modules", "4")
    b.metric("Image review", "Optional Gemini")
    c.metric("Reports", "JSON")
    d.metric("App", "Streamlit")
    st.write("Upload site photos for preliminary reviews, calculate a rough construction budget, and get weather-aware checklists.")
    st.warning("Educational prototype only. Not a certified safety inspection, structural assessment, engineering estimate, or property appraisal.")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

elif page == "Site Safety & PPE Audit":
    st.header("🦺 Site Safety & PPE Audit")
    uploaded = st.file_uploader("Upload a site image", type=["jpg","jpeg","png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_container_width=True)
        if st.button("Analyze site safety", type="primary"):
            prompt = "Review this construction site image for visible PPE and hazards. Return concise findings, severity, evidence, recommended action, and limitations. Do not claim certainty for unclear items. This is not a formal compliance inspection."
            result = ask_gemini(prompt, image)
            report = {"created_at": datetime.now().isoformat(), "module": "Safety audit",
                      "analysis": result or "Demo mode: no vision model ran. A qualified safety officer must inspect PPE, fall protection, access, lifting operations, electrical hazards and housekeeping."}
            st.write(report["analysis"])
            export_report(report, "safety_report.json")

elif page == "Crack Diagnostics":
    st.header("🧱 Crack Diagnostics")
    uploaded = st.file_uploader("Upload a wall or concrete image", type=["jpg","jpeg","png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_container_width=True)
        if st.button("Review visible defect", type="primary"):
            prompt = "Review this wall/concrete image for visible cracks or defects. Describe only visible evidence, possible causes with uncertainty, urgency and next steps. Do not estimate crack width without a scale and never certify structural safety. Recommend a qualified structural engineer for concerning defects."
            result = ask_gemini(prompt, image)
            report = {"created_at": datetime.now().isoformat(), "module": "Crack diagnostics",
                      "analysis": result or "Demo mode: no image model ran. Photograph with a scale, track changes, and consult a structural engineer for widening, diagonal, through-member cracks or deformation."}
            st.write(report["analysis"])
            export_report(report, "crack_report.json")

elif page == "Planning & Valuation":
    st.header("📐 Planning & Valuation Calculator")
    c1,c2 = st.columns(2)
    with c1:
        structure = st.selectbox("Structure", ["Residential","Commercial","Warehouse","Renovation"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, value=2000, step=100)
        rate = st.number_input("Estimated cost (₹/sq ft)", min_value=500, value=2200, step=100)
    with c2:
        completion = st.slider("Completion (%)", 0, 100, 25)
        multiplier = st.number_input("Market value multiplier", min_value=0.5, max_value=5.0, value=1.25, step=0.05)
    budget = area * rate
    incurred = budget * completion / 100
    value = budget * multiplier
    x,y,z = st.columns(3)
    x.metric("Indicative budget", f"₹{budget:,.0f}")
    y.metric("Progress cost proxy", f"₹{incurred:,.0f}")
    z.metric("Illustrative asset value", f"₹{value:,.0f}")
    st.caption("Use local quotes and professional appraisal. These figures are rough arithmetic estimates only.")
    export_report({"structure":structure,"area_sqft":area,"rate_inr_sqft":rate,"completion_percent":completion,
                   "estimated_budget_inr":budget,"progress_cost_proxy_inr":incurred,"illustrative_value_inr":value},
                  "planning_estimate.json")

elif page == "Site Assistant":
    st.header("🌦️ Site Assistant")
    weather = st.selectbox("Site conditions", ["Normal","High wind","Heavy rain","Extreme heat"])
    advice = {
        "Normal": ["Hold a toolbox talk and verify PPE.", "Check approved drawings, permits and housekeeping."],
        "High wind": ["Follow crane and work-at-height wind limits.", "Secure loose materials and temporary structures."],
        "Heavy rain": ["Check excavation stability, drainage and electrical protection.", "Keep people away from flooded or unstable areas."],
        "Extreme heat": ["Provide drinking water, shade, rest and heat-illness monitoring.", "Adjust strenuous work to conditions and local guidance."]
    }
    for item in advice[weather]:
        st.write("• " + item)
    question = st.text_area("Ask a construction question")
    if st.button("Get guidance", disabled=not question.strip()):
        prompt = f"Give cautious construction checklist guidance. Conditions: {weather}. Question: {question}. State uncertainty and refer safety-critical decisions to qualified professionals."
        result = ask_gemini(prompt)
        st.write(result or "Demo guidance: check method statements, drawings, permits, PPE, weather limits, materials, inspection hold points and responsible-person sign-off. Consult the project engineer or safety officer for safety-critical decisions.")

st.divider()
st.caption("BuildSight AI • Educational capstone prototype • Verify safety-critical outputs with qualified professionals.")
