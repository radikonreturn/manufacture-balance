import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict
import io

from engine.graph import PrecedenceGraph
from ui.styles import C, PLOTLY_LAYOUT

def metric_card(value, label, color=None):
    if color is None:
        color = C["text"]
    return f'<div class="mc"><div class="v" style="color:{color};">{value}</div><div class="l">{label}</div></div>'

def create_dag_figure(g: PrecedenceGraph) -> go.Figure:
    """Create a Plotly network graph defining the DAG layout manually using topological layers."""
    try:
        order = g.topological_sort()
    except Exception:
        return go.Figure()

    depth = {}
    for tid in order:
        preds = g.predecessors[tid]
        depth[tid] = 0 if not preds else max(depth[p] for p in preds) + 1

    layers = defaultdict(list)
    for tid, d in depth.items():
        layers[d].append(tid)

    pos = {}
    for d, nodes in layers.items():
        n = len(nodes)
        for i, tid in enumerate(nodes):
            pos[tid] = (d, (n - 1) / 2.0 - i)

    edge_x, edge_y = [], []
    for tid in g.tasks:
        x0, y0 = pos[tid]
        for succ in g.successors[tid]:
            x1, y1 = pos[succ]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

    node_x = [pos[t][0] for t in g.tasks]
    node_y = [pos[t][1] for t in g.tasks]
    node_color = [g.tasks[t]["duration"] for t in g.tasks]
    node_text = [
        f"<b>{t}</b><br>{g.tasks[t]['name']}<br>{g.tasks[t]['duration']}s"
        for t in g.tasks
    ]

    fig = go.Figure()
    # Edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(color="rgba(148,163,184,0.3)", width=2),
        hoverinfo="none", showlegend=False
    ))
    # Nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=list(g.tasks.keys()), textposition="middle center",
        hovertext=node_text, hoverinfo="text",
        marker=dict(
            size=38, color=node_color, colorscale="Viridis", showscale=True,
            colorbar=dict(title="Duration (s)", thickness=10, len=0.8),
            line=dict(width=2, color=C["bg"])
        ),
        textfont=dict(color="white", size=11, weight="bold"), showlegend=False
    ))
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_layout(
        title=dict(text="Task Precedence Graph (DAG)", font=dict(size=14)),
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        height=400, margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def generate_excel_export(metrics, stations, energy, jes_all, ct, algo):
    """Generate in-memory Excel file with multiple sheets."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # 1. Summary
        pd.DataFrame([{
            "Algorithm": algo, "Cycle Time (s)": ct,
            "Efficiency (%)": metrics["line_efficiency"],
            "Stations": metrics["num_stations"],
            "Theoretical Min": metrics["theoretical_min_stations"],
            "Smoothness Index": metrics["smoothness_index"]
        }]).to_excel(writer, sheet_name="Summary", index=False)
        
        # 2. Stations
        st_data = []
        for s in stations:
            for t in s["task_details"]:
                st_data.append({
                    "Station": s["station_id"], "Task ID": t["id"],
                    "Task Name": t["name"], "Duration (s)": t["duration"]
                })
        pd.DataFrame(st_data).to_excel(writer, sheet_name="Stations", index=False)
        
        # 3. Energy
        pd.DataFrame([{
            "Station": d.station_id, "Idle Time (s)": d.idle_time,
            "Energy (kWh)": d.energy_kwh, "Cost ($)": d.cost, "CO2 (kg)": d.co2_kg
        } for d in energy.per_station]).to_excel(writer, sheet_name="Energy", index=False)

        # 4. JES
        jes_data = []
        for sid, jes in jes_all.items():
            for step in jes["steps"]:
                jes_data.append({
                    "Station": sid, "Step": step["step"],
                    "Task ID": step["task_id"], "Task Name": step["task_name"],
                    "Duration": step["duration"], "Cumulative Time": step["cumulative_time"],
                    "Key Points": step["key_points"]
                })
        pd.DataFrame(jes_data).to_excel(writer, sheet_name="JES Works Instructions", index=False)
    return output.getvalue()
