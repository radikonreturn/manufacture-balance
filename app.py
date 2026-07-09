"""
app.py — Manufacture Balance 4.0 Dashboard
Sustainable Lean Manufacturing · Assembly Line Balancing · Operator 4.0

Run: python -m streamlit run app.py
"""

import streamlit as st
from data.database import init_db

from ui.styles import C, apply_styles
from ui.icons import svg
from ui.tabs.input_tab import render_input_tab
from ui.tabs.results_tab import render_results_tab
from ui.tabs.operator_tab import render_operator_tab
from ui.tabs.sustainability_tab import render_sustainability_tab
from ui.tabs.compare_tab import render_compare_tab

# ── Page Config ───────────────────────────────────────────────────── #
st.set_page_config(
    page_title="Manufacture Balance 4.0",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)
init_db()

# ── CSS ───────────────────────────────────────────────────────────── #
apply_styles()

# ── Header ────────────────────────────────────────────────────────── #
st.markdown(f"""
<div style="display:flex; justify-content:between; align-items:center; border-bottom:2px solid {C['border']}; padding-bottom:1rem; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
    <div style="flex-grow:1;">
        <div style="font-family:'Fira Code',monospace; font-size:1.8rem; font-weight:700; letter-spacing:-.02em; line-height:1.1;">
            MANUFACTURE<span style="color:{C['primary']};">.BALANCE</span> <span style="font-size:0.9rem; color:{C['muted']}; font-weight:400; vertical-align:middle;">[v4.0]</span>
        </div>
        <div style="font-size:0.75rem; color:{C['muted']}; font-family:'Fira Code',monospace; margin-top:0.25rem; letter-spacing:0.02em;">
            SYSTEM_STATUS: ACTIVE // DECISION_SUPPORT_ENGINE
        </div>
    </div>
    <div style="display:flex; gap:.5rem; align-items:center;">
        <span class="b b-i">LINE OPTIMIZATION</span>
        <span class="b b-g">ENERGY EFFICIENCY</span>
        <span class="b b-p">OPERATOR 4.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────── #
with st.sidebar:
    st.markdown(f"""
    <div style="padding:.5rem 0 1rem; border-bottom:1px solid {C['border']}; margin-bottom:1rem;">
        <div style="font-family:'Fira Code',monospace; font-size:1.1rem; font-weight:700;">
            SYSTEM<span style="color:{C['primary']};">.CTRL</span>
        </div>
        <div style="font-size:.65rem; color:{C['muted']}; letter-spacing:.1em; text-transform:uppercase; margin-top:.3rem;">
            PARAMETER CONFIGURATION
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'### {svg("clock", 18, C["primary"])} SIMULATION', unsafe_allow_html=True)
    cycle_time = st.slider("Cycle Time (sec)", 5.0, 60.0, 15.0, 0.5)
    algorithm = st.selectbox("Algorithm", ["RPW (Ranked Positional Weight)", "Greedy (Largest Candidate)", "Compare (Both)"])

    st.markdown(f'### {svg("lightning", 18, C["warning"])} ENERGY MODEL', unsafe_allow_html=True)
    kwh_rate = st.number_input("Station Power (kW)", 0.1, 50.0, 7.2, 0.1)
    kwh_per_sec = kwh_rate / 3600
    cost_per_kwh = st.number_input("Energy Cost ($/kWh)", 0.1, 20.0, 2.5, 0.1)
    co2_factor = st.number_input("CO₂ Factor (kg/kWh)", 0.01, 2.0, 0.47, 0.01)

# ── Tabs ──────────────────────────────────────────────────────────── #
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Data Input", "Results", "Operator JES", "Sustainability", "Compare"
])

with tab1:
    render_input_tab()

with tab2:
    render_results_tab(algorithm, cycle_time, kwh_per_sec, cost_per_kwh, co2_factor)

with tab3:
    render_operator_tab(cycle_time)

with tab4:
    render_sustainability_tab()

with tab5:
    render_compare_tab()

# ── Footer ────────────────────────────────────────────────────────── #
st.markdown('<div class="ft">MANUFACTURE BALANCE 4.0 &nbsp;·&nbsp; Sustainable Lean Manufacturing</div>', unsafe_allow_html=True)
