"""
ROI Lens — Streamlit Dashboard  (clean rewrite, all bugs fixed)
Mistral Worldwide Hackathon 2026
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import asyncio, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from database import init_db, get_db
from advanced_features import BudgetGuardian, PromptOptimizer, ABTester, ROIForecaster, AnomalyDetector
from power_features import SmartPromptLibrary, CostOptimizer, WorkflowHealthScore, TeamROIDashboard
from mistral_wrapper import MistralWrapper
from roi_engine import ROIEngine

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ROI Lens — AI Accountability",
    page_icon="🔬", layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PALETTE ──────────────────────────────────────────────────────────────────
BG      = "#07080a"
SURF    = "#0e1117"
SURF2   = "#13161f"
BORDER  = "#1e2530"
GREEN   = "#00e5a0"
BLUE    = "#4d9fff"
RED     = "#ff4d6d"
WARN    = "#ffb84d"
TEXT    = "#e8eaf2"
MUTED   = "#5a6070"
MUTED2  = "#8890a0"

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');
html,body,[class*="css"]{{font-family:'Syne',sans-serif!important;background:{BG}!important;color:{TEXT}!important}}
.stApp{{background:{BG}}}
.block-container{{padding-top:1.2rem!important}}

/* Sidebar */
section[data-testid="stSidebar"]{{background:{SURF}!important;border-right:1px solid {BORDER}!important}}
section[data-testid="stSidebar"] *{{color:{TEXT}!important}}
section[data-testid="stSidebar"] input{{background:{SURF2}!important;color:{TEXT}!important;border:1px solid {BORDER}!important;border-radius:2px!important;font-family:'Space Mono',monospace!important;font-size:11px!important}}
section[data-testid="stSidebar"] label{{color:{MUTED2}!important;font-size:10px!important;font-family:'Space Mono',monospace!important;letter-spacing:0.1em!important;text-transform:uppercase!important}}
section[data-testid="stSidebar"] hr{{border-color:{BORDER}!important}}

/* Tabs — nuclear override for all Streamlit versions */
button[data-baseweb="tab"]{{
    font-family:'Space Mono',monospace!important;
    font-size:12px!important;
    font-weight:700!important;
    letter-spacing:0.08em!important;
    text-transform:uppercase!important;
    color:{TEXT}!important;
    background:transparent!important;
    border:none!important;
    border-radius:0!important;
    padding:14px 22px!important;
    white-space:nowrap!important;
    opacity:1!important;
}}
button[data-baseweb="tab"] *{{
    color:{TEXT}!important;
    font-family:'Space Mono',monospace!important;
    font-size:12px!important;
    font-weight:700!important;
    opacity:1!important;
}}
button[data-baseweb="tab"][aria-selected="true"]{{
    color:{GREEN}!important;
    border-bottom:3px solid {GREEN}!important;
    background:rgba(0,229,160,0.06)!important;
}}
button[data-baseweb="tab"][aria-selected="true"] *{{
    color:{GREEN}!important;
}}
div[data-baseweb="tab-list"]{{
    background:{SURF}!important;
    border-bottom:1px solid {BORDER}!important;
    gap:0!important;
    overflow-x:auto!important;
    padding:0!important;
}}
div[data-baseweb="tab-border"]{{display:none!important}}
div[data-baseweb="tab-highlight"]{{background:{GREEN}!important;height:3px!important}}
.stTabs [data-baseweb="tab-panel"]{{background:{BG}!important;padding-top:20px!important}}

/* Buttons */
.stButton>button{{font-family:'Space Mono',monospace!important;font-size:11px!important;letter-spacing:0.12em!important;text-transform:uppercase!important;background:{GREEN}!important;color:{BG}!important;border:none!important;border-radius:0!important;font-weight:700!important;padding:8px 20px!important}}
.stButton>button:hover{{background:#00ffb3!important;border:none!important}}

/* Inputs */
.stTextInput input,.stTextArea textarea,.stNumberInput input{{background:{SURF2}!important;color:{TEXT}!important;border:1px solid {BORDER}!important;border-radius:2px!important;font-family:'Space Mono',monospace!important;font-size:12px!important}}
.stTextInput input:focus,.stTextArea textarea:focus,.stNumberInput input:focus{{border-color:{GREEN}!important;box-shadow:none!important}}
.stSelectbox>div>div{{background:{SURF2}!important;color:{TEXT}!important;border:1px solid {BORDER}!important;border-radius:2px!important;font-family:'Space Mono',monospace!important;font-size:12px!important}}
[data-baseweb="popover"],[data-baseweb="menu"]{{background:{SURF2}!important}}
[data-baseweb="menu"] li{{color:{TEXT}!important;background:{SURF2}!important}}
[data-baseweb="menu"] li:hover{{background:{BORDER}!important}}
label,div[data-testid="stWidgetLabel"] p{{color:{MUTED2}!important;font-family:'Space Mono',monospace!important;font-size:10px!important;letter-spacing:0.12em!important;text-transform:uppercase!important}}
.stCheckbox label p{{color:{TEXT}!important;font-size:12px!important;text-transform:none!important;letter-spacing:0!important}}

/* Alerts */
div[data-testid="stInfoMessage"],div[data-testid="stSuccessMessage"],
div[data-testid="stWarningMessage"],div[data-testid="stErrorMessage"]{{background:{SURF2}!important;border-radius:0!important}}
div[data-testid="stInfoMessage"] *,div[data-testid="stSuccessMessage"] *,
div[data-testid="stWarningMessage"] *,div[data-testid="stErrorMessage"] *{{color:{TEXT}!important;font-family:'Space Mono',monospace!important;font-size:11px!important}}

/* Scrollbar */
::-webkit-scrollbar{{width:4px;height:4px}}
::-webkit-scrollbar-track{{background:{BG}}}
::-webkit-scrollbar-thumb{{background:{BORDER}}}

/* Custom components */
.panel-title{{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.22em;text-transform:uppercase;color:{MUTED};margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid {BORDER}}}
.logo-h{{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;letter-spacing:0.06em;color:{TEXT}}}
.logo-h span{{color:{GREEN}}}
.logo-s{{font-family:'Space Mono',monospace;font-size:9px;color:{MUTED};letter-spacing:0.2em;text-transform:uppercase;margin-top:2px}}
.kc{{background:{SURF};border:1px solid {BORDER};border-top:2px solid {GREEN};padding:18px 16px;margin-bottom:4px}}
.kl{{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:{MUTED};margin-bottom:8px}}
.kv{{font-family:'Space Mono',monospace;font-size:26px;font-weight:700;line-height:1}}
.ks{{font-family:'Space Mono',monospace;font-size:10px;margin-top:6px}}
.rbox{{background:{SURF2};border:1px solid {GREEN};padding:18px;font-family:'Space Mono',monospace;font-size:12px;line-height:1.8;color:{TEXT};margin-top:12px;white-space:pre-wrap}}
.chip{{display:inline-block;background:rgba(0,229,160,0.08);border:1px solid rgba(0,229,160,0.25);color:{GREEN};font-family:'Space Mono',monospace;font-size:10px;padding:3px 10px;margin:3px 4px 3px 0}}
.ac{{background:rgba(255,77,109,0.07);border:1px solid rgba(255,77,109,0.25);border-left:3px solid {RED};padding:14px 16px;margin-bottom:12px}}
.aw{{background:rgba(255,184,77,0.07);border:1px solid rgba(255,184,77,0.25);border-left:3px solid {WARN};padding:14px 16px;margin-bottom:12px}}
.ai{{background:rgba(77,159,255,0.07);border:1px solid rgba(77,159,255,0.25);border-left:3px solid {BLUE};padding:14px 16px;margin-bottom:12px}}
.rpt{{background:{SURF2};border:1px solid {BORDER};padding:28px;font-family:'Syne',sans-serif;font-size:14px;line-height:2;color:{TEXT};white-space:pre-wrap}}
.info-bar{{background:{SURF2};border-left:2px solid {BLUE};padding:12px 16px;font-family:'Space Mono',monospace;font-size:11px;color:{MUTED2};margin-bottom:20px}}
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY BASE LAYOUT (no legend key — avoids duplicate kwarg bug) ──────────
def plot_layout(**extra):
    """Return a clean Plotly layout dict. Pass legend= separately if needed."""
    return dict(
        paper_bgcolor=SURF, plot_bgcolor=SURF,
        font=dict(family="Space Mono, monospace", color=MUTED2, size=10),
        margin=dict(l=44, r=16, t=36, b=44),
        xaxis=dict(gridcolor=BORDER, showgrid=True, zeroline=False,
                   linecolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
        yaxis=dict(gridcolor=BORDER, showgrid=True, zeroline=False,
                   linecolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
        title=dict(font=dict(size=10, color=MUTED, family="Space Mono, monospace")),
        **extra
    )

# ─── INIT ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    init_db()
    return ROIEngine()

engine   = get_engine()
mistral  = MistralWrapper()
budget   = BudgetGuardian()
optimizer = PromptOptimizer()
abtester = ABTester()
forecaster = ROIForecaster()
anomalies  = AnomalyDetector()
prompt_lib = SmartPromptLibrary()
cost_opt   = CostOptimizer()
health     = WorkflowHealthScore()
team_roi   = TeamROIDashboard()

# ─── DARK PLOTLY TABLE ────────────────────────────────────────────────────────
def dark_table(df: pd.DataFrame, height=280, col_widths=None, col_colors=None):
    """
    Render a pandas DataFrame as a fully dark Plotly table.
    col_colors: list of hex colors per column for text (optional).
    """
    n = len(df)
    ncols = len(df.columns)
    row_fills = [SURF if i % 2 == 0 else SURF2 for i in range(n)]

    # Per-column font color: each entry must be a list of length n
    if col_colors:
        font_color = [[c] * n for c in col_colors]
    else:
        font_color = [[TEXT] * n] * ncols

    fig = go.Figure(data=[go.Table(
        columnwidth=col_widths or ([160] + [90] * (ncols - 1)),
        header=dict(
            values=[f"<b>{c}</b>" for c in df.columns],
            fill_color=SURF2,
            font=dict(color=MUTED2, size=10, family="Space Mono, monospace"),
            align="left", line_color=BORDER, height=34,
        ),
        cells=dict(
            values=[df[c].tolist() for c in df.columns],
            fill_color=[row_fills] * ncols,
            font=dict(color=font_color, size=11, family="Space Mono, monospace"),
            align="left", line_color=BORDER, height=30,
        )
    )])
    fig.update_layout(
        paper_bgcolor=SURF, plot_bgcolor=SURF,
        margin=dict(l=0, r=0, t=0, b=0), height=height
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─── KPI CARD HTML ────────────────────────────────────────────────────────────
def kpi(label, value, sub, color=GREEN, top_color=None):
    tc = top_color or color
    return (f'<div class="kc" style="border-top-color:{tc}">'
            f'<div class="kl">{label}</div>'
            f'<div class="kv" style="color:{color}">{value}</div>'
            f'<div class="ks" style="color:{MUTED2}">{sub}</div></div>')

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-h">ROI <span>LENS</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-s">AI Accountability Layer</div>', unsafe_allow_html=True)
    st.markdown("---")

    api_key = st.text_input("Mistral API Key",
                             value=os.getenv("MISTRAL_API_KEY", ""),
                             type="password", placeholder="paste key here...")
    if api_key:
        os.environ["MISTRAL_API_KEY"] = api_key
        mistral.api_key = api_key

    has_key = bool(api_key or os.getenv("MISTRAL_API_KEY"))
    kc = GREEN if has_key else RED
    kl = "✓ Key set — live mode" if has_key else "✗ No key — demo mode"
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:10px;color:{kc};margin-top:4px;">{kl}</div>',
                unsafe_allow_html=True)
    st.markdown("---")

    if st.button("🔄  Refresh Dashboard", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown('<div class="panel-title">Register New Workflow</div>', unsafe_allow_html=True)
    with st.form("reg_wf", clear_on_submit=True):
        wf_id_i   = st.text_input("Workflow ID",   placeholder="wf_my_workflow")
        wf_name_i = st.text_input("Name",          placeholder="My AI Workflow")
        wf_desc_i = st.text_input("Description",   placeholder="What it does")
        wf_hrly_i = st.number_input("Hourly Value ($)", min_value=0.0, value=60.0, step=5.0)
        if st.form_submit_button("Register →", use_container_width=True):
            if wf_id_i and wf_name_i:
                db = get_db()
                db.execute("INSERT OR REPLACE INTO workflows VALUES (?,?,?,?,?)",
                           (wf_id_i, wf_name_i, wf_desc_i, wf_hrly_i, datetime.utcnow().isoformat()))
                db.commit()
                st.success(f"✓ {wf_name_i}")
            else:
                st.error("ID and Name required")

    st.markdown("---")
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};letter-spacing:0.15em;">MISTRAL HACKATHON 2026</div>',
                unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs([
    "📊  Dashboard", "🚀  Live Demo", "💰  Record Outcome",
    "⚠️  Kill-Switch", "📝  Exec Report", "💸  Budget Guard",
    "🔬  A/B Test", "🔮  Forecaster", "📚  Prompt Library",
    "⚙️  Cost Optimizer", "🏆  Health Score", "👥  Team ROI"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    dash = engine.get_dashboard()
    s    = dash["summary"]

    # KPI row
    k1, k2, k3, k4, k5 = st.columns(5)
    roi_c = GREEN if s["overall_roi_pct"] >= 0 else RED
    q_c   = GREEN if s["avg_quality_score"] >= 0.8 else (WARN if s["avg_quality_score"] >= 0.6 else RED)

    k1.markdown(kpi("Total API Cost",    f'${s["total_cost_usd"]:.4f}',  f'{s["total_tokens"]:,} tokens', WARN,  WARN),  unsafe_allow_html=True)
    k2.markdown(kpi("Value Generated",   f'${s["total_value_usd"]:.2f}', f'Net ${s["net_value_usd"]:.2f}',GREEN, GREEN), unsafe_allow_html=True)
    k3.markdown(kpi("Net ROI",           f'{s["overall_roi_pct"]:+.1f}%',
                    "ROI positive ✓" if s["overall_roi_pct"] >= 0 else "Needs attention",
                    roi_c, roi_c), unsafe_allow_html=True)
    k4.markdown(kpi("Total API Calls",   f'{s["total_calls"]:,}',        f'avg {s["avg_latency_ms"]}ms', BLUE, BLUE),  unsafe_allow_html=True)
    k5.markdown(kpi("Avg Quality Score", f'{s["avg_quality_score"]*100:.0f}%', "evaluator model", q_c, MUTED), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_wf, col_right = st.columns([1.5, 1])

    with col_wf:
        st.markdown('<div class="panel-title">// Workflow ROI Breakdown</div>', unsafe_allow_html=True)
        wf_data = dash["workflows"]
        if wf_data:
            df_wf    = pd.DataFrame(wf_data)
            n        = len(df_wf)
            roi_fill = [GREEN if r >= 0 else RED for r in df_wf["roi_pct"]]
            alt_fill = [SURF if i % 2 == 0 else SURF2 for i in range(n)]

            fig_tbl = go.Figure(data=[go.Table(
                columnwidth=[160, 50, 110, 95, 90, 75],
                header=dict(
                    values=["<b>Workflow</b>","<b>Calls</b>","<b>ROI</b>","<b>Cost</b>","<b>Value</b>","<b>Quality</b>"],
                    fill_color=SURF2,
                    font=dict(color=MUTED2, size=10, family="Space Mono, monospace"),
                    align="left", line_color=BORDER, height=34,
                ),
                cells=dict(
                    values=[
                        df_wf["workflow_name"].tolist(),
                        df_wf["call_count"].astype(str).tolist(),
                        df_wf["roi_pct"].apply(lambda x: f"{x:+.1f}%").tolist(),
                        df_wf["cost_usd"].apply(lambda x: f"${x:.4f}").tolist(),
                        df_wf["value_usd"].apply(lambda x: f"${x:.2f}").tolist(),
                        df_wf["avg_quality"].apply(lambda x: f"{x*100:.0f}%").tolist(),
                    ],
                    # fill: alternate rows everywhere; ROI col gets green/red
                    fill_color=[alt_fill, alt_fill, roi_fill, alt_fill, alt_fill, alt_fill],
                    # font color: must be list-of-lists (one list per column, each of length n)
                    font=dict(
                        color=[
                            [TEXT]   * n,   # Workflow name
                            [MUTED2] * n,   # Calls
                            [BG]     * n,   # ROI — dark text on colored bg
                            [WARN]   * n,   # Cost
                            [GREEN]  * n,   # Value
                            [BLUE]   * n,   # Quality
                        ],
                        size=11, family="Space Mono, monospace"
                    ),
                    align="left", line_color=BORDER, height=30,
                )
            )])
            fig_tbl.update_layout(paper_bgcolor=SURF, plot_bgcolor=SURF,
                                  margin=dict(l=0,r=0,t=0,b=0), height=220)
            st.plotly_chart(fig_tbl, use_container_width=True, config={"displayModeBar": False})

            # ROI bar chart
            fig_bar = go.Figure(go.Bar(
                x=df_wf["workflow_name"], y=df_wf["roi_pct"],
                marker_color=[GREEN if r >= 0 else RED for r in df_wf["roi_pct"]],
                text=df_wf["roi_pct"].apply(lambda x: f"{x:+.1f}%"),
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color=MUTED2)
            ))
            fig_bar.update_layout(**plot_layout(title_text="ROI % per Workflow", height=230,
                                                showlegend=False, yaxis_title="ROI %"))
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:32px;text-align:center;border:1px dashed {BORDER}">No workflow data yet.</div>',
                        unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="panel-title">// 14-Day Call Volume</div>', unsafe_allow_html=True)
        trend = dash["daily_trend"]
        if trend:
            df_tr = pd.DataFrame(trend)
            fig_tr = go.Figure()
            fig_tr.add_trace(go.Bar(x=df_tr["date"], y=df_tr["calls"],
                                    marker_color=BLUE, opacity=0.75, name="Calls"))
            fig_tr.add_trace(go.Scatter(x=df_tr["date"], y=df_tr["calls"],
                                        mode="lines", line=dict(color=GREEN, width=2), showlegend=False))
            fig_tr.update_layout(**plot_layout(title_text="Calls / Day", height=210, showlegend=False))
            st.plotly_chart(fig_tr, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="panel-title">// Model Cost Breakdown</div>', unsafe_allow_html=True)
        models = dash["model_breakdown"]
        if models:
            df_m  = pd.DataFrame(models)
            fig_m = go.Figure(go.Pie(
                labels=df_m["model"], values=df_m["cost_usd"], hole=0.6,
                marker=dict(colors=[GREEN, BLUE, WARN, RED]),
                textfont=dict(family="Space Mono", size=9, color=TEXT),
                textinfo="percent",
            ))
            # NOTE: pass legend inline here — NOT via **PLOT to avoid duplicate key
            fig_m.update_layout(
                paper_bgcolor=SURF, plot_bgcolor=SURF,
                font=dict(family="Space Mono, monospace", color=MUTED2, size=10),
                margin=dict(l=10, r=10, t=10, b=10),
                height=210,
                legend=dict(font=dict(size=9, color=MUTED2), bgcolor=SURF2, bordercolor=BORDER)
            )
            st.plotly_chart(fig_m, use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="panel-title">// Value by Outcome Type</div>', unsafe_allow_html=True)
        outcomes = dash["outcome_types"]
        if outcomes:
            df_ot = pd.DataFrame(outcomes)
            fig_ot = go.Figure(go.Bar(
                x=df_ot["total_value_usd"], y=df_ot["type"], orientation="h",
                marker_color=GREEN, opacity=0.85,
                text=df_ot["total_value_usd"].apply(lambda x: f"${x:.0f}"),
                textposition="outside",
                textfont=dict(family="Space Mono", size=10, color=TEXT)
            ))
            fig_ot.update_layout(**plot_layout(title_text="Value by Outcome", height=200, showlegend=False))
            st.plotly_chart(fig_ot, use_container_width=True, config={"displayModeBar": False})

    # Audit trail
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:20px 0">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">// Recent Audit Trail — Last 20 Calls</div>', unsafe_allow_html=True)
    calls = engine.get_recent_calls(20)
    if calls:
        df_c = pd.DataFrame(calls)
        df_c["cost_usd"]      = df_c["cost_usd"].apply(lambda x: f"${x:.6f}")
        df_c["outcome_value"] = df_c["outcome_value"].apply(lambda x: f"${x:.2f}" if x > 0 else "—")
        df_c["created_at"]    = pd.to_datetime(df_c["created_at"]).dt.strftime("%m/%d %H:%M")
        call_df = df_c[["workflow_name","model","cost_usd","outcome_value","outcome_type","created_at"]].rename(
            columns={"workflow_name":"Workflow","model":"Model","cost_usd":"Cost",
                     "outcome_value":"Value","outcome_type":"Outcome","created_at":"Time"}
        ).fillna("—")
        dark_table(call_df, height=310,
                   col_widths=[150,140,95,80,110,90],
                   col_colors=[TEXT, MUTED2, WARN, GREEN, MUTED2, MUTED2])
    else:
        st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:24px;text-align:center;border:1px dashed {BORDER}">No calls yet. Use Live Demo tab.</div>',
                    unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LIVE DEMO
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="panel-title">// Live Tracked Call — Mistral API Through ROI Lens</div>', unsafe_allow_html=True)

    WORKFLOWS = {
        "Customer Support AI":   ("wf_support", 8.0),
        "Sales Email Drafter":   ("wf_sales",   150.0),
        "Fraud Detection":       ("wf_fraud",   500.0),
        "Code Review Assistant": ("wf_code",    20.0),
        "Document Summarizer":   ("wf_docs",    12.0),
    }
    PROMPTS = {
        "Customer Support AI":
            "Draft a professional reply to a customer upset about a 2-week delayed shipment. Keep it under 80 words.",
        "Sales Email Drafter":
            "Write a cold outreach email to a fintech startup CTO about our AI fraud detection API. Under 80 words.",
        "Fraud Detection":
            "Analyze for fraud: User 9921, $4,899 charge, Lagos Nigeria, card registered Ohio USA, 3am, new device, 5 failed attempts before success. Respond in JSON: {is_fraud, confidence, reason}",
        "Code Review Assistant":
            "Review this Python function for bugs:\ndef get_user(id):\n  users = db.query('SELECT * FROM users')\n  return [u for u in users if u.id == id][0]",
        "Document Summarizer":
            "Summarize the key risks in a standard SaaS subscription contract for a procurement manager.",
    }

    col_form, col_res = st.columns([1, 1])

    with col_form:
        sel_wf   = st.selectbox("Workflow", list(WORKFLOWS.keys()), key="d_wf")
        wf_id_d, def_val = WORKFLOWS[sel_wf]
        model_d  = st.selectbox("Model", ["mistral-large-latest","mistral-small-latest","open-mistral-7b","codestral-latest"])
        prompt_d = st.text_area("Prompt", value=PROMPTS[sel_wf], height=150, key="d_prompt")
        exp_val  = st.number_input("Expected Business Value ($)", min_value=0.0, value=def_val, step=1.0)
        sys_p    = st.text_input("System Prompt (optional)", placeholder="You are a helpful assistant...")
        run_btn  = st.button("▶  Run Tracked Call", use_container_width=True)

    with col_res:
        st.markdown('<div class="panel-title">// Response + Tracking Metadata</div>', unsafe_allow_html=True)
        if run_btn:
            if not prompt_d.strip():
                st.error("Please enter a prompt.")
            elif not mistral.api_key:
                st.warning("⚠️  Add your MISTRAL_API_KEY in the sidebar.")
            else:
                with st.spinner("Sending through ROI Lens tracking layer..."):
                    msgs = []
                    if sys_p.strip():
                        msgs.append({"role":"system","content":sys_p})
                    msgs.append({"role":"user","content":prompt_d})
                    try:
                        res = asyncio.run(mistral.chat_with_tracking(
                            messages=msgs, workflow_id=wf_id_d,
                            workflow_name=sel_wf, model=model_d,
                            expected_value_usd=exp_val
                        ))
                        st.session_state["last_call_id"]   = res["call_id"]
                        st.session_state["last_call_cost"] = res["cost_usd"]

                        st.markdown(f'<div style="color:{GREEN};font-family:Space Mono,monospace;font-size:10px;margin-bottom:8px;">✓ CALL TRACKED SUCCESSFULLY</div>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<div class="rbox">{res["content"]}</div>', unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="margin-top:12px;">
                          <span class="chip">ID: {res['call_id'][:10]}...</span>
                          <span class="chip">cost: ${res['cost_usd']:.6f}</span>
                          <span class="chip">{res['usage']['total_tokens']} tokens</span>
                          <span class="chip">{res['latency_ms']}ms</span>
                          <span class="chip">{model_d}</span>
                        </div>
                        <div style="margin-top:10px;font-family:Space Mono,monospace;font-size:10px;color:{MUTED2};">
                          → Copy the call ID → go to 💰 Record Outcome to close the ROI loop.
                        </div>""", unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"API Error: {e}")
        else:
            st.markdown(f"""
            <div style="border:1px dashed {BORDER};padding:48px;text-align:center;margin-top:16px;">
              <div style="font-family:Space Mono,monospace;font-size:11px;color:{MUTED};line-height:2.2;">
                Fill the form and click<br>
                <span style="color:{GREEN};font-weight:700;font-size:13px;">▶ RUN TRACKED CALL</span><br><br>
                Every call is auto-logged with<br>cost · tokens · latency · quality
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RECORD OUTCOME
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="panel-title">// Link a Business Outcome to an AI Call</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">After an AI call creates real business value — deal closed, fraud caught, ticket resolved — record it here to close the ROI loop.</div>',
                unsafe_allow_html=True)

    col_o1, col_o2 = st.columns([1, 1])

    with col_o1:
        cid    = st.text_input("Call ID", value=st.session_state.get("last_call_id",""),
                                placeholder="Paste call_id from Live Demo...")
        otype  = st.selectbox("Outcome Type", ["time_saved","conversion","fraud_prevented","reply_received","bug_caught","custom"])
        oval   = st.number_input("Business Value ($)", min_value=0.0, value=10.0, step=1.0)
        odesc  = st.text_area("Description",
                               placeholder="e.g. Ticket resolved without escalation, saved 8 min @ $60/hr", height=80)
        overif = st.checkbox("Mark as verified (human-confirmed)", value=True)

        if st.button("💰  Record Outcome", use_container_width=True):
            if not cid.strip():
                st.error("Call ID is required")
            else:
                try:
                    r = engine.record_outcome(cid.strip(), otype, oval, odesc, overif)
                    st.success(f"✓ Recorded! outcome_id: {r['outcome_id'][:14]}...")
                    st.json(r)
                except ValueError as e:
                    st.error(str(e))

    with col_o2:
        last_cost = st.session_state.get("last_call_cost", 0.0)
        if last_cost > 0:
            roi_p  = (oval - last_cost) / last_cost * 100
            roi_c2 = GREEN if roi_p >= 0 else RED
            st.markdown(f"""
            <div style="background:{SURF2};border:1px solid {BORDER};padding:22px;">
              <div class="panel-title">ROI Preview — Last Demo Call</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:12px;">
                <div>
                  <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">API Cost</div>
                  <div style="font-family:Space Mono,monospace;font-size:22px;color:{WARN};font-weight:700;margin-top:4px;">${last_cost:.6f}</div>
                </div>
                <div>
                  <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Business Value</div>
                  <div style="font-family:Space Mono,monospace;font-size:22px;color:{GREEN};font-weight:700;margin-top:4px;">${oval:.2f}</div>
                </div>
                <div>
                  <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Net Value</div>
                  <div style="font-family:Space Mono,monospace;font-size:22px;color:{TEXT};font-weight:700;margin-top:4px;">${oval-last_cost:.2f}</div>
                </div>
                <div>
                  <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">ROI</div>
                  <div style="font-family:Space Mono,monospace;font-size:22px;color:{roi_c2};font-weight:700;margin-top:4px;">{roi_p:+.0f}%</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="border:1px dashed {BORDER};padding:36px;text-align:center;font-family:Space Mono,monospace;font-size:11px;color:{MUTED};line-height:2;">Run a tracked call in<br><span style="color:{GREEN}">🚀 Live Demo</span> first,<br>then record its outcome here.</div>',
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-title">// Outcome Reference</div>', unsafe_allow_html=True)
        ref_df = pd.DataFrame({
            "Type":    ["time_saved","conversion","fraud_prevented","reply_received","bug_caught"],
            "Example": ["Agent time saved","Deal closed","Transaction blocked","Lead re-engaged","Bug fix saved"],
            "Range":   ["$2–$50","$50–$10k","$100–$100k","$5–$500","$20–$200"],
        })
        dark_table(ref_df, height=200, col_widths=[120,160,90],
                   col_colors=[GREEN, MUTED2, WARN])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — KILL-SWITCH ALERTS
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="panel-title">// Kill-Switch Recommender</div>', unsafe_allow_html=True)
    alerts = engine.get_kill_switch_alerts()

    if not alerts:
        st.markdown(f'<div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.2);border-left:3px solid {GREEN};padding:16px;font-family:Space Mono,monospace;font-size:12px;color:{GREEN};">✓ All workflows are ROI positive — no alerts.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:11px;color:{WARN};margin-bottom:16px;">⚠ {len(alerts)} workflow(s) flagged</div>',
                    unsafe_allow_html=True)
        emojis = {"critical":"🔴","warning":"🟡","info":"🔵"}
        css_cls = {"critical":"ac","warning":"aw","info":"ai"}

        for a in alerts:
            sev = a["severity"]
            st.markdown(f"""
            <div class="{css_cls.get(sev,'aw')}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:{TEXT};">
                  {emojis.get(sev,'⚪')} {a['workflow_name']}
                </div>
                <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED2};letter-spacing:0.1em;text-align:right;">
                  ROI: {a['roi_pct']:+.1f}% &nbsp;|&nbsp; Cost: ${a['total_cost_usd']:.4f}<br>
                  Value: ${a['total_value_usd']:.2f} &nbsp;|&nbsp; {a['call_count']} calls
                </div>
              </div>
              <div style="font-size:12px;color:{MUTED2};margin-bottom:6px;">{a['reason']}</div>
              <div style="font-family:Space Mono,monospace;font-size:11px;color:{GREEN};">→ {a['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-title">// Cost vs Value — Flagged Workflows</div>', unsafe_allow_html=True)
        df_al = pd.DataFrame(alerts)
        fig_al = go.Figure()
        fig_al.add_trace(go.Bar(name="Cost ($)", x=df_al["workflow_name"],
                                y=df_al["total_cost_usd"], marker_color=RED, opacity=0.8))
        fig_al.add_trace(go.Bar(name="Value ($)", x=df_al["workflow_name"],
                                y=df_al["total_value_usd"], marker_color=GREEN, opacity=0.8))
        fig_al.update_layout(**plot_layout(barmode="group", height=280,
                                           title_text="Cost vs Value — Flagged Workflows",
                                           legend=dict(font=dict(size=9,color=MUTED2), bgcolor=SURF2, bordercolor=BORDER)))
        st.plotly_chart(fig_al, use_container_width=True, config={"displayModeBar": False})

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — EXEC REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="panel-title">// AI-Generated Executive ROI Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Generates a plain-English CFO brief via Mistral AI — 3 paragraphs covering spend, ROI, wins, and one concrete recommendation. Requires API key.</div>',
                unsafe_allow_html=True)

    if st.button("⬡  Generate Executive Report"):
        if not mistral.api_key:
            st.warning("Set your MISTRAL_API_KEY in the sidebar first.")
        else:
            with st.spinner("Mistral is drafting your executive report..."):
                try:
                    data   = engine.get_dashboard()
                    report = asyncio.run(mistral.generate_roi_report(data))
                    st.session_state["exec_report"] = report
                    st.session_state["report_ts"]   = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
                except Exception as e:
                    st.error(f"Error: {e}")

    if "exec_report" in st.session_state:
        st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};letter-spacing:0.15em;margin-bottom:10px;text-transform:uppercase;">Generated: {st.session_state.get("report_ts","")}</div>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="rpt">{st.session_state["exec_report"]}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-title">// Data Snapshot</div>', unsafe_allow_html=True)
        snap = engine.get_dashboard()["summary"]
        roi_c3 = GREEN if snap["overall_roi_pct"] >= 0 else RED
        r1, r2, r3, r4 = st.columns(4)
        r1.markdown(kpi("Total Spent",   f'${snap["total_cost_usd"]:.4f}', "",  WARN, WARN),  unsafe_allow_html=True)
        r2.markdown(kpi("Value Created", f'${snap["total_value_usd"]:.2f}', "", GREEN, GREEN), unsafe_allow_html=True)
        r3.markdown(kpi("ROI",           f'{snap["overall_roi_pct"]:+.1f}%',"", roi_c3, roi_c3), unsafe_allow_html=True)
        r4.markdown(kpi("Total Calls",   f'{snap["total_calls"]:,}', "",         BLUE, BLUE),  unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — BUDGET GUARDIAN
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="panel-title">// Budget Guardian — Dynamic Per-Workflow Spend Limits</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Set a real budget for each AI workflow. The system tracks burn rate in real time, alerts at your chosen threshold, and shows how many days until you run out — all from actual API call data.</div>', unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([1, 1.4])

    with col_b1:
        st.markdown('<div class="panel-title">// Set Budget</div>', unsafe_allow_html=True)

        db_wfs = get_db().execute("SELECT workflow_id, name FROM workflows").fetchall()
        wf_options = {f"{w['name']} ({w['workflow_id']})": w['workflow_id'] for w in db_wfs}

        if wf_options:
            sel_wf_budget = st.selectbox("Workflow", list(wf_options.keys()), key="bg_wf")
            budget_amt    = st.number_input("Budget Amount ($)", min_value=0.001, value=1.0, step=0.1, format="%.3f")
            period_days   = st.slider("Period (days)", min_value=1, max_value=90, value=30)
            alert_pct     = st.slider("Alert when spend reaches (%)", min_value=50, max_value=95, value=80)

            if st.button("💸  Set Budget", use_container_width=True):
                wf_id_b = wf_options[sel_wf_budget]
                result  = budget.set_budget(wf_id_b, budget_amt, period_days, float(alert_pct))
                st.success(f"✓ Budget set: ${budget_amt:.3f} over {period_days} days for {sel_wf_budget}")
        else:
            st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:16px;border:1px dashed {BORDER}">Register workflows in the sidebar first.</div>', unsafe_allow_html=True)

    with col_b2:
        st.markdown('<div class="panel-title">// Live Budget Status</div>', unsafe_allow_html=True)
        all_budgets = budget.get_all_budgets()

        if not all_budgets:
            st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:24px;text-align:center;border:1px dashed {BORDER}">No budgets set yet.<br>Set one on the left to start tracking.</div>', unsafe_allow_html=True)
        else:
            SEV_COLOR = {"healthy": GREEN, "warning": WARN, "at_limit": RED, "over_budget": RED}
            SEV_ICON  = {"healthy": "✅", "warning": "⚠️", "at_limit": "🔴", "over_budget": "💀"}

            for b_item in all_budgets:
                sev   = b_item["severity"]
                color = SEV_COLOR.get(sev, MUTED2)
                icon  = SEV_ICON.get(sev, "⚪")
                bar_w = min(b_item["pct_used"], 100)
                bar_color = GREEN if bar_w < 80 else WARN if bar_w < 100 else RED

                st.markdown(f"""
                <div style="background:{SURF2};border:1px solid {BORDER};border-left:3px solid {color};padding:14px 16px;margin-bottom:12px;">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                    <div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:{TEXT};">{icon} {b_item['workflow_name']}</div>
                    <div style="font-family:Space Mono,monospace;font-size:10px;color:{color};font-weight:700;">{b_item['pct_used']:.1f}% used</div>
                  </div>
                  <div style="background:{BORDER};height:6px;margin-bottom:8px;">
                    <div style="width:{bar_w}%;height:100%;background:{bar_color};"></div>
                  </div>
                  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
                    <div style="font-family:Space Mono,monospace;">
                      <div style="font-size:8px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Budget</div>
                      <div style="font-size:13px;color:{TEXT};font-weight:700;">${b_item['budget_usd']:.3f}</div>
                    </div>
                    <div style="font-family:Space Mono,monospace;">
                      <div style="font-size:8px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Spent</div>
                      <div style="font-size:13px;color:{WARN};font-weight:700;">${b_item['spent_usd']:.6f}</div>
                    </div>
                    <div style="font-family:Space Mono,monospace;">
                      <div style="font-size:8px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Remaining</div>
                      <div style="font-size:13px;color:{GREEN};font-weight:700;">${b_item['remaining_usd']:.6f}</div>
                    </div>
                    <div style="font-family:Space Mono,monospace;">
                      <div style="font-size:8px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;">Days Left</div>
                      <div style="font-size:13px;color:{BLUE};font-weight:700;">{b_item['days_until_empty']:.0f}d</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 — A/B MODEL TESTER
# ═══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="panel-title">// A/B Model Tester — Compare Any 2 Mistral Models Live</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Run the exact same prompt through 2 models simultaneously. Compare real cost, latency, and token usage side by side. Results saved to history. Use this to find the cheapest model that meets your quality bar.</div>', unsafe_allow_html=True)

    col_ab1, col_ab2 = st.columns([1, 1])

    MODELS_AB = ["mistral-large-latest", "mistral-small-latest", "open-mistral-7b",
                 "open-mixtral-8x7b", "codestral-latest"]

    with col_ab1:
        st.markdown('<div class="panel-title">// Test Configuration</div>', unsafe_allow_html=True)
        model_a_sel = st.selectbox("Model A", MODELS_AB, index=0, key="ab_ma")
        model_b_sel = st.selectbox("Model B", MODELS_AB, index=1, key="ab_mb")
        ab_sys      = st.text_input("System Prompt", placeholder="You are a helpful assistant...", key="ab_sys")
        ab_prompt   = st.text_area("Prompt to Test (same sent to both models)",
            value="Explain the ROI of implementing AI in customer support in 3 bullet points. Be specific and cite example numbers.",
            height=120, key="ab_prompt")

        run_ab = st.button("⚡  Run A/B Test (Parallel)", use_container_width=True)

    with col_ab2:
        st.markdown('<div class="panel-title">// Results</div>', unsafe_allow_html=True)

        if run_ab:
            if model_a_sel == model_b_sel:
                st.error("Please select two different models.")
            elif not mistral.api_key:
                st.warning("Add your MISTRAL_API_KEY in the sidebar.")
            else:
                with st.spinner(f"Calling {model_a_sel} and {model_b_sel} in parallel..."):
                    try:
                        result = asyncio.run(abtester.run_ab_test(
                            prompt=ab_prompt, model_a=model_a_sel, model_b=model_b_sel,
                            system_prompt=ab_sys, api_key=mistral.api_key
                        ))
                        st.session_state["ab_result"] = result
                    except Exception as e:
                        st.error(f"Error: {e}")

        ab_r = st.session_state.get("ab_result")
        if ab_r:
            winner_cost = ab_r["cheaper_model"]
            winner_lat  = ab_r["latency_winner"]

            c1, c2 = st.columns(2)
            for col, key, label in [(c1, "model_a", "Model A"), (c2, "model_b", "Model B")]:
                m    = ab_r[key]
                is_cheap = m["model"] == winner_cost
                border_c = GREEN if is_cheap else BORDER
                badge    = f'<span style="background:{GREEN};color:{BG};font-size:9px;padding:2px 6px;font-family:Space Mono,monospace;font-weight:700;margin-left:8px;">CHEAPER</span>' if is_cheap else ""
                col.markdown(f"""
                <div style="background:{SURF2};border:1px solid {border_c};padding:16px;">
                  <div style="font-family:Space Mono,monospace;font-size:10px;font-weight:700;color:{TEXT};margin-bottom:12px;">{m['model']}{badge}</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-family:Space Mono,monospace;">
                    <div><div style="font-size:8px;color:{MUTED};text-transform:uppercase;">Cost</div>
                         <div style="font-size:18px;color:{WARN};font-weight:700;">${m['cost_usd']:.6f}</div></div>
                    <div><div style="font-size:8px;color:{MUTED};text-transform:uppercase;">Latency</div>
                         <div style="font-size:18px;color:{BLUE};font-weight:700;">{m['latency_ms']}ms</div></div>
                    <div><div style="font-size:8px;color:{MUTED};text-transform:uppercase;">In Tokens</div>
                         <div style="font-size:14px;color:{TEXT};">{m['input_tokens']}</div></div>
                    <div><div style="font-size:8px;color:{MUTED};text-transform:uppercase;">Out Tokens</div>
                         <div style="font-size:14px;color:{TEXT};">{m['output_tokens']}</div></div>
                  </div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.2);
                        border-left:3px solid {GREEN};padding:14px;margin-top:12px;
                        font-family:Space Mono,monospace;font-size:11px;color:{TEXT};">
              <div style="color:{GREEN};font-weight:700;margin-bottom:4px;">SAVINGS: {ab_r['savings_pct']:.1f}% cheaper</div>
              {ab_r['recommendation']}
            </div>""", unsafe_allow_html=True)

            with st.expander("View Responses Side by Side"):
                r1, r2 = st.columns(2)
                r1.markdown(f'<div class="rbox" style="font-size:11px;">{ab_r["model_a"]["content"]}</div>', unsafe_allow_html=True)
                r2.markdown(f'<div class="rbox" style="font-size:11px;">{ab_r["model_b"]["content"]}</div>', unsafe_allow_html=True)

    # AB History
    st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:20px 0">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">// A/B Test History</div>', unsafe_allow_html=True)
    history = abtester.get_ab_history(10)
    if history:
        df_h = pd.DataFrame(history)
        df_h["created_at"] = pd.to_datetime(df_h["created_at"]).dt.strftime("%m/%d %H:%M")
        df_h["savings"]    = df_h["savings_pct"].apply(lambda x: f"{x:.1f}%")
        df_h["cost_a"]     = df_h["cost_a"].apply(lambda x: f"${x:.6f}")
        df_h["cost_b"]     = df_h["cost_b"].apply(lambda x: f"${x:.6f}")
        dark_table(
            df_h[["model_a","model_b","cost_a","cost_b","winner","savings","created_at"]].rename(
                columns={"model_a":"Model A","model_b":"Model B","cost_a":"Cost A",
                         "cost_b":"Cost B","winner":"Winner","savings":"Savings","created_at":"Time"}),
            height=220, col_widths=[130,130,90,90,130,70,90],
            col_colors=[MUTED2, MUTED2, WARN, WARN, GREEN, GREEN, MUTED2]
        )
    else:
        st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:16px;text-align:center;border:1px dashed {BORDER}">No tests yet. Run your first A/B test above.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 8 — ROI FORECASTER + ANOMALY DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab8:
    st.markdown('<div class="panel-title">// ROI Forecaster & Anomaly Detector</div>', unsafe_allow_html=True)

    sub1, sub2 = st.tabs(["🔮  ROI Forecast", "🚨  Anomaly Detector"])

    with sub1:
        st.markdown(f'<div class="info-bar">Predicts future AI costs and value using linear regression on your real historical data. No hardcoded numbers — all projections come from actual DB records. Confidence score reflects data quality.</div>', unsafe_allow_html=True)

        fc1, fc2 = st.columns([1, 2])
        with fc1:
            days_ahead = st.slider("Forecast Horizon (days)", min_value=7, max_value=90, value=30, step=7)
            run_fc = st.button("🔮  Generate Forecast", use_container_width=True)

        with fc2:
            if run_fc or "forecast_data" in st.session_state:
                if run_fc:
                    fc_data = forecaster.forecast(days_ahead)
                    st.session_state["forecast_data"] = fc_data
                fc_data = st.session_state.get("forecast_data", {})

                if "error" in fc_data:
                    st.warning(f"⚠️ {fc_data['error']}")
                else:
                    c1, c2, c3, c4 = st.columns(4)
                    roi_fc = GREEN if fc_data["projected_roi_pct"] >= 0 else RED
                    conf_c = GREEN if fc_data["confidence_score"] > 70 else WARN if fc_data["confidence_score"] > 40 else RED

                    c1.markdown(kpi("Projected Cost",  f'${fc_data["projected_total_cost"]:.4f}',  fc_data["cost_trend"],  WARN, WARN),  unsafe_allow_html=True)
                    c2.markdown(kpi("Projected Value", f'${fc_data["projected_total_value"]:.2f}',  fc_data["value_trend"], GREEN, GREEN), unsafe_allow_html=True)
                    c3.markdown(kpi("Projected ROI",   f'{fc_data["projected_roi_pct"]:+.1f}%',    f'{days_ahead} days',   roi_fc, roi_fc), unsafe_allow_html=True)
                    c4.markdown(kpi("Confidence",      f'{fc_data["confidence_score"]:.0f}%',       f'{fc_data["data_points_used"]} data pts', conf_c, conf_c), unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Chart: historical + forecast
                    fig_fc = go.Figure()
                    fig_fc.add_trace(go.Scatter(
                        x=fc_data["historical_dates"], y=fc_data["historical_values"],
                        name="Actual Value", mode="lines+markers",
                        line=dict(color=GREEN, width=2),
                        marker=dict(size=5)
                    ))
                    fig_fc.add_trace(go.Scatter(
                        x=fc_data["forecast_dates"], y=fc_data["forecast_values"],
                        name="Forecast Value", mode="lines",
                        line=dict(color=GREEN, width=2, dash="dot")
                    ))
                    fig_fc.add_trace(go.Bar(
                        x=fc_data["historical_dates"], y=fc_data["historical_costs"],
                        name="Actual Cost", marker_color=WARN, opacity=0.5, yaxis="y2"
                    ))
                    fig_fc.add_trace(go.Bar(
                        x=fc_data["forecast_dates"], y=fc_data["forecast_costs"],
                        name="Forecast Cost", marker_color=WARN, opacity=0.25, yaxis="y2"
                    ))
                    fig_fc.add_vline(
                        x=datetime.utcnow().strftime("%Y-%m-%d"),
                        line_dash="dash", line_color=MUTED,
                        annotation_text="TODAY", annotation_font_color=MUTED
                    )
                    fig_fc.update_layout(
                        paper_bgcolor=SURF, plot_bgcolor=SURF,
                        font=dict(family="Space Mono, monospace", color=MUTED2, size=10),
                        margin=dict(l=44, r=44, t=36, b=44),
                        height=340,
                        xaxis=dict(gridcolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
                        yaxis=dict(title="Value ($)", gridcolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
                        yaxis2=dict(title="Cost ($)", overlaying="y", side="right",
                                    tickfont=dict(color=MUTED2, size=9)),
                        legend=dict(bgcolor=SURF2, bordercolor=BORDER, font=dict(color=MUTED2, size=9)),
                        title=dict(text=f"{days_ahead}-Day ROI Forecast (Historical + Projected)",
                                   font=dict(size=10, color=MUTED))
                    )
                    st.plotly_chart(fig_fc, use_container_width=True, config={"displayModeBar": False})

    with sub2:
        st.markdown(f'<div class="info-bar">Learns the normal baseline (cost, latency, quality) for each workflow from real data. Automatically flags calls that are statistically abnormal. Tune the sensitivity with the sigma slider — lower = more sensitive.</div>', unsafe_allow_html=True)

        an1, an2 = st.columns([1, 2])
        with an1:
            sigma = st.slider("Sensitivity (σ threshold)", min_value=1.0, max_value=4.0,
                              value=2.5, step=0.1,
                              help="Lower = more sensitive. 2.0 catches more anomalies. 3.0 only flags extreme cases.")
            refresh_an = st.button("🚨  Detect Anomalies", use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="panel-title">// Baselines (Last 30 Days)</div>', unsafe_allow_html=True)
            bases = anomalies.get_baselines()
            if bases:
                for b in bases:
                    st.markdown(f"""
                    <div style="background:{SURF2};border:1px solid {BORDER};padding:10px 12px;margin-bottom:8px;font-family:Space Mono,monospace;">
                      <div style="font-size:11px;font-weight:700;color:{TEXT};margin-bottom:6px;">{b['workflow_name']}</div>
                      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:9px;">
                        <div><div style="color:{MUTED};">AVG COST</div><div style="color:{WARN};">${b['avg_cost']:.6f}</div></div>
                        <div><div style="color:{MUTED};">AVG LAT</div><div style="color:{BLUE};">{b['avg_latency']:.0f}ms</div></div>
                        <div><div style="color:{MUTED};">AVG QUAL</div><div style="color:{GREEN};">{b['avg_quality']:.2f}</div></div>
                      </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:10px;">Need 5+ calls per workflow to build a baseline.</div>', unsafe_allow_html=True)

        with an2:
            st.markdown('<div class="panel-title">// Detected Anomalies (Last 72 Hours)</div>', unsafe_allow_html=True)
            if refresh_an or "anomaly_list" in st.session_state:
                if refresh_an:
                    found = anomalies.detect_anomalies(sigma_threshold=sigma)
                    st.session_state["anomaly_list"] = found
                found = st.session_state.get("anomaly_list", [])

                if not found:
                    st.markdown(f'<div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.2);border-left:3px solid {GREEN};padding:14px;font-family:Space Mono,monospace;font-size:12px;color:{GREEN};">✓ No anomalies detected in the last 72 hours at σ={sigma}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:11px;color:{WARN};margin-bottom:14px;">⚠ {len(found)} anomalous call(s) detected at σ={sigma}</div>', unsafe_allow_html=True)
                    for a in found[:10]:
                        sev_c = RED if a["severity"] == "critical" else WARN
                        flags_html = "".join([
                            f'<span style="background:rgba(255,77,109,0.1);border:1px solid rgba(255,77,109,0.3);color:{RED};font-family:Space Mono,monospace;font-size:9px;padding:2px 8px;margin-right:6px;">{f["label"]}: {f["detail"]}</span>'
                            for f in a["flags"]
                        ])
                        st.markdown(f"""
                        <div style="background:{SURF2};border:1px solid {BORDER};border-left:3px solid {sev_c};padding:12px 14px;margin-bottom:10px;">
                          <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                            <div style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:{TEXT};">{a['workflow_name']}</div>
                            <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED2};">{a['model']} · {a['created_at'][:16]}</div>
                          </div>
                          <div style="margin-bottom:6px;">{flags_html}</div>
                          <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};">call_id: {a['call_id'][:16]}...</div>
                        </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="border:1px dashed {BORDER};padding:32px;text-align:center;font-family:Space Mono,monospace;font-size:11px;color:{MUTED};">Click <span style="color:{GREEN}">🚨 Detect Anomalies</span> to scan the last 72 hours.</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 9 — SMART PROMPT LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════
with tab9:
    st.markdown('<div class="panel-title">// Smart Prompt Library — Save & Rank Prompts by Real Performance</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Save any prompt to the library. The system automatically tracks which saved prompts generate the highest quality scores and ROI over real usage. Ranking updates every time a prompt is used — no manual scoring needed.</div>', unsafe_allow_html=True)

    pl1, pl2 = st.columns([1, 1.4])

    with pl1:
        st.markdown('<div class="panel-title">// Save New Prompt</div>', unsafe_allow_html=True)
        db_wfs2 = get_db().execute("SELECT workflow_id, name FROM workflows").fetchall()
        wf_map2 = {f"{w['name']}": w['workflow_id'] for w in db_wfs2}

        if wf_map2:
            pl_wf    = st.selectbox("Workflow", list(wf_map2.keys()), key="pl_wf")
            pl_title = st.text_input("Prompt Title", placeholder="e.g. Fraud analysis v2 — structured JSON output")
            pl_tags  = st.text_input("Tags (comma-separated)", placeholder="fraud, json, structured")
            pl_text  = st.text_area("Prompt Text", height=160, placeholder="Enter the full prompt here...")

            if st.button("📚  Save to Library", use_container_width=True):
                if pl_title and pl_text:
                    tags = [t.strip() for t in pl_tags.split(",") if t.strip()]
                    result = prompt_lib.save_prompt(wf_map2[pl_wf], pl_title, pl_text, tags)
                    st.success(f"✓ Saved: {pl_title}")
                    st.session_state["pl_load_text"] = pl_text
                else:
                    st.error("Title and Prompt Text are required")

            if "pl_load_text" in st.session_state:
                st.markdown(f'<div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.2);padding:10px 12px;font-family:Space Mono,monospace;font-size:10px;color:{GREEN};margin-top:8px;">✓ Prompt saved and ready to track</div>', unsafe_allow_html=True)
        else:
            st.info("Register workflows first in the sidebar.")

    with pl2:
        st.markdown('<div class="panel-title">// Prompt Leaderboard (Ranked by Performance)</div>', unsafe_allow_html=True)

        filter_wf = st.selectbox("Filter by Workflow", ["All"] + list(wf_map2.keys()) if wf_map2 else ["All"], key="pl_filter")
        wf_filter_id = wf_map2.get(filter_wf) if filter_wf != "All" else None

        prompts = prompt_lib.get_ranked_prompts(wf_filter_id)

        if not prompts:
            st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:24px;text-align:center;border:1px dashed {BORDER}">No prompts saved yet. Add your first prompt on the left.</div>', unsafe_allow_html=True)
        else:
            for i, p in enumerate(prompts):
                rank_c = GREEN if i == 0 else (BLUE if i == 1 else MUTED2)
                qual_c = GREEN if p["avg_quality"] >= 0.8 else (WARN if p["avg_quality"] >= 0.6 else RED)
                conf_badge = {"high": f"background:{GREEN};color:{BG}", "medium": f"background:{WARN};color:{BG}", "low": f"background:{MUTED};color:{TEXT}"}.get(p["confidence"], "")
                tags_html = "".join([f'<span style="background:{SURF2};border:1px solid {BORDER};color:{MUTED2};font-size:9px;padding:1px 6px;margin-right:4px;font-family:Space Mono,monospace;">{t}</span>' for t in p["tags"][:4]])

                st.markdown(f"""
                <div style="background:{SURF2};border:1px solid {BORDER};border-left:3px solid {rank_c};padding:12px 14px;margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <div>
                      <span style="font-family:Space Mono,monospace;font-size:11px;font-weight:700;color:{rank_c};">#{i+1}</span>
                      <span style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:{TEXT};margin-left:8px;">{p['title']}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                      <span style="font-family:Space Mono,monospace;font-size:10px;color:{qual_c};">Q: {p['avg_quality']:.2f}</span>
                      <span style="font-size:9px;padding:2px 6px;font-family:Space Mono,monospace;font-weight:700;{conf_badge}">{p['confidence'].upper()}</span>
                    </div>
                  </div>
                  <div style="font-family:Space Mono,monospace;font-size:10px;color:{MUTED2};margin-bottom:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{p['prompt_text'][:120]}...</div>
                  <div style="display:flex;gap:16px;font-family:Space Mono,monospace;font-size:9px;color:{MUTED};margin-bottom:6px;">
                    <span>Uses: <span style="color:{TEXT}">{p['uses']}</span></span>
                    <span>ROI: <span style="color:{'#00e5a0' if p['roi_pct']>=0 else '#ff4d6d'}">{p['roi_pct']:+.0f}%</span></span>
                    <span>Value: <span style="color:{GREEN}">${p['total_value']:.2f}</span></span>
                    <span>Avg Cost: <span style="color:{WARN}">${p['avg_cost']:.6f}</span></span>
                  </div>
                  {f'<div style="margin-top:4px;">{tags_html}</div>' if tags_html else ''}
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 10 — COST OPTIMIZER
# ═══════════════════════════════════════════════════════════════════════════════
with tab10:
    st.markdown('<div class="panel-title">// Cost Optimizer — Find the Cheapest Model That Still Meets Your Quality Bar</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Analyzes your real quality scores per model per workflow. Recommends the cheapest model above your threshold. Shows projected annual savings based on actual call volumes. No guessing — pure data.</div>', unsafe_allow_html=True)

    co1, co2 = st.columns([1, 1.6])

    with co1:
        quality_thresh = st.slider("Minimum Quality Threshold", min_value=0.5, max_value=0.95,
                                   value=0.75, step=0.05,
                                   help="Only recommend models that achieve at least this quality score")
        run_opt = st.button("⚙️  Analyze All Workflows", use_container_width=True)

    with co2:
        if run_opt or "opt_results" in st.session_state:
            if run_opt:
                opt_results = cost_opt.get_all_optimizations(quality_thresh)
                st.session_state["opt_results"] = opt_results
            opt_results = st.session_state.get("opt_results", [])

            if not opt_results:
                st.info("No workflows with enough call history yet. Make some tracked calls first.")
            else:
                total_savings = sum(r["savings_annual"] for r in opt_results if r["can_optimize"])
                if total_savings > 0:
                    st.markdown(f"""
                    <div style="background:rgba(0,229,160,0.08);border:1px solid rgba(0,229,160,0.3);padding:14px 18px;margin-bottom:16px;font-family:Space Mono,monospace;">
                      <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;margin-bottom:4px;">Total Projected Annual Savings</div>
                      <div style="font-size:28px;font-weight:700;color:{GREEN};">${total_savings:,.2f}</div>
                      <div style="font-size:10px;color:{MUTED2};">by switching to optimal models across {len([r for r in opt_results if r['can_optimize']])} workflow(s)</div>
                    </div>""", unsafe_allow_html=True)

                for r in opt_results:
                    can_opt   = r["can_optimize"]
                    border_c  = GREEN if can_opt else BORDER
                    badge     = f'<span style="background:{GREEN};color:{BG};font-family:Space Mono,monospace;font-size:9px;font-weight:700;padding:2px 8px;">SAVE ${r["savings_annual"]:.2f}/yr</span>' if can_opt else f'<span style="background:{SURF2};color:{MUTED};font-family:Space Mono,monospace;font-size:9px;padding:2px 8px;">ALREADY OPTIMAL</span>'

                    with st.expander(f"{'⚡' if can_opt else '✅'} {r['workflow_name']} — {r['monthly_calls']} calls/mo"):
                        if can_opt:
                            st.markdown(f"""
                            <div style="background:rgba(0,229,160,0.06);border:1px solid rgba(0,229,160,0.2);padding:12px;margin-bottom:12px;font-family:Space Mono,monospace;">
                              <div style="font-size:9px;color:{MUTED};text-transform:uppercase;">Recommendation</div>
                              <div style="font-size:13px;color:{TEXT};margin-top:4px;">
                                Switch from <span style="color:{WARN}">{r['current_model']}</span> → <span style="color:{GREEN}">{r['recommended_model']}</span>
                              </div>
                              <div style="font-size:10px;color:{MUTED2};margin-top:4px;">Save {r['savings_pct']:.0f}% · ${r['savings_annual']:.2f}/year at current volume</div>
                            </div>""", unsafe_allow_html=True)

                        # Model comparison table
                        df_models = pd.DataFrame(r["models"])
                        df_models["is_recommended"] = df_models["model"] == r["recommended_model"]
                        df_models["is_current"]     = df_models["model"] == r["current_model"]
                        df_models_display = pd.DataFrame({
                            "Model":       df_models["model"],
                            "Avg Quality": df_models["avg_quality"].apply(lambda x: f"{x:.3f}"),
                            "Avg Cost":    df_models["avg_cost"].apply(lambda x: f"${x:.6f}"),
                            "Annual Cost": df_models["annual_cost"].apply(lambda x: f"${x:.2f}"),
                            "Calls":       df_models["calls_measured"].astype(str),
                            "Source":      df_models["source"],
                            "Meets Bar":   df_models["meets_threshold"].apply(lambda x: "✓" if x else "✗"),
                        })
                        model_colors = []
                        for _, row in df_models.iterrows():
                            if row["model"] == r["recommended_model"]:
                                model_colors.append(GREEN)
                            elif row["model"] == r["current_model"]:
                                model_colors.append(WARN)
                            else:
                                model_colors.append(TEXT)
                        dark_table(df_models_display, height=210,
                                   col_widths=[140,80,90,90,50,80,60],
                                   col_colors=[TEXT,MUTED2,WARN,RED,MUTED2,MUTED2,GREEN])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 11 — WORKFLOW HEALTH SCORE
# ═══════════════════════════════════════════════════════════════════════════════
with tab11:
    st.markdown('<div class="panel-title">// Workflow Health Score — One Number That Tells You Everything</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">A single 0–100 score per workflow, like a credit score for AI. Combines ROI (30%), quality (25%), outcome coverage (20%), cost efficiency (15%), and call volume (10%). Grade A–D. Tells you exactly what to fix.</div>', unsafe_allow_html=True)

    all_scores = health.get_all_scores()

    if not all_scores:
        st.markdown(f'<div style="color:{MUTED};font-family:Space Mono,monospace;font-size:11px;padding:32px;text-align:center;border:1px dashed {BORDER}">Make some tracked API calls first to generate health scores.</div>', unsafe_allow_html=True)
    else:
        # Leaderboard row
        cols_h = st.columns(min(len(all_scores), 5))
        for i, (col, s) in enumerate(zip(cols_h, all_scores[:5])):
            col.markdown(f"""
            <div style="background:{SURF2};border:1px solid {BORDER};border-top:2px solid {s['grade_color']};padding:16px;text-align:center;">
              <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;">{s['workflow_name'][:18]}</div>
              <div style="font-size:36px;font-weight:800;color:{s['grade_color']};font-family:Syne,sans-serif;">{s['grade']}</div>
              <div style="font-family:Space Mono,monospace;font-size:18px;font-weight:700;color:{TEXT};margin-top:2px;">{s['total_score']:.0f}</div>
              <div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};margin-top:4px;">/ 100</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Detailed breakdown per workflow
        for s in all_scores:
            with st.expander(f"{s['grade']} — {s['workflow_name']} ({s['total_score']:.0f}/100)  ·  {s['top_recommendation']}"):
                dc1, dc2 = st.columns([1, 1.5])

                with dc1:
                    st.markdown('<div class="panel-title">// Score Components</div>', unsafe_allow_html=True)
                    for key, comp in s["components"].items():
                        bar_c = GREEN if comp["score"] >= 70 else (WARN if comp["score"] >= 40 else RED)
                        st.markdown(f"""
                        <div style="margin-bottom:10px;">
                          <div style="display:flex;justify-content:space-between;font-family:Space Mono,monospace;font-size:10px;margin-bottom:3px;">
                            <span style="color:{MUTED2};">{comp['label']} <span style="color:{MUTED};font-size:9px;">({comp['weight']})</span></span>
                            <span style="color:{bar_c};font-weight:700;">{comp['score']:.0f} <span style="color:{MUTED};font-size:9px;">{comp['raw']}</span></span>
                          </div>
                          <div style="background:{BORDER};height:5px;">
                            <div style="width:{comp['score']}%;height:100%;background:{bar_c};"></div>
                          </div>
                        </div>""", unsafe_allow_html=True)

                with dc2:
                    st.markdown('<div class="panel-title">// Key Metrics</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;font-family:Space Mono,monospace;">
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">ROI</div>
                        <div style="font-size:18px;color:{'#00e5a0' if s['roi_pct']>=0 else '#ff4d6d'};font-weight:700;">{s['roi_pct']:+.1f}%</div>
                      </div>
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">Avg Quality</div>
                        <div style="font-size:18px;color:{GREEN};font-weight:700;">{s['avg_quality']:.2f}</div>
                      </div>
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">Outcome Coverage</div>
                        <div style="font-size:18px;color:{BLUE};font-weight:700;">{s['outcome_rate']:.0f}%</div>
                      </div>
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">Monthly Calls</div>
                        <div style="font-size:18px;color:{TEXT};font-weight:700;">{s['monthly_calls']}</div>
                      </div>
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">Total Cost</div>
                        <div style="font-size:18px;color:{WARN};font-weight:700;">${s['total_cost']:.4f}</div>
                      </div>
                      <div style="background:{SURF};border:1px solid {BORDER};padding:12px;">
                        <div style="font-size:9px;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;">Total Value</div>
                        <div style="font-size:18px;color:{GREEN};font-weight:700;">${s['total_value']:.2f}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background:rgba(77,159,255,0.07);border-left:3px solid {BLUE};padding:10px 14px;margin-top:12px;font-family:Space Mono,monospace;font-size:11px;color:{TEXT};">
                      → {s['top_recommendation']}
                    </div>""", unsafe_allow_html=True)

        # Radar chart comparing all workflows
        if len(all_scores) >= 2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="panel-title">// Radar Comparison — All Workflows</div>', unsafe_allow_html=True)
            
            categories = ["ROI","Quality","Coverage","Cost Eff","Volume"]
            fig_radar = go.Figure()
            colors_radar = [GREEN, BLUE, WARN, RED, MUTED2]
            for i, s in enumerate(all_scores[:5]):
                vals = [
                    s["components"]["roi"]["score"],
                    s["components"]["quality"]["score"],
                    s["components"]["coverage"]["score"],
                    s["components"]["cost_eff"]["score"],
                    s["components"]["volume"]["score"],
                ]
                fig_radar.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    name=s["workflow_name"][:20],
                    line=dict(color=colors_radar[i % len(colors_radar)], width=2),
                    fillcolor=colors_radar[i % len(colors_radar)],
                    opacity=0.15
                ))
            fig_radar.update_layout(
                paper_bgcolor=SURF, plot_bgcolor=SURF,
                polar=dict(
                    bgcolor=SURF2,
                    radialaxis=dict(visible=True, range=[0,100], gridcolor=BORDER,
                                    tickfont=dict(color=MUTED2, size=8)),
                    angularaxis=dict(gridcolor=BORDER, tickfont=dict(color=TEXT, size=10))
                ),
                legend=dict(bgcolor=SURF2, bordercolor=BORDER, font=dict(color=MUTED2, size=9)),
                margin=dict(l=60,r=60,t=30,b=30), height=350
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 12 — TEAM ROI DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab12:
    st.markdown('<div class="panel-title">// Team ROI Dashboard — AI Spend & Value by Department</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-bar">Tag any workflow with a team name. See total ROI broken down by department. Identify which teams get most value from AI — and which are burning budget without results.</div>', unsafe_allow_html=True)

    tr1, tr2 = st.columns([1, 1.6])

    with tr1:
        st.markdown('<div class="panel-title">// Tag a Workflow</div>', unsafe_allow_html=True)
        db_wfs3 = get_db().execute("SELECT workflow_id, name FROM workflows").fetchall()
        wf_map3 = {f"{w['name']}": w['workflow_id'] for w in db_wfs3}

        if wf_map3:
            with st.form("tag_form", clear_on_submit=True):
                tag_wf   = st.selectbox("Workflow", list(wf_map3.keys()))
                team_nm  = st.text_input("Team Name", placeholder="e.g. Customer Success")
                dept_nm  = st.text_input("Department", placeholder="e.g. Operations")
                owner_nm = st.text_input("Owner", placeholder="e.g. Sarah Chen")
                if st.form_submit_button("👥  Tag Workflow", use_container_width=True):
                    if team_nm:
                        result = team_roi.tag_workflow(wf_map3[tag_wf], team_nm, dept_nm, owner_nm)
                        st.success(f"✓ Tagged '{tag_wf}' → Team: {team_nm}")
                    else:
                        st.error("Team name required")
        else:
            st.info("Register workflows in the sidebar first.")

        # Quick tag presets
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel-title">// Quick Tag — Demo Setup</div>', unsafe_allow_html=True)
        if st.button("⚡  Auto-Tag Seeded Workflows", use_container_width=True):
            presets = [
                ("wf_support", "Customer Success", "Operations"),
                ("wf_sales",   "Revenue",          "Sales"),
                ("wf_fraud",   "Risk & Compliance","Finance"),
                ("wf_code",    "Engineering",      "Product"),
                ("wf_docs",    "Legal",            "Operations"),
            ]
            for wid, team, dept in presets:
                try:
                    team_roi.tag_workflow(wid, team, dept)
                except Exception:
                    pass
            st.success("✓ All 5 workflows tagged to teams. Refresh the right panel.")

    with tr2:
        st.markdown('<div class="panel-title">// ROI by Team (Last 30 Days)</div>', unsafe_allow_html=True)
        team_data = team_roi.get_team_breakdown()

        if not team_data:
            st.markdown(f'<div style="border:1px dashed {BORDER};padding:32px;text-align:center;font-family:Space Mono,monospace;font-size:11px;color:{MUTED};">Tag workflows to teams on the left.<br>Use <span style="color:{GREEN}">⚡ Auto-Tag</span> to see a demo instantly.</div>', unsafe_allow_html=True)
        else:
            # Summary bar chart
            df_teams = pd.DataFrame(team_data)
            fig_teams = go.Figure()
            fig_teams.add_trace(go.Bar(
                name="Cost", x=df_teams["team"], y=df_teams["total_cost"],
                marker_color=WARN, opacity=0.85
            ))
            fig_teams.add_trace(go.Bar(
                name="Value", x=df_teams["team"], y=df_teams["total_value"],
                marker_color=GREEN, opacity=0.85
            ))
            fig_teams.update_layout(
                paper_bgcolor=SURF, plot_bgcolor=SURF,
                font=dict(family="Space Mono, monospace", color=MUTED2, size=10),
                margin=dict(l=44,r=16,t=36,b=44), barmode="group", height=240,
                xaxis=dict(gridcolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
                yaxis=dict(gridcolor=BORDER, tickfont=dict(color=MUTED2, size=9)),
                title=dict(text="Cost vs Value by Team", font=dict(size=10, color=MUTED)),
                legend=dict(bgcolor=SURF2, bordercolor=BORDER, font=dict(color=MUTED2, size=9))
            )
            st.plotly_chart(fig_teams, use_container_width=True, config={"displayModeBar": False})

            # Team cards
            for t in team_data:
                roi_c_t = GREEN if t["roi_pct"] >= 0 else RED
                best_wf  = t["best_workflow"]
                worst_wf = t["worst_workflow"]
                st.markdown(f"""
                <div style="background:{SURF2};border:1px solid {BORDER};border-left:3px solid {roi_c_t};padding:14px 16px;margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                    <div>
                      <div style="font-family:Syne,sans-serif;font-size:14px;font-weight:700;color:{TEXT};">👥 {t['team']}</div>
                      {f'<div style="font-family:Space Mono,monospace;font-size:9px;color:{MUTED};">{t["department"]} {("· " + t["owner"]) if t["owner"] else ""}</div>' if t["department"] else ""}
                    </div>
                    <div style="font-family:Space Mono,monospace;font-size:22px;font-weight:700;color:{roi_c_t};">{t['roi_pct']:+.1f}%</div>
                  </div>
                  <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;font-family:Space Mono,monospace;font-size:9px;">
                    <div><div style="color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Workflows</div><div style="color:{TEXT};font-size:13px;font-weight:700;">{t['workflows']}</div></div>
                    <div><div style="color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Calls</div><div style="color:{TEXT};font-size:13px;font-weight:700;">{t['monthly_calls']}</div></div>
                    <div><div style="color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Cost</div><div style="color:{WARN};font-size:13px;font-weight:700;">${t['total_cost']:.4f}</div></div>
                    <div><div style="color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Value</div><div style="color:{GREEN};font-size:13px;font-weight:700;">${t['total_value']:.2f}</div></div>
                    <div><div style="color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;">Quality</div><div style="color:{BLUE};font-size:13px;font-weight:700;">{t['avg_quality']:.2f}</div></div>
                  </div>
                  {f'<div style="margin-top:8px;font-family:Space Mono,monospace;font-size:9px;display:flex;gap:16px;"><span style="color:{MUTED};">Best: <span style="color:{GREEN}">{best_wf["name"]} ({best_wf["roi"]:+.0f}%)</span></span><span style="color:{MUTED};">Worst: <span style="color:{RED}">{worst_wf["name"]} ({worst_wf["roi"]:+.0f}%)</span></span></div>' if best_wf and worst_wf else ""}
                </div>""", unsafe_allow_html=True)