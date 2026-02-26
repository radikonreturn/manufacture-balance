
with open('app.py', 'r') as f:
    content = f.read()

# 1. Replace CSS
old_css_start = "#  CSS — Premium Dark Industrial Theme"
old_css_end = "</style>\n\"\"\""

new_css = """#  CSS — Manufacture Balance 4.0 Theme (Fira Sans & Fira Code)
# ------------------------------------------------------------------ #
st.markdown(\"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');

    .stApp {
        font-family: 'Fira Sans', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Metric cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-family: 'Fira Code', monospace;
        font-size: 2.25rem;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.05em;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* JES step card */
    .jes-step {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s ease;
    }
    .jes-step:hover {
        background: rgba(30, 41, 59, 0.8);
        border-left-color: #818cf8;
    }
    .jes-step-header {
        font-family: 'Fira Sans', sans-serif;
        font-weight: 600;
        color: #f8fafc;
        font-size: 1.1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .jes-step-time {
        font-family: 'Fira Code', monospace;
        color: #818cf8;
        font-weight: 500;
        font-size: 1rem;
    }
    .jes-step-detail {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        font-family: 'Fira Code', monospace;
    }

    /* Sustainability card */
    .sustain-card {
        background: rgba(6, 78, 59, 0.3);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .sustain-card:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.5);
    }
    .sustain-value {
        font-family: 'Fira Code', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #10b981;
    }
    .sustain-label {
        font-size: 0.875rem;
        color: #a7f3d0;
        margin-top: 0.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Fira Code', monospace;
        letter-spacing: 0.025em;
    }
    .badge-green { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-yellow { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-red { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }
    .badge-orange { background: rgba(249, 115, 22, 0.1); color: #fb923c; border: 1px solid rgba(249, 115, 22, 0.2); }
    .badge-indigo { background: rgba(99, 102, 241, 0.1); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.2); }

    /* Section header */
    .section-header {
        font-family: 'Fira Sans', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #f8fafc;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Streamlit overrides */
    div[data-testid="stTabs"] button {
        font-family: 'Fira Sans', sans-serif;
        font-weight: 500;
        color: #94a3b8;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* Progress bar track */
    .progress-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 9999px;
        margin-top: 0.75rem;
        padding: 2px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
</style>
\"\"\""""

start_idx = content.find(old_css_start)
end_idx = content.find(old_css_end) + len(old_css_end)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_css + content[end_idx:]

# 2. Update JES loop
old_jes_loop = '''            for step in jes["steps"]:
                progress_pct = round((step["cumulative_time"] / jes["cycle_time"]) * 100, 1)

                st.markdown(f"""
                <div class="jes-step">
                    <div class="jes-step-header">
                        Adım {step['step']}: {step['task_name']}
                        <span style="float:right; color:#818cf8;">⏱️ {step['duration']} sn</span>
                    </div>
                    <div class="jes-step-detail">
                        Görev ID: <code>{step['task_id']}</code> · 
                        Kümülatif: {step['cumulative_time']}/{jes['cycle_time']} sn · 
                        Kalan: {step['remaining_time']} sn
                    </div>
                    <div style="background:#0f172a; border-radius:4px; margin-top:0.5rem; padding:2px;">
                        <div style="width:{progress_pct}%; background:linear-gradient(90deg, #6366f1, #818cf8); 
                             height:5px; border-radius:3px;"></div>
                    </div>
                    {"<div style='color:#fbbf24; font-size:0.8rem; margin-top:0.3rem;'>📌 " + step['key_points'] + "</div>" if step['key_points'] else ""}
                </div>
                """, unsafe_allow_html=True)'''

new_jes_loop = '''            for step in jes["steps"]:
                progress_pct = round((step["cumulative_time"] / jes["cycle_time"]) * 100, 1)
                
                # Sanitize user-controlled fields for HTML rendering
                safe_task_name = html.escape(str(step['task_name']))
                safe_task_id = html.escape(str(step['task_id']))
                safe_key_points = html.escape(str(step['key_points']))

                st.markdown(f"""
                <div class="jes-step">
                    <div class="jes-step-header">
                        <span>Adım {step['step']}: {safe_task_name}</span>
                        <span class="jes-step-time">⏱️ {step['duration']} sn</span>
                    </div>
                    <div class="jes-step-detail">
                        <span>Görev ID: {safe_task_id}</span> | 
                        <span>Kümülatif: {step['cumulative_time']}/{jes['cycle_time']} sn</span> | 
                        <span>Kalan: {step['remaining_time']} sn</span>
                    </div>
                    <div class="progress-track">
                        <div style="width:{progress_pct}%; background:linear-gradient(90deg, #6366f1, #818cf8); 
                             height:6px; border-radius:9999px; transition: width 0.5s;"></div>
                    </div>
                    {"<div style='color:#fb923c; font-size:0.85rem; margin-top:0.5rem; font-family: \\"Fira Sans\\", sans-serif;'>📌 " + safe_key_points + "</div>" if safe_key_points else ""}
                </div>
                """, unsafe_allow_html=True)'''

content = content.replace(old_jes_loop, new_jes_loop)

# 3. Update Font families in Plotly Charts
content = content.replace('font=dict(family="Inter", color="#e2e8f0"),', 'font=dict(family="Fira Sans", color="#f8fafc"),')

# 4. Color logic adjustments
content = content.replace('color = "#34d399" if eff >= 80 else "#fbbf24" if eff >= 60 else "#f87171"', 'color = "#10b981" if eff >= 80 else "#fbbf24" if eff >= 60 else "#f87171"')
content = content.replace('color="#34d399"', 'color="#10b981"') # Replace emerald colors

with open('app.py', 'w') as f:
    f.write(content)

print("UI Refactoring Applied Successfully.")
