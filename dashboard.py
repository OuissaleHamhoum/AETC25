# dashboard.py
import streamlit as st
import pandas as pd
import random
from tars_guardian import AIModule, AnomalyDetectionSystem
import altair as alt

# ===============================
# PAGE CONFIGURATION
# ===============================
st.set_page_config(page_title="TARS-Guardian Dashboard", layout="wide")
st.title("🚀 TARS-Guardian: HORIZON-1 AI Dashboard")
st.markdown("---")

# ===============================
# Initialize detector (singleton)
# ===============================
if "detector" not in st.session_state:
    st.session_state.detector = AnomalyDetectionSystem()
    modules = [
        AIModule(1, "Navigation AI", critical=True),
        AIModule(2, "Life Support AI", critical=True),
        AIModule(3, "Communication AI", critical=False),
        AIModule(4, "Power Management AI", critical=True),
        AIModule(5, "Scientific Research AI", critical=False),
        AIModule(6, "Propulsion Control AI", critical=True),
    ]
    for m in modules:
        st.session_state.detector.add_module(m)
    st.session_state.detector.establish_baseline()

detector = st.session_state.detector

# ===============================
# Sidebar actions
# ===============================
st.sidebar.header("Actions")
if st.sidebar.button("Reset Modules"):
    detector = AnomalyDetectionSystem()
    st.session_state.detector = detector
    modules = [
        AIModule(1, "Navigation AI", critical=True),
        AIModule(2, "Life Support AI", critical=True),
        AIModule(3, "Communication AI", critical=False),
        AIModule(4, "Power Management AI", critical=True),
        AIModule(5, "Scientific Research AI", critical=False),
        AIModule(6, "Propulsion Control AI", critical=True),
    ]
    for m in modules:
        detector.add_module(m)
    detector.establish_baseline()
    st.success("Modules reset successfully!")

# ===============================
# Main actions
# ===============================
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Run Simulation Cycle"):
        # Inject compromise randomly
        compromised_module = random.choice(list(detector.modules.values()))
        if not compromised_module.compromised:
            severity = random.choice(["low", "medium", "high"])
            detector.inject_compromise(compromised_module.module_id, severity)

        # Run one monitoring cycle
        anomalies = detector.monitor_cycle(detector.cycle_count + 1)
        # Update status: isolate compromised modules
        for module in detector.modules.values():
            if module.compromised:
                module.status = "ISOLATED"
            else:
                module.status = "ACTIVE"
        st.success("Simulation cycle executed!")

# ===============================
# Function to color Status column
# ===============================
def color_status(val):
    colors = {
        "ACTIVE": "green",
        "ISOLATED": "red",
        "INACTIVE": "grey"
    }
    return f"color: {colors.get(val, 'black')}"

# ===============================
# Module status table
# ===============================
st.subheader("Module Status Table")
table_data = pd.DataFrame([
    {
        "module_id": m.module_id,
        "name": m.name,
        "status": m.status,
        "compromised": m.compromised,
        "compromise_severity": m.compromise_severity.upper() if m.compromised else ""
    }
    for m in detector.modules.values()
])
st.table(table_data.style.map(color_status, subset=["status"]))

# ===============================
# Graphique coloré par module
# ===============================
st.subheader("Module Status Overview")
chart_data = pd.DataFrame([
    {"Module": m.name, "Status": m.status} for m in detector.modules.values()
])

status_colors = {
    "ACTIVE": "green",
    "ISOLATED": "red",
    "INACTIVE": "grey"
}

chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X('Module', sort=None),
    y=alt.Y('Status', aggregate='count', title=''),
    color=alt.Color('Status', scale=alt.Scale(domain=list(status_colors.keys()),
                                              range=list(status_colors.values()))),
    tooltip=['Module', 'Status']
).properties(width=700, height=300, title="Module Status Overview")

st.altair_chart(chart, use_container_width=True)

# ===============================
# Global system status
# ===============================
isolated_count = sum(1 for m in detector.modules.values() if m.status == "ISOLATED")
if isolated_count > 0:
    st.warning(f"⚠️ Threat detected: {isolated_count} module(s) isolated!")
else:
    st.success("✅ All modules are ACTIVE and secure.")
