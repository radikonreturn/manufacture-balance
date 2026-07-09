import streamlit as st

C = {
    "bg":       "#090a0f",
    "card":     "#121520",
    "card2":    "#1c2030",
    "primary":  "#00f0ff",
    "primary2": "#38bdf8",
    "success":  "#10b981",
    "success2": "#34d399",
    "warning":  "#fbbf24",
    "danger":   "#ef4444",
    "info":     "#38bdf8",
    "text":     "#f4f4f5",
    "muted":    "#71717a",
    "border":   "#202738",
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
    xaxis=dict(gridcolor="rgba(32,39,56,0.5)", zerolinecolor="rgba(32,39,56,0.5)"),
    yaxis=dict(gridcolor="rgba(32,39,56,0.5)", zerolinecolor="rgba(32,39,56,0.5)"),
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
    .main .block-container {{ padding:1.5rem 2rem 2rem; max-width:1400px; }}
    ::-webkit-scrollbar {{ width:4px; height:4px; }}
    ::-webkit-scrollbar-track {{ background:var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background:var(--card2); border-radius:0px; }}
    ::-webkit-scrollbar-thumb:hover {{ background:var(--pri); }}
    
    section[data-testid="stSidebar"] {{
        background: #090a0f;
        border-right:1px solid var(--bdr);
    }}
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        font-family:'Fira Code',monospace; font-size:0.75rem; color:var(--muted);
        text-transform:uppercase; letter-spacing:0.15em; margin:1.5rem 0 0.75rem;
    }}
    
    /* Engineering Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: transparent;
        border-bottom: 2px solid var(--bdr);
        padding: 0;
    }}
    .stTabs [data-baseweb="tab"] {{
        padding: 0.6rem 1.25rem !important;
        background: var(--card) !important;
        border: 1px solid var(--bdr) !important;
        border-bottom: none !important;
        border-radius: 0px !important;
        color: var(--muted) !important;
        font-family: 'Fira Code', monospace !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.2s;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        color: var(--txt) !important;
        background: var(--card2) !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: var(--pri) !important;
        background: var(--card2) !important;
        border-top: 2px solid var(--pri) !important;
        font-weight: 700 !important;
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}
    
    /* Instrument Metrics Cards */
    .mc {{
        background:var(--card); border:1px solid var(--bdr); border-left:3px solid var(--pri);
        border-radius:0px; padding:1.25rem 1rem; text-align:left; transition:all .2s ease;
    }}
    .mc:hover {{ border-color:var(--pri); background:var(--card2); }}
    .mc .v {{ font-family:'Fira Code',monospace; font-size:2rem; font-weight:700; line-height:1; color:var(--txt); margin-bottom:.35rem; }}
    .mc .l {{ font-size:.65rem; color:var(--muted); font-weight:600; text-transform:uppercase; letter-spacing:.1em; }}
    
    /* JES step card */
    .js {{
        background:var(--card); border:1px solid var(--bdr); border-left:3px solid var(--pri);
        border-radius:0px; padding:1.1rem; margin-bottom:.75rem; position:relative; overflow:hidden; transition:all .2s ease;
    }}
    .js:hover {{ background:var(--card2); border-color:var(--pri); }}
    .js .h {{ display:flex; justify-content:space-between; align-items:center; font-weight:600; color:var(--txt); font-size:0.95rem; margin-bottom:.5rem; }}
    .js .t {{ font-family:'Fira Code',monospace; color:var(--pri); font-weight:600; font-size:.8rem; background:rgba(0,240,255,.06); border:1px solid rgba(0,240,255,.15); padding:.15rem .5rem; border-radius:0px; }}
    .js .d {{ color:var(--muted); font-size:.78rem; font-family:'Fira Code',monospace; display:flex; gap:.75rem; flex-wrap:wrap; }}
    .js .d code {{ background:rgba(255,255,255,.04); color:var(--txt); padding:1px 6px; border-radius:0px; font-size:.78rem; border:1px solid rgba(255,255,255,0.05); }}
    
    /* Sustainability Cards */
    .sc {{
        background:var(--card); border:1px solid var(--bdr); border-left:3px solid var(--ok);
        border-radius:0px; padding:1.25rem 1rem; text-align:left; transition:all .2s ease;
    }}
    .sc:hover {{ border-color:var(--ok); background:var(--card2); }}
    .sc .ico {{ font-size:1.5rem; margin-bottom:.5rem; }}
    .sc .v {{ font-family:'Fira Code',monospace; font-size:2rem; font-weight:700; color:var(--ok); margin:.25rem 0; }}
    .sc .l {{ font-size:.65rem; color:var(--muted); font-weight:600; text-transform:uppercase; letter-spacing:.1em; }}
    
    /* Badges */
    .b {{ display:inline-flex; align-items:center; padding:.25rem .55rem; border-radius:0px; font-size:.65rem; font-weight:600; font-family:'Fira Code',monospace; letter-spacing:.05em; text-transform:uppercase; }}
    .b-g {{ background:rgba(16,185,129,.06); color:#34d399; border:1px solid rgba(16,185,129,.2); }}
    .b-y {{ background:rgba(245,158,11,.06); color:#fbbf24; border:1px solid rgba(245,158,11,.2); }}
    .b-r {{ background:rgba(239,68,68,.06); color:#f87171; border:1px solid rgba(239,68,68,.2); }}
    .b-i {{ background:rgba(0,240,255,.06); color:#38bdf8; border:1px solid rgba(0,240,255,.2); }}
    .b-p {{ background:rgba(168,85,247,.06); color:#c084fc; border:1px solid rgba(168,85,247,.2); }}
    
    /* Section Headers */
    .sh {{ font-family:'Fira Code',monospace; font-size:1.1rem; font-weight:600; color:var(--txt); padding-bottom:.5rem; border-bottom:1px solid var(--bdr); margin:1.5rem 0 1.25rem; display:flex; align-items:center; gap:.5rem; }}
    
    /* Progress Bars */
    .pt {{ background:rgba(255,255,255,.04); border-radius:0px; height:4px; overflow:hidden; margin:.5rem 0; }}
    .pb {{ height:100%; border-radius:0px; transition:width .5s cubic-bezier(.4,0,.2,1); }}
    
    /* Bottleneck Cards */
    .bn {{ text-align:center; background:var(--card); padding:1rem .5rem; border-radius:0px; border:1px solid var(--bdr); }}
    .bn .sid {{ font-weight:600; color:var(--muted); font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; margin-bottom:.3rem; }}
    .bn .pct {{ font-size:1.35rem; font-family:'Fira Code',monospace; font-weight:700; color:var(--txt); margin-bottom:.4rem; }}
    
    .ft {{ text-align:center; color:#52525b; font-size:.7rem; padding:2rem 0 .5rem; font-family:'Fira Code',monospace; letter-spacing:.05em; border-top:1px solid var(--bdr); margin-top:2rem; }}
    
    /* Form Label Styling */
    .stSelectbox label, .stSlider label, .stNumberInput label, .stRadio label, .stFileUploader label {{ font-family:'Fira Code',monospace !important; font-size:.8rem !important; color:var(--muted) !important; text-transform:uppercase !important; letter-spacing:0.05em !important; }}
    
    /* Button overrides */
    button[data-testid="stBaseButton-primary"] {{ background:var(--pri) !important; color:#090a0f !important; border:none !important; border-radius:0px !important; font-weight:700 !important; font-family:'Fira Code',monospace !important; text-transform:uppercase !important; letter-spacing:0.05em !important; }}
    button[data-testid="stBaseButton-secondary"] {{ border-radius:0px !important; font-family:'Fira Code',monospace !important; }}
    div[data-testid="stForm"] {{ border-radius:0px !important; border-color:var(--bdr) !important; }}
    </style>
    """, unsafe_allow_html=True)
