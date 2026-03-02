# 🔬 ROI Lens — AI Accountability Agent

**Mistral Worldwide Hackathon 2026 · Track: Developer Tools & Software Lifecycle**

> *Here is the pain: developers ship AI features with no way to know if they are working, breaking, or burning money. Here is what ROI Lens does about it: five autonomous agents watch every AI call in production, react to triggers automatically, and take action before problems become disasters. Here is what changes for developers: you stop flying blind.*

---

## The Pain

Every developer who has shipped an AI-powered feature into production knows this feeling.

You open the Mistral invoice on the first of the month. The number is higher than last month. You don't know why. You pull up your logs. You see API calls. You see token counts. You cannot see whether any of those calls actually helped a user, closed a deal, caught a fraud, or fixed a bug.

You have shipped an AI feature. You have no idea if it is working.

This is not a logging problem. You have logs. This is a **signal problem** — your logs tell you what happened but not whether it mattered.

Meanwhile three things are quietly going wrong:

**1. A workflow's quality score has been declining for 11 days.**
Nobody noticed. The outputs started getting worse after a system prompt change two weeks ago. Users are complaining to support. Your team thinks it's a product issue. It's an AI issue. But there's no metric that caught it.

**2. You're using `mistral-large-latest` for a task that `mistral-small-latest` handles equally well.**
It's costing you $340/month more than necessary. Nobody ran the comparison because it felt like too much work to set up a proper test.

**3. One workflow crossed the monthly budget limit four days ago.**
The alert went to an email inbox nobody checks. Calls are still running. The bill is still growing.

These are not edge cases. These are the normal operating conditions of any team running AI in production.

---

## What ROI Lens Does About It

ROI Lens is an accountability agent layer that wraps any Mistral AI deployment. It does not replace your existing code. It sits between your application and the Mistral API and runs five autonomous agents in the background.

**It is not a chat interface. The agents react to data triggers and take action without being asked.**

Here is what fires automatically, with no human in the loop:

---

### Agent 1 — The Quality Evaluator
**Trigger:** Every single API call, immediately after the response arrives.

**What it does:** A second lightweight Mistral model reads the response and scores it from 0.0 to 1.0 across four dimensions — task completion, business relevance, accuracy, and efficiency. This score is saved to the database alongside the call.

**Why it matters for developers:** You now have a continuous quality signal on every AI feature in production. Not just "did it return a response" but "was the response actually good." When a system prompt change breaks quality, you see it in the score trend the same day — not two weeks later when users start complaining.

**What changes for developers:** You have a quality time series for every AI feature. Deployments that hurt quality show up as a score drop. Prompt improvements show up as a score rise. You can correlate AI quality changes with user behaviour metrics for the first time.

---

### Agent 2 — The Kill-Switch Engine
**Trigger:** Automatically runs every time the dashboard loads. Also callable programmatically.

**What it does:** Scans every AI workflow that has had at least three calls in the last seven days. For each one, it computes cost vs recorded business value and fires a severity-classified alert if something is wrong.

The exact logic from the codebase:

```
ROI < -50%   → CRITICAL  "Losing money fast. Pause immediately."
ROI <   0%   → WARNING   "Not yet profitable. Review model and prompt."
Quality < 0.6 → WARNING  "Outputs unreliable. Fix system prompt."
Outcomes < 20% → INFO    "Blind spot. Add outcome tracking."
```

**Why it matters for developers:** This is the difference between finding out a workflow is broken at the end-of-month review versus finding out the same day it crosses a threshold. The agent fires the alert. The developer does not have to remember to check.

**What changes for developers:** Broken or unprofitable AI features get flagged before they become a line item in a budget cut conversation. The agent creates the audit trail that shows when the problem started and what the specific threshold violation was.

---

### Agent 3 — The Anomaly Detector
**Trigger:** Fires on demand but operates on live production data from the last 72 hours.

**What it does:** Learns the statistical baseline for each workflow from the rolling 30-day window of real API calls — average cost per call, average latency, average quality score. Then scans recent calls and flags any that deviate beyond a configurable sigma threshold (default 2.5 standard deviations).

It detects three anomaly types:

- **Cost spike** — a call cost significantly more than normal (example: $0.0042 vs baseline of $0.0008 — that is 4.2σ above normal)
- **Latency spike** — a call took significantly longer than normal (indicates model degradation or network issue)
- **Quality drop** — a call scored significantly below the workflow's quality baseline

**Why it matters for developers:** Anomalies in production AI systems often appear before they cause visible user impact. A cost spike can mean a prompt is sending unexpectedly large context. A latency spike can mean the model tier changed. A quality drop can mean a dependency silently broke. The anomaly detector surfaces these before they become incidents.

**What changes for developers:** You get a 72-hour rolling anomaly log for every AI feature. The agent computes the z-score of each deviation so you know exactly how unusual the event is — not just that it happened.

---

### Agent 4 — The Budget Guardian
**Trigger:** Fires automatically every time a new API call is logged for a budget-tracked workflow.

**What it does:** Computes current spend against budget in real time from the database. Calculates daily burn rate from actual historical calls. Projects days remaining at current rate. Fires severity-classified alerts at user-configured thresholds (default 80% of budget used).

The system also supports one-click pause — which stops calls from being made for a workflow when it crosses its limit.

**Why it matters for developers:** AI cost spikes in production are not gradual. A change in how a feature is used (users sending longer messages, a new integration triggering more calls) can double your monthly bill in three days. Budget Guardian catches this at 80% and gives you time to respond, not at 120% when the damage is done.

**What changes for developers:** AI features have enforced cost ceilings. The CFO conversation about surprise AI bills becomes a dashboard screenshot conversation instead.

---

### Agent 5 — The Quality Evaluator (Exec Report Generator)
**Trigger:** Fires on demand. Reads live database state to produce the report.

**What it does:** Passes current dashboard data — all workflow costs, ROI figures, quality trends, alert states — to Mistral and asks it to write a plain-English executive brief. The report covers total spend, best performing workflows, worst performing workflows, and one concrete recommendation. It writes from your actual data, not a template.

**Why it matters for developers:** The biggest soft cost in running AI features is the time developers spend writing status reports for leadership. This agent eliminates that. The report is generated from live data and is accurate to the minute it is generated.

**What changes for developers:** You stop translating technical metrics into business language manually. The agent does it.

---

## The Full Feature Set

Beyond the five agents, ROI Lens includes eight additional tools that developers use manually to investigate, optimise, and plan:

### 📊 Dashboard
Live KPI view of every AI workflow: total cost, total value, net ROI, call volume, average quality. Workflow table with ROI colour coding. 14-day call volume trend. Model cost breakdown. Full audit trail of every API call with timestamp, cost, quality score, and linked business outcome.

### 🚀 Live Demo (Tracked API Call)
Make a real Mistral API call from the dashboard. See the cost calculated to six decimal places the instant the response arrives. Get a call ID to record outcomes against. Every call goes through the same tracking layer as production calls.

### 💰 Record Outcome
The mechanism that closes the ROI loop. After an AI call produces a real business result — a ticket resolved, a fraud caught, a sale closed — you paste the call ID and enter the dollar value. The system calculates ROI for that specific call and saves it permanently. Five outcome types built in: time saved, conversion, fraud prevented, reply received, bug caught.

### 🔬 A/B Model Tester
Select any two Mistral models. Enter a prompt. Both calls fire in parallel via `asyncio.gather`. Side-by-side comparison of cost, latency, input tokens, and output tokens. The system calculates savings percentage and outputs a direct recommendation. Every test result is saved to history. This is how developers answer "should we switch models for this workflow" with data instead of opinion.

### 🔮 ROI Forecaster
Linear regression on real historical call data. Projects cost, value, and ROI for any horizon from 7 to 90 days. Combined chart of historical actuals and projected values with a today marker. Confidence score based on data volume and variance. Everything computed from the actual database — no invented trends.

### 📚 Smart Prompt Library
Save prompts with titles and tags. The system tracks which saved prompts produce the highest quality scores and ROI over real usage. Prompts are ranked by a composite performance score (60% quality, 40% ROI signal). Developers stop rewriting prompts from memory and start building from what actually worked.

### ⚙️ Cost Optimizer
Analyses real quality scores per model per workflow from the database. Recommends the cheapest model that still meets a quality threshold the developer sets. Shows projected annual savings at current call volumes. If no real data exists for a model on a given workflow, it estimates from known quality ceilings.

### 🏆 Workflow Health Score
Single score from 0 to 100 per workflow. Five weighted components: ROI performance (30%), output quality (25%), outcome coverage (20%), cost efficiency trend (15%), call volume consistency (10%). Letter grade A through D. Radar chart comparing all workflows. One specific fix recommendation per workflow based on its lowest-scoring component.

### 👥 Team ROI Dashboard
Tag workflows to team names and departments. Full ROI breakdown per team from real database joins: total cost, total value, net ROI, quality average, best workflow, worst workflow. Bar chart comparing teams. This is the answer to budget debates where every team claims their AI is valuable. The data replaces the argument.

---

## What "Agents React to Triggers" Looks Like in Practice

The hackathon brief asks for agents that react to triggers and take action. Here is exactly how that works in ROI Lens for a real development team over a real week:

**Monday morning:** Developer merges a prompt change for the Customer Support workflow.

**Monday afternoon:** The Quality Evaluator fires on every call going through the updated prompt. Quality scores for the workflow drop from 0.81 average to 0.58 average across 23 calls.

**Monday evening:** The Kill-Switch Engine fires on the next dashboard load. Severity: WARNING. Reason: "Average quality score is 0.58 — outputs may be unreliable." Recommendation: "Improve system prompt, add examples, or switch to larger model."

**Tuesday morning:** Developer sees the alert. Checks the A/B Test tab. Runs the old prompt vs new prompt against the same model. Old prompt scores 0.84. New prompt scores 0.61. The regression is confirmed. Rollback takes 10 minutes.

**Wednesday:** A new integration starts sending unusually long messages to the Fraud Detection workflow. Cost per call spikes from $0.002 to $0.009 — 3.8 standard deviations above baseline.

**Wednesday afternoon:** Anomaly Detector flags the spike. Developer investigates the integration. Finds that a connected system started prepending full customer history to every prompt. Fixes the truncation. Cost returns to baseline.

**Friday:** The Sales Email workflow hits 82% of its monthly budget with 12 days left in the month. Budget Guardian fires. Developer adjusts the workflow to only trigger on leads above a certain score threshold. Burn rate drops. Budget is no longer on track to overrun.

None of these required the developer to check anything. The agents caught the problems and surfaced them.

---

## Integration — Two Lines of Code

The entire tracking layer activates with one change to existing code. No architecture changes. No new infrastructure.

**Before:**
```python
from mistralai import Mistral
response = Mistral(api_key=key).chat.complete(
    model="mistral-large-latest",
    messages=messages
)
text = response.choices[0].message.content
```

**After:**
```python
import httpx
result  = httpx.post("http://localhost:8000/api/chat", json={
    "messages":            messages,
    "workflow_id":         "wf_code_review",
    "workflow_name":       "Code Review Assistant",
    "model":               "mistral-large-latest",
    "expected_value_usd":  20.0
}).json()
text    = result["content"]   # identical to before
call_id = result["call_id"]   # new: permanent ID for outcome recording
```

**Record the outcome when it happens:**
```python
httpx.post("http://localhost:8000/api/outcomes", json={
    "call_id":             call_id,
    "outcome_type":        "bug_caught",
    "outcome_value_usd":   20.0,
    "outcome_description": "Security vulnerability caught before merge"
})
```

From this point forward, every call through that endpoint is tracked, quality-scored, anomaly-monitored, budget-tracked, and included in the kill-switch scan. All five agents are active with no further configuration.

---

## The Audit Trail

Every API call stored in ROI Lens creates a permanent record:

```
call_id          — unique identifier, links to outcomes
workflow_id      — which feature or workflow made this call
model            — which Mistral model was used
input_tokens     — exact token count (input)
output_tokens    — exact token count (output)
cost_usd         — calculated to 8 decimal places
latency_ms       — round-trip time in milliseconds
quality_score    — 0.0 to 1.0, scored by evaluator model
quality_reason   — text explanation of the score
created_at       — UTC timestamp
```

This is a compliance-ready record of every AI decision made through the system. If a regulator asks "what AI was involved in this decision and how good was the output" — the answer is in the database with a timestamp.

---

## Quick Start

### 1. Install

```bash
git clone <your-repo>
cd roi-lens-streamlit
pip install -r requirements.txt
```

### 2. Add API Key

```bash
cp .env.example .env
# Set: MISTRAL_API_KEY=your_key_here
```

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

> No API key? The app loads with 90 pre-seeded demo calls across 5 workflows. All 5 agents run on the demo data immediately.

### 4. Verify

```bash
python3 -c "
from database import init_db
from roi_engine import ROIEngine
init_db()
d = ROIEngine().get_dashboard()
alerts = ROIEngine().get_kill_switch_alerts()
print('Calls:', d['summary']['total_calls'])
print('ROI:  ', d['summary']['overall_roi_pct'], '%')
print('Alerts:', len(alerts))
"
```

---

## File Structure

```
roi-lens-streamlit/
│
├── app.py                 Streamlit dashboard — 12 pages, sidebar navigation
│                          All 5 agents surface their output here
│
├── roi_engine.py          Kill-Switch Engine + Outcome Linker
│                          Core ROI calculation logic
│                          get_kill_switch_alerts() — the trigger-based agent
│
├── advanced_features.py   Budget Guardian, Anomaly Detector, A/B Tester,
│                          ROI Forecaster, Prompt Optimizer
│                          detect_anomalies() — statistical trigger agent
│
├── power_features.py      Smart Prompt Library, Cost Optimizer,
│                          Workflow Health Score, Team ROI Dashboard
│
├── mistral_wrapper.py     API interception layer
│                          Quality Evaluator agent runs here on every call
│                          Exec Report Generator
│
├── database.py            SQLite schema — 7 tables
│                          Auto-seeds 90 realistic demo calls on first run
│
├── requirements.txt
└── .env.example
```

---

## Demo Flow for Judges (3 Minutes)

**Minute 1 — The agents are already working**

Open the dashboard. Point to the Kill-Switch tab — there are already alerts on the seeded data. One workflow is flagged WARNING. Show the specific reason and recommendation. Point to the audit trail at the bottom of the Dashboard page — every call logged with cost and quality score. This is the agent output running on demo data.

**Minute 2 — Trigger an agent live**

Go to Live Demo. Run a Fraud Detection call. Watch the cost appear: `$0.0048`. Copy the call ID. Go to Record Outcome. Enter `$500`. Click record. Go back to Dashboard and refresh. The ROI numbers update in real time. Go to Anomaly Detector and click Detect — show the baseline it learned from the seeded data.

**Minute 3 — Show the developer tools**

Go to A/B Test. Run `mistral-large-latest` vs `mistral-small-latest` on the same prompt. Show both completing in parallel. Show the savings percentage — typically 70-88% cheaper. Go to Health Score. Show every workflow with a letter grade and the radar comparison chart. Go to Budget Guardian and set a limit — show it calculating days remaining from real data immediately.

---

## Requirements

```
streamlit==1.40.2
plotly==5.24.1
pandas==2.2.3
httpx==0.27.2
python-dotenv==1.0.1
```

Python 3.9 or higher required.

---

## The Story in One Paragraph

A developer ships an AI feature. It works on Tuesday. By Thursday, something changed — a prompt edit, a model update, a new integration — and the quality dropped. Nobody noticed for two weeks because there was no metric watching it. ROI Lens watches it. The Quality Evaluator scores every call. The Kill-Switch Engine scans for degradation every time the dashboard loads. The Anomaly Detector flags the day the cost pattern changed. The Budget Guardian caught the overspend before it doubled. The developer spends 10 minutes fixing a prompt instead of six weeks explaining to a CFO why the AI investment is not showing returns. That is the problem. That is the solution. That is what changes.

---

*Mistral Worldwide Hackathon 2026 · February 28 – March 1, 2026*
