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
- Exports in /wireframes and /docs/design

---

## Software Design

### Overview
The Stock Strategy Backtester Lite has been refactored using **modular design principles** to ensure maintainability, extensibility, and clarity. The codebase demonstrates professional software engineering practices including abstraction, high cohesion, low coupling, and design patterns.

### Architecture Style: Layered Architecture

The application follows a **3-layer architecture** with clear separation of concerns:

```
┌─────────────────────────────────────┐
│     PRESENTATION LAYER              │
│  (UI Components, Visualization)     │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│     BUSINESS LOGIC LAYER            │
│  (Strategies, Backtest Engine)      │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│     DATA LAYER                      │
│  (Data Loading, Validation)         │
└─────────────────────────────────────┘
```

**Why Layered Architecture?**
- Clear separation between UI, business logic, and data handling
- Changes in one layer don't affect others
- Each layer has a well-defined responsibility
- Perfect fit for data pipeline workflow (load → process → display)

### Module Structure

The application consists of **6 independent modules**, each with a single responsibility:

| Module | Responsibility | Key Classes |
|--------|---------------|-------------|
| `data_loader.py` | CSV loading, validation, cleaning | `DataLoader` |
| `strategies.py` | Trading strategy algorithms | `Strategy`, `SMAStrategy`, `RSIStrategy`, `StrategyFactory` |
| `backtest_engine.py` | Backtest execution, metrics | `BacktestEngine` |
| `visualization.py` | Charts, result display | `Visualizer` |
| `ui_components.py` | Streamlit UI elements | `UIComponents` |
| `app.py` | Application orchestration | `main()` |

### Design Principles Applied

#### 1. **Abstraction**
- Abstract `Strategy` base class defines interface for all trading strategies
- Concrete implementations (SMA, RSI) hidden behind abstraction
- UI code works with strategy interface without knowing implementation details

#### 2. **Modularity**
- Application separated into 6 focused modules
- Each module is independently developed, tested, and maintained
- Modules communicate through well-defined interfaces (DataFrames, dictionaries)

#### 3. **High Cohesion**
- Each module has a single, well-defined purpose
- All related functionality grouped together (e.g., all data operations in `DataLoader`)
- No mixing of concerns (e.g., UI code doesn't contain calculation logic)

#### 4. **Low Coupling**
- Modules depend on interfaces, not concrete implementations
- `BacktestEngine` doesn't know about specific strategies—just works with signals
- UI doesn't know about algorithm details—uses `StrategyFactory`
- Changes in one module don't cascade through the system

### Design Patterns Used

#### **Strategy Pattern**
Allows selecting trading algorithm at runtime without modifying existing code.
```python
Strategy (Abstract)
├── SMAStrategy
└── RSIStrategy
```

**Benefits:**
- Easy to add new strategies (Open/Closed Principle)
- Strategies are interchangeable
- Each strategy encapsulates its own logic

#### **Factory Pattern**
Centralizes strategy creation and decouples UI from strategy classes.
```python
strategy = StrategyFactory.create_strategy("SMA Crossover")
```

**Benefits:**
- UI doesn't need to know about strategy classes
- One place to manage all strategies
- Easy to add/remove strategies from the system

### Key Design Decisions

#### Decision 1: Separate BacktestEngine from Strategies
**Rationale:** Backtesting logic is complex and reusable. Strategies should only generate signals, not execute trades.

**Benefit:** Same engine works with all strategies. Improvements to backtesting benefit all strategies simultaneously.

#### Decision 2: Next-Day Execution
**Rationale:** Prevents lookahead bias. Position today = signal from yesterday.

**Benefit:** Realistic, educational, professional backtesting methodology.

#### Decision 3: Form-Based UI Parameters
**Rationale:** Prevents app from rerunning on every parameter change.

**Benefit:** Better user experience—only recalculates when user clicks "Run Backtest."

#### Decision 4: DataFrame Communication
**Rationale:** Pandas DataFrames are industry standard for financial data.

**Benefit:** Flexible, powerful, familiar to developers. Easy to add columns without breaking interfaces.

#### Decision 5: Clear Error Messages
**Rationale:** Help users fix problems themselves.

**Example:** "Fast SMA (5) must be less than Slow SMA (5). Try Fast=5 and Slow=20."

**Benefit:** Better user experience, educational value, reduced frustration.

### Extensibility

The modular design makes it easy to add features:

**Adding a New Strategy:**
```python
# 1. Create class implementing Strategy interface
class MACDStrategy(Strategy):
    def generate_signals(self, df, params):
        # Implementation
        pass

# 2. Register in StrategyFactory
StrategyFactory._strategies['MACD'] = MACDStrategy
```

**Adding a New Metric:**
```python
# Add to BacktestEngine.calculate_metrics()
def calculate_metrics(self, df, trade_log):
    # ... existing metrics ...
    sharpe_ratio = self._calculate_sharpe(df)
    return {..., 'sharpe_ratio': sharpe_ratio}
```

### Documentation

Complete design documentation available in `/docs/design/`:
- 📄 **SOFTWARE_DESIGN_DOCUMENT.md** - Complete 18-page design document
- 📄 **DESIGN_PRINCIPLES.md** - Detailed explanation of principles applied
- 📄 **DESIGN_DECISIONS.md** - Rationale for key decisions
- 📄 **UI_DESIGN.md** - User interface design documentation
- 🖼️ **Architecture diagrams** - High-level and detailed architecture
- 🖼️ **Wireframes** - All 6 UI screen designs

### Architecture Diagrams

![High-Level Architecture](docs/design/high%20level%20architecture.png)

*Figure 1: High-level system architecture showing layered structure*

![Backtest Pipeline](docs/design/backtest%20pipline.png)

*Figure 2: Backtest execution pipeline*

### Diagrams
- High-level architecture: `/docs/design/high level architecture.png`
- Detailed architecture: `/docs/design/Architecture.png`
- Backtest pipeline: `/docs/design/backtest pipline.png`
- All diagrams available in `/diagrams` and `/docs/design`

### Summary

The refactored design provides:
- ✅ **Maintainability** - Easy to understand and modify
- ✅ **Extensibility** - Simple to add new features
- ✅ **Testability** - Modules can be tested independently
- ✅ **Professional Quality** - Follows industry best practices
- ✅ **Educational Value** - Demonstrates good software design

---

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

## DA3 Automated Testing (for screenshots)

```bash
pip install -r requirements-dev.txt
```

### Integration tests
```bash
python -m pytest -v tests/test_integration_pipeline.py
```

### Regression tests
```bash
python -m pytest -v tests/test_regression_backtest.py
```

### Mutation tests
```bash
python tools/run_mutation_tests.py
```

Detailed command guide: `docs/da3/TESTING_EVIDENCE_STEPS.md`


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
