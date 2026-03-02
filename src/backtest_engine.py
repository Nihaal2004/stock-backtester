"""
Backtesting Engine Module
Core backtesting logic with transaction costs and equity tracking.
Demonstrates separation of concerns - backtesting independent of strategies.
"""
import pandas as pd
import numpy as np
from typing import List, Tuple


class BacktestEngine:
    """
    Executes backtest given signals and market data.
    Single Responsibility: Execute trades and calculate returns.
    Low coupling: Works with any signal source (doesn't depend on strategy details).
    """
    
    def __init__(self, initial_capital: float = 100000, 
                 transaction_cost_pct: float = 0.004):
        """
        Initialize backtest engine.
        
        Args:
            initial_capital: Starting capital
            transaction_cost_pct: Transaction cost as decimal (0.004 = 0.4%)
        """
        self.initial_capital = initial_capital
        self.transaction_cost = transaction_cost_pct
        self.results = None
        
    def run(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Execute backtest on data with signals.
        
        Args:
            df: DataFrame with 'Close' and 'signal' columns
            
        Returns:
            DataFrame with backtest results including equity curve
        """
        df = df.copy()
        
        # Next-day execution: position today = signal yesterday
        # Prevents lookahead bias
        df['position'] = df['signal'].shift(1).fillna(0).astype(int)
        
        # Calculate returns
        df['returns'] = df['Close'].pct_change().fillna(0.0)
        df['strategy_returns'] = df['position'] * df['returns']
        
        # Apply transaction costs on position changes
        df['trade_flag'] = df['position'].diff().abs().fillna(0).astype(int)
        df['strategy_returns'] = df['strategy_returns'] - (
            df['trade_flag'] * self.transaction_cost
        )
        
        # Calculate equity curve
        df['equity'] = self.initial_capital * (1 + df['strategy_returns']).cumprod()
        
        self.results = df
        return df
    
    def get_trade_log(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract individual trades from backtest results.
        
        Args:
            df: DataFrame with backtest results
            
        Returns:
            DataFrame with trade entries and exits
        """
        if df is None or len(df) == 0:
            return pd.DataFrame()
        
        trades = []
        position_prev = df['position'].shift(1).fillna(0).astype(int)
        
        # Find entries and exits
        entries = df.index[(position_prev == 0) & (df['position'] == 1)].tolist()
        exits = df.index[(position_prev == 1) & (df['position'] == 0)].tolist()
        
        # Match entries with exits
        for entry_idx in entries:
            matching_exits = [x for x in exits if x > entry_idx]
            if not matching_exits:
                break  # Open trade, ignore for now
            
            exit_idx = matching_exits[0]
            
            entry_date = df.loc[entry_idx, 'Date']
            exit_date = df.loc[exit_idx, 'Date']
            entry_price = df.loc[entry_idx, 'Close']
            exit_price = df.loc[exit_idx, 'Close']
            pnl_pct = (exit_price / entry_price - 1) * 100
            
            trades.append({
                'Entry Date': entry_date,
                'Exit Date': exit_date,
                'Entry Price': entry_price,
                'Exit Price': exit_price,
                'P/L %': round(pnl_pct, 2)
            })
            
            exits.remove(exit_idx)
        
        return pd.DataFrame(trades)
    
    def calculate_metrics(self, df: pd.DataFrame, 
                         trade_log: pd.DataFrame) -> dict:
        """
        Calculate performance metrics.
        
        Args:
            df: Backtest results DataFrame
            trade_log: Trade log DataFrame
            
        Returns:
            Dictionary of performance metrics
        """
        equity = df['equity']
        dates = df['Date']
        
        total_return = (equity.iloc[-1] / equity.iloc[0] - 1) * 100
        cagr = self._calculate_cagr(equity, dates)
        max_dd = self._calculate_max_drawdown(equity)
        
        win_rate = np.nan
        if not trade_log.empty and 'P/L %' in trade_log.columns:
            win_rate = (trade_log['P/L %'] > 0).mean() * 100
        
        num_trades = len(trade_log)
        days_in_market = int(df['position'].sum())
        
        return {
            'total_return': total_return,
            'cagr': cagr,
            'max_drawdown': max_dd,
            'win_rate': win_rate,
            'num_trades': num_trades,
            'days_in_market': days_in_market
        }
    
    @staticmethod
    def _calculate_cagr(equity: pd.Series, dates: pd.Series) -> float:
        """Calculate Compound Annual Growth Rate."""
        if len(equity) < 2:
            return np.nan
        
        days = (dates.iloc[-1] - dates.iloc[0]).days
        if days <= 0:
            return np.nan
        
        years = days / 365.25
        cagr = ((equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1) * 100
        return float(cagr)
    
    @staticmethod
    def _calculate_max_drawdown(equity: pd.Series) -> float:
        """Calculate maximum drawdown percentage."""
        if len(equity) == 0:
            return 0.0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        return float(drawdown.min() * 100)
