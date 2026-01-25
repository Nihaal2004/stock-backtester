# Stock Strategy Backtester Lite (Educational)

## Project Overview

## Vision Document
### Problem it Solves
Beginners often follow trading “signals” without knowing whether a strategy works over time. Existing backtesting tools are either too complex or paid. This project provides a simple, educational tool to evaluate basic stock strategies on historical data and understand risk (drawdowns, losing streaks) and performance outcomes.

### Target Users (Personas)
1. **Student Learner**: Wants to learn how strategies behave using historical data with simple inputs and clear outputs.
2. **Beginner Analyst**: Wants a quick way to test 1–2 strategies on a CSV dataset and compare results.
3. **Faculty/Evaluator**: Needs a small software project with clear documentation, requirements, diagrams, and test evidence.

### Vision Statement
Build a lightweight, user-friendly “Strategy Backtester Lite” that allows users to upload historical stock data, run simple strategies, and generate an easy-to-understand performance and risk report for educational use.

### Key Features / Goals
- Upload stock price CSV (minimum: Date and Close)
- Run 2 basic strategies: SMA Crossover and RSI Threshold
- Backtest using clearly documented assumptions (long-only, next-day execution)
- Display equity curve, trade log, and key metrics (CAGR, max drawdown, win rate)
- Provide clear validation and error messages for incorrect inputs

### Success Metrics
- Runs end-to-end on at least 3 sample datasets without crashing
- Produces a report (chart + metrics + trades) within a few seconds for daily data
- Users can complete a backtest without help (upload → select strategy → run → view results)
- Test cases cover main edge scenarios (invalid CSV, missing columns, short data)

### Assumptions & Constraints
- Educational tool only; not financial advice and not real-time trading
- Daily historical data; long-only; single position at a time
- Strategy signals are executed on the next trading day to avoid lookahead bias
- Minimal scope: focus on documentation quality and a working prototype


## User Stories + MoSCoW

### MoSCoW Prioritization

| Priority | User Stories | Rationale |
|---|---|---|
| Must | US-01 to US-10 | Core workflow required for an end-to-end demo: upload → strategy → backtest → results. |
| Should | US-11 to US-18 | Improves usability and realism but not required for a basic working prototype. |
| Could | US-19 to US-23 | Enhancements for comparison, reporting, and UX polish if time permits. |
| Won’t | US-24 to US-25 | Out of scope to keep the project small and educational (no real trading, no prediction). |



## Wireframes
- Figma Link:
- Exports in /wireframes

## Architecture Diagram
- Exports in /diagrams
- Export: /diagrams/Architecture.png

## Branching Strategy
- PR proof: merged feature branch into main
## Quick Start – Local Development (Docker)
### What it does
- Upload CSV (required columns: Date, Close)
- Choose strategy: SMA Crossover or RSI Threshold
- Run backtest (next-day execution)
- View equity curve, key metrics, and trade log

```bash
docker compose up --build

### Run locally (without Docker)
```bash
pip install -r src/requirements.txt
streamlit run src/app.py



## Local Development Tools

## Proof / Screenshots
- Stored in /screenshots
