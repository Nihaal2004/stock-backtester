"""
UI Components Module
Streamlit UI components for user interaction.
Demonstrates modularity - UI elements separated from business logic.
"""
import streamlit as st
import pandas as pd
from typing import Tuple, Optional


class UIComponents:
    """
    Collection of reusable UI components.
    Provides consistent interface elements across the application.
    """
    
    @staticmethod
    def render_header() -> None:
        """Render application header."""
        st.set_page_config(
            page_title="Stock Strategy Backtester Lite", 
            layout="wide"
        )
        st.title("📈 Stock Strategy Backtester Lite")
        st.caption(
            "Educational use only. Not financial advice. "
            "Trades execute on next-day close (no lookahead bias)."
        )
    
    @staticmethod
    def render_file_uploader() -> Optional[object]:
        """
        Render file upload component.
        
        Returns:
            Uploaded file object or None
        """
        st.sidebar.header("1️⃣ Data Upload")
        uploaded = st.sidebar.file_uploader(
            "Upload CSV (required: Date, Close)", 
            type=["csv"],
            help="Upload a CSV file with at least 'Date' and 'Close' columns"
        )
        return uploaded
    
    @staticmethod
    def render_date_range_filter(df: pd.DataFrame) -> Tuple[pd.Timestamp, pd.Timestamp]:
        """
        Render date range filter component.
        
        Args:
            df: DataFrame with 'Date' column
            
        Returns:
            Tuple of (start_date, end_date)
        """
        st.sidebar.header("2️⃣ Date Range (Optional)")
        min_date = df['Date'].iloc[0]
        max_date = df['Date'].iloc[-1]
        
        date_range = st.sidebar.date_input(
            "Backtest range",
            value=(min_date.date(), max_date.date()),
            help="Select the date range for backtesting"
        )
        
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1])
        else:
            start_date = min_date
            end_date = max_date
        
        return start_date, end_date
    
    @staticmethod
    def render_strategy_form(strategy_names: list) -> Tuple[str, dict, bool]:
        """
        Render strategy configuration form.
        
        Args:
            strategy_names: List of available strategy names
            
        Returns:
            Tuple of (strategy_name, parameters, run_button_clicked)
        """
        st.sidebar.header("3️⃣ Strategy Configuration")
        
        with st.sidebar.form("backtest_form"):
            strategy = st.selectbox(
                "Choose strategy",
                strategy_names,
                help="Select the trading strategy to backtest"
            )
            
            st.subheader("Backtest Settings")
            initial_capital = st.number_input(
                "Initial capital ($)",
                min_value=1000,
                value=100000,
                step=1000,
                help="Starting portfolio value"
            )
            
            cost_pct = st.number_input(
                "Transaction cost per trade (%)",
                min_value=0.0,
                max_value=5.0,
                value=0.4,
                step=0.1,
                help="Cost incurred on each buy/sell transaction"
            )
            
            st.subheader("Strategy Parameters")
            params = {}
            
            if strategy == "SMA Crossover":
                params['fast'] = st.number_input(
                    "Fast SMA period",
                    min_value=2,
                    value=10,
                    step=1,
                    help="Shorter moving average period"
                )
                params['slow'] = st.number_input(
                    "Slow SMA period",
                    min_value=3,
                    value=30,
                    step=1,
                    help="Longer moving average period"
                )
            
            elif strategy == "RSI Threshold":
                params['period'] = st.number_input(
                    "RSI Period",
                    min_value=2,
                    value=14,
                    step=1,
                    help="Number of periods for RSI calculation"
                )
                params['buy_threshold'] = st.number_input(
                    "Buy when RSI <",
                    min_value=1,
                    max_value=99,
                    value=30,
                    step=1,
                    help="Enter position when RSI falls below this level"
                )
                params['sell_threshold'] = st.number_input(
                    "Sell when RSI >",
                    min_value=1,
                    max_value=99,
                    value=70,
                    step=1,
                    help="Exit position when RSI rises above this level"
                )
            
            params['initial_capital'] = initial_capital
            params['transaction_cost'] = cost_pct / 100.0
            
            run = st.form_submit_button(
                "🚀 Run Backtest",
                use_container_width=True
            )
        
        return strategy, params, run
    
    @staticmethod
    def show_info(message: str) -> None:
        """Display info message."""
        st.info(message)
    
    @staticmethod
    def show_success(message: str) -> None:
        """Display success message."""
        st.success(message)
    
    @staticmethod
    def show_warning(message: str) -> None:
        """Display warning message."""
        st.warning(message)
    
    @staticmethod
    def show_error(message: str) -> None:
        """Display error message."""
        st.error(message)
