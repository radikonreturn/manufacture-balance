"""
server.py — Manufacture Balance 4.0
Flask web server replacing Streamlit.
Engine and data modules are reused unchanged.

Run: python server.py
Open: http://localhost:5000
"""

import os
import io
import json
import traceback

from flask import Flask, request, jsonify, send_file, render_template

from data.database import init_db, save_scenario, list_scenarios, load_scenario
from data.parser import parse_csv
from engine.graph import PrecedenceGraph
from engine.rpw_solver import solve_rpw
from engine.greedy_solver import solve_greedy
from engine.metrics import compute_all_metrics
from engine.energy_waste import calculate_energy_waste
from engine.jes_generator import generate_jes, format_jes_markdown
from ui.components import generate_excel_export

app = Flask(__name__)

# ── Init DB on startup ────────────────────────────────────────── #
init_db()


# ── Helpers ───────────────────────────────────────────────────── #

def _df_to_json(df):
    return df.to_dict(orient="records")


def _build_graph(tasks_data):
    """Rebuild a PrecedenceGraph from a list of task dicts."""
    import pandas as pd
    df = pd.DataFrame(tasks_data)
    g = PrecedenceGraph()
    g.load_from_dataframe(df)
    return g


def _graph_summary(g):
    s = g.summary()
    return {
        "task_count": s["task_count"],
        "total_work_content": s["total_work_content"],
        "entry_tasks": s["entry_tasks"],
        "exit_tasks": s["exit_tasks"],
    }


def _dag_traces(g):
    """Return Plotly trace data for the DAG chart."""
    from collections import defaultdict
    try:
        order = g.topological_sort()
    except Exception:
        return [], []

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
    node_labels = list(g.tasks.keys())

    return {
        "edge_x": edge_x,
        "edge_y": edge_y,
        "node_x": node_x,
        "node_y": node_y,
        "node_color": node_color,
        "node_text": node_text,
        "node_labels": node_labels,
    }


# ── Routes ────────────────────────────────────────────────────── #

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/sample", methods=["GET"])
def api_sample():
    """Load sample_tasks.csv and return parsed task data."""
    try:
        df = parse_csv("sample_tasks.csv")
        g = PrecedenceGraph()
        g.load_from_dataframe(df)
        return jsonify({
            "ok": True,
            "tasks": _df_to_json(df),
            "summary": _graph_summary(g),
            "dag": _dag_traces(g),
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/upload", methods=["POST"])
def api_upload():
    """Parse an uploaded CSV file and return task data + graph summary."""
    try:
        if "file" in request.files:
            f = request.files["file"]
            df = parse_csv(io.BytesIO(f.read()))
        elif request.is_json:
            # Manual entry: receive tasks as JSON
            body = request.get_json()
            import pandas as pd
            df = pd.DataFrame(body["tasks"])
            from data.parser import parse_csv as _parse
            df = _parse(io.StringIO(df.to_csv(index=False)))
        else:
            return jsonify({"ok": False, "error": "No file or JSON body"}), 400

        g = PrecedenceGraph()
        g.load_from_dataframe(df)
        return jsonify({
            "ok": True,
            "tasks": _df_to_json(df),
            "summary": _graph_summary(g),
            "dag": _dag_traces(g),
        })
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/solve", methods=["POST"])
def api_solve():
    """Run line-balancing solver(s) on the provided tasks."""
    try:
        body = request.get_json()
        tasks_data    = body["tasks"]
        cycle_time    = float(body["cycle_time"])
        algorithm     = body.get("algorithm", "rpw")   # rpw | greedy | compare
        kwh_per_sec   = float(body.get("kwh_per_sec",   0.002))
        cost_per_kwh  = float(body.get("cost_per_kwh",  2.5))
        co2_factor    = float(body.get("co2_factor",    0.47))

        g = _build_graph(tasks_data)
        algo_map = {"rpw": ["rpw"], "greedy": ["greedy"], "compare": ["rpw", "greedy"]}
        algos = algo_map.get(algorithm, ["rpw"])

        results = []
        for algo in algos:
            stations = solve_rpw(g, cycle_time) if algo == "rpw" else solve_greedy(g, cycle_time)
            metrics  = compute_all_metrics(stations, cycle_time, g.total_work_content())
            energy   = calculate_energy_waste(stations, cycle_time, kwh_per_sec, cost_per_kwh, co2_factor)
            jes_all  = generate_jes(stations, cycle_time)

            # Serialise JES (keys are int station ids → convert to str for JSON)
            jes_json = {}
            for sid, jes in jes_all.items():
                jes_json[str(sid)] = jes

            results.append({
                "algo":     algo.upper(),
                "stations": stations,
                "metrics":  metrics,
                "energy":   energy.to_dict(),
                "jes":      jes_json,
            })

        return jsonify({"ok": True, "results": results})

    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/scenarios", methods=["GET"])
def api_list_scenarios():
    try:
        return jsonify({"ok": True, "scenarios": list_scenarios()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/scenarios", methods=["POST"])
def api_save_scenario():
    try:
        body         = request.get_json()
        name         = body["name"]
        cycle_time   = float(body["cycle_time"])
        algorithm    = body["algorithm"]
        tasks_data   = body["tasks"]
        metrics      = body["metrics"]
        stations     = body["stations"]
        energy_dict  = body.get("energy", {})

        sid = save_scenario(name, cycle_time, algorithm, tasks_data, metrics, stations, energy_dict)
        return jsonify({"ok": True, "id": sid})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/scenarios/<int:scenario_id>", methods=["GET"])
def api_load_scenario(scenario_id):
    try:
        sc = load_scenario(scenario_id)
        if not sc:
            return jsonify({"ok": False, "error": "Not found"}), 404
        return jsonify({"ok": True, "scenario": sc})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/export", methods=["POST"])
def api_export():
    """Generate and return an Excel report as a file download."""
    try:
        body       = request.get_json()
        metrics    = body["metrics"]
        stations   = body["stations"]
        energy_d   = body["energy"]
        cycle_time = float(body["cycle_time"])
        algo       = body["algo"]

        # Reconstruct energy object from dict for generate_excel_export
        from engine.energy_waste import EnergyReport, StationEnergyDetail
        per_station = [
            StationEnergyDetail(
                station_id=s["station_id"],
                idle_time=s["idle_time"],
                energy_kwh=s["energy_kwh"],
                cost=s["cost"],
                co2_kg=s["co2_kg"],
            )
            for s in energy_d["per_station"]
        ]
        energy = EnergyReport(
            total_idle_time=energy_d["total_idle_time"],
            total_energy_kwh=energy_d["total_energy_kwh"],
            total_cost=energy_d["total_cost"],
            total_co2_kg=energy_d["total_co2_kg"],
            per_station=per_station,
        )

        g_tmp = _build_graph(body["tasks"])
        jes_all = generate_jes(stations, cycle_time)
        excel_bytes = generate_excel_export(metrics, stations, energy, jes_all, cycle_time, algo)

        return send_file(
            io.BytesIO(excel_bytes),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"Report_{algo}_CT{cycle_time}.xlsx",
        )
    except Exception as e:
        traceback.print_exc()
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/api/jes_markdown", methods=["POST"])
def api_jes_markdown():
    """Return JES markdown text for a single station."""
    try:
        body = request.get_json()
        jes_data = body["jes"]
        md = format_jes_markdown(jes_data)
        return jsonify({"ok": True, "markdown": md})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ── Entry point ───────────────────────────────────────────────── #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
