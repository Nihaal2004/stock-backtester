from backtest_engine import BacktestEngine
from data_loader import DataLoader
from strategies import StrategyFactory


def test_sma_pipeline_integration(deterministic_csv_file):
    loader = DataLoader()
    loaded_df = loader.load_csv(deterministic_csv_file)

    strategy = StrategyFactory.create_strategy("SMA Crossover")
    params = {
        "fast": 5,
        "slow": 15,
        "initial_capital": 100000,
        "transaction_cost": 0.001,
    }
    strategy.validate_params(params, len(loaded_df))
    signal_df = strategy.generate_signals(loaded_df, params)

    engine = BacktestEngine(
        initial_capital=params["initial_capital"],
        transaction_cost_pct=params["transaction_cost"],
    )
    results = engine.run(signal_df)
    trade_log = engine.get_trade_log(results)
    metrics = engine.calculate_metrics(results, trade_log)

    assert len(results) == len(loaded_df)
    assert {
        "signal",
        "position",
        "returns",
        "strategy_returns",
        "trade_flag",
        "equity",
    }.issubset(results.columns)
    assert results["equity"].notna().all()
    assert metrics["days_in_market"] > 0
    assert metrics["num_trades"] >= 1
    assert len(trade_log) == metrics["num_trades"]
