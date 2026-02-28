"""
Mistral API Wrapper
Intercepts every call, tracks tokens/cost, logs to DB
"""

import os
import time
import uuid
import json
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional
from database import get_db

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_BASE_URL = "https://api.mistral.ai/v1"

# Current Mistral pricing per 1K tokens (input, output) USD
MODEL_PRICING: Dict[str, tuple] = {
    "mistral-large-latest":         (0.002,   0.006),
    "mistral-large-2411":           (0.002,   0.006),
    "mistral-medium-latest":        (0.0027,  0.0081),
    "mistral-small-latest":         (0.0002,  0.0006),
    "mistral-small-2409":           (0.0002,  0.0006),
    "open-mistral-7b":              (0.00025, 0.00025),
    "open-mixtral-8x7b":            (0.0007,  0.0007),
    "open-mixtral-8x22b":           (0.002,   0.006),
    "open-codestral-mamba":         (0.00025, 0.00025),
    "codestral-latest":             (0.001,   0.003),
    "voxtral-mini-latest":          (0.0002,  0.0006),
}


def calc_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model, (0.002, 0.006))
    return round(
        (input_tokens / 1000 * pricing[0]) + (output_tokens / 1000 * pricing[1]),
        8
    )


class MistralWrapper:
    def __init__(self):
        self.api_key = MISTRAL_API_KEY
        if not self.api_key:
            print("⚠️  MISTRAL_API_KEY not set — using mock mode")
    
    async def _call_mistral(
        self,
        messages: List[Dict],
        model: str,
        max_tokens: int = 1024,
        system: Optional[str] = None
    ) -> Dict:
        """Raw Mistral API call"""
        if not self.api_key:
            # Mock mode for testing without API key
            return self._mock_response(messages, model)
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
        }
        if system:
            payload["messages"] = [{"role": "system", "content": system}] + messages
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{MISTRAL_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            resp.raise_for_status()
            return resp.json()
    
    def _mock_response(self, messages: List[Dict], model: str) -> Dict:
        """Mock Mistral response for demo mode"""
        import random
        content = f"[DEMO] This is a mock Mistral response for model {model}. In production, real AI output would appear here."
        return {
            "id": f"mock-{uuid.uuid4()}",
            "model": model,
            "choices": [{"message": {"content": content}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": random.randint(100, 500),
                "completion_tokens": random.randint(50, 300),
                "total_tokens": 0
            }
        }
    
    async def chat_with_tracking(
        self,
        messages: List[Dict],
        workflow_id: str,
        workflow_name: str,
        model: str = "mistral-large-latest",
        expected_value_usd: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Main tracked chat — wraps Mistral, logs everything"""
        call_id = str(uuid.uuid4())
        start_ms = time.time()
        
        try:
            raw = await self._call_mistral(messages, model)
            latency_ms = int((time.time() - start_ms) * 1000)
            
            usage = raw.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            cost_usd = calc_cost(model, input_tokens, output_tokens)
            
            content = raw["choices"][0]["message"]["content"]
            
            # Log to DB
            db = get_db()
            db.execute(
                """INSERT INTO api_calls
                   (call_id, workflow_id, workflow_name, model, input_tokens, output_tokens,
                    cost_usd, latency_ms, expected_value_usd, quality_score, quality_reason,
                    metadata, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    call_id, workflow_id, workflow_name, model,
                    input_tokens, output_tokens, cost_usd, latency_ms,
                    expected_value_usd, None, None,
                    json.dumps(metadata or {}),
                    datetime.utcnow().isoformat()
                )
            )
            db.commit()
            
            return {
                "call_id": call_id,
                "content": content,
                "model": model,
                "usage": {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens
                },
                "cost_usd": cost_usd,
                "latency_ms": latency_ms,
                "workflow_id": workflow_id
            }
        
        except Exception as e:
            # Still log failed calls
            db = get_db()
            db.execute(
                """INSERT INTO api_calls
                   (call_id, workflow_id, workflow_name, model, input_tokens, output_tokens,
                    cost_usd, latency_ms, expected_value_usd, quality_score, quality_reason,
                    metadata, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (call_id, workflow_id, workflow_name, model, 0, 0, 0.0,
                 int((time.time() - start_ms) * 1000),
                 expected_value_usd, 0.0, f"ERROR: {str(e)}",
                 json.dumps(metadata or {}), datetime.utcnow().isoformat())
            )
            db.commit()
            raise
    
    async def evaluate_output_quality(
        self,
        original_messages: List[Dict],
        ai_response: str,
        workflow_id: str
    ) -> Dict:
        """
        Use a second Mistral call to evaluate quality and business relevance.
        This is the 'evaluator model' that powers Layer 2 of ROI Lens.
        """
        eval_prompt = f"""You are an AI output quality evaluator for business ROI tracking.

Evaluate this AI response on a 0.0-1.0 scale across these dimensions:
1. Task Completion (did it fully answer the request?)
2. Business Value (is the output actionable for a business use case?)
3. Accuracy & Safety (no hallucinations or harmful content?)
4. Efficiency (was it concise and clear?)

Original request: {original_messages[-1].get('content', '')[:500]}

AI Response: {ai_response[:800]}

Respond ONLY with valid JSON in this exact format:
{{
  "score": 0.85,
  "task_completion": 0.9,
  "business_value": 0.8,
  "accuracy_safety": 0.95,
  "efficiency": 0.75,
  "reason": "One sentence explaining the score",
  "improvement": "One specific suggestion to improve ROI"
}}"""

        try:
            raw = await self._call_mistral(
                [{"role": "user", "content": eval_prompt}],
                model="mistral-small-latest",  # Use cheaper model for eval
                max_tokens=256
            )
            content = raw["choices"][0]["message"]["content"]
            # Parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"Evaluator error: {e}")
        
        return {"score": 0.7, "reason": "Evaluation unavailable", "improvement": "N/A"}
    
    async def generate_roi_report(self, dashboard_data: Dict) -> str:
        """Generate plain-English executive report from dashboard data"""
        prompt = f"""You are an AI ROI analyst. Generate a concise executive summary (3 paragraphs max) 
based on this AI usage data. Be specific with numbers. Use plain business language. 
Highlight wins, flag concerns, and give ONE concrete recommendation.

Data:
{json.dumps(dashboard_data, indent=2)[:2000]}

Format: Plain text, no markdown, no bullet points. Write as a senior analyst briefing a CFO."""
        
        try:
            raw = await self._call_mistral(
                [{"role": "user", "content": prompt}],
                model="mistral-large-latest",
                max_tokens=512
            )
            return raw["choices"][0]["message"]["content"]
        except Exception:
            total_cost = dashboard_data.get("total_cost_usd", 0)
            total_value = dashboard_data.get("total_value_usd", 0)
            roi = dashboard_data.get("overall_roi_pct", 0)
            return (
                f"Your AI systems have generated ${total_value:.2f} in measurable business value "
                f"against ${total_cost:.4f} in API costs, representing a {roi:.1f}% ROI. "
                f"Continue monitoring the kill-switch alerts for underperforming workflows."
            )
