"""
Database layer — SQLite for hackathon simplicity, swap for Postgres in prod
"""

import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "./roi_lens.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()
    
    db.executescript("""
        CREATE TABLE IF NOT EXISTS workflows (
            workflow_id     TEXT PRIMARY KEY,
            name            TEXT NOT NULL,
            description     TEXT,
            hourly_value_usd REAL DEFAULT 50.0,
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS api_calls (
            call_id         TEXT PRIMARY KEY,
            workflow_id     TEXT NOT NULL,
            workflow_name   TEXT NOT NULL,
            model           TEXT NOT NULL,
            input_tokens    INTEGER DEFAULT 0,
            output_tokens   INTEGER DEFAULT 0,
            cost_usd        REAL DEFAULT 0.0,
            latency_ms      INTEGER DEFAULT 0,
            expected_value_usd REAL,
            quality_score   REAL,           -- 0-1 from evaluator
            quality_reason  TEXT,
            metadata        TEXT,           -- JSON
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS outcomes (
            outcome_id      TEXT PRIMARY KEY,
            call_id         TEXT NOT NULL,
            outcome_type    TEXT NOT NULL,
            outcome_value_usd REAL NOT NULL,
            outcome_description TEXT,
            verified        INTEGER DEFAULT 0,
            created_at      TEXT NOT NULL,
            FOREIGN KEY (call_id) REFERENCES api_calls(call_id)
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            log_id          TEXT PRIMARY KEY,
            event_type      TEXT NOT NULL,
            workflow_id     TEXT,
            call_id         TEXT,
            data            TEXT,           -- JSON
            created_at      TEXT NOT NULL
        );
    """)
    
    # Seed demo workflows if empty
    count = db.execute("SELECT COUNT(*) FROM workflows").fetchone()[0]
    if count == 0:
        _seed_demo_data(db)
    
    db.commit()
    print("✅ Database initialized")


def _seed_demo_data(db):
    """Insert demo workflows and sample calls for a rich initial dashboard"""
    from datetime import datetime, timedelta
    import json, uuid, random
    
    workflows = [
        ("wf_support", "Customer Support AI", "Auto-draft replies to support tickets", 45.0),
        ("wf_sales", "Sales Email Drafter", "Generate personalized outreach emails", 80.0),
        ("wf_fraud", "Fraud Detection", "Flag suspicious transactions in real-time", 200.0),
        ("wf_docs", "Document Summarizer", "Summarize legal/compliance documents", 60.0),
        ("wf_code", "Code Review Assistant", "Review PRs and suggest improvements", 90.0),
    ]
    
    now = datetime.utcnow()
    
    for wf_id, name, desc, hourly in workflows:
        db.execute(
            "INSERT OR IGNORE INTO workflows VALUES (?, ?, ?, ?, ?)",
            (wf_id, name, desc, hourly, (now - timedelta(days=30)).isoformat())
        )
    
    # Pricing per 1K tokens (input, output) for common Mistral models
    MODEL_PRICING = {
        "mistral-large-latest":    (0.002, 0.006),
        "mistral-small-latest":    (0.0002, 0.0006),
        "open-mistral-7b":         (0.00025, 0.00025),
    }
    
    OUTCOME_TYPES = {
        "wf_support": ("time_saved", 8.0),
        "wf_sales":   ("conversion", 150.0),
        "wf_fraud":   ("fraud_prevented", 500.0),
        "wf_docs":    ("time_saved", 12.0),
        "wf_code":    ("time_saved", 20.0),
    }
    
    # Generate 90 calls over last 14 days
    for i in range(90):
        wf_id, wf_name, _, _ = random.choice(workflows)
        model = random.choice(list(MODEL_PRICING.keys()))
        input_tk = random.randint(200, 2000)
        output_tk = random.randint(100, 800)
        ip, op = MODEL_PRICING[model]
        cost = (input_tk / 1000 * ip) + (output_tk / 1000 * op)
        latency = random.randint(400, 3000)
        call_id = str(uuid.uuid4())
        ts = (now - timedelta(days=random.randint(0, 14), hours=random.randint(0, 23))).isoformat()
        quality = round(random.uniform(0.55, 0.98), 2)
        
        db.execute(
            """INSERT INTO api_calls VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (call_id, wf_id, wf_name, model, input_tk, output_tk,
             round(cost, 6), latency, None, quality, "Auto-evaluated", "{}", ts)
        )
        
        # 70% of calls have a recorded outcome
        if random.random() < 0.7:
            otype, base_val = OUTCOME_TYPES[wf_id]
            val = base_val * random.uniform(0.5, 1.5)
            db.execute(
                "INSERT INTO outcomes VALUES (?,?,?,?,?,?,?)",
                (str(uuid.uuid4()), call_id, otype, round(val, 2),
                 f"Auto-recorded: {otype}", 1,
                 (now - timedelta(days=random.randint(0, 7))).isoformat())
            )
    
    db.commit()
    print("🌱 Demo data seeded")
