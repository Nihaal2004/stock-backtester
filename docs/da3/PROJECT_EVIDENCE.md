# Digital Assignment 3 - Project Evidence

## Project
**Stock Strategy Backtester Lite**  
GitHub: https://github.com/Nihaal2004/stock-backtester

---

## 1. Integration / Regression / Mutation Testing (Screenshots)

Run these commands from repository root, then capture screenshots of terminal output.

```powershell
python -m pip install -r requirements-dev.txt
```

### 1.1 Integration Testing
- Run:
  ```powershell
  python -m pytest -v tests\test_integration_pipeline.py
  ```
- Save screenshot as: `screenshots/integration-test-proof.png`
- Caption: End-to-end flow (data load -> strategy run -> results generation)

### 1.2 Regression Testing
- Run:
  ```powershell
  python -m pytest -v tests\test_regression_backtest.py
  ```
- Save screenshot as: `screenshots/regression-test-proof.png`
- Caption: Existing behavior retained after changes

### 1.3 Mutation Testing
- Run:
  ```powershell
  python tools\run_mutation_tests.py
  ```
- Save screenshot as: `screenshots/mutation-test-proof.png`
- Caption: Mutation harness run with killed/survived mutants summary

---

## 2. Version Management and System Building (Screenshots)

Use these available screenshots:

- `screenshots/pull req proof.png` - Pull request evidence
- `screenshots/merge pr proof.png` - Merge evidence
- `screenshots/project board proof.png` - Project board / work tracking
- `screenshots/docker run.png` - Container build/run proof
- `screenshots/docker dashboard.png` - Running container dashboard
- `screenshots/streamlit run.png` - App startup proof

---

## 3. Developed Functionalities (Screenshots)

Use these available screenshots:

- `screenshots/streamlit dashboard.png` - Main UI
- `screenshots/run1.png` - Backtest execution
- `screenshots/equity curve ex.png` - Equity curve output
- `screenshots/performance.png` - Performance metrics output
- `screenshots/Issues proof.pdf` - Issue tracking proof (optional supporting evidence)

---

## 4. Tools / Technologies Used

| Category | Tools / Technologies |
|---|---|
| Programming Language | Python 3.x |
| UI Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Plotting / Visualization | Matplotlib |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub (PR + merge workflow) |
| Automated Testing | Pytest |
| Mutation Testing | Custom Python mutation harness (`tools/run_mutation_tests.py`) |
| Documentation | Markdown, LaTeX |
| Environment | Windows / PowerShell |

---

## 5. Final PDF Assembly Checklist

1. Insert screenshots under Sections 1, 2, and 3 with short captions.
2. Keep this section order exactly as required in DA3.
3. Export this document as a single PDF named `DA3_Project_Evidence_Nihaal2004.pdf`.
4. Verify all screenshots are readable and not cropped.
