"""
Data Loader Module
Handles CSV file loading, validation, and preprocessing.
Demonstrates high cohesion - all data-related operations in one place.
"""
import pandas as pd
from typing import Tuple


class DataLoader:
    """
    Responsible for loading and validating stock price data.
    Single Responsibility: Data input and validation only.
    """
    
    REQUIRED_COLUMNS = {"Date", "Close"}
    MIN_ROWS = 10
    
    def __init__(self):
        self.df = None
        
    def load_csv(self, uploaded_file) -> pd.DataFrame:
        """
        Load and clean CSV file with required columns.
        
        Args:
            uploaded_file: File object from streamlit uploader
            
        Returns:
            pd.DataFrame: Cleaned dataframe with Date and Close columns
            
        Raises:
            ValueError: If required columns missing or insufficient data
        """
        df = pd.read_csv(uploaded_file)
        df = self._normalize_columns(df)
        self._validate_columns(df)
        df = self._clean_data(df)
        self._validate_min_rows(df)
        self.df = df
        return df
    
    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Strip whitespace from column names."""
        col_map = {c: c.strip() for c in df.columns}
        return df.rename(columns=col_map)
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Check if required columns exist."""
        if not self.REQUIRED_COLUMNS.issubset(df.columns):
            missing = sorted(list(self.REQUIRED_COLUMNS - set(df.columns)))
            raise ValueError(f"Missing required columns: {missing}. Required: Date, Close")
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to proper types and remove invalid rows."""
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df = df.dropna(subset=["Date", "Close"])
        df = df.sort_values("Date").reset_index(drop=True)
        return df
    
    def _validate_min_rows(self, df: pd.DataFrame) -> None:
        """Ensure minimum data requirement."""
        if len(df) < self.MIN_ROWS:
            raise ValueError(
                f"Not enough valid rows after cleaning. "
                f"Provide at least {self.MIN_ROWS} rows."
            )
    
    def filter_date_range(self, df: pd.DataFrame, 
                         start_date: pd.Timestamp, 
                         end_date: pd.Timestamp) -> pd.DataFrame:
        """
        Filter dataframe by date range.
        
        Args:
            df: Input dataframe
            start_date: Start date
            end_date: End date
            
        Returns:
            Filtered dataframe
        """
        filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)].copy()
        filtered = filtered.reset_index(drop=True)
        
        if len(filtered) < self.MIN_ROWS:
            raise ValueError(
                f"Date range resulted in insufficient data ({len(filtered)} rows). "
                f"Need at least {self.MIN_ROWS} rows."
            )
        
        return filtered
