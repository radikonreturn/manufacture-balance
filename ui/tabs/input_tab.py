import streamlit as st
import pandas as pd
import io

from ui.styles import C
from ui.components import metric_card, create_dag_figure
from data.parser import parse_csv
from engine.graph import PrecedenceGraph


def load_graph(df: pd.DataFrame) -> PrecedenceGraph:
    g = PrecedenceGraph()
    g.load_from_dataframe(df)
    return g


def render_input_tab():
    st.markdown('<div class="sh">📥 Task Data Input</div>', unsafe_allow_html=True)

    data_source = st.radio(
        "Select data source",
        ["📂 Sample Data", "📤 Upload CSV", "✏️ Manual Entry"],
        horizontal=True, label_visibility="collapsed",
    )

    df = None

    if data_source == "📂 Sample Data":
        try:
            df = parse_csv("sample_tasks.csv")
            st.success("Loaded 10 tasks from `sample_tasks.csv`")
        except Exception as e:
            st.error(str(e))
    elif data_source == "📤 Upload CSV":
        uploaded = st.file_uploader("Upload CSV", type=["csv"], help="Columns: task_id, task_name, duration, predecessors")
        if uploaded:
            try:
                df = parse_csv(io.BytesIO(uploaded.read()))
                st.success("CSV uploaded and validated!")
            except ValueError as e:
                st.error(f"Validation error: {e}")
    elif "Manual Entry" in data_source:
        default_data = pd.DataFrame({"task_id": ["T1", "T2"], "task_name": ["Task 1", "Task 2"], "duration": [5.0, 4.0], "predecessors": ["", "T1"]})
        edited = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)
        if st.button("✅ Confirm Data", type="primary"):
            try:
                df = parse_csv(io.StringIO(edited.to_csv(index=False)))
                st.success("Data validated!")
            except ValueError as e:
                st.error(f"Validation error: {e}")
                df = None

    if df is not None:
        st.session_state["task_df"] = df
        try:
            graph = load_graph(df)
            st.session_state["graph"] = graph
            s = graph.summary()

            c1, c2 = st.columns([1, 2])
            with c1:
                cols = st.columns(2)
                with cols[0]:
                    st.markdown(metric_card(s["task_count"], "Tasks", C["primary"]), unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(metric_card(f"{s['total_work_content']}s", "Work Content", C["warning"]), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                cols2 = st.columns(2)
                with cols2[0]:
                    st.markdown(metric_card(len(s["entry_tasks"]), "Start Nodes", C["success"]), unsafe_allow_html=True)
                with cols2[1]:
                    st.markdown(metric_card(len(s["exit_tasks"]), "End Nodes", C["danger"]), unsafe_allow_html=True)

            with c2:
                # ── Feature 1: DAG Visualization ──
                st.plotly_chart(create_dag_figure(graph), use_container_width=True)

        except Exception as e:
            st.error(f"Graph error: {e}")
