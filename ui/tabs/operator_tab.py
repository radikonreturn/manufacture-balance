import streamlit as st
import html

from engine.jes_generator import generate_jes, format_jes_markdown
from ui.styles import C
from ui.icons import svg
from ui.components import metric_card


def render_operator_tab(cycle_time):
    st.markdown(f'<div class="sh">{svg("hard_hat", 18, C["primary"])} Digital Work Instructions <span class="b b-i" style="margin-left:.75rem;">JES</span></div>', unsafe_allow_html=True)
    available_stations = st.session_state.get("stations_rpw") or st.session_state.get("stations_greedy")

    if not available_stations:
        st.warning("Solver results missing: Execute line balancing in the Results tab first.", icon=None)
    else:
        jes_all = generate_jes(available_stations, cycle_time)
        selected_station = st.selectbox("Select Station", sorted(jes_all.keys()), format_func=lambda x: f"Station {x}")

        if selected_station:
            jes = jes_all[selected_station]
            pct = jes["utilization_pct"]
            j1, j2, j3 = st.columns(3)
            with j1:
                st.markdown(metric_card(f"{jes['cycle_time']}s", "Cycle Time", C["muted"]), unsafe_allow_html=True)
            with j2:
                st.markdown(metric_card(f"{jes['total_time']}s", "Load", C["primary"]), unsafe_allow_html=True)
            with j3:
                st.markdown(metric_card(f"{pct}%", "Utilization", C["success"] if pct >= 80 else C["warning"]), unsafe_allow_html=True)

            bar_c = C["success"] if pct >= 80 else C["warning"] if pct >= 60 else C["danger"]
            st.markdown(f'<div class="pt" style="height:6px; margin:1rem 0 1.5rem;"><div class="pb" style="width:{min(pct,100)}%; background:linear-gradient(90deg,{bar_c},{bar_c}88);"></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="sh" style="margin-top:0;">{svg("clipboard", 16, C["primary"])} Work Steps</div>', unsafe_allow_html=True)

            for s in jes["steps"]:
                prog = round((s["cumulative_time"] / jes["cycle_time"]) * 100, 1)
                kp = f'<div style="color:{C["warning"]}; font-size:.8rem; margin-top:.5rem;">{svg("pin", 13, C["warning"])} {html.escape(s["key_points"])}</div>' if s["key_points"] else ""
                st.markdown(f"""
                <div class="js"><div class="h"><span>Step {s['step']}: {html.escape(s['task_name'])}</span><span class="t">{svg('clock', 13, C['muted'])} {s['duration']}s</span></div>
                <div class="d"><span>ID: <code>{html.escape(s['task_id'])}</code></span><span>&#x3A3; {s['cumulative_time']}/{jes['cycle_time']}s</span><span>Rem: {s['remaining_time']}s</span></div>
                <div class="pt"><div class="pb" style="width:{prog}%; background:linear-gradient(90deg,{C['primary']},{C['primary2']});"></div></div>{kp}</div>
                """, unsafe_allow_html=True)

            with st.expander(f"{svg('document', 14)} Export Markdown"):
                md = format_jes_markdown(jes)
                st.code(md, language="markdown")
                st.download_button(f"{svg('download', 14)} Download", md, f"JES_Station_{selected_station}.md", "text/markdown")
