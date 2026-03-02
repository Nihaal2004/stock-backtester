"""
Trading Strategies Module
Implements various trading strategies using Strategy pattern.
Demonstrates abstraction and polymorphism through base Strategy class.
"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any


class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    Demonstrates abstraction - defines interface without implementation.
    """
    
    @abstractmethod
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """
        Generate trading signals for the given data.
        
        Args:
            df: DataFrame with at least 'Close' column
            params: Strategy-specific parameters
            
        Returns:
            DataFrame with added 'signal' column (1=long, 0=flat)
        """
        pass
    
    @abstractmethod
    def validate_params(self, params: Dict[str, Any], data_length: int) -> None:
        """
        Validate strategy parameters.
        
        Args:
            params: Strategy parameters to validate
            data_length: Number of rows in data
            
        Raises:
            ValueError: If parameters are invalid
        """
        pass


class SMAStrategy(Strategy):
    """
    Simple Moving Average Crossover Strategy.
    Buy when fast SMA crosses above slow SMA, sell on cross below.
    """
    
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Generate signals based on SMA crossover."""
        df = df.copy()
        fast_period = int(params['fast'])
        slow_period = int(params['slow'])
        
        df['fast_sma'] = self._sma(df['Close'], fast_period)
        df['slow_sma'] = self._sma(df['Close'], slow_period)
        df['signal'] = (df['fast_sma'] > df['slow_sma']).astype(int)
        
        return df
    
    def validate_params(self, params: Dict[str, Any], data_length: int) -> None:
        """Validate SMA parameters."""
        fast = int(params.get('fast', 0))
        slow = int(params.get('slow', 0))
        
        if fast >= slow:
            raise ValueError("Fast SMA must be less than Slow SMA.")
        
        if data_length < slow + 2:
            raise ValueError(
                f"Not enough rows ({data_length}) for Slow SMA={slow}. "
                f"Use smaller windows or more data."
            )
    
    @staticmethod
    def _sma(series: pd.Series, window: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        return series.rolling(window, min_periods=window).mean()


class RSIStrategy(Strategy):
    """
    RSI (Relative Strength Index) Strategy.
    Buy when RSI < buy_threshold, sell when RSI > sell_threshold.
    """
    
    def generate_signals(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Generate signals based on RSI thresholds."""
        df = df.copy()
        period = int(params['period'])
        buy_threshold = float(params['buy_threshold'])
        sell_threshold = float(params['sell_threshold'])
        
        df['rsi'] = self._rsi(df['Close'], period)
        df['signal'] = self._generate_position_signals(
            df['rsi'], buy_threshold, sell_threshold
        )
        
        return df
    
    def validate_params(self, params: Dict[str, Any], data_length: int) -> None:
        """Validate RSI parameters."""
        period = int(params.get('period', 0))
        buy_threshold = float(params.get('buy_threshold', 0))
        sell_threshold = float(params.get('sell_threshold', 100))
        
        if buy_threshold >= sell_threshold:
            raise ValueError("Buy threshold must be less than Sell threshold.")
        
        if data_length < period + 2:
            raise ValueError(
                f"Not enough rows ({data_length}) for RSI period={period}. "
                f"Use smaller period or more data."
            )
    
    @staticmethod
    def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index."""
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        avg_gain = gain.rolling(period, min_periods=period).mean()
        avg_loss = loss.rolling(period, min_periods=period).mean()
        rs = avg_gain / (avg_loss + 1e-12)
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def _generate_position_signals(rsi: pd.Series, 
                                   buy_threshold: float, 
                                   sell_threshold: float) -> pd.Series:
        """
        Generate position signals using state machine logic.
        Maintains position state to avoid oscillation.
        """
        in_position = 0
        positions = []
        
        for value in rsi.fillna(50):
            if in_position == 0 and value < buy_threshold:
                in_position = 1
            elif in_position == 1 and value > sell_threshold:
                in_position = 0
            positions.append(in_position)
        
        return pd.Series(positions, index=rsi.index)


class StrategyFactory:
    """
    Factory pattern for creating strategy instances.
    Demonstrates low coupling - UI doesn't need to know strategy internals.
    """
    
    _strategies = {
        'SMA Crossover': SMAStrategy,
        'RSI Threshold': RSIStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_name: str) -> Strategy:
        """
        Create strategy instance by name.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Strategy instance
            
        Raises:
            ValueError: If strategy name not found
        """
        strategy_class = cls._strategies.get(strategy_name)
        if strategy_class is None:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        return strategy_class()
    
    @classmethod
    def get_available_strategies(cls) -> list:
        """Get list of available strategy names."""
        return list(cls._strategies.keys())
