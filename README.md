# 🔬 ROI Lens — The AI Accountability Layer

> *Every company is spending on AI. Nobody knows if it's working. ROI Lens closes that loop — automatically.*

**Mistral Worldwide Hackathon 2026 · Track: Anything Goes**

Built with **Mistral AI · Streamlit · Plotly · SQLite**

---

## 📸 What It Looks Like

```
┌─────────────────────────────────────────────────────────────────┐
│  ROI LENS                                    [Deploy]           │
│  AI Accountability Layer                                        │
├─────────────────────────────────────────────────────────────────┤
│  📊 Dashboard  🚀 Live Demo  💰 Record Outcome  ⚠️ Alerts  📝 Report │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TOTAL API COST    VALUE GENERATED    NET ROI    API CALLS      │
│  $0.1929           $5,976.52          +3098%     91             │
│                                                                 │
│  ┌── Workflow ROI ──────────────────────────────────────────┐   │
│  │ Fraud Detection        18 calls   +6911%   $3,757        │   │
│  │ Sales Email Drafter    15 calls   +14256%  $1,694        │   │
│  │ Code Review Assistant  21 calls   -43%     $287          │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 The Problem

The AI industry's #1 unsolved challenge in 2025–2026:

```
AI Call Made ──→ Response Generated ──→  ???  ──→ Business Result
      ↑                                              ↑
  Tracked ✓                                  Nobody tracks this ✗
```

Companies spend thousands on LLM API calls. They see outputs.
They never see if those outputs created revenue, saved costs, or caught fraud.
CFOs cut AI budgets. Engineers can't prove value. Projects die.

**ROI Lens fixes this.**

---

## 💡 What It Does

ROI Lens is a **middleware accountability layer** that wraps any Mistral API deployment and answers the one question every CFO asks:

### *"Is our AI actually making us money?"*

```
Your App ──→ ROI Lens ──→ Mistral API ──→ ROI Lens ──→ Your App
                 │                              │
                 └──────── SQLite DB ───────────┘
                              │
                    Cost + Value + ROI + Audit
```

---

## 🏗️ Architecture — 5 Layers

### Layer 1 — Cost Tracker
Every API call is intercepted and logged with:
- Token count (input + output)
- Cost in USD (calculated per model's current pricing)
- Latency in milliseconds
- Workflow that triggered the call
- Full audit trail with timestamps

### Layer 2 — Quality Evaluator
A second lightweight Mistral model runs **in the background** after every call and scores output quality 0.0–1.0 across:
- Task completion
- Business value
- Accuracy & safety
- Efficiency

No manual review needed. Fully automated.

### Layer 3 — Outcome Linker *(the novel part)*
When a real business result happens downstream, you record it against the original `call_id`:

```python
# A lead converted after the AI-drafted email → record it
POST /api/outcomes
{
  "call_id": "abc-123",
  "outcome_type": "conversion",
  "outcome_value_usd": 150.00,
  "description": "Lead booked a demo call"
}
```

Now you have: **Cost per call** + **Value per call** = **Real ROI**

### Layer 4 — Kill-Switch Engine
Automatically scans all workflows and flags underperformers:

| Severity | Trigger | Action |
|----------|---------|--------|
| 🔴 Critical | ROI < -50% | Pause immediately |
| 🟡 Warning | ROI < 0% | Review & optimize |
| 🔵 Info | <20% outcomes tracked | Add tracking |

### Layer 5 — Exec Report Generator
One click → Mistral writes a plain-English CFO brief in 3 paragraphs. No manual reporting. No spreadsheets.

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone <your-repo-url>
cd roi-lens-streamlit
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your API Key

```bash
# Option A: .env file (permanent)
cp .env.example .env
# Edit .env and add: MISTRAL_API_KEY=your_key_here

# Option B: paste directly in the app sidebar (no file needed)
```

Get your key at → [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys)

### 4. Run

```bash
streamlit run app.py
```

Open **http://localhost:8501** 🎉

> **No API key?** The app loads instantly with 90 pre-seeded demo calls across 5 workflows — full dashboard experience without any setup.

---

## 📁 File Structure

```
roi-lens-streamlit/
│
├── app.py                  ← Main Streamlit dashboard (all 5 tabs)
│
├── mistral_wrapper.py      ← Mistral API client with cost tracking
│                             Intercepts every call, logs tokens & cost
│                             Runs background quality evaluation
│                             Generates executive reports
│
├── roi_engine.py           ← Core ROI analytics engine
│                             Per-workflow ROI calculations
│                             Kill-switch alert logic
│                             Outcome linking & verification
│                             Dashboard data aggregation
│
├── database.py             ← SQLite schema + demo seed data
│                             4 tables: workflows, api_calls,
│                             outcomes, audit_log
│                             Auto-seeds 90 realistic demo calls
│
├── requirements.txt        ← Python dependencies
├── .env.example            ← Environment variable template
├── start.sh                ← One-command launcher
└── README.md               ← This file
```

---

## 🖥️ The 5 Dashboard Tabs

### 📊 Tab 1 — Dashboard
The main overview screen. Shows everything at a glance.

| Section | What You See |
|---------|-------------|
| KPI Row | Total cost, value generated, net ROI%, total calls, avg quality |
| Workflow Table | Per-workflow: calls, ROI%, cost, value, quality — color coded |
| ROI Bar Chart | Visual ROI comparison across all workflows |
| 14-Day Trend | Daily call volume with line overlay |
| Model Breakdown | Donut chart — cost split by model |
| Outcome Types | Horizontal bar — value by outcome category |
| Audit Trail | Last 20 API calls with cost, value, and timestamp |

---

### 🚀 Tab 2 — Live Demo
Make a real tracked Mistral API call directly from the dashboard.

**Inputs:**
- Workflow (Customer Support, Sales, Fraud Detection, Code Review, Doc Summary)
- Model (mistral-large-latest, mistral-small-latest, open-mistral-7b, codestral)
- Prompt (auto-fills based on workflow)
- Expected Business Value ($)
- System Prompt (optional)

**Output:** Full AI response + tracking chips showing `call_id`, `cost`, `tokens`, `latency`

---

### 💰 Tab 3 — Record Outcome
Link a business result to an AI call to close the ROI loop.

**After running a tracked call:**
1. Copy the `call_id` from the Live Demo chips
2. Paste it here
3. Select outcome type
4. Enter the business value in USD
5. Add a description
6. Click **Record Outcome**

**Live ROI Preview** shows cost vs value vs net ROI for the last call in real time.

**Outcome Types Reference:**

| Type | Example | Typical Value |
|------|---------|--------------|
| `time_saved` | Agent avoided 8 min manual work | $2–$50 |
| `conversion` | Lead converted after AI-drafted email | $50–$10,000 |
| `fraud_prevented` | Transaction flagged and blocked | $100–$100,000 |
| `reply_received` | Customer replied to AI support draft | $5–$500 |
| `bug_caught` | Code review caught production bug | $20–$200 |
| `custom` | Any domain-specific value | Anything |

---

### ⚠️ Tab 4 — Kill-Switch Alerts
Automatically identifies workflows burning money or flying blind.

```
🔴 CRITICAL  Code Review Assistant
             ROI is -43% — not yet profitable
             → Review prompt efficiency, consider cheaper model

🔵 INFO      Document Summarizer
             Only 18% of calls have recorded outcomes
             → Add outcome tracking for accurate ROI visibility
```

Includes a Cost vs Value bar chart comparing all flagged workflows.

---

### 📝 Tab 5 — Exec Report
One click → Mistral writes a 3-paragraph CFO brief.

```
Example output:

"Your AI systems have generated $5,976 in measurable business value
against $0.19 in API costs this period, representing a 3,098% ROI.
Fraud Detection and Sales Email Drafter are the top performers...

The Code Review workflow shows a -43% ROI and should be reviewed.
Switching to mistral-small-latest for this workflow would reduce
costs by 70% with minimal quality impact...

Recommendation: Expand the Fraud Detection workflow by 3x — at
current conversion rates, this represents $15,000/month in
prevented losses at under $0.50 in API costs."
```

---

## 🔌 Integration — Drop Into Any Existing App

**Before (direct Mistral call):**
```python
response = client.chat(model="mistral-large-latest", messages=[...])
```

**After (ROI-tracked call — 3 lines changed):**
```python
import httpx

response = httpx.post("http://localhost:8000/api/chat", json={
    "messages": [...],
    "workflow_id": "wf_support",
    "workflow_name": "Customer Support AI",
    "model": "mistral-large-latest",
    "expected_value_usd": 8.0
}).json()

call_id = response["call_id"]   # use this to record outcomes later
content = response["content"]   # the actual AI response
```

**Record a business outcome when it happens:**
```python
httpx.post("http://localhost:8000/api/outcomes", json={
    "call_id": call_id,
    "outcome_type": "time_saved",
    "outcome_value_usd": 8.0,
    "description": "Ticket resolved without human escalation",
    "verified": True
})
```

**JavaScript / Node.js:**
```javascript
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    messages: [{ role: 'user', content: prompt }],
    workflow_id: 'wf_sales',
    workflow_name: 'Sales Email Drafter',
    model: 'mistral-large-latest',
    expected_value_usd: 150.0
  })
});
const { call_id, content, cost_usd } = await response.json();
```

---

## 💾 Database Schema

```sql
-- All registered AI workflows
workflows (
    workflow_id       TEXT PRIMARY KEY,
    name              TEXT,
    description       TEXT,
    hourly_value_usd  REAL,
    created_at        TEXT
)

-- Every Mistral API call, fully logged
api_calls (
    call_id           TEXT PRIMARY KEY,
    workflow_id       TEXT,
    workflow_name     TEXT,
    model             TEXT,
    input_tokens      INTEGER,
    output_tokens     INTEGER,
    cost_usd          REAL,
    latency_ms        INTEGER,
    expected_value_usd REAL,
    quality_score     REAL,       -- 0.0-1.0 from evaluator model
    quality_reason    TEXT,
    metadata          TEXT,       -- JSON
    created_at        TEXT
)

-- Business outcomes linked to calls
outcomes (
    outcome_id        TEXT PRIMARY KEY,
    call_id           TEXT,       -- FK → api_calls
    outcome_type      TEXT,
    outcome_value_usd REAL,
    outcome_description TEXT,
    verified          INTEGER,    -- 0 or 1
    created_at        TEXT
)
```

---

## 💰 Mistral Model Pricing (Built-in)

ROI Lens automatically calculates cost for all models:

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| mistral-large-latest | $0.002 | $0.006 |
| mistral-small-latest | $0.0002 | $0.0006 |
| open-mistral-7b | $0.00025 | $0.00025 |
| codestral-latest | $0.001 | $0.003 |
| voxtral-mini-latest | $0.0002 | $0.0006 |

---

## 🧪 Test Inputs to Verify Everything Works

### Test 1 — Customer Support
- **Workflow:** Customer Support AI
- **Model:** mistral-small-latest
- **Prompt:** `Draft a professional reply to a customer upset about a 2-week delayed shipment. Keep it under 80 words.`
- **Expected Value:** $8

### Test 2 — Fraud Detection
- **Workflow:** Fraud Detection
- **Model:** mistral-large-latest
- **Prompt:** `Analyze for fraud: User 9921, $4,899 charge, Lagos Nigeria, card registered Ohio USA, 3am local time, new device, 5 failed attempts before success. Respond in JSON: {is_fraud, confidence, reason}`
- **Expected Value:** $500

### Test 3 — Sales Email
- **Workflow:** Sales Email Drafter
- **Model:** mistral-small-latest
- **Prompt:** `Write a cold outreach email to a fintech startup CTO about our AI fraud detection API. Under 80 words.`
- **Expected Value:** $150

After each test → go to **💰 Record Outcome** → paste the `call_id` → record the business value → refresh dashboard to see ROI update live.

---

## 🏆 Why This Wins

### Solves the #1 Business Problem
AI ROI is the most frequently cited blocker to enterprise AI adoption in 2025. Every company needs this.

### Technical Innovation
- **Dual-model architecture** — large model does the task, small model judges the output
- **Causal outcome linking** — connects AI actions to business results with a unique ID chain
- **Automated kill-switch** — no human needed to spot money-losing workflows

### Immediately Monetizable
- SaaS layer on top of any LLM stack
- Works with every Mistral model
- 2-line integration — zero friction to adopt

### Perfect Demo
- Loads instantly with rich seeded data
- Live Mistral calls visible in real time
- Full end-to-end story in under 2 minutes

---

## 📋 Requirements

```
streamlit==1.40.2
plotly==5.24.1
pandas==2.2.3
httpx==0.27.2
python-dotenv==1.0.1
```

Python 3.9+ required.

---

## 🔧 Environment Variables

```bash
# Required for live mode
MISTRAL_API_KEY=your_mistral_api_key_here

# Optional — defaults to ./roi_lens.db
DB_PATH=./roi_lens.db
```

---

## 🌐 Hackathon Links

- **Hackathon Platform:** [hackiterate.com](https://hackiterate.com)
- **Mistral API Console:** [console.mistral.ai](https://console.mistral.ai)
- **Free Credits (HuggingFace):** Join the hackathon org for free API credits
- **Discord:** All updates posted in the official hackathon Discord

---

## 👥 Built At

**Mistral Worldwide Hackathon 2026**
February 28 – March 1, 2026
Track: Anything Goes

Partners: Weights & Biases · NVIDIA · AWS · ElevenLabs · HuggingFace · Supercell

---

## 📄 License

MIT — use freely, build on it, win with it.

---

*"The companies that survive the AI wave won't be the ones who used the most AI. They'll be the ones who knew which AI was worth keeping."*
