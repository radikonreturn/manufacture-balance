import streamlit as st

C = {
    "bg":       "#020617",
    "card":     "#0f172a",
    "card2":    "#1e293b",
    "primary":  "#6366f1",
    "primary2": "#818cf8",
    "success":  "#22c55e",
    "success2": "#4ade80",
    "warning":  "#f59e0b",
    "danger":   "#ef4444",
    "info":     "#38bdf8",
    "text":     "#f8fafc",
    "muted":    "#94a3b8",
    "border":   "rgba(148,163,184,0.08)",
}

PLOTLY_LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Fira Code, monospace", color=C["text"], size=12),
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
        font=dict(size=11), bgcolor="rgba(0,0,0,0)",
    ),
    xaxis=dict(gridcolor="rgba(148,163,184,0.06)", zerolinecolor="rgba(148,163,184,0.06)"),
    yaxis=dict(gridcolor="rgba(148,163,184,0.06)", zerolinecolor="rgba(148,163,184,0.06)"),
)

def apply_styles():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {{
        --bg: {C["bg"]}; --card: {C["card"]}; --card2: {C["card2"]};
        --pri: {C["primary"]}; --pri2: {C["primary2"]};
        --ok: {C["success"]}; --ok2: {C["success2"]};
        --warn: {C["warning"]}; --err: {C["danger"]};
        --txt: {C["text"]}; --muted: {C["muted"]};
        --bdr: {C["border"]};
    }}
    .stApp {{ font-family:'Inter',sans-serif; background:var(--bg); color:var(--txt); }}
    .main .block-container {{ padding:1.5rem 2rem 2rem; max-width:1300px; }}
    ::-webkit-scrollbar {{ width:6px; height:6px; }}
    ::-webkit-scrollbar-track {{ background:transparent; }}
    ::-webkit-scrollbar-thumb {{ background:var(--card2); border-radius:3px; }}
    ::-webkit-scrollbar-thumb:hover {{ background:var(--pri); }}
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #010313 0%, #0a0e27 100%);
        border-right:1px solid var(--bdr);
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        font-family:'Fira Code',monospace; font-size:0.75rem; color:var(--muted);
        text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.75rem;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap:0; background:transparent; border-bottom:1px solid var(--bdr); padding:0; }}
    .stTabs [data-baseweb="tab"] {{
        padding:0.85rem 1.25rem; background:transparent !important; border:none !important;
        color:var(--muted) !important; font-weight:500 !important; font-size:0.95rem !important; transition:color 0.2s;
    }}
    .stTabs [data-baseweb="tab"]:hover {{ color:var(--txt) !important; }}
    .stTabs [aria-selected="true"] {{ color:var(--pri) !important; font-weight:700 !important; }}
    .stTabs [data-baseweb="tab-highlight"] {{ background:var(--pri) !important; height:2px !important; }}
    .mc {{
        background:var(--card); border:1px solid var(--bdr); border-radius:14px;
        padding:1.5rem 1rem; text-align:center; transition:all .25s cubic-bezier(.4,0,.2,1);
    }}
    .mc:hover {{ transform:translateY(-3px); border-color:rgba(99,102,241,.35); box-shadow:0 12px 28px rgba(0,0,0,.25); }}
    .mc .v {{ font-family:'Fira Code',monospace; font-size:2.2rem; font-weight:700; line-height:1; margin-bottom:.35rem; }}
    .mc .l {{ font-size:.65rem; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:.12em; }}
    .js {{
        background:var(--card); border:1px solid var(--bdr); border-radius:12px;
        padding:1.25rem 1.25rem 1.25rem 1.5rem; margin-bottom:.75rem; position:relative; overflow:hidden; transition:all .2s ease;
    }}
    .js::before {{ content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--pri); border-radius:0 2px 2px 0; }}
    .js:hover {{ background:var(--card2); border-color:rgba(99,102,241,.25); }}
    .js .h {{ display:flex; justify-content:space-between; align-items:center; font-weight:600; color:var(--txt); font-size:1rem; margin-bottom:.6rem; }}
    .js .t {{ font-family:'Fira Code',monospace; color:var(--pri); font-weight:600; font-size:.85rem; background:rgba(99,102,241,.08); padding:.2rem .65rem; border-radius:6px; }}
    .js .d {{ color:var(--muted); font-size:.8rem; font-family:'Fira Code',monospace; display:flex; gap:.75rem; flex-wrap:wrap; }}
    .js .d code {{ background:rgba(255,255,255,.04); color:var(--txt); padding:1px 6px; border-radius:4px; font-size:.8rem; }}
    .sc {{ background:linear-gradient(145deg, rgba(6,78,59,.3), rgba(2,6,23,.5)); border:1px solid rgba(34,197,94,.15); border-radius:14px; padding:1.75rem 1rem; text-align:center; transition:all .3s ease; }}
    .sc:hover {{ transform:scale(1.02); border-color:rgba(34,197,94,.4); }}
    .sc .ico {{ font-size:2rem; margin-bottom:.75rem; }}
    .sc .v {{ font-family:'Fira Code',monospace; font-size:2.4rem; font-weight:700; color:var(--ok); margin:.25rem 0; }}
    .sc .l {{ font-size:.65rem; color:#a7f3d0; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }}
    .b {{ display:inline-flex; align-items:center; padding:.3rem .7rem; border-radius:6px; font-size:.65rem; font-weight:700; font-family:'Fira Code',monospace; letter-spacing:.06em; text-transform:uppercase; }}
    .b-g {{ background:rgba(34,197,94,.08); color:#4ade80; border:1px solid rgba(34,197,94,.18); }}
    .b-y {{ background:rgba(245,158,11,.08); color:#fbbf24; border:1px solid rgba(245,158,11,.18); }}
    .b-r {{ background:rgba(239,68,68,.08); color:#f87171; border:1px solid rgba(239,68,68,.18); }}
    .b-i {{ background:rgba(99,102,241,.08); color:#818cf8; border:1px solid rgba(99,102,241,.18); }}
    .b-p {{ background:rgba(168,85,247,.08); color:#c084fc; border:1px solid rgba(168,85,247,.18); }}
    .sh {{ font-family:'Fira Code',monospace; font-size:1.25rem; font-weight:700; color:var(--txt); padding-bottom:.6rem; border-bottom:1px solid var(--bdr); margin:1.75rem 0 1.5rem; display:flex; align-items:center; gap:.6rem; }}
    .pt {{ background:rgba(255,255,255,.04); border-radius:99px; height:5px; overflow:hidden; margin:.6rem 0; }}
    .pb {{ height:100%; border-radius:99px; transition:width .5s cubic-bezier(.4,0,.2,1); }}
    .bn {{ text-align:center; background:var(--card); padding:1.25rem .5rem; border-radius:12px; border:1px solid var(--bdr); }}
    .bn .sid {{ font-weight:700; color:var(--muted); font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:.4rem; }}
    .bn .pct {{ font-size:1.5rem; font-family:'Fira Code',monospace; font-weight:700; color:var(--txt); margin-bottom:.5rem; }}
    .ft {{ text-align:center; color:#475569; font-size:.72rem; padding:2rem 0 .5rem; font-family:'Fira Code',monospace; letter-spacing:.03em; }}
    .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label, .stFileUploader label {{ font-size:.85rem !important; color:var(--muted) !important; }}
    button[data-testid="stBaseButton-primary"] {{ background:var(--pri) !important; border:none !important; border-radius:8px !important; font-weight:600 !important; }}
    </style>
    """, unsafe_allow_html=True)
