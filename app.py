import json
import re
from datetime import datetime
from urllib.parse import quote
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Multimodal Construction Intelligence Platform", page_icon="🏗️", layout="wide")
st.markdown("""
<style>
.stApp {background: linear-gradient(180deg,#f6f8fc 0%,#ffffff 45%);}
[data-testid="stSidebar"] {background:#10213b;}
[data-testid="stSidebar"] * {color:#f8fafc;}
.hero {padding:1.5rem 1.7rem;border-radius:18px;background:linear-gradient(120deg,#10213b,#146b83);color:white;margin-bottom:1rem;}
.hero h1,.hero p {color:white;}
[data-testid="stMetric"] {background:white;padding:14px;border:1px solid #e2e8f0;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🏗️ Multimodal Construction Intelligence Platform</h1><p>AI-assisted site safety, structural defect triage, project planning, valuation and weather-aware guidance.</p></div>', unsafe_allow_html=True)
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API key (optional)", type="password", help="Key is used for this app session only; never commit it to GitHub.")
    st.caption("Architecture: Streamlit UI • Gemini multimodal AI • JSON report contracts • Local calculations")
    st.info("Demo mode works without an API key. AI analysis is advisory and must be verified by qualified professionals.")
    page = st.radio("Modules", ["Overview", "Site Safety & PPE Audit", "Crack Diagnostics", "Planning & Valuation", "Site Assistant & Weather"])

def ask_gemini(prompt, image=None):
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        contents = [prompt, image] if image is not None else prompt
        response = client.models.generate_content(model="gemini-2.5-flash", contents=contents)
        return response.text
    except Exception as exc:
        st.warning(f"Live AI request failed; safe demo guidance is shown instead. Details: {exc}")
        return None

def parse_json_response(text):
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass
    return {"analysis_text": text, "note": "The model did not return valid JSON; raw text is preserved."}

def export_report(report, filename):
    st.download_button("⬇️ Download JSON report", json.dumps(report, indent=2, ensure_ascii=False), filename, "application/json")

def show_hazards(report):
    score = report.get("safety_score")
    if isinstance(score, (int, float)):
        a,b = st.columns(2)
        a.metric("Safety score (AI estimate)", f"{score}/100")
        b.metric("Overall status", str(report.get("overall_status", "Review required")))
    ppe = report.get("ppe_detection")
    if isinstance(ppe, dict):
        st.subheader("PPE checklist")
        st.json(ppe)
    hazards = report.get("hazards", [])
    if isinstance(hazards, list) and hazards:
        st.subheader("Visible hazards and corrective actions")
        for item in hazards:
            if isinstance(item, dict):
                with st.expander(f"{item.get('severity','Review')} — {item.get('hazard','Site hazard')}"):
                    st.write("**Evidence:**", item.get("evidence", "Not specified"))
                    st.write("**Recommended remedy:**", item.get("remedy", "Qualified site review required"))
    st.json(report)

if page == "Overview":
    a,b,c,d = st.columns(4)
    a.metric("Core modules", "4")
    b.metric("AI mode", "Gemini / Demo")
    c.metric("Data contracts", "JSON")
    d.metric("Deployment target", "Streamlit")
    st.subheader("Project workflow")
    st.write("1. Configure optional Gemini access. 2. Upload site imagery or enter planning inputs. 3. Review structured results. 4. Export JSON reports and verify decisions with qualified professionals.")
    st.info("Scope follows the Skill Wallet Project 1 brief: PPE safety vision, crack diagnostics, construction cost and valuation, Pollinations conceptual-render prompt, weather-aware advisories, and a construction assistant.")
    st.warning("This educational decision-support prototype is not a formal OSHA/IS-code inspection, structural certification, bill of quantities, or professional property appraisal.")

elif page == "Site Safety & PPE Audit":
    st.header("🦺 Site Safety & PPE Audit")
    st.write("Upload a JPG/PNG construction-site photo for a preliminary visual review.")
    uploaded = st.file_uploader("Construction site photo", type=["jpg","jpeg","png"], key="safety_photo")
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded construction-site photo", use_container_width=True)
        if st.button("Analyze PPE and hazards", type="primary"):
            prompt = """Analyze the provided construction-site image for visible PPE and hazards. Consider hard hats, high-visibility vests, safety footwear only when visible, and harness/fall protection where applicable. Use OSHA/IS 456 only as context; do not claim formal compliance certification. Return ONLY valid JSON with schema:
{"safety_score": integer 0-100 or null, "overall_status": "Acceptable for review"|"Needs corrective action"|"Critical concerns"|"Unable to assess", "ppe_detection":{"helmet":"Present/Absent/Unclear/Not visible","high_visibility_vest":"Present/Absent/Unclear/Not visible","safety_footwear":"Present/Absent/Unclear/Not visible","harness":"Present/Absent/Unclear/Not applicable"}, "hazards":[{"hazard":"...", "severity":"Low|Medium|High|Critical", "evidence":"visible evidence only", "remedy":"corrective action"}], "limitations":"..."}.
Do not infer unseen details; if evidence is unclear, mark Unclear. This is not a formal inspection."""
            raw = ask_gemini(prompt, image)
            report = parse_json_response(raw) if raw else {
                "safety_score": None, "overall_status": "Manual review required",
                "ppe_detection": {"helmet":"Unassessed in demo mode","high_visibility_vest":"Unassessed in demo mode","safety_footwear":"Unassessed in demo mode","harness":"Unassessed in demo mode"},
                "hazards":[{"hazard":"Site inspection required","severity":"Review","evidence":"Demo mode did not run a vision model.","remedy":"Have a competent safety officer inspect PPE, fall protection, lifting operations, electrical hazards and housekeeping."}],
                "limitations":"No automated image inference was performed."
            }
            show_hazards(report)
            export_report({"module":"Site Safety & PPE Audit","created_at":datetime.now().isoformat(),"report":report}, "safety_audit.json")

elif page == "Crack Diagnostics":
    st.header("🧱 Crack Diagnostics & Structural Integrity")
    uploaded = st.file_uploader("Concrete or wall surface photo", type=["jpg","jpeg","png"], key="crack_photo")
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded surface image", use_container_width=True)
        scale_available = st.checkbox("A ruler or known-size reference is visible in the image")
        if st.button("Analyze visible defect", type="primary"):
            prompt = f"""Review this concrete/wall image for visible defects. Reference scale available: {scale_available}. Return ONLY valid JSON:
{{"defect_type":"Hairline|Settlement|Structural Shear|Thermal Expansion|Spalling|Other|Unable to assess","estimated_crack_width_mm": number or null,"severity_score": integer 0-100 or null,"possible_root_causes":["..."],"recommended_repairs":["..."],"urgency":"Routine monitoring|Prompt engineering inspection|Urgent restricted access and inspection","visible_evidence":"...","limitations":"..."}}
Do not estimate width unless a reliable scale is clearly visible. Do not certify structural integrity. Repair methods such as epoxy injection or structural re-grouting must only be recommended after qualified engineering diagnosis."""
            raw = ask_gemini(prompt, image)
            report = parse_json_response(raw) if raw else {
                "defect_type":"Not assessed in demo mode","estimated_crack_width_mm":None,"severity_score":None,
                "possible_root_causes":["Cannot determine without image-model review and site context"],
                "recommended_repairs":["Document with a ruler for scale","Monitor and record changes","Seek a qualified structural engineer for widening, diagonal, through-member cracks or deformation"],
                "urgency":"Professional review required","visible_evidence":"No automated visual analysis was performed.",
                "limitations":"A photograph alone cannot establish structural safety."
            }
            if isinstance(report, dict):
                x,y = st.columns(2)
                x.metric("Defect category", str(report.get("defect_type","Review required")))
                y.metric("Severity score", str(report.get("severity_score") if report.get("severity_score") is not None else "Not scored"))
            st.json(report)
            export_report({"module":"Crack Diagnostics","created_at":datetime.now().isoformat(),"report":report}, "crack_diagnostics.json")

elif page == "Planning & Valuation":
    st.header("📐 Construction Planning & Real Estate Valuation")
    c1,c2 = st.columns(2)
    with c1:
        structure = st.selectbox("Structure type", ["Residential","Commercial","Warehouse","Renovation"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=1000000, value=2000, step=100)
        tier = st.selectbox("Indian city tier", ["Tier 1","Tier 2","Tier 3"])
    with c2:
        base_rate = st.number_input("Base construction rate (₹/sq ft)", min_value=500, max_value=20000, value=2200, step=100)
        completion = st.slider("Project completion (%)", 0, 100, 25)
        valuation_multiplier = st.number_input("Indicative market value multiplier", min_value=0.5, max_value=5.0, value=1.25, step=0.05)
    tier_factor = {"Tier 1":1.15,"Tier 2":1.0,"Tier 3":0.9}[tier]
    adjusted_rate = base_rate * tier_factor
    budget = area * adjusted_rate
    incurred = budget * completion / 100
    market_value = budget * valuation_multiplier
    # Broad thumb-rule assumptions for early planning only; actual quantities depend on design and specifications.
    steel_kg = area * 4.0
    cement_bags = area * 0.4
    st.caption(f"Rate adjusted by illustrative {tier} planning factor ({tier_factor:.2f}); replace with local quotations.")
    a,b,c = st.columns(3)
    a.metric("Indicative project budget", f"₹{budget/100000:.2f} lakh")
    b.metric("Cost incurred proxy", f"₹{incurred/100000:.2f} lakh")
    c.metric("Illustrative market valuation", f"₹{market_value/100000:.2f} lakh")
    st.progress(completion/100, text=f"Milestone progress: {completion}%")
    d,e = st.columns(2)
    d.metric("Steel planning allowance", f"{steel_kg:,.0f} kg")
    e.metric("Cement planning allowance", f"{cement_bags:,.0f} bags")
    st.warning("Steel/cement figures are generic early-stage thumb rules, not a quantity takeoff. Confirm with structural drawings and a quantity surveyor.")
    report = {"module":"Planning & Valuation","created_at":datetime.now().isoformat(),"structure_type":structure,"built_up_area_sqft":area,"city_tier":tier,"base_rate_inr_sqft":base_rate,"tier_factor":tier_factor,"adjusted_rate_inr_sqft":adjusted_rate,"completion_percent":completion,"estimated_budget_inr":round(budget,2),"capital_expenditure_proxy_inr":round(incurred,2),"illustrative_market_value_inr":round(market_value,2),"steel_allowance_kg":round(steel_kg,2),"cement_allowance_bags":round(cement_bags,2),"assumptions":"Illustrative estimates only; validate locally."}
    export_report(report, "construction_planning_estimate.json")
    st.subheader("Conceptual 3D architectural rendering prompt")
    render_prompt = st.text_area("Describe the concept", f"Photorealistic conceptual 3D architectural rendering of a {structure.lower()} building of approximately {area} sq ft, modern Indian context, clear daylight, realistic materials, professional architectural visualization. Concept only, not an approved design.")
    st.code(render_prompt)
    st.link_button("Open Pollinations image generator", "https://image.pollinations.ai/prompt/" + quote(render_prompt, safe=""))

elif page == "Site Assistant & Weather":
    st.header("🌦️ Daily Site Assistant & Weather-Aware Advisory")
    weather = st.selectbox("Site conditions", ["Normal","High Wind","Heavy Rain","Extreme Heat"])
    advice = {
        "Normal":["Conduct a toolbox talk and verify PPE before work.","Check approved drawings, permits, access routes and housekeeping.","Follow the approved concrete placement and curing method statement."],
        "High Wind":["Suspend crane lifts and work at height when site/equipment limits are exceeded.","Secure loose materials and inspect temporary structures.","Follow the site lift plan and manufacturer wind limits."],
        "Heavy Rain":["Review excavation stability, drainage and electrical protection.","Keep workers away from flooded or unstable areas.","Inspect access routes and concrete protection/curing arrangements before restarting."],
        "Extreme Heat":["Provide drinking water, shade, rest breaks and heat-illness monitoring.","Reschedule strenuous work where feasible.","Protect fresh concrete and follow the approved hot-weather curing protocol."]
    }
    st.subheader("Recommended daily checklist")
    for item in advice[weather]:
        st.write("• " + item)
    st.divider()
    st.subheader("Construction engineering assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    question = st.chat_input("Ask about construction planning, site safety or methods")
    if question:
        st.session_state.chat_history.append({"role":"user","content":question})
        prompt = "You are a cautious construction engineering assistant. Site condition: " + weather + ". Provide practical checklist guidance, explain uncertainty, do not invent code requirements, and refer structural/life-safety decisions to qualified professionals. Question: " + question
        history_context = "\n".join(m["role"] + ": " + m["content"] for m in st.session_state.chat_history[-8:])
        answer = ask_gemini(prompt + "\nRecent conversation:\n" + history_context)
        if not answer:
            answer = "Demo guidance: verify approved drawings, method statements, permits, PPE, weather/equipment limits, material quality, inspection hold points and responsible-person sign-off. Share the exact activity and site conditions for a more specific checklist. For safety-critical decisions, consult the project engineer or safety officer."
        st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.rerun()
    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()

st.divider()
st.caption("Skill Wallet Capstone Project 1 • Multimodal Construction Intelligence Platform • AI output is advisory, not engineering certification.")
