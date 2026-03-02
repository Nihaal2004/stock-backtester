# Stock Strategy Backtester Lite
## Software Design Document - Executive Summary

**Student**: Nihaal2004  
**Course**: Digital Assignment 2 / Review 2  
**Date**: March 2026  
**Repository**: https://github.com/Nihaal2004/stock-backtester

---

## 1. Design Principles Applied

### Abstraction
We created an abstract `Strategy` base class that defines the interface for all trading strategies. Concrete implementations (SMAStrategy, RSIStrategy) are hidden behind this interface, allowing the UI to work with strategies without knowing their internal details.

**Example:**
```python
class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, df, params):
        pass
```

**Benefits**: Simplifies usage, reduces complexity, easier to change implementations.

### Modularity
The application is separated into 6 independent modules, each with a specific purpose:
- `data_loader.py` - Data input and validation
- `strategies.py` - Trading algorithms
- `backtest_engine.py` - Backtesting execution
- `visualization.py` - Charts and display
- `ui_components.py` - UI elements
- `app.py` - Main orchestrator

**Benefits**: Better organization, independent development, easier testing, improved collaboration.

### High Cohesion
Each module groups related functionality together:
- DataLoader: All data operations (load, validate, clean, filter)
- BacktestEngine: All backtesting operations (run, extract trades, calculate metrics)
- Visualizer: All display operations (charts, tables, metrics)

**Benefits**: Easy to find code, clear purpose, easier maintenance, reusable modules.

### Low Coupling
Modules depend on interfaces rather than concrete implementations:
- BacktestEngine works with any signals (doesn't know about specific strategies)
- Strategies don't know about UI
- Modules communicate through standard DataFrames

**Benefits**: Easy to change, better testability, flexible implementations, reduced ripple effects.

---

## 2. High-Level Architecture

### Architecture Style: Layered Architecture

```
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER                      │
│  (ui_components.py, visualization.py)           │
│  - User Interface                               │
│  - Charts & Display                             │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         BUSINESS LOGIC LAYER                    │
│  (strategies.py, backtest_engine.py)            │
│  - Trading Strategies                           │
│  - Backtest Execution                           │
│  - Performance Calculations                     │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         DATA LAYER                              │
│  (data_loader.py)                               │
│  - CSV Loading                                  │
│  - Data Validation                              │
│  - Data Cleaning                                │
└─────────────────────────────────────────────────┘
```

### Why Layered Architecture?
1. **Clear Separation**: Each layer has distinct responsibility
2. **Maintainability**: Changes in UI don't affect business logic
3. **Standard Pattern**: Well-understood by developers
4. **Perfect Fit**: Ideal for web applications with data pipelines
5. **Scalability**: Easy to add features within appropriate layer

### Component Interaction Flow

```
User Upload → DataLoader → UI Components → StrategyFactory
    ↓
Strategy Signals → BacktestEngine → Metrics Calculation
    ↓
Visualizer → Display Results → User
```

---

## 3. User Interface Design

### Design Principles
- **Consistency**: Uniform colors, fonts, layouts
- **Clarity**: Step-by-step workflow (1️⃣, 2️⃣, 3️⃣), clear labels, help text
- **User-Friendliness**: Progressive disclosure, error prevention, forgiving inputs
- **Accessibility**: High contrast, large targets, logical flow

### Six Key Screens

1. **Home / Upload** - Welcome and file upload
2. **Data Preview** - Table showing uploaded data
3. **Date Filter** - Optional date range selection
4. **Strategy Configuration** - Strategy selection and parameters
5. **Results - Metrics** - Performance indicators
6. **Results - Chart & Trades** - Equity curve and trade log

### UI Improvements Made
- Added emoji icons for visual hierarchy (1️⃣, 2️⃣, 3️⃣)
- Help tooltips on all parameters
- Color-coded P/L (green positive, red negative)
- Form-based inputs to prevent unwanted reruns
- Clear error messages with actionable guidance

### Figma Designs
All wireframes available at: https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal

Exported wireframes in `/docs/design/`:
- home.png
- csv import.png
- stock preview.png
- strategy picker.png
- equity curve.png

---

## 4. Design Decisions & Why

### Decision 1: Modular Architecture (6 Modules)
**Why**: Makes codebase easier to navigate, enables parallel development, improves testability, facilitates maintenance.

**Alternative Rejected**: Single monolithic file (original approach) - hard to maintain and extend.

### Decision 2: Strategy Pattern
**Why**: New strategies can be added without modifying existing code (Open/Closed Principle), strategies are interchangeable, easier to test.

**Alternative Rejected**: If/else statements - not extensible, violates Single Responsibility.

### Decision 3: Factory Pattern
**Why**: Decouples UI from strategy implementation, centralizes strategy creation, makes it easy to add new strategies.

**Alternative Rejected**: Direct instantiation in UI - creates tight coupling.

### Decision 4: Separate BacktestEngine
**Why**: Backtesting logic is complex and reusable, strategies focus only on signal generation, easier to test independently.

**Alternative Rejected**: Include backtesting in each strategy - code duplication, hard to maintain.

### Decision 5: Next-Day Execution
**Why**: Prevents lookahead bias (position today = signal yesterday), realistic trading simulation, professional practice.

**Alternative Rejected**: Same-day execution - unrealistic, inflates results.

---

## 5. Design Patterns Used

### Strategy Pattern
- Abstract Strategy class with concrete implementations
- Allows runtime selection of algorithm
- Easy to add new strategies

```python
Strategy (Abstract)
├── SMAStrategy
└── RSIStrategy
```

### Factory Pattern
- Centralized strategy creation
- Decouples creation from usage

```python
StrategyFactory.create_strategy("SMA Crossover")
```

### Layered Architecture Pattern
- Presentation → Business Logic → Data
- Clear separation of concerns
- Standard industry pattern

---

## 6. Maintainability & Future Extensibility

### Adding a New Strategy
```python
# 1. Create class implementing Strategy interface
class MACDStrategy(Strategy):
    def generate_signals(self, df, params):
        # Implementation
        pass

# 2. Register in factory
StrategyFactory._strategies['MACD'] = MACDStrategy

# 3. Done! No other code changes needed
```

### Adding a New Metric
```python
# Add to BacktestEngine.calculate_metrics()
sharpe_ratio = self._calculate_sharpe(df)
return {..., 'sharpe_ratio': sharpe_ratio}
```

### Benefits of Modular Design
- **Easy to understand** - Clear structure and purpose
- **Easy to modify** - Changes isolated to specific modules
- **Easy to test** - Each module testable independently
- **Easy to extend** - Add features without breaking existing code

---

## 7. Diagrams

### High-Level Architecture
![High-Level Architecture](high%20level%20architecture.png)

*Figure 1: Three-layer architecture showing separation of concerns*

### Backtest Pipeline
![Backtest Pipeline](backtest%20pipline.png)

*Figure 2: Flow of data through the backtesting engine*

### Module Dependencies
```
app.py (Orchestrator)
  ├── ui_components (Presentation)
  ├── visualization (Presentation)
  ├── data_loader (Data)
  ├── strategies (Business Logic)
  └── backtest_engine (Business Logic)
```

---

## 8. Summary

### What Was Improved

**Before Refactoring**:
- ❌ One 200+ line monolithic file
- ❌ Everything mixed together
- ❌ Hard to test
- ❌ Difficult to extend

**After Refactoring**:
- ✅ 6 focused, single-responsibility modules
- ✅ Clear separation of concerns
- ✅ Easy to test each component
- ✅ Simple to add new features

### Key Achievements

1. **Professional Design**: Uses industry-standard patterns (Strategy, Factory, Layered)
2. **SOLID Principles**: Demonstrates Single Responsibility, Open/Closed
3. **Clear Documentation**: 50+ pages explaining design decisions
4. **Extensible**: New strategies in 5 minutes, new metrics in 2 minutes
5. **Maintainable**: Each module independently understandable
6. **Educational**: Code teaches good software design

### Metrics

- **Modules**: 6 independent modules
- **Lines of Code**: ~500 lines (well-organized)
- **Documentation**: 50+ pages
- **Diagrams**: 3 architecture + 5 wireframes
- **Design Patterns**: 3 major patterns applied

---

## 9. Repository Structure

```
stock-backtester/
├── src/
│   ├── app.py                 # Main application
│   ├── data_loader.py         # Data layer
│   ├── strategies.py          # Business logic
│   ├── backtest_engine.py     # Business logic
│   ├── visualization.py       # Presentation
│   ├── ui_components.py       # Presentation
│   └── requirements.txt       # Dependencies
├── docs/
│   └── design/
│       ├── SOFTWARE_DESIGN_DOCUMENT.md    (18 pages)
│       ├── DESIGN_PRINCIPLES.md           (8 pages)
│       ├── DESIGN_DECISIONS.md            (13 pages)
│       ├── UI_DESIGN.md                   (11 pages)
│       ├── README.md                      (Summary)
│       └── *.png                          (All diagrams)
├── diagrams/                  # Architecture diagrams
├── wireframes/                # Figma exports
└── README.md                  # Main documentation
```

---

## 10. Tools Used

- **Diagrams**: PNG exports (originally created with design tools)
- **UI Design**: Figma (link: https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal)
- **Code**: Python 3.x with Streamlit, Pandas, Matplotlib
- **Version Control**: Git/GitHub
- **Documentation**: Markdown

---

## Conclusion

The Stock Strategy Backtester Lite demonstrates professional software design through:
- Proper application of abstraction, modularity, cohesion, and coupling principles
- Use of industry-standard design patterns (Strategy, Factory, Layered Architecture)
- Clear documentation of design decisions with rationale
- User-friendly interface with consistent design language
- Extensible architecture that makes future enhancements easy

The refactored codebase is maintainable, testable, and serves as an excellent example of good software engineering practices in an educational context.

---

**GitHub Repository**: https://github.com/Nihaal2004/stock-backtester  
**Complete Documentation**: `/docs/design/`  
**Figma Designs**: https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal

---

*End of Executive Summary*
