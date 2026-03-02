"""
Stock Strategy Backtester Lite - Main Application
Refactored with modular design principles.

Architecture:
- Layered architecture separating UI, Business Logic, and Data
- Strategy pattern for trading strategies
- Factory pattern for strategy creation
- Single Responsibility Principle throughout
- Low coupling between modules

Author: Nihaal2004
"""

# Core imports
import streamlit as st
import pandas as pd

# Module imports - demonstrates modular design
from data_loader import DataLoader
from strategies import StrategyFactory
from backtest_engine import BacktestEngine
from visualization import Visualizer
from ui_components import UIComponents


def main():
    """
    Main application entry point.
    Orchestrates the workflow without containing business logic.
    """
    # Initialize components
    ui = UIComponents()
    data_loader = DataLoader()
    visualizer = Visualizer()
    
    # Render UI
    ui.render_header()
    
    # Step 1: Data Upload
    uploaded_file = ui.render_file_uploader()
    
    if uploaded_file is None:
        ui.show_info("📤 Upload a CSV to continue. Required columns: Date, Close.")
        st.stop()
    
    # Step 2: Load and validate data
    try:
        df = data_loader.load_csv(uploaded_file)
        st.sidebar.success(f"✅ Loaded {len(df)} rows")
        visualizer.display_data_preview(df)
    except Exception as e:
        ui.show_error(f"❌ Data Error: {str(e)}")
        st.stop()
    
    # Step 3: Date range filter (optional)
    try:
        start_date, end_date = ui.render_date_range_filter(df)
        df = data_loader.filter_date_range(df, start_date, end_date)
    except Exception as e:
        ui.show_error(f"❌ Date Range Error: {str(e)}")
        st.stop()
    
    # Step 4: Strategy configuration
    strategy_names = StrategyFactory.get_available_strategies()
    strategy_name, params, run_clicked = ui.render_strategy_form(strategy_names)
    
    if not run_clicked:
        ui.show_info("⚙️ Configure strategy parameters and click **Run Backtest**.")
        st.stop()
    
    # Step 5: Execute backtest
    try:
        # Create strategy instance
        strategy = StrategyFactory.create_strategy(strategy_name)
        
        # Validate parameters
        strategy.validate_params(params, len(df))
        
        # Generate signals
        df_with_signals = strategy.generate_signals(df, params)
        
        # Run backtest
        engine = BacktestEngine(
            initial_capital=params['initial_capital'],
            transaction_cost_pct=params['transaction_cost']
        )
        results = engine.run(df_with_signals)
        
        # Extract trades and calculate metrics
        trade_log = engine.get_trade_log(results)
        metrics = engine.calculate_metrics(results, trade_log)
        
        # Display results
        display_results(visualizer, ui, results, trade_log, metrics)
        
    except Exception as e:
        ui.show_error(f"❌ Backtest Error: {str(e)}")
        st.stop()


def display_results(visualizer: Visualizer, ui: UIComponents,
                   results: pd.DataFrame, trade_log: pd.DataFrame,
                   metrics: dict) -> None:
    """
    Display backtest results.
    
    Args:
        visualizer: Visualizer instance
        ui: UI components instance
        results: Backtest results DataFrame
        trade_log: Trade log DataFrame
        metrics: Performance metrics dictionary
    """
    st.markdown("---")
    st.header("📊 Backtest Results")
    
    # Check if any trades were generated
    if metrics['days_in_market'] == 0:
        ui.show_warning(
            "⚠️ No trades were generated with these parameters. "
            "Try different strategy settings."
        )
    
    # Display metrics
    st.subheader("Performance Metrics")
    visualizer.display_metrics(metrics)
    
    # Display equity curve
    st.subheader("Equity Curve")
    fig = visualizer.plot_equity_curve(results)
    st.pyplot(fig, clear_figure=True)
    
    # Display trade log
    st.subheader("Trade Log")
    visualizer.display_trade_log(trade_log)


if __name__ == "__main__":
    main()
