<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" />
</p>

<h1 align="center">🏭 Manufacture Balance 4.0</h1>

<p align="center">
  <strong>Sustainable Lean Manufacturing · Assembly Line Balancing · Operator 4.0</strong><br/>
  An academically grounded, sustainability-focused, end-to-end <em>decision support system</em><br/>that includes the operator perspective.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-csv-format">CSV Format</a> •
  <a href="#-algorithms">Algorithms</a> •
  <a href="#-metrics">Metrics</a> •
  <a href="#-academic-references">References</a>
</p>

---

> [!WARNING]
> **Beta Software** — This application is under active development and is not yet ready for production use. Features may change without notice.

---

## ✨ Features

| Tab | Feature | Description |
|-----|---------|-------------|
| 📥 **Data Input** | CSV / Upload / Manual | Load tasks from sample data, upload your own CSV, or enter manually |
| 📥 **Data Input** | DAG Visualization | Interactive precedence graph with color-coded task durations |
| 📊 **Results** | RPW Solver | Ranked Positional Weight line balancing (Helgeson & Birnie, 1961) |
| 📊 **Results** | Greedy Solver | Largest Candidate Rule heuristic |
| 📊 **Results** | Side-by-Side Compare | Run both algorithms and compare results instantly |
| 📊 **Results** | Kaizen Simulator | Takt time slider with instant recalculation |
| 📊 **Results** | Excel Export | Download comprehensive `.xlsx` report with all results |
| 👷 **Operator JES** | Digital Work Instructions | Station-level step-by-step instructions (Operator 4.0) |
| 🌿 **Sustainability** | 9th Waste Analysis | Energy waste (kWh), cost ($), CO₂ footprint (kg) from idle time |
| ⚖️ **Compare** | Scenario Management | Save, load, and compare scenarios side-by-side with SQLite |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Local Installation

```bash
# Clone the repository
git clone https://github.com/radikonreturn/manufacture-balance.git
cd manufacture-balance

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python -m streamlit run app.py
```

Open your browser at **http://localhost:8501**

### Docker

```bash
docker-compose up --build
```

## 🏗️ Architecture

```
manufacture-balance/
│
├── app.py                    # Main entry point (90 lines)
│
├── ui/                       # 🎨 UI Layer
│   ├── styles.py             #    Theme, colors, CSS
│   ├── components.py         #    Reusable widgets (metric cards, DAG, Excel export)
│   └── tabs/                 #    One module per tab
│       ├── input_tab.py      #      📥 Data Input
│       ├── results_tab.py    #      📊 Results & Visualization
│       ├── operator_tab.py   #      👷 Digital Operator (JES)
│       ├── sustainability_tab.py  #  🌿 Sustainability Report
│       └── compare_tab.py    #      ⚖️ Scenario Comparison
│
├── engine/                   # ⚙️ ALB Engine
│   ├── graph.py              #    Precedence DAG (Directed Acyclic Graph)
│   ├── rpw_solver.py         #    Ranked Positional Weight algorithm
│   ├── greedy_solver.py      #    Largest Candidate Rule algorithm
│   ├── metrics.py            #    Line balancing performance metrics
│   ├── energy_waste.py       #    9th Waste energy calculator
│   └── jes_generator.py      #    Electronic Job Element Sheet generator
│
├── data/                     # 💾 Data Layer
│   ├── parser.py             #    CSV parsing & validation
│   └── database.py           #    SQLite scenario persistence
│
├── tests/                    # 🧪 Test Suite
│   └── test_engine.py        #    22 unit + integration tests
│
├── sample_tasks.csv          # 10-task sample dataset
├── sample_20_tasks.csv       # 20-task sample dataset
├── sample_30_tasks.csv       # 30-task sample dataset
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build
└── docker-compose.yml        # Container orchestration
```

## 📄 CSV Format

```csv
task_id,task_name,duration,predecessors
T1,Body Cutting,6,
T2,Hole Drilling,4,T1
T3,Bending,3,T1
T4,Welding A,5,T2
T5,Welding B,4,T2 T3
```

| Column | Type | Description |
|--------|------|-------------|
| `task_id` | `string` | Unique task identifier (e.g. `T1`, `OP_05`) |
| `task_name` | `string` | Human-readable task name |
| `duration` | `float` | Task duration in seconds (must be > 0) |
| `predecessors` | `string` | Space-separated predecessor IDs (empty = no dependencies) |

## ⚙️ Algorithms

### RPW — Ranked Positional Weight

Based on **Helgeson & Birnie (1961)**, the classic line balancing heuristic:

1. Compute each task's RPW = own duration + longest successor path
2. Sort tasks by descending RPW
3. Assign to stations respecting cycle time and precedence constraints

### Greedy — Largest Candidate Rule

A simpler heuristic that prioritizes larger tasks:

1. Sort tasks by descending duration
2. For each station, assign the largest eligible task (precedence + capacity OK)
3. Open a new station when no more tasks fit

## 📊 Metrics

| Metric | Formula | Perfect Score |
|--------|---------|---------------|
| **Line Efficiency** | Σ(station loads) / (n × CT) × 100 | 100% |
| **Balance Delay** | 100 − Line Efficiency | 0% |
| **Smoothness Index** | √Σ(ST_max − ST_i)² | 0.0 |
| **Theoretical Min Stations** | ⌈Total Work / CT⌉ | — |
| **Bottleneck Score** | (station load / CT) × 100 | < 90% |
| **Energy Waste** | idle_time × kW/3600 | 0 kWh |
| **Carbon Footprint** | energy_waste × CO₂ factor | 0 kg |

## 🧪 Testing

```bash
# Run all 22 tests
python -m pytest tests/ -v

# Lint check (requires ruff)
python -m ruff check . --exclude=".venv,__pycache__"
```

## 📚 Academic References

1. **Helgeson, W.B. & Birnie, D.P. (1961)**. *Assembly line balancing using the ranked positional weight technique.* — RPW algorithm foundation

2. **Ciliberto, C. et al. (2021)**. *Exploring lean and green supply chain integration.* — "9th Waste" energy waste concept in sustainable manufacturing

3. **Ciano, M.P. et al. (2021)**. *One-to-one relationships between Industry 4.0 technologies and Lean production principles.* — Operator 4.0 and digital JES integration

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with ❤️ for sustainable manufacturing</sub>
</p>
