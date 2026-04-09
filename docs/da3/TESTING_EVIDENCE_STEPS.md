# DA3 Testing Evidence Steps

Run every command from the repository root:

## 1. Install test tools

```powershell
python -m pip install -r requirements-dev.txt
```

## 2. Integration testing screenshot

```powershell
python -m pytest -v tests\test_integration_pipeline.py
```

Take a screenshot of the terminal showing the test passed.  
Suggested filename: `screenshots/integration-test-proof.png`

## 3. Regression testing screenshot

```powershell
python -m pytest -v tests\test_regression_backtest.py
```

Take a screenshot of the terminal showing the regression tests passed.  
Suggested filename: `screenshots/regression-test-proof.png`

## 4. Mutation testing screenshot

```powershell
python tools\run_mutation_tests.py
```

Take screenshots showing:
1. Individual mutant status lines (killed/survived).
2. Final mutation summary (score and counts).

Suggested filename: `screenshots/mutation-test-proof.png`
