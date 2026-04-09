import pytest

from backtest_engine import BacktestEngine
from strategies import RSIStrategy, SMAStrategy


def test_sma_regression_metrics_are_stable(regression_price_df):
    strategy = SMAStrategy()
    params = {"fast": 4, "slow": 9}
    strategy.validate_params(params, len(regression_price_df))
    signal_df = strategy.generate_signals(regression_price_df, params)

    engine = BacktestEngine(initial_capital=100000, transaction_cost_pct=0.001)
    results = engine.run(signal_df)
    trade_log = engine.get_trade_log(results)
    metrics = engine.calculate_metrics(results, trade_log)

    assert metrics["num_trades"] == 2
    assert metrics["days_in_market"] == 14
    assert metrics["total_return"] == pytest.approx(-9.935732012304976, abs=1e-9)
    assert metrics["max_drawdown"] == pytest.approx(-12.218932010172374, abs=1e-9)
    assert float(results["equity"].iloc[-1]) == pytest.approx(90064.26798769503, abs=1e-9)
    assert results["position"].tolist() == [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
        1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
        1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
    ]


def test_rsi_regression_signal_sequence_is_stable(regression_price_df):
    strategy = RSIStrategy()
    params = {"period": 5, "buy_threshold": 40, "sell_threshold": 60}
    strategy.validate_params(params, len(regression_price_df))
    signal_df = strategy.generate_signals(regression_price_df, params)

    assert signal_df["signal"].tolist() == [
        0, 0, 0, 0, 0, 0, 0, 1, 1, 1,
        1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
    ]
