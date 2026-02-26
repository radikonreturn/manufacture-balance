import streamlit as st
import plotly.graph_objects as go

from ui.styles import C, PLOTLY_LAYOUT


def render_sustainability_tab():
    st.markdown('<div class="sh">🌿 Sustainability Report <span class="b b-g" style="margin-left:.75rem;">9TH WASTE</span></div>', unsafe_allow_html=True)
    energy_report = st.session_state.get("energy_rpw") or st.session_state.get("energy_greedy")

    if not energy_report:
        st.warning("⚠️ Run the solver in **Results** tab first.")
    else:
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f'<div class="sc"><div class="ico">⚡</div><div class="v">{energy_report.total_energy_kwh:.4f}</div><div class="l">Energy Waste (kWh)</div></div>', unsafe_allow_html=True)
        with s2:
            st.markdown(f'<div class="sc"><div class="ico">💰</div><div class="v">${energy_report.total_cost:.2f}</div><div class="l">Waste Cost</div></div>', unsafe_allow_html=True)
        with s3:
            st.markdown(f'<div class="sc"><div class="ico">🌍</div><div class="v">{energy_report.total_co2_kg:.4f}</div><div class="l">CO₂ Footprint (kg)</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sh">📊 Station-Level Analysis</div>', unsafe_allow_html=True)
        fig_e = go.Figure()
        labels = [f"Stn {d.station_id}" for d in energy_report.per_station]
        fig_e.add_trace(go.Bar(x=labels, y=[d.idle_time for d in energy_report.per_station], name="Idle Time (s)", marker_color=C["danger"], opacity=0.8))
        fig_e.add_trace(go.Bar(x=labels, y=[d.energy_kwh * 1000 for d in energy_report.per_station], name="Energy Waste (Wh)", marker_color=C["warning"], opacity=0.8))
        fig_e.update_layout(**PLOTLY_LAYOUT)
        fig_e.update_layout(barmode="group", height=350, margin=dict(b=0, t=10))
        st.plotly_chart(fig_e, use_container_width=True)
