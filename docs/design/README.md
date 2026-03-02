# Design Documentation

This folder contains comprehensive design documentation for the Stock Strategy Backtester Lite application.

## 📄 Documents

### 1. SOFTWARE_DESIGN_DOCUMENT.md
**Complete software design document (18 pages)**

Includes:
- Introduction and design goals
- Design principles applied (abstraction, modularity, cohesion, coupling)
- High-level architecture explanation
- Detailed module design
- User interface design
- Design decisions and rationale
- Future extensibility considerations

**Read this first** for a complete understanding of the system design.

### 2. DESIGN_PRINCIPLES.md
**Detailed explanation of design principles (8 pages)**

Covers:
- Abstraction with examples
- Modularity and module structure
- High cohesion implementation
- Low coupling strategies
- Design patterns (Strategy, Factory)
- Single Responsibility Principle
- Open/Closed Principle
- Before/after comparison

**Read this** to understand the principles behind the design.

### 3. DESIGN_DECISIONS.md
**Rationale for key design decisions (13 pages)**

Explains:
- Why modular architecture?
- Why Strategy pattern?
- Why Factory pattern?
- Why separate BacktestEngine?
- Why layered architecture?
- Why next-day execution?
- Why transaction costs?
- Why form-based UI?
- Why DataFrames?
- Why clear error messages?

Each decision includes alternatives considered and trade-offs made.

**Read this** to understand WHY we made specific choices.

### 4. UI_DESIGN.md
**User interface design documentation (11 pages)**

Covers:
- UI design principles (consistency, clarity, accessibility)
- All 6 screen designs with wireframes
- User workflow and journey
- Layout structure
- Color scheme and typography
- Interactive elements
- Feedback mechanisms
- Mobile considerations

**Read this** to understand the user interface design.

## 🖼️ Diagrams

### Architecture Diagrams
- **high level architecture.png** - 3-layer architecture overview
- **Architecture.png** - Detailed component architecture
- **backtest pipline.png** - Backtest execution flow

### UI Wireframes (from Figma)
- **home.png** - Welcome screen
- **csv import.png** - File upload interface
- **stock preview.png** - Data preview table
- **strategy picker.png** - Strategy configuration
- **equity curve.png** - Results chart
- *(Need 6th screen - consider adding Settings or Trade Details)*

## 📊 Quick Reference

### Design Principles Summary

| Principle | Implementation | Benefit |
|-----------|---------------|---------|
| **Abstraction** | Strategy base class | Simpler usage |
| **Modularity** | 6 independent modules | Better organization |
| **High Cohesion** | Single-purpose modules | Easier to understand |
| **Low Coupling** | Interface communication | Easier to change |
| **SRP** | One responsibility per module | Easier to maintain |
| **Open/Closed** | Strategy pattern | Safe to extend |

### Module Structure

```
src/
├── data_loader.py       # Data Layer
├── strategies.py        # Business Logic Layer
├── backtest_engine.py   # Business Logic Layer
├── visualization.py     # Presentation Layer
├── ui_components.py     # Presentation Layer
└── app.py              # Orchestrator
```

### Architecture Layers

```
Presentation Layer
    ↓ (displays)
Business Logic Layer
    ↓ (processes)
Data Layer
    ↓ (loads)
CSV File
```

## 🎯 For Assignment Reviewers

This documentation demonstrates:

✅ **Design Principles Applied**
- Clear examples of abstraction, modularity, cohesion, coupling
- Design patterns (Strategy, Factory, Layered)
- SOLID principles (especially SRP and OCP)

✅ **High-Level Architecture**
- Layered architecture with clear justification
- Component diagrams showing interactions
- Flow diagrams showing execution pipeline

✅ **User Interface Design**
- 6 Figma screens (5 in wireframes, need 1 more)
- Consistent design language
- User-friendly features documented

✅ **Design Decisions & Rationale**
- 10 key decisions explained
- Alternatives considered for each
- Trade-offs explicitly stated

✅ **Complete Documentation**
- 50+ pages of design documentation
- Professional diagrams
- Code examples throughout

## 📦 Deliverables Checklist

For Digital Assignment 2:

### Design Document (PDF)
- [ ] Convert SOFTWARE_DESIGN_DOCUMENT.md to PDF
- [ ] Include all diagrams
- [ ] Ensure 6-10 pages (currently 18 pages - may need to condense)

### GitHub Repo Updates
- [x] Created /docs/design/ folder
- [x] Added all documentation files
- [x] Added PNG exports of diagrams
- [x] Added wireframe screenshots
- [x] Updated README.md with Software Design section
- [x] Included Figma link

### Tools Used
- [x] Diagrams: Available in /diagrams (PNG format)
- [x] UI: Figma link in README
- [x] Code: Fully refactored to demonstrate design

## 🚀 How to Use This Documentation

### For Understanding the Design
1. Start with **SOFTWARE_DESIGN_DOCUMENT.md**
2. Review **Architecture Diagrams** (high level architecture.png)
3. Read **DESIGN_PRINCIPLES.md** for detailed explanations

### For Understanding Decisions
1. Read **DESIGN_DECISIONS.md**
2. Each decision has "Why?" and "Alternatives" sections
3. See trade-offs explicitly stated

### For Understanding UI
1. Read **UI_DESIGN.md**
2. View wireframes in this folder
3. Check Figma link for interactive prototype

### For Implementation
1. Review module structure in design docs
2. Check code in `/src` folder
3. See how design principles are applied in actual code

## 📝 Notes

### Strengths of This Design
- **Professional Quality**: Industry-standard patterns and practices
- **Educational**: Code clearly demonstrates design principles
- **Maintainable**: Easy to understand and modify
- **Extensible**: Simple to add new features
- **Well-Documented**: Comprehensive documentation

### Areas for Future Enhancement
1. Add 6th Figma screen (Settings or Help page)
2. Create Draw.io source files (.drawio format) for diagrams
3. Add unit tests to demonstrate testability
4. Create sequence diagrams for complex interactions
5. Add database layer for saving results

## 🔗 Links

- **GitHub Repo**: https://github.com/Nihaal2004/stock-backtester
- **Figma Designs**: https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal
- **Main README**: [../../README.md](../../README.md)

---

**Last Updated**: March 2, 2026  
**Version**: 2.0 (Modular Refactor)
