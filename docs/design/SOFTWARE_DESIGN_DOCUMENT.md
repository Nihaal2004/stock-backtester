# Software Design Document
## Stock Strategy Backtester Lite

**Author:** Nihaal2004  
**Date:** March 2026  
**Version:** 2.0

---

## Table of Contents
1. [Introduction](#introduction)
2. [Design Principles Applied](#design-principles-applied)
3. [High-Level Architecture](#high-level-architecture)
4. [Module Design](#module-design)
5. [User Interface Design](#user-interface-design)
6. [Design Decisions & Rationale](#design-decisions-rationale)
7. [Future Extensibility](#future-extensibility)

---

## 1. Introduction

### 1.1 Purpose
This document describes the software design for the Stock Strategy Backtester Lite application. The design emphasizes modularity, maintainability, and adherence to software engineering best practices.

### 1.2 Scope
The design covers the complete application architecture including:
- Data handling layer
- Business logic layer (strategies and backtesting)
- Presentation layer (UI and visualization)
- Module interactions and dependencies

### 1.3 Design Goals
- **Modularity**: Separate concerns into independent, reusable modules
- **Extensibility**: Easy to add new strategies and features
- **Maintainability**: Clear structure with single responsibilities
- **Testability**: Loosely coupled components that can be tested independently

---

## 2. Design Principles Applied

### 2.1 Abstraction
**Implementation:**
- Created abstract `Strategy` base class defining the interface for all trading strategies
- Clients work with the Strategy interface without knowing implementation details
- Strategy implementations (SMA, RSI) are hidden behind the abstraction

**Benefits:**
- UI code doesn't need to know how strategies work internally
- New strategies can be added without changing existing code
- Reduces complexity by hiding implementation details

**Code Example:**
```python
class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, df, params):
        pass
```

### 2.2 Modularity
**Implementation:**
- Separated application into 6 distinct modules:
  1. `data_loader.py` - Data input and validation
  2. `strategies.py` - Trading strategy implementations
  3. `backtest_engine.py` - Core backtesting logic
  4. `visualization.py` - Chart and display generation
  5. `ui_components.py` - Streamlit UI elements
  6. `app.py` - Main orchestrator

**Benefits:**
- Each module can be developed and tested independently
- Changes in one module don't affect others
- Code is organized logically by functionality
- Easier to understand and navigate codebase

**Module Independence:**
```
data_loader → backtest_engine → visualization
             ↗
strategies →
```

### 2.3 High Cohesion
**Implementation:**
- Each module has a single, well-defined purpose
- `DataLoader` only handles data loading and validation
- `BacktestEngine` only handles backtest execution
- `Visualizer` only handles display and charts

**Examples:**
- **DataLoader**: All data-related methods grouped together
  - `load_csv()`, `validate_columns()`, `clean_data()`, `filter_date_range()`
- **BacktestEngine**: All backtesting operations together
  - `run()`, `get_trade_log()`, `calculate_metrics()`

**Benefits:**
- Easy to locate functionality
- Changes to one concern don't affect others
- Modules are self-contained and understandable

### 2.4 Low Coupling
**Implementation:**
- Modules depend on interfaces, not concrete implementations
- `BacktestEngine` doesn't know about strategies - just works with signals
- UI doesn't know about strategy algorithms - uses StrategyFactory
- Communication through well-defined data structures (DataFrames, dictionaries)

**Dependency Minimization:**
- `strategies.py` → Independent (no internal dependencies)
- `backtest_engine.py` → Independent (just pandas)
- `data_loader.py` → Independent (just pandas)
- `app.py` → Orchestrates all modules (knows about interfaces only)

**Benefits:**
- Modules can be changed independently
- Easy to swap implementations
- Better testability - can mock dependencies
- Reduced ripple effects from changes

### 2.5 Design Patterns Used

#### Strategy Pattern
- Abstract `Strategy` class with concrete implementations (`SMAStrategy`, `RSIStrategy`)
- Allows selecting strategy at runtime
- New strategies added without modifying existing code

#### Factory Pattern
- `StrategyFactory` creates strategy instances by name
- Decouples strategy creation from usage
- Centralizes strategy management

#### Layered Architecture
- Clear separation between layers: UI → Business Logic → Data
- Each layer only communicates with adjacent layers
- Promotes organized code structure

---

## 3. High-Level Architecture

### 3.1 Architecture Style
**Layered Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│         PRESENTATION LAYER                   │
│  (ui_components.py, visualization.py)       │
│  - User Interface                           │
│  - Display & Charts                         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         BUSINESS LOGIC LAYER                │
│  (strategies.py, backtest_engine.py)        │
│  - Trading Strategies                       │
│  - Backtest Execution                       │
│  - Performance Calculations                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         DATA LAYER                          │
│  (data_loader.py)                           │
│  - CSV Loading                              │
│  - Data Validation                          │
│  - Data Cleaning                            │
└─────────────────────────────────────────────┘
```

### 3.2 Component Interaction Flow

```
User Upload CSV
      ↓
[DataLoader] ← Load & Validate
      ↓
[UI Components] ← Select Strategy & Parameters
      ↓
[StrategyFactory] ← Create Strategy Instance
      ↓
[Strategy] ← Generate Trading Signals
      ↓
[BacktestEngine] ← Execute Backtest
      ↓
[BacktestEngine] ← Calculate Metrics
      ↓
[Visualizer] ← Display Results
      ↓
User Views Results
```

### 3.3 Architecture Benefits
- **Separation of Concerns**: Each layer has distinct responsibility
- **Maintainability**: Changes in UI don't affect business logic
- **Testability**: Each layer can be tested independently
- **Scalability**: Easy to add features within appropriate layer

### 3.4 Why This Architecture?
1. **Educational Context**: Clear structure helps understand application flow
2. **Small-Medium Scale**: Layered architecture perfect for this size
3. **Web Application**: Fits Streamlit's interactive nature
4. **Future Growth**: Easy to add new strategies, data sources, or visualizations

---

## 4. Module Design

### 4.1 Data Layer

#### DataLoader Module
**Responsibility**: Handle all data input and validation operations

**Key Methods:**
- `load_csv(file)` - Load and validate CSV file
- `filter_date_range(df, start, end)` - Filter data by dates
- `_validate_columns(df)` - Check required columns exist
- `_clean_data(df)` - Convert types and remove invalid rows

**Design Decisions:**
- All validation logic centralized in one class
- Clear error messages for user feedback
- Defensive programming (handle invalid data gracefully)

**Why DataLoader?**
- Separates data concerns from business logic
- Reusable for different data sources in future
- Single place to modify validation rules

### 4.2 Business Logic Layer

#### Strategies Module
**Responsibility**: Implement trading strategy algorithms

**Class Hierarchy:**
```
Strategy (Abstract)
├── SMAStrategy
└── RSIStrategy
```

**Key Components:**
- `Strategy` - Abstract base class defining interface
- `SMAStrategy` - Moving average crossover implementation
- `RSIStrategy` - RSI threshold implementation
- `StrategyFactory` - Creates strategy instances

**Design Decisions:**
- Strategy pattern allows easy addition of new strategies
- Each strategy validates its own parameters
- Factory pattern decouples creation from usage

**Extension Example:**
```python
# Adding a new strategy is straightforward:
class MACDStrategy(Strategy):
    def generate_signals(self, df, params):
        # Implementation here
        pass
```

#### BacktestEngine Module
**Responsibility**: Execute backtests and calculate performance

**Key Methods:**
- `run(df)` - Execute backtest with signals
- `get_trade_log(df)` - Extract individual trades
- `calculate_metrics(df, trades)` - Compute performance metrics

**Design Decisions:**
- Independent of strategy details (works with any signals)
- Implements next-day execution to avoid lookahead bias
- Transaction costs included for realism
- Returns standard data structures (DataFrames, dicts)

**Why Separate Engine?**
- Backtesting logic complex enough to deserve own module
- Can be reused with different strategies
- Easier to test backtesting correctness

### 4.3 Presentation Layer

#### Visualization Module
**Responsibility**: Create charts and display results

**Key Methods:**
- `plot_equity_curve(df)` - Generate equity chart
- `display_metrics(metrics)` - Show performance metrics
- `display_trade_log(trades)` - Format and show trades
- `display_data_preview(df)` - Show data table

**Design Decisions:**
- All matplotlib/chart code in one place
- Consistent styling across charts
- Separates presentation from calculation

#### UIComponents Module
**Responsibility**: Render Streamlit UI elements

**Key Methods:**
- `render_header()` - App title and description
- `render_file_uploader()` - File upload widget
- `render_date_range_filter()` - Date selection
- `render_strategy_form()` - Strategy configuration form

**Design Decisions:**
- Reusable UI components
- Consistent styling and help text
- Form-based input to prevent unwanted reruns

---

## 5. User Interface Design

### 5.1 UI Design Principles Applied

#### Consistency
- Uniform color scheme across all screens
- Consistent button styles and sizes
- Standard layout patterns throughout

#### Clarity
- Clear section headers (1️⃣, 2️⃣, 3️⃣ for steps)
- Help text on all input fields
- Descriptive labels and tooltips

#### Feedback
- Success messages when data loads
- Error messages with actionable guidance
- Loading states for long operations
- Colored metrics (green for positive, red for negative)

#### Progressive Disclosure
- Step-by-step workflow
- Advanced options collapsed by default
- Information revealed as needed

### 5.2 Screen Flow

**Screen 1: Home/Upload**
- Welcome message and instructions
- File upload widget
- Shows required format

**Screen 2: Data Preview**
- Table showing uploaded data
- Summary statistics
- Date range filter

**Screen 3: Strategy Configuration**
- Strategy selection dropdown
- Parameter inputs (context-sensitive)
- Transaction cost settings

**Screen 4: Results - Metrics**
- Key performance indicators
- Large, readable numbers
- Color-coded for quick scanning

**Screen 5: Results - Equity Curve**
- Line chart showing portfolio value over time
- Clear axis labels
- Professional appearance

**Screen 6: Results - Trade Log**
- Detailed table of all trades
- P/L highlighted in color
- Sortable and scrollable

### 5.3 Responsive Design Considerations
- Wide layout for desktop use
- Flexible columns that adapt to screen size
- Scrollable tables for large datasets
- Mobile-friendly where possible

### 5.4 User Experience Enhancements
- Form prevents accidental parameter resets
- Progress indicators during processing
- Warnings for edge cases (no trades generated)
- Educational tooltips explaining metrics

### 5.5 Accessibility
- High contrast color scheme
- Clear font sizes
- Descriptive labels for screen readers
- Logical tab order

---

## 6. Design Decisions & Rationale

### 6.1 Key Design Decisions

#### Decision 1: Modular Architecture (6 separate modules)
**Why:**
- Makes codebase easier to navigate and understand
- Enables parallel development (different people can work on different modules)
- Improves testability (each module can be tested independently)
- Facilitates maintenance (bugs isolated to specific modules)

**Alternative Considered:**
- Single monolithic file (original approach)
- Rejected because: Hard to maintain, test, and extend

**Impact:**
- Increased number of files but much better organization
- Slight overhead in imports but worth it for maintainability

#### Decision 2: Strategy Pattern for Trading Algorithms
**Why:**
- New strategies can be added without modifying existing code (Open/Closed Principle)
- Strategies are interchangeable at runtime
- Each strategy encapsulates its own logic and validation
- Easier to test individual strategies

**Alternative Considered:**
- If/else statements in main code
- Rejected because: Not extensible, violates Single Responsibility

**Impact:**
- More upfront design work but much easier to extend
- Clear contract (interface) for all strategies

#### Decision 3: Factory Pattern for Strategy Creation
**Why:**
- Decouples UI from strategy implementation details
- Centralizes strategy instantiation logic
- Makes it easy to add new strategies to the system
- UI just works with strategy names (strings)

**Alternative Considered:**
- Direct instantiation in UI code
- Rejected because: Creates tight coupling, hard to maintain

**Impact:**
- One extra class but much cleaner architecture

#### Decision 4: Separate BacktestEngine from Strategies
**Why:**
- Backtesting logic is complex and deserves its own module
- Engine is reusable with any signal source
- Strategies focus only on signal generation
- Easier to test backtesting correctness independently

**Alternative Considered:**
- Include backtesting in each strategy
- Rejected because: Code duplication, hard to maintain consistency

**Impact:**
- Clear separation makes both modules simpler

#### Decision 5: Layered Architecture (UI → Business Logic → Data)
**Why:**
- Standard pattern that developers understand
- Clear separation of concerns
- Each layer has well-defined responsibility
- Perfect fit for web applications like this

**Alternative Considered:**
- MVC (Model-View-Controller)
- Rejected because: Overkill for this application size

**Impact:**
- Intuitive structure that's easy to navigate

### 6.2 Trade-offs Made

#### Code Volume vs. Maintainability
**Trade-off:** More files and classes vs. simpler single file
**Chosen:** More structure for better maintainability
**Reason:** Long-term benefits outweigh short-term simplicity

#### Performance vs. Clarity
**Trade-off:** Optimized algorithms vs. readable code
**Chosen:** Readable code with adequate performance
**Reason:** Educational context prioritizes understanding

#### Flexibility vs. Simplicity
**Trade-off:** Support all features vs. focused scope
**Chosen:** Limited feature set done well
**Reason:** Better to do core features excellently

---

## 7. Future Extensibility

### 7.1 How to Add New Features

#### Adding a New Strategy
```python
# 1. Create new strategy class in strategies.py
class NewStrategy(Strategy):
    def generate_signals(self, df, params):
        # Implementation
        pass
    
    def validate_params(self, params, data_length):
        # Validation
        pass

# 2. Register in StrategyFactory
_strategies = {
    'SMA Crossover': SMAStrategy,
    'RSI Threshold': RSIStrategy,
    'New Strategy': NewStrategy  # Add here
}

# 3. Add UI parameters in ui_components.py
if strategy == "New Strategy":
    params['param1'] = st.number_input(...)
```

#### Adding New Metrics
```python
# In backtest_engine.py, add to calculate_metrics()
def calculate_metrics(self, df, trade_log):
    # ... existing metrics ...
    sharpe_ratio = self._calculate_sharpe(df)
    return {
        # ... existing metrics ...
        'sharpe_ratio': sharpe_ratio
    }
```

#### Adding New Visualizations
```python
# In visualization.py
@staticmethod
def plot_drawdown_chart(df):
    # New chart implementation
    pass
```

### 7.2 Extensibility Benefits of Current Design

1. **New Data Sources**: Just modify DataLoader or create DataLoaderV2
2. **New Strategies**: Follow Strategy interface, register in Factory
3. **New Metrics**: Add methods to BacktestEngine
4. **New Charts**: Add methods to Visualizer
5. **New UI Elements**: Add methods to UIComponents

### 7.3 Design Supports Future Requirements

**Potential Future Features:**
- Multiple strategy comparison → Already modular, can run multiple backtests
- Real-time data → Swap DataLoader implementation
- Machine learning strategies → Implement Strategy interface
- Database storage → Add new data layer module
- API access → Add new interface layer

---

## Appendix: Diagrams

### Module Dependencies
```
app.py (Orchestrator)
  ├── imports ui_components
  ├── imports data_loader
  ├── imports strategies
  ├── imports backtest_engine
  └── imports visualization

Each module is independent (no cross-module dependencies)
```

### Class Diagram
```
Strategy (Abstract)
  ├── generate_signals()
  ├── validate_params()
  │
  ├── SMAStrategy
  └── RSIStrategy

StrategyFactory
  └── create_strategy()

DataLoader
  ├── load_csv()
  └── filter_date_range()

BacktestEngine
  ├── run()
  ├── get_trade_log()
  └── calculate_metrics()

Visualizer
  ├── plot_equity_curve()
  ├── display_metrics()
  └── display_trade_log()

UIComponents
  ├── render_header()
  ├── render_file_uploader()
  └── render_strategy_form()
```

---

**Document Version History:**
- v2.0 (March 2026) - Complete modular redesign
- v1.0 (February 2026) - Initial monolithic design

---

**End of Document**
