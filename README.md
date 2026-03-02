<div align="center">

```
██████╗  ██████╗ ██╗    ██╗     ███████╗███╗   ██╗███████╗
██╔══██╗██╔═══██╗██║    ██║     ██╔════╝████╗  ██║██╔════╝
██████╔╝██║   ██║██║    ██║     █████╗  ██╔██╗ ██║███████╗
██╔══██╗██║   ██║██║    ██║     ██╔══╝  ██║╚██╗██║╚════██║
██║  ██║╚██████╔╝██║    ███████╗███████╗██║ ╚████║███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝    ╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝
```

# 🔬 AI Accountability Layer

**5 Autonomous Agents · 12 Live Dashboards · Zero Blind Spots**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-FF6B35?style=for-the-badge)](https://mistral.ai)
[![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

*Mistral Worldwide Hackathon 2026 · Track: Developer Tools & Software Lifecycle*

---

**[✨ Features](#-features) · [🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#%EF%B8%8F-architecture) · [🤖 The 5 Agents](#-the-5-autonomous-agents) · [📊 Dashboard](#-12-dashboard-pages) · [🔌 Integration](#-integration)**

</div>

---

## 💥 The Problem

Every team shipping AI features into production faces the same invisible crisis:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE AI BLACK BOX PROBLEM                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Your App  ──────────────────────────────►  Mistral API       │
│                                                                 │
│   ✅ You know: the call was made                                │
│   ✅ You know: tokens were consumed                             │
│   ✅ You know: you were billed                                  │
│                                                                 │
│   ❌ You DON'T know: was the output any good?                   │
│   ❌ You DON'T know: did it create business value?              │
│   ❌ You DON'T know: which workflow is costing too much?        │
│   ❌ You DON'T know: when quality started dropping?             │
│   ❌ You DON'T know: are you using the right model?             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

Meanwhile, **three silent disasters** are happening right now at most AI teams:

| 🔴 Silent Disaster | What's Actually Happening |
|---|---|
| **Quality Decay** | A prompt change 11 days ago broke output quality. Users are complaining. Your team thinks it's a product bug. |
| **Model Overspend** | You're using `mistral-large` for tasks `mistral-small` handles equally well. That's $340/month wasted. |
| **Budget Overrun** | A workflow crossed its monthly limit 4 days ago. The alert email went unread. Costs are still climbing. |

> *These aren't edge cases. This is the normal operating condition of every team running AI in production without an accountability layer.*

---

## ✨ The Solution

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          ROI LENS IN ACTION                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Your App  ──►  [ ROI LENS LAYER ]  ──►  Mistral API                 │
│                         │                                               │
│              ┌──────────┴──────────────────────┐                       │
│              │                                 │                       │
│              ▼                                 ▼                       │
│     📊 Every call logged              🤖 Quality scored               │
│     💰 Cost calculated                ⚠️  Anomalies flagged            │
│     🔗 Outcomes linked                💸 Budget tracked                │
│     📈 ROI computed                   🔔 Alerts triggered              │
│              │                                                          │
│              └──────────────────────────────────────────────────────►  │
│                              Live Dashboard                             │
│                    "Which AI is making money? Which isn't?"            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**ROI Lens** is a middleware accountability agent that wraps any Mistral AI deployment. It intercepts every API call, runs 5 autonomous agents in the background, and surfaces everything through a live 12-page dashboard.

**Chat alone won't qualify — ROI Lens is all agents. Every agent reacts to triggers. Every agent takes action without being asked.**

---

## 🏗️ Architecture

### System Overview

```
╔═══════════════════════════════════════════════════════════════════════╗
║                        ROI LENS ARCHITECTURE                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌──────────────┐    ┌─────────────────────────────────────────────┐  ║
║  │  Your App /  │    │              ROI LENS LAYER                 │  ║
║  │  Integration │───►│                                             │  ║
║  └──────────────┘    │  ┌─────────────┐   ┌───────────────────┐   │  ║
║                       │  │mistral_     │   │   roi_engine.py   │   │  ║
║                       │  │wrapper.py   │   │                   │   │  ║
║                       │  │             │   │ • ROI Calculator  │   │  ║
║                       │  │ • Intercept │   │ • Kill-Switch     │   │  ║
║                       │  │ • Cost Calc │   │ • Outcome Linker  │   │  ║
║                       │  │ • Quality   │   │ • Alert Engine    │   │  ║
║                       │  │   Scorer    │   └────────┬──────────┘   │  ║
║                       │  └──────┬──────┘            │              │  ║
║                       │         │                    │              │  ║
║                       │         ▼                    ▼              │  ║
║                       │  ┌─────────────────────────────────────┐   │  ║
║                       │  │           SQLite Database           │   │  ║
║                       │  │                                     │   │  ║
║                       │  │  api_calls │ outcomes │ workflows   │   │  ║
║                       │  │  budgets   │ ab_tests │ teams       │   │  ║
║                       │  └─────────────────────────────────────┘   │  ║
║                       │         │                                   │  ║
║                       └─────────┼───────────────────────────────────┘  ║
║                                 │                                        ║
║                                 ▼                                        ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │                    STREAMLIT DASHBOARD                           │   ║
║  │   📊 Dashboard  🚀 Live Demo  💰 Outcomes  ⚠️ Kill-Switch        │   ║
║  │   📝 Reports    💸 Budget     🔬 A/B Test  🔮 Forecaster         │   ║
║  │   📚 Library    ⚙️ Optimizer  🏆 Health    👥 Team ROI            │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
║                                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐   ║
║  │                    MISTRAL API                                   │   ║
║  │   mistral-large-latest  │  mistral-small-latest  │  codestral   │   ║
║  └──────────────────────────────────────────────────────────────────┘   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Data Flow — Every Single API Call

```
  Step 1          Step 2          Step 3          Step 4          Step 5
    │               │               │               │               │
    ▼               ▼               ▼               ▼               ▼
┌───────┐      ┌─────────┐     ┌─────────┐    ┌─────────┐    ┌─────────┐
│ App   │      │ ROI     │     │ Mistral │    │ ROI     │    │ Agents  │
│ sends │─────►│ Lens    │────►│   API   │───►│ Lens    │───►│  fire   │
│request│      │intercept│     │processes│    │ logs &  │    │ on the  │
│       │      │& logs   │     │  call   │    │ scores  │    │ result  │
└───────┘      └─────────┘     └─────────┘    └─────────┘    └─────────┘
                   │                               │
                   ▼                               ▼
             call_id created              ┌─────────────────┐
             cost calculated             │  Quality Agent  │
             latency measured            │  scores output  │
                                         │  0.0 → 1.0      │
                                         └─────────────────┘
```

### The ROI Loop — Connecting AI to Business Value

```
                         THE ROI LOOP
                         ════════════

  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │   1. API CALL           2. TRACKING                     │
  │   ┌──────────┐         ┌──────────────────────────┐    │
  │   │ Mistral  │         │ call_id: abc-123          │    │
  │   │ responds │────────►│ cost:   $0.0048           │    │
  │   │          │         │ tokens: 1,240             │    │
  │   └──────────┘         │ latency: 842ms            │    │
  │                        │ quality: 0.87             │    │
  │                        └───────────┬──────────────┘    │
  │                                    │                     │
  │                                    ▼                     │
  │   4. ROI CALCULATED     3. OUTCOME LINKED               │
  │   ┌──────────────┐      ┌──────────────────────────┐   │
  │   │ ROI = 10,316%│      │ call_id: abc-123          │   │
  │   │              │◄─────│ type: fraud_prevented     │   │
  │   │ Cost: $0.0048│      │ value: $500               │   │
  │   │ Value: $500  │      │ verified: true            │   │
  │   └──────────────┘      └──────────────────────────┘   │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

---

## 🤖 The 5 Autonomous Agents

> *These are not chatbots. They don't wait to be asked. They react to triggers and take action.*

---

### Agent 1 — 🎯 Quality Evaluator

```
  TRIGGER: Every API call · immediately after response arrives
  ════════════════════════════════════════════════════════════

  API Call ──► Mistral responds ──► Quality Agent fires
                                           │
                              ┌────────────┘
                              ▼
                   ┌─────────────────────┐
                   │  Scoring Dimensions  │
                   ├─────────────────────┤
                   │ ✓ Task Completion   │
                   │ ✓ Business Value    │
                   │ ✓ Accuracy          │
                   │ ✓ Efficiency        │
                   └──────────┬──────────┘
                              │
                              ▼
                   Score: 0.0 ─────────── 1.0
                          BAD            GREAT
                              │
                              ▼
                   Saved to DB with call_id
                   Powers health scores, trends, alerts
```

**What changes:** You see quality trends per workflow per day. A prompt change that hurts quality shows up **that same day** — not two weeks later when users start complaining.

---

### Agent 2 — ⚠️ Kill-Switch Engine

```
  TRIGGER: Fires on every dashboard load · also callable programmatically
  ═══════════════════════════════════════════════════════════════════════

  Scans ALL workflows with 3+ calls in last 7 days
                    │
         ┌──────────┼──────────┬──────────┐
         ▼          ▼          ▼          ▼
      ROI < -50%  ROI < 0%  Quality   Outcomes
                            < 0.6     < 20%
         │          │          │          │
         ▼          ▼          ▼          ▼
      🔴 CRITICAL  🟡 WARNING 🟡 WARNING  🔵 INFO
      "Pause now"  "Review"  "Fix prompt" "Add tracking"
         │
         ▼
  Specific recommendation generated per workflow
  Alert surfaced on dashboard instantly
```

**What changes:** Broken or money-losing AI features get caught **the same day** they cross a threshold — not at end-of-month budget review.

---

### Agent 3 — 🚨 Anomaly Detector

```
  TRIGGER: Scans last 72 hours of production calls on demand
  ════════════════════════════════════════════════════════════

  30-day rolling window per workflow
           │
           ▼
  Baseline learned from real data:
  ┌─────────────────────────────────────────┐
  │  avg_cost:    $0.0008 per call          │
  │  avg_latency: 644ms                     │
  │  avg_quality: 0.81                      │
  └────────────────┬────────────────────────┘
                   │
                   ▼
  Recent call arrives:
  ┌─────────────────────────────────────────┐
  │  cost: $0.0042  ← 4.2σ above baseline  │ 🔴 COST SPIKE
  │  latency: 2,100ms ← 3.1σ above        │ 🟡 LATENCY SPIKE
  │  quality: 0.41  ← 2.8σ below          │ 🔴 QUALITY DROP
  └─────────────────────────────────────────┘
                   │
                   ▼
  Flagged with exact deviation + call_id
  Developer knows WHAT broke and WHEN
```

**What changes:** You catch a runaway prompt sending 10x too many tokens **before** it doubles your monthly bill. You catch quality degradation **before** users churn.

---

### Agent 4 — 💸 Budget Guardian

```
  TRIGGER: Fires on every new API call logged for budget-tracked workflows
  ═════════════════════════════════════════════════════════════════════════

  Developer sets:                    System computes:
  ┌─────────────────────┐           ┌─────────────────────────────┐
  │ Budget: $50.00      │           │ Spent:     $38.20           │
  │ Period: 30 days     │──────────►│ Remaining: $11.80           │
  │ Alert at: 80%       │           │ Burn rate: $1.27/day        │
  └─────────────────────┘           │ Days left: 9.3 days         │
                                    │ Status:    ⚠️ WARNING (76%)  │
                                    └─────────────────────────────┘

  Alert thresholds:
  0%──────────────────80%────────95%────100%──────────►
  ✅ Healthy          ⚠️ Warn    🔴 Limit  💀 Over
```

**What changes:** AI costs have enforced ceilings. You get a warning at 80% — while there's still time to act. Not at 120% when the damage is done.

---

### Agent 5 — 📝 Executive Report Generator

```
  TRIGGER: On demand · reads live database state at generation time
  ═══════════════════════════════════════════════════════════════════

  Live DB data ──► Mistral prompt ──► Plain English CFO Brief
       │
       ▼
  ┌─────────────────────────────────────────────────────────┐
  │  Data fed to Mistral:                                   │
  │  • Total AI spend this period                          │
  │  • ROI per workflow (green/red)                        │
  │  • Best performing workflow + ROI%                     │
  │  • Worst performing workflow + reason                  │
  │  • Quality trends                                      │
  │  • Kill-switch alerts active                           │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │  OUTPUT: 3-paragraph executive brief                   │
  │                                                         │
  │  "Our AI portfolio generated $5,847 in business value  │
  │   this month against $0.19 in API costs, representing  │
  │   a 3,000,000%+ ROI. The Fraud Detection workflow..."  │
  └─────────────────────────────────────────────────────────┘
```

**What changes:** The developer stops writing status reports. The agent writes them from live data in seconds.

---

## 📊 12 Dashboard Pages

```
╔═══════════════════════════════════════════════════════════════════╗
║                    NAVIGATION OVERVIEW                            ║
╠═══════╦═══════════════════╦══════════════════════════════════════╣
║ Icon  ║ Page              ║ What You See                         ║
╠═══════╬═══════════════════╬══════════════════════════════════════╣
║  📊   ║ Dashboard         ║ KPIs, ROI table, charts, audit trail ║
║  🚀   ║ Live Demo         ║ Real tracked Mistral call + cost     ║
║  💰   ║ Record Outcome    ║ Link AI call → business value ($)    ║
║  ⚠️   ║ Kill-Switch       ║ Auto-flagged failing workflows       ║
║  📝   ║ Exec Report       ║ AI-written CFO brief from live data  ║
║  💸   ║ Budget Guard      ║ Spend limits + burn rate tracking    ║
║  🔬   ║ A/B Model Test    ║ Parallel model comparison + savings  ║
║  🔮   ║ Forecaster        ║ Linear regression cost/ROI forecast  ║
║  📚   ║ Prompt Library    ║ Save + rank prompts by real ROI      ║
║  ⚙️   ║ Cost Optimizer    ║ Cheapest model above quality bar     ║
║  🏆   ║ Health Score      ║ 0-100 grade per workflow + radar     ║
║  👥   ║ Team ROI          ║ Department-level ROI breakdown       ║
╚═══════╩═══════════════════╩══════════════════════════════════════╝
```

### Dashboard — KPI Overview

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ TOTAL COST  │ │   VALUE     │ │   NET ROI   │ │ API CALLS   │ │   QUALITY   │
│             │ │ GENERATED   │ │             │ │             │ │    SCORE    │
│  $0.1929    │ │  $5,976.52  │ │ +3,098,420% │ │     91      │ │     77%     │
│ 137k tokens │ │ Net $5,976  │ │ ROI positive│ │ avg 1,032ms │ │ evaluator   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### Workflow Health Score — The AI Credit Score

```
  Each workflow gets scored across 5 dimensions:

  ┌────────────────────────────────────────────────────────────┐
  │   ROI Performance    ████████████████████░░░░  30% weight  │
  │   Output Quality     ████████████████░░░░░░░░  25% weight  │
  │   Outcome Coverage   ████████████░░░░░░░░░░░░  20% weight  │
  │   Cost Efficiency    ████████████████████░░░░  15% weight  │
  │   Call Volume        ████████░░░░░░░░░░░░░░░░  10% weight  │
  └────────────────────────────────────────────────────────────┘

  Combined → Single Score → Letter Grade

  90-100: A  🟢  Excellent — expand this workflow
  70-89:  B  🔵  Good — minor optimizations available
  50-69:  C  🟡  Fair — specific issues to address
  0-49:   D  🔴  Poor — needs immediate attention
```

---

## 🔌 Integration

### It Takes 2 Lines to Change

**Before ROI Lens (standard Mistral call):**

```python
from mistralai import Mistral

client   = Mistral(api_key="your_key")
response = client.chat.complete(
    model    = "mistral-large-latest",
    messages = [{"role": "user", "content": "Your prompt here"}]
)
text = response.choices[0].message.content
# ❌ No cost tracking
# ❌ No quality scoring
# ❌ No ROI measurement
# ❌ No anomaly detection
# ❌ No budget enforcement
```

**After ROI Lens (full accountability — same result):**

```python
import httpx

result  = httpx.post("http://localhost:8000/api/chat", json={
    "messages":            [{"role": "user", "content": "Your prompt here"}],
    "workflow_id":         "wf_fraud_detection",
    "workflow_name":       "Fraud Detection",
    "model":               "mistral-large-latest",
    "expected_value_usd":  500.0,               # what success is worth
    "metadata":            {"transaction_id": "TXN-99821"}
}).json()

text    = result["content"]    # ✅ identical to before
call_id = result["call_id"]    # ✅ NEW: permanent audit ID
cost    = result["cost_usd"]   # ✅ NEW: exact cost this call
# ✅ Quality scored automatically in background
# ✅ Budget checked automatically
# ✅ Anomaly detection running
```

**Record the business outcome when it happens:**

```python
# Minutes or hours later, when a real result occurs:
httpx.post("http://localhost:8000/api/outcomes", json={
    "call_id":             call_id,
    "outcome_type":        "fraud_prevented",
    "outcome_value_usd":   4899.00,         # the fraud amount blocked
    "outcome_description": "Transaction flagged, $4,899 fraud prevented",
    "verified":            True
})

# ROI is now calculated automatically:
# ($4,899 value - $0.0048 cost) / $0.0048 cost = 102,062,400% ROI
```

---

## 🌍 Real World Use Cases

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      INDUSTRY APPLICATIONS                              ║
╠══════════════════╦═══════════════════════════════╦═════════════════════╣
║ Industry         ║ AI Use Case                   ║ Tracked Outcome     ║
╠══════════════════╬═══════════════════════════════╬═════════════════════╣
║ 🏦 Banking       ║ Fraud detection on transact.  ║ $ fraud prevented   ║
║ 🛒 E-Commerce    ║ Personalised sales emails     ║ conversion value    ║
║ 💼 SaaS          ║ Support ticket AI drafts      ║ agent time saved    ║
║ 🏥 Healthcare    ║ Clinical note assistance      ║ compliance audit    ║
║ ⚖️  Legal         ║ Contract risk analysis        ║ risk $ avoided      ║
║ 💻 Dev Tools     ║ Code review automation        ║ bugs caught value   ║
╚══════════════════╩═══════════════════════════════╩═════════════════════╝
```

### A Real Week in Production (with ROI Lens)

```
MONDAY
  10:00 AM │ Developer merges prompt change for Customer Support workflow
  2:00  PM │ 🎯 Quality Agent flags: score dropped from 0.81 → 0.58
  2:01  PM │ ⚠️  Kill-Switch alerts: "Quality 0.58 — outputs unreliable"
  3:00  PM │ Developer sees alert, runs A/B test: old vs new prompt
  3:05  PM │ A/B result: old prompt 0.84 quality, new prompt 0.61
  3:15  PM │ Rollback deployed. Crisis resolved in 3 hours, not 2 weeks.

WEDNESDAY
  9:00  AM │ New integration starts prepending full history to prompts
  9:01  AM │ 🚨 Anomaly Detector: cost spike 4.2σ above baseline
  9:30  AM │ Developer traces to integration. Truncation fix deployed.
  9:35  AM │ Cost returns to baseline. Monthly bill unaffected.

FRIDAY
  4:00  PM │ Sales Email workflow hits 82% of monthly budget
  4:01  PM │ 💸 Budget Guardian fires WARNING alert
  4:30  PM │ Developer adjusts trigger threshold. Overrun avoided.
  5:00  PM │ CFO asks "what's our AI ROI this week?"
  5:02  PM │ 📝 Exec Report generated. Answer ready in 90 seconds.
```

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.9+
pip (package manager)
Mistral API key (free at console.mistral.ai)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/SimranShaikh20/roi-lens
cd roi-lens

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
echo "MISTRAL_API_KEY=your_key_here" >> .env

# 4. Launch
streamlit run app.py
```

Open **http://localhost:8501** — the dashboard loads instantly with 90 pre-seeded demo calls across 5 workflows. All 5 agents are active immediately.

### No API Key? No Problem.

The app loads in **full demo mode** with pre-seeded data:
- 90 realistic API calls across 5 workflows
- Real ROI calculations from seeded outcomes
- Kill-switch alerts already firing on demo data
- Health scores, anomaly baselines, forecasts — all working

```bash
# Verify everything is working
python3 -c "
from database import init_db
from roi_engine import ROIEngine
init_db()
d = ROIEngine().get_dashboard()
a = ROIEngine().get_kill_switch_alerts()
print('✅ Calls loaded:  ', d['summary']['total_calls'])
print('✅ Overall ROI:   ', d['summary']['overall_roi_pct'], '%')
print('✅ Active alerts: ', len(a))
"
```

---

## 📁 File Structure

```
roi-lens/
│
├── 🎯 app.py                    Main dashboard — 12 pages, sidebar nav
│                                1,400+ lines · zero placeholder values
│
├── 🤖 roi_engine.py             Kill-Switch Engine + ROI Calculator
│                                get_kill_switch_alerts() ← trigger agent
│                                record_outcome() ← closes ROI loop
│
├── ⚡ advanced_features.py       Budget Guardian ← spend trigger agent
│                                Anomaly Detector ← statistical trigger agent
│                                A/B Tester ← parallel model comparison
│                                ROI Forecaster ← linear regression engine
│
├── 💡 power_features.py         Smart Prompt Library ← performance ranking
│                                Cost Optimizer ← cheapest model finder
│                                Workflow Health Score ← 0-100 AI grade
│                                Team ROI Dashboard ← dept breakdown
│
├── 🔗 mistral_wrapper.py        API intercept layer
│                                Quality Evaluator agent ← fires every call
│                                Executive Report Generator
│
├── 🗄️  database.py              SQLite schema — 7 tables
│                                Auto-seeds 90 demo calls on first run
│
├── 📋 requirements.txt
├── 🔑 .env.example
└── 🚀 start.sh
```

---

## 📦 Database Schema

```sql
-- Every AI call ever made — the permanent audit trail
api_calls (
    call_id          TEXT PRIMARY KEY,   -- unique receipt ID
    workflow_id      TEXT,               -- which feature
    model            TEXT,               -- which Mistral model
    input_tokens     INTEGER,            -- exact token count
    output_tokens    INTEGER,            -- exact token count
    cost_usd         REAL,               -- calculated to 8 decimal places
    latency_ms       INTEGER,            -- round trip time
    quality_score    REAL,               -- 0.0 to 1.0, auto-scored
    quality_reason   TEXT,               -- why that score
    created_at       TEXT                -- UTC timestamp
)

-- Business results linked to calls
outcomes (
    outcome_id         TEXT PRIMARY KEY,
    call_id            TEXT,             -- links to api_calls
    outcome_type       TEXT,             -- fraud_prevented, conversion, etc
    outcome_value_usd  REAL,             -- $ value of the outcome
    verified           BOOLEAN,          -- human confirmed?
    created_at         TEXT
)

-- Plus: workflows · budgets · ab_tests · prompt_library · workflow_teams
```

---

## ⚙️ Requirements

```
streamlit==1.40.2      # Dashboard framework
plotly==5.24.1         # Interactive charts
pandas==2.2.3          # Data processing
httpx==0.27.2          # Async HTTP client
python-dotenv==1.0.1   # Environment config
```

---

## 🏆 Why This Wins

```
╔══════════════════════════════════════════════════════════════════╗
║                   HACKATHON JUDGING CRITERIA                     ║
╠══════════════════════╦═══════════════════════════════════════════╣
║ Criterion            ║ How ROI Lens Delivers                     ║
╠══════════════════════╬═══════════════════════════════════════════╣
║ Agents not chat      ║ 5 trigger-based agents, zero chat UI      ║
║ React to triggers    ║ Quality/cost/budget/anomaly all auto-fire ║
║ Take action          ║ Alerts, pauses, recommendations generated ║
║ Developer lifecycle  ║ Covers deploy → monitor → optimise → report║
║ Real problem         ║ Every AI team has this exact problem       ║
║ Story: pain → fix    ║ Full week-in-production narrative          ║
║ Production ready     ║ SQLite → Postgres swap = 1 line           ║
╚══════════════════════╩═══════════════════════════════════════════╝
```



<div align="center">

## The One-Sentence Pitch

*ROI Lens is the missing accountability layer for enterprise AI — five autonomous agents that watch every Mistral API call, catch problems before they become disasters, and prove to your CFO exactly which AI features are worth keeping.*

---

**Built with ❤️ for Mistral Worldwide Hackathon 2026**

*"The companies that survive the AI wave won't be the ones who used the most AI.*
*They'll be the ones who knew which AI was worth keeping."*

</div>