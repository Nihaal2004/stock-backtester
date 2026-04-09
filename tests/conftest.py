import io
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture
def deterministic_price_df() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=120, freq="D")
    close = 100 + np.sin(np.linspace(0, 12 * np.pi, 120)) * 5 + np.linspace(0, 8, 120)
    return pd.DataFrame({"Date": dates, "Close": close})


@pytest.fixture
def regression_price_df() -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=40, freq="D")
    close = 100 + np.sin(np.linspace(0, 6 * np.pi, 40)) * 5 + np.linspace(0, 3, 40)
    return pd.DataFrame({"Date": dates, "Close": close})


@pytest.fixture
def deterministic_csv_file(deterministic_price_df: pd.DataFrame) -> io.StringIO:
    return io.StringIO(deterministic_price_df.to_csv(index=False))
