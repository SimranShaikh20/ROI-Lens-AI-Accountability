"""
ROI Engine
Core analytics: cost tracking, outcome linking, kill-switch alerts, dashboard aggregation
"""

import json
import uuid
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from database import get_db


class ROIEngine:
    
    def get_dashboard(self) -> Dict:
        """Aggregate dashboard metrics"""
        db = get_db()
        
        # Overall totals
        totals = db.execute("""
            SELECT 
                COUNT(*) as total_calls,
                SUM(cost_usd) as total_cost,
                SUM(input_tokens + output_tokens) as total_tokens,
                AVG(latency_ms) as avg_latency,
                AVG(quality_score) as avg_quality
            FROM api_calls
        """).fetchone()
        
        total_value = db.execute(
            "SELECT SUM(outcome_value_usd) FROM outcomes"
        ).fetchone()[0] or 0.0
        
        total_cost = totals["total_cost"] or 0.0
        roi_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        # Per-workflow breakdown
        workflows = db.execute("""
            SELECT 
                a.workflow_id,
                a.workflow_name,
                COUNT(a.call_id) as call_count,
                SUM(a.cost_usd) as cost_usd,
                AVG(a.quality_score) as avg_quality,
                AVG(a.latency_ms) as avg_latency,
                COALESCE(SUM(o.outcome_value_usd), 0) as value_usd
            FROM api_calls a
            LEFT JOIN outcomes o ON a.call_id = o.call_id
            GROUP BY a.workflow_id, a.workflow_name
            ORDER BY value_usd DESC
        """).fetchall()
        
        workflow_data = []
        for w in workflows:
            cost = w["cost_usd"] or 0.0
            value = w["value_usd"] or 0.0
            roi = ((value - cost) / cost * 100) if cost > 0 else 0
            workflow_data.append({
                "workflow_id": w["workflow_id"],
                "workflow_name": w["workflow_name"],
                "call_count": w["call_count"],
                "cost_usd": round(cost, 4),
                "value_usd": round(value, 2),
                "roi_pct": round(roi, 1),
                "avg_quality": round(w["avg_quality"] or 0, 2),
                "avg_latency_ms": int(w["avg_latency"] or 0),
                "is_roi_positive": roi > 0
            })
        
        # Daily cost trend (last 14 days)
        trend = db.execute("""
            SELECT 
                DATE(created_at) as date,
                SUM(cost_usd) as cost,
                COUNT(*) as calls
            FROM api_calls
            WHERE created_at >= DATE('now', '-14 days')
            GROUP BY DATE(created_at)
            ORDER BY date ASC
        """).fetchall()
        
        # Model usage breakdown
        models = db.execute("""
            SELECT 
                model,
                COUNT(*) as calls,
                SUM(cost_usd) as cost,
                SUM(input_tokens) as input_tokens,
                SUM(output_tokens) as output_tokens
            FROM api_calls
            GROUP BY model
            ORDER BY cost DESC
        """).fetchall()
        
        # Outcome types breakdown
        outcome_types = db.execute("""
            SELECT 
                outcome_type,
                COUNT(*) as count,
                SUM(outcome_value_usd) as total_value
            FROM outcomes
            GROUP BY outcome_type
            ORDER BY total_value DESC
        """).fetchall()
        
        return {
            "summary": {
                "total_calls": totals["total_calls"] or 0,
                "total_cost_usd": round(total_cost, 4),
                "total_value_usd": round(total_value, 2),
                "overall_roi_pct": round(roi_pct, 1),
                "total_tokens": totals["total_tokens"] or 0,
                "avg_latency_ms": int(totals["avg_latency"] or 0),
                "avg_quality_score": round(totals["avg_quality"] or 0, 2),
                "net_value_usd": round(total_value - total_cost, 2)
            },
            "workflows": workflow_data,
            "daily_trend": [
                {"date": r["date"], "cost": round(r["cost"], 4), "calls": r["calls"]}
                for r in trend
            ],
            "model_breakdown": [
                {
                    "model": r["model"],
                    "calls": r["calls"],
                    "cost_usd": round(r["cost"] or 0, 4),
                    "input_tokens": r["input_tokens"] or 0,
                    "output_tokens": r["output_tokens"] or 0
                }
                for r in models
            ],
            "outcome_types": [
                {
                    "type": r["outcome_type"],
                    "count": r["count"],
                    "total_value_usd": round(r["total_value"] or 0, 2)
                }
                for r in outcome_types
            ],
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def get_workflow_roi(self, workflow_id: str) -> Dict:
        """Detailed ROI breakdown for one workflow"""
        db = get_db()
        
        calls = db.execute("""
            SELECT a.*, COALESCE(o.outcome_value_usd, 0) as outcome_value,
                   o.outcome_type, o.outcome_description
            FROM api_calls a
            LEFT JOIN outcomes o ON a.call_id = o.call_id
            WHERE a.workflow_id = ?
            ORDER BY a.created_at DESC
            LIMIT 50
        """, (workflow_id,)).fetchall()
        
        return {
            "workflow_id": workflow_id,
            "calls": [dict(c) for c in calls]
        }
    
    def get_recent_calls(self, limit: int = 20) -> List[Dict]:
        """Recent API calls with costs"""
        db = get_db()
        rows = db.execute("""
            SELECT a.call_id, a.workflow_name, a.model, a.cost_usd,
                   a.latency_ms, a.input_tokens, a.output_tokens,
                   a.quality_score, a.created_at,
                   COALESCE(o.outcome_value_usd, 0) as outcome_value,
                   o.outcome_type
            FROM api_calls a
            LEFT JOIN outcomes o ON a.call_id = o.call_id
            ORDER BY a.created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        
        return [dict(r) for r in rows]
    
    def get_kill_switch_alerts(self) -> List[Dict]:
        """Identify ROI-negative workflows that should be reviewed or killed"""
        db = get_db()
        
        workflows = db.execute("""
            SELECT 
                a.workflow_id,
                a.workflow_name,
                COUNT(a.call_id) as call_count,
                SUM(a.cost_usd) as total_cost,
                COALESCE(SUM(o.outcome_value_usd), 0) as total_value,
                AVG(a.quality_score) as avg_quality,
                COUNT(o.outcome_id) as outcomes_recorded
            FROM api_calls a
            LEFT JOIN outcomes o ON a.call_id = o.call_id
            WHERE a.created_at >= DATE('now', '-7 days')
            GROUP BY a.workflow_id, a.workflow_name
            HAVING call_count >= 3
        """).fetchall()
        
        alerts = []
        for w in workflows:
            cost = w["total_cost"] or 0.0
            value = w["total_value"] or 0.0
            roi = ((value - cost) / cost * 100) if cost > 0 else 0
            quality = w["avg_quality"] or 0
            outcome_rate = w["outcomes_recorded"] / w["call_count"] if w["call_count"] > 0 else 0
            
            severity = None
            reason = ""
            recommendation = ""
            
            if roi < -50:
                severity = "critical"
                reason = f"ROI is {roi:.1f}% — losing money fast"
                recommendation = "Pause this workflow immediately and re-evaluate the use case"
            elif roi < 0:
                severity = "warning"
                reason = f"ROI is {roi:.1f}% — not yet profitable"
                recommendation = "Review prompt efficiency, consider cheaper model or fewer calls"
            elif quality < 0.6:
                severity = "warning"
                reason = f"Average quality score is {quality:.2f} — outputs may be unreliable"
                recommendation = "Improve system prompt, add examples, or switch to larger model"
            elif outcome_rate < 0.2:
                severity = "info"
                reason = f"Only {outcome_rate:.0%} of calls have recorded outcomes"
                recommendation = "Add outcome tracking to get accurate ROI visibility"
            
            if severity:
                alerts.append({
                    "workflow_id": w["workflow_id"],
                    "workflow_name": w["workflow_name"],
                    "severity": severity,
                    "reason": reason,
                    "recommendation": recommendation,
                    "roi_pct": round(roi, 1),
                    "total_cost_usd": round(cost, 4),
                    "total_value_usd": round(value, 2),
                    "call_count": w["call_count"],
                    "avg_quality": round(quality, 2)
                })
        
        # Sort: critical first
        severity_order = {"critical": 0, "warning": 1, "info": 2}
        alerts.sort(key=lambda x: severity_order.get(x["severity"], 3))
        
        return alerts
    
    def record_outcome(
        self,
        call_id: str,
        outcome_type: str,
        outcome_value_usd: float,
        outcome_description: str,
        verified: bool = False
    ) -> Dict:
        """Record a business outcome and link it to an API call"""
        db = get_db()
        
        # Verify call exists
        call = db.execute(
            "SELECT call_id, workflow_id FROM api_calls WHERE call_id = ?",
            (call_id,)
        ).fetchone()
        
        if not call:
            raise ValueError(f"Call {call_id} not found")
        
        outcome_id = str(uuid.uuid4())
        db.execute(
            """INSERT INTO outcomes VALUES (?,?,?,?,?,?,?)""",
            (
                outcome_id, call_id, outcome_type, outcome_value_usd,
                outcome_description, 1 if verified else 0,
                datetime.utcnow().isoformat()
            )
        )
        db.commit()
        
        return {
            "outcome_id": outcome_id,
            "call_id": call_id,
            "workflow_id": call["workflow_id"],
            "outcome_type": outcome_type,
            "value_usd": outcome_value_usd,
            "status": "recorded"
        }
    
    async def evaluate_output_async(
        self,
        call_id: str,
        messages: List,
        response: str,
        workflow_id: str
    ):
        """Background task: evaluate output quality and update DB"""
        try:
            from mistral_wrapper import MistralWrapper
            wrapper = MistralWrapper()
            eval_result = await wrapper.evaluate_output_quality(
                original_messages=messages,
                ai_response=response,
                workflow_id=workflow_id
            )
            
            db = get_db()
            db.execute(
                """UPDATE api_calls 
                   SET quality_score = ?, quality_reason = ?
                   WHERE call_id = ?""",
                (
                    eval_result.get("score", 0.7),
                    eval_result.get("reason", ""),
                    call_id
                )
            )
            db.commit()
        except Exception as e:
            print(f"Background evaluator failed for {call_id}: {e}")
