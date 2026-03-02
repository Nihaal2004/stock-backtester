"""
Visualization Module
Handles all chart generation and data presentation.
Demonstrates separation of concerns - presentation logic isolated.
"""
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from typing import Dict, Any


class Visualizer:
    """
    Responsible for creating charts and displaying results.
    Single Responsibility: Visual presentation only.
    """
    
    @staticmethod
    def plot_equity_curve(df: pd.DataFrame, title: str = "Equity Curve") -> plt.Figure:
        """
        Create equity curve plot.
        
        Args:
            df: DataFrame with 'Date' and 'equity' columns
            title: Chart title
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df['Date'], df['equity'], linewidth=2, color='#1f77b4')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def display_metrics(metrics: Dict[str, Any]) -> None:
        """
        Display performance metrics in Streamlit.
        
        Args:
            metrics: Dictionary of metric names and values
        """
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total Return", 
                f"{metrics['total_return']:.2f}%"
            )
        
        with col2:
            cagr = metrics['cagr']
            st.metric(
                "CAGR", 
                f"{cagr:.2f}%" if pd.notna(cagr) else "N/A"
            )
        
        with col3:
            st.metric(
                "Max Drawdown", 
                f"{metrics['max_drawdown']:.2f}%"
            )
        
        with col4:
            win_rate = metrics['win_rate']
            st.metric(
                "Win Rate", 
                f"{win_rate:.2f}%" if pd.notna(win_rate) else "N/A"
            )
        
        with col5:
            st.metric(
                "# Trades", 
                f"{metrics['num_trades']}"
            )
    
    @staticmethod
    def display_trade_log(trade_log: pd.DataFrame) -> None:
        """
        Display trade log table.
        
        Args:
            trade_log: DataFrame with trade information
        """
        if trade_log.empty:
            st.info("No completed trades found.")
            return
        
        st.dataframe(
            trade_log.style.applymap(
                lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0 
                else 'color: red' if isinstance(x, (int, float)) and x < 0 
                else '',
                subset=['P/L %']
            ),
            use_container_width=True
        )
    
    @staticmethod
    def display_data_preview(df: pd.DataFrame, num_rows: int = 10) -> None:
        """
        Display data preview table.
        
        Args:
            df: DataFrame to display
            num_rows: Number of rows to show
        """
        st.write(f"Data Preview (last {num_rows} rows)")
        st.dataframe(df.tail(num_rows), use_container_width=True)
