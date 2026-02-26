import streamlit as st
import plotly.graph_objects as go
import html

from engine.rpw_solver import solve_rpw
from engine.greedy_solver import solve_greedy
from engine.metrics import compute_all_metrics
from engine.energy_waste import calculate_energy_waste
from engine.jes_generator import generate_jes
from data.database import save_scenario
from ui.styles import C, PLOTLY_LAYOUT
from ui.components import metric_card, generate_excel_export


def render_results_tab(algorithm, cycle_time, kwh_per_sec, cost_per_kwh, co2_factor):
    st.markdown('<div class="sh">📊 Line Balancing Results</div>', unsafe_allow_html=True)

    if "graph" not in st.session_state:
        st.warning("⚠️ Load data in the **Data Input** tab first.")
    else:
        graph = st.session_state["graph"]
        try:
            algo_key = {"RPW (Ranked Positional Weight)": "rpw", "Greedy (Largest Candidate)": "greedy", "Compare (Both)": "compare"}[algorithm]

            if algo_key == "compare":
                results_list = [("RPW", solve_rpw(graph, cycle_time)), ("Greedy", solve_greedy(graph, cycle_time))]
            elif algo_key == "rpw":
                results_list = [("RPW", solve_rpw(graph, cycle_time))]
            else:
                results_list = [("Greedy", solve_greedy(graph, cycle_time))]

            for algo_name, stations in results_list:
                if algo_key == "compare":
                    st.markdown(f"""<div style="margin:1.5rem 0 .75rem; font-family:'Fira Code',monospace; font-size:1.1rem; font-weight:700; color:{C['text']}; border-bottom:1px solid {C['border']}; padding-bottom:0.5rem;"><span style="color:{C['primary']};">▸</span> {algo_name} Algorithm</div>""", unsafe_allow_html=True)

                metrics = compute_all_metrics(stations, cycle_time, graph.total_work_content())
                energy = calculate_energy_waste(stations, cycle_time, kwh_per_sec, cost_per_kwh, co2_factor)

                # ── Metric Cards ──
                m1, m2, m3, m4, m5 = st.columns(5)
                eff = metrics["line_efficiency"]
                eff_color = C["success"] if eff >= 80 else C["warning"] if eff >= 60 else C["danger"]
                with m1:
                    st.markdown(metric_card(f"{eff}%", "Efficiency", eff_color), unsafe_allow_html=True)
                with m2:
                    st.markdown(metric_card(f"{metrics['balance_delay']}%", "Balance Delay"), unsafe_allow_html=True)
                with m3:
                    st.markdown(metric_card(metrics["smoothness_index"], "Smoothness"), unsafe_allow_html=True)
                with m4:
                    st.markdown(metric_card(metrics["num_stations"], "Stations", C["primary"]), unsafe_allow_html=True)
                with m5:
                    st.markdown(metric_card(metrics["theoretical_min_stations"], "Theo. Min", C["muted"]), unsafe_allow_html=True)

                st.markdown("")

                # ── Station Load Chart ──
                fig = go.Figure()
                for s_item in stations:
                    safe_tasks = ", ".join(html.escape(str(t)) for t in s_item["tasks"])
                    fig.add_trace(go.Bar(
                        x=[s_item["total_time"]], y=[f"Stn {s_item['station_id']}"],
                        orientation="h", name=f"Stn {s_item['station_id']}",
                        text=f"{s_item['total_time']}s  ({safe_tasks})", textposition="inside", textfont=dict(size=11),
                        marker=dict(color=C["primary"], line=dict(width=0)),
                        hovertemplate=f"<b>Station {s_item['station_id']}</b><br>Load: {s_item['total_time']}s<br>Idle: {s_item['idle_time']}s<br>Tasks: {safe_tasks}<extra></extra>",
                    ))
                    if s_item["idle_time"] > 0:
                        fig.add_trace(go.Bar(
                            x=[s_item["idle_time"]], y=[f"Stn {s_item['station_id']}"],
                            orientation="h", name="Idle", showlegend=False,
                            text=f"{s_item['idle_time']}s", textposition="inside", textfont=dict(size=10, color="rgba(248,250,252,0.5)"),
                            marker=dict(color="rgba(239,68,68,0.2)", line=dict(width=0)),
                        ))

                fig.add_vline(x=cycle_time, line_dash="dash", line_color=C["warning"], annotation_text=f"CT={cycle_time}s", annotation_font=dict(color=C["warning"], size=11))
                fig.update_layout(**PLOTLY_LAYOUT, barmode="stack", title=dict(text=f"Station Loads — {algo_name}", font=dict(size=14)), xaxis_title="Time (sec)", yaxis_title="", height=max(220, len(stations) * 55 + 60), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

                # ── Bottlenecks ──
                bn_scores = metrics["bottleneck_scores"]
                bn_cols = st.columns(len(bn_scores))
                for i, bn in enumerate(bn_scores):
                    with bn_cols[i]:
                        bc = "b-r" if bn["is_bottleneck"] else "b-y" if bn["load_percent"] >= 70 else "b-g"
                        bl = "BOTTLENECK" if bn["is_bottleneck"] else "OPTIMAL"
                        st.markdown(f'<div class="bn"><div class="sid">Station {bn["station_id"]}</div><div class="pct">{bn["load_percent"]}%</div><span class="b {bc}">{bl}</span></div>', unsafe_allow_html=True)

                st.session_state[f"energy_{algo_name.lower()}"] = energy
                st.session_state[f"stations_{algo_name.lower()}"] = stations
                st.session_state[f"metrics_{algo_name.lower()}"] = metrics

            # ── Excel Export (Feature 3) & Saving ──
            st.markdown("---")
            
            algo_for_export, stations_for_export = results_list[0]
            if len(results_list) > 1:
                selected_algo = st.selectbox("Select algorithm for saving/exporting:", [r[0] for r in results_list])
                algo_for_export, stations_for_export = next(r for r in results_list if r[0] == selected_algo)

            cc1, cc2 = st.columns(2)

            with cc1:
                st.markdown("### 💾 Save Scenario to Database")
                scen_name = st.text_input("Name", value=f"{algo_for_export[:3]}_CT{cycle_time}", label_visibility="collapsed")
                if st.button("Save Scenario", type="primary"):
                    try:
                        m_key = f"metrics_{algo_for_export.lower()}"
                        e_key = f"energy_{algo_for_export.lower()}"
                        last_m = st.session_state.get(m_key, {})
                        last_e = st.session_state.get(e_key)
                        tdf = st.session_state.get("task_df")
                        sid = save_scenario(scen_name, cycle_time, algo_for_export.lower(), tdf.to_dict("records") if tdf is not None else [], last_m, stations_for_export, last_e.to_dict() if last_e else {})
                        st.success(f"Saved! (ID: {sid})")
                    except Exception as e:
                        st.error(str(e))

            with cc2:
                st.markdown("### 📥 Download Excel Report")
                metrics_exp = st.session_state.get(f"metrics_{algo_for_export.lower()}")
                energy_exp = st.session_state.get(f"energy_{algo_for_export.lower()}")
                jes_exp = generate_jes(stations_for_export, cycle_time)
                excel_data = generate_excel_export(metrics_exp, stations_for_export, energy_exp, jes_exp, cycle_time, algo_for_export)

                st.download_button(
                    label="Download .xlsx",
                    data=excel_data,
                    file_name=f"Report_{algo_for_export}_CT{cycle_time}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        except ValueError as e:
            st.error(f"Solution error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
