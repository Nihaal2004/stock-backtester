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
- Figma Link: https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal?node-id=0-1&t=nmizP5MyeNEyDcvN-1
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
```
### Run locally (without Docker)
```bash
pip install -r src/requirements.txt
streamlit run src/app.py
```


## Local Development Tools

## Proof / Screenshots
- Stored in /screenshots

## Test Plan

### Test Cases

| TC ID | Scenario | Input/Setup | Steps | Expected Result |
|---|---|---|---|---|
| TC-01 | Valid CSV upload | CSV with Date, Close | Upload file | File loads; preview shown; no error |
| TC-02 | Missing required column | CSV missing Date or Close | Upload file | Clear error: missing columns; app stops safely |
| TC-03 | Invalid date values | Date column has invalid strings | Upload file | Invalid rows dropped; if too few rows remain show error |
| TC-04 | Non-numeric Close | Close has text values | Upload file | Non-numeric rows dropped; app continues or shows “not enough rows” |
| TC-05 | SMA fast >= slow | Fast=10 Slow=10 | Select SMA; run | Error shown; backtest not executed |
| TC-06 | SMA window > data length | Slow SMA larger than rows | Select SMA; run | Error: not enough rows for Slow SMA; no crash |
| TC-07 | RSI buy >= sell | Buy=70 Sell=30 | Select RSI; run | Error shown; backtest not executed |
| TC-08 | RSI period > data length | Period larger than rows | Select RSI; run | Error: not enough rows for RSI period; no crash |
| TC-09 | No-trade scenario | Params that produce no entries | Run backtest | Warning shown; equity curve flat; metrics still display |
| TC-10 | Docker run | Docker installed | `docker compose up --build` then open localhost | App accessible at http://localhost:8501 |

## Functional Requirements (for Traceability)
- FR-01: Upload CSV with required columns (Date, Close)
- FR-02: Validate input file and show clear errors
- FR-03: Allow strategy selection (SMA / RSI)
- FR-04: Allow parameter configuration for the selected strategy
- FR-05: Run backtest using next-day execution rule
- FR-06: Display equity curve
- FR-07: Display key metrics (Total Return, CAGR, Max Drawdown, Win Rate, #Trades)
- FR-08: Display trade log table
- FR-09: Support optional date range selection
- FR-10: Run application via Docker

## Traceability Matrix (FR ↔ Test Cases)

| Requirement | Covered By Test Cases |
|---|---|
| FR-01 | TC-01 |
| FR-02 | TC-02, TC-03, TC-04 |
| FR-03 | TC-05, TC-07 |
| FR-04 | TC-05, TC-06, TC-07, TC-08 |
| FR-05 | TC-01, TC-05, TC-07 |
| FR-06 | TC-01, TC-09 |
| FR-07 | TC-01, TC-09 |
| FR-08 | TC-01 |
| FR-09 | TC-01 |
| FR-10 | TC-10 |
