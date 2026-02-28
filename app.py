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

engine  = get_engine()
mistral = MistralWrapper()

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Dashboard", "🚀  Live Demo",
    "💰  Record Outcome", "⚠️   Kill-Switch Alerts", "📝  Exec Report"
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