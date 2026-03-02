# Design Decisions & Rationale

## Document Purpose
This document explains the key design decisions made for the Stock Strategy Backtester Lite application and the reasoning behind each decision.

---

## Decision 1: Modular Architecture (6 Separate Modules)

### Decision
Split the application into 6 distinct modules instead of one monolithic file.

### Modules Created
1. `data_loader.py` - Data handling
2. `strategies.py` - Trading algorithms
3. `backtest_engine.py` - Backtesting logic
4. `visualization.py` - Display and charts
5. `ui_components.py` - UI elements
6. `app.py` - Main orchestrator

### Rationale

#### Why We Did This
1. **Maintainability**: Easier to locate and fix bugs
2. **Understandability**: Each module has a clear, focused purpose
3. **Testability**: Can test each module independently
4. **Collaboration**: Multiple developers can work on different modules
5. **Reusability**: Modules can be used in other projects

#### Alternative Considered
Keep everything in one file (original approach)

#### Why We Rejected Alternative
- Becomes unwieldy as project grows
- Hard to find specific functionality
- Changes in one area can break unrelated features
- Difficult to test individual components
- Poor separation of concerns

#### Impact
- **Positive**: Much better code organization and maintainability
- **Trade-off**: More files to manage, but benefits far outweigh the cost

---

## Decision 2: Strategy Pattern for Trading Algorithms

### Decision
Use an abstract `Strategy` base class with concrete strategy implementations.

### Implementation
```python
Strategy (Abstract)
├── SMAStrategy (Concrete)
└── RSIStrategy (Concrete)
```

### Rationale

#### Why We Did This
1. **Extensibility**: Easy to add new strategies without modifying existing code
2. **Polymorphism**: All strategies share the same interface
3. **Encapsulation**: Each strategy manages its own logic and validation
4. **Open/Closed Principle**: Open for extension, closed for modification

#### How It Helps
```python
# Adding a new strategy is straightforward:
class MACDStrategy(Strategy):
    def generate_signals(self, df, params):
        # Implementation here
        pass
```

#### Alternative Considered
Use if/else statements in main code to handle different strategies

#### Why We Rejected Alternative
```python
# BAD: Not extensible
if strategy == "SMA":
    # SMA logic here
elif strategy == "RSI":
    # RSI logic here
# Have to modify this code every time we add a strategy
```

#### Impact
- **Positive**: Very easy to add new strategies (5-10 minutes per strategy)
- **Trade-off**: Slightly more upfront design work, but pays off quickly

---

## Decision 3: Factory Pattern for Strategy Creation

### Decision
Create a `StrategyFactory` class to instantiate strategies by name.

### Implementation
```python
class StrategyFactory:
    _strategies = {
        'SMA Crossover': SMAStrategy,
        'RSI Threshold': RSIStrategy
    }
    
    @classmethod
    def create_strategy(cls, name):
        return cls._strategies[name]()
```

### Rationale

#### Why We Did This
1. **Decoupling**: UI doesn't need to know about strategy classes
2. **Centralization**: One place to manage all strategies
3. **Simplicity**: UI just uses strategy names (strings)
4. **Flexibility**: Easy to add/remove strategies from the system

#### How It Helps UI Code
```python
# UI only knows strategy names
strategy_name = "SMA Crossover"
strategy = StrategyFactory.create_strategy(strategy_name)
# Don't need to know it's SMAStrategy class
```

#### Alternative Considered
Direct instantiation in UI code
```python
if strategy_name == "SMA Crossover":
    strategy = SMAStrategy()
elif strategy_name == "RSI Threshold":
    strategy = RSIStrategy()
```

#### Why We Rejected Alternative
- Creates coupling between UI and strategy classes
- Have to modify UI code when adding strategies
- Violates Single Responsibility (UI shouldn't manage strategy creation)

#### Impact
- **Positive**: Clean separation, easy to maintain
- **Trade-off**: One extra class, but well worth it

---

## Decision 4: Separate BacktestEngine from Strategies

### Decision
Create independent `BacktestEngine` that works with any signals.

### Rationale

#### Why We Did This
1. **Separation of Concerns**: Strategy generates signals, Engine executes trades
2. **Reusability**: Same engine works with all strategies
3. **Testability**: Can test backtesting logic independently
4. **Maintainability**: Backtesting improvements benefit all strategies
5. **Single Responsibility**: Each module does one thing well

#### How They Interact
```python
# Strategy: Generate signals
df = strategy.generate_signals(df, params)  # Adds 'signal' column

# Engine: Execute backtest (doesn't know/care about strategy)
results = engine.run(df)  # Just needs 'signal' column
```

#### Alternative Considered
Include backtesting logic in each strategy class

#### Why We Rejected Alternative
- Code duplication across strategies
- Hard to maintain consistency
- Can't improve backtesting without touching all strategies
- Strategies become too complex (multiple responsibilities)

#### Impact
- **Positive**: Clean design, easy to maintain and extend
- **Trade-off**: None - this is clearly the better approach

---

## Decision 5: Layered Architecture

### Decision
Organize code into three layers: Presentation → Business Logic → Data

### Architecture
```
┌─────────────────────────────┐
│   PRESENTATION LAYER        │
│   (UI, Visualization)       │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│   BUSINESS LOGIC LAYER      │
│   (Strategies, Backtesting) │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│   DATA LAYER                │
│   (Loading, Validation)     │
└─────────────────────────────┘
```

### Rationale

#### Why We Did This
1. **Clear Separation**: Each layer has distinct responsibility
2. **Industry Standard**: Well-understood pattern
3. **Maintainability**: Changes in one layer don't affect others
4. **Testability**: Can test each layer independently
5. **Scalability**: Easy to add features in appropriate layer

#### Layer Responsibilities
- **Presentation**: What user sees (UI, charts)
- **Business Logic**: What app does (strategies, calculations)
- **Data**: Where data comes from (loading, validation)

#### Alternative Considered
MVC (Model-View-Controller) pattern

#### Why We Chose Layered Over MVC
- Simpler for this application size
- Better fit for data pipeline workflow
- MVC adds complexity without significant benefit here
- Layered architecture more intuitive for this use case

#### Impact
- **Positive**: Clear structure everyone understands
- **Trade-off**: Must respect layer boundaries (worth it for organization)

---

## Decision 6: Next-Day Execution for Signals

### Decision
Position today = Signal from yesterday

### Implementation
```python
df['position'] = df['signal'].shift(1)
```

### Rationale

#### Why We Did This
1. **Avoid Lookahead Bias**: Can't trade on today's signal today (unrealistic)
2. **Realism**: Mimics actual trading (signal → decision → execution next day)
3. **Fair Backtesting**: Prevents artificially inflated results
4. **Educational Value**: Teaches proper backtesting methodology

#### Lookahead Bias Example
```python
# WRONG: Lookahead bias
position[today] = signal[today]  # Can't act on today's info today

# CORRECT: No lookahead bias
position[today] = signal[yesterday]  # Act on yesterday's signal
```

#### Alternative Considered
Same-day execution

#### Why We Rejected Alternative
- Unrealistic (can't time the market perfectly)
- Gives false confidence in strategy performance
- Bad educational practice
- Professional backtests always avoid lookahead bias

#### Impact
- **Positive**: Realistic, educational, professional
- **Trade-off**: Slightly lower returns, but accurate representation

---

## Decision 7: Include Transaction Costs

### Decision
Deduct 0.4% on each trade (buy or sell)

### Rationale

#### Why We Did This
1. **Realism**: Real trading has costs (commissions, spreads, slippage)
2. **Honest Results**: Strategies must overcome costs to be profitable
3. **Strategy Selection**: Helps identify strategies that trade too frequently
4. **Educational Value**: Understanding cost impact is important

#### Impact on Results
```python
# Without costs: 25% return
# With costs: 18% return  ← More realistic
```

#### Alternative Considered
No transaction costs (frictionless trading)

#### Why We Rejected Alternative
- Unrealistic and misleading
- Encourages overtrading strategies
- False sense of profitability
- Poor educational practice

#### Impact
- **Positive**: Honest, realistic backtests
- **Trade-off**: Lower returns, but accurate

---

## Decision 8: Form-Based UI for Parameters

### Decision
Use Streamlit form for strategy parameters

### Implementation
```python
with st.form("backtest_form"):
    # All inputs here
    run = st.form_submit_button()
```

### Rationale

#### Why We Did This
1. **User Experience**: Prevents app from rerunning on every parameter change
2. **Performance**: Only recalculate when user clicks "Run"
3. **Clarity**: Clear submission point (button)
4. **Control**: User decides when to execute

#### Without Form (Problem)
```
User changes Fast SMA: 10 → 15
App reruns immediately (annoying!)
User changes Slow SMA: 30 → 50
App reruns again (annoying!)
```

#### With Form (Solution)
```
User changes Fast SMA: 10 → 15  (no rerun)
User changes Slow SMA: 30 → 50  (no rerun)
User clicks "Run Backtest"       (single rerun)
```

#### Alternative Considered
Direct input widgets (no form)

#### Why We Rejected Alternative
- Poor user experience (too many reruns)
- Wastes computation (unnecessary recalculations)
- Frustrating for users adjusting multiple parameters

#### Impact
- **Positive**: Much better user experience
- **Trade-off**: None - forms are clearly better here

---

## Decision 9: DataFrame-Based Communication

### Decision
Use Pandas DataFrames to pass data between modules

### Rationale

#### Why We Did This
1. **Standard Format**: Industry standard for financial data
2. **Flexibility**: Easy to add columns without breaking interfaces
3. **Powerful**: Built-in operations for data manipulation
4. **Familiar**: Most Python developers know Pandas
5. **Self-Documenting**: Column names make data meaning clear

#### How Modules Communicate
```python
# DataLoader produces DataFrame
df = loader.load_csv(file)  # Returns DataFrame with Date, Close

# Strategy adds signal column
df = strategy.generate_signals(df, params)  # Adds 'signal' column

# Engine adds equity column
df = engine.run(df)  # Adds 'equity' column
```

#### Alternative Considered
Custom data classes or dictionaries

#### Why We Rejected Alternative
- More work to create custom classes
- Less flexible
- Have to write serialization/deserialization code
- DataFrames already perfect for this use case

#### Impact
- **Positive**: Easy to work with, powerful, standard
- **Trade-off**: Must have Pandas dependency (acceptable)

---

## Decision 10: Error Messages with Guidance

### Decision
Provide actionable error messages that tell users how to fix problems

### Examples
```python
# BAD
raise ValueError("Invalid parameters")

# GOOD
raise ValueError(
    "Fast SMA (5) must be less than Slow SMA (5). "
    "Try Fast=5 and Slow=20."
)
```

### Rationale

#### Why We Did This
1. **User Experience**: Users know how to fix problems
2. **Educational**: Teaches proper parameter selection
3. **Reduces Frustration**: Clear guidance prevents trial-and-error
4. **Professional**: Shows attention to detail and user needs

#### Examples in Code
```python
# Clear, helpful error
if len(df) < slow_sma + 2:
    raise ValueError(
        f"Not enough rows ({len(df)}) for Slow SMA={slow_sma}. "
        f"Need at least {slow_sma + 2} rows. "
        f"Use a smaller SMA window or upload more data."
    )
```

#### Alternative Considered
Generic error messages

#### Why We Rejected Alternative
- Frustrating for users
- Requires users to guess what went wrong
- Poor user experience
- Not educational

#### Impact
- **Positive**: Much better user experience
- **Trade-off**: More code for error messages (worth it)

---

## Summary of Key Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Modular Architecture | Maintainability, testability | Easier to work with |
| Strategy Pattern | Extensibility, encapsulation | Easy to add strategies |
| Factory Pattern | Decoupling, centralization | Clean code |
| Separate Engine | Reusability, SRP | Better organization |
| Layered Architecture | Standard pattern, clarity | Clear structure |
| Next-Day Execution | Avoid lookahead bias | Realistic results |
| Transaction Costs | Realism, honesty | Accurate backtests |
| Form-Based UI | Better UX, performance | Smoother experience |
| DataFrames | Standard, flexible | Easy to work with |
| Clear Errors | UX, educational | Users can fix issues |

---

## Design Philosophy

Our overall design philosophy:
1. **Simplicity**: Keep it as simple as possible, but no simpler
2. **Clarity**: Code should be self-explanatory
3. **Maintainability**: Think about the developer who comes after you
4. **Education**: Code should teach good practices
5. **Realism**: Backtest results should be honest and realistic

---

**Document End**
