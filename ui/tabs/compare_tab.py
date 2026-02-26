import streamlit as st
import plotly.graph_objects as go

from data.database import list_scenarios, load_scenario
from ui.styles import C, PLOTLY_LAYOUT


def delta_metric(label, v1, v2, suffix="", invert=False):
    diff = v2 - v1
    is_better = diff < 0 if invert else diff > 0
    if diff == 0:
        color = C["muted"]
        sign = ""
    elif is_better:
        color = C["success"]
        sign = "↓" if invert else "↑"
    else:
        color = C["danger"]
        sign = "↑" if invert else "↓"

    return f"""<div class="mc" style="padding:1rem;">
        <div class="l">{label}</div>
        <div style="font-family:'Fira Code',monospace; font-size:1.8rem; font-weight:700; color:{C['text']}; margin:.5rem 0;">{v2}{suffix}</div>
        <div style="color:{color}; font-size:.8rem; font-weight:700; font-family:'Fira Code',monospace;">{sign} {abs(diff):.2f}{suffix} vs baseline</div>
    </div>"""


def render_compare_tab():
    st.markdown('<div class="sh">⚖️ Scenario Comparison</div>', unsafe_allow_html=True)
    saved = list_scenarios()

    if len(saved) < 2:
        st.info("⚠️ Please save at least 2 scenarios in the Results tab to compare them here.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            s1_idx = st.selectbox("Select Baseline Scenario", range(len(saved)), format_func=lambda i: f"[{saved[i]['algorithm'].upper()}] {saved[i]['name']} (CT={saved[i]['cycle_time']})", key="sc1")
        with c2:
            s2_idx = st.selectbox("Select Target Scenario", range(len(saved)), index=min(1, len(saved)-1), format_func=lambda i: f"[{saved[i]['algorithm'].upper()}] {saved[i]['name']} (CT={saved[i]['cycle_time']})", key="sc2")

        sc1 = load_scenario(saved[s1_idx]["id"])
        sc2 = load_scenario(saved[s2_idx]["id"])

        if not sc1 or not sc2 or not sc1.get("results") or not sc2.get("results"):
            st.error("One or more selected scenarios have missing results data.")
            return

        m1 = sc1["results"]
        m2 = sc2["results"]

        st.markdown("### 📈 Metric Deltas")
        mc1, mc2, mc3, mc4 = st.columns(4)

        with mc1:
            st.markdown(delta_metric("Efficiency", m1["line_efficiency"], m2["line_efficiency"], "%"), unsafe_allow_html=True)
        with mc2:
            st.markdown(delta_metric("Stations", m1["num_stations"], m2["num_stations"], "", invert=True), unsafe_allow_html=True)
        with mc3:
            st.markdown(delta_metric("Smoothness", m1["smoothness_index"], m2["smoothness_index"], "", invert=True), unsafe_allow_html=True)
        with mc4:
            e1 = sc1["results"].get("total_energy_kwh", 0)
            e2 = sc2["results"].get("total_energy_kwh", 0)
            st.markdown(delta_metric("Energy Waste", e1, e2, " kWh", invert=True), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Load Comparison Chart
        st1_loads = [s["total_time"] for s in sc1["results"].get("stations", [])]
        st2_loads = [s["total_time"] for s in sc2["results"].get("stations", [])]

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name=f"Baseline: {sc1['name']}", x=[f"Stn {i+1}" for i in range(len(st1_loads))], y=st1_loads, marker_color=C["muted"]))
        fig_comp.add_trace(go.Bar(name=f"Target: {sc2['name']}", x=[f"Stn {i+1}" for i in range(len(st2_loads))], y=st2_loads, marker_color=C["primary"]))
        fig_comp.update_layout(**PLOTLY_LAYOUT, barmode="group", title=dict(text="Station Loads Comparison", font=dict(size=14)), yaxis_title="Load Time (sec)", height=350)

        # Add Cycle Time Lines
        fig_comp.add_hline(y=sc1["cycle_time"], line_dash="dash", line_color=C["muted"], annotation_text="Baseline CT")
        if sc1["cycle_time"] != sc2["cycle_time"]:
            fig_comp.add_hline(y=sc2["cycle_time"], line_dash="dash", line_color=C["primary"], annotation_text="Target CT")

        st.plotly_chart(fig_comp, use_container_width=True)
