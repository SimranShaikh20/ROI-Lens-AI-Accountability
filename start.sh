#!/bin/bash
# ROI Lens — Streamlit Quick Start
echo "╔══════════════════════════════════════╗"
echo "║  ROI LENS — Streamlit Dashboard       ║"
echo "║  Mistral Worldwide Hackathon 2026     ║"
echo "╚══════════════════════════════════════╝"

# Setup .env
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "📋 Created .env — add your MISTRAL_API_KEY"
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🚀 Launching Streamlit on http://localhost:8501"
echo "   Press Ctrl+C to stop."
echo ""

streamlit run app.py \
  --server.port=8501 \
  --server.headless=true \
  --theme.base=dark \
  --theme.primaryColor=#00e5a0 \
  --theme.backgroundColor=#07080a \
  --theme.secondaryBackgroundColor=#0e1117 \
  --theme.textColor=#e8eaf2
