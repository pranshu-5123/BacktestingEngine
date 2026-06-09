import pandas as pd

class DataPreprocessor:
    def __init__(self, df):
        self.df = df

    def handle_missing_values(self):
        self.df = self.df.ffill().bfill()
        return self.df

    def adjust_prices(self, adjustment_factor):
        # Ensure the columns are numeric
        self.df[['Open', 'High', 'Low', 'Close']] = self.df[['Open', 'High', 'Low', 'Close']].apply(pd.to_numeric, errors='coerce')
        self.df[['Open', 'High', 'Low', 'Close']] *= adjustment_factor
        return self.df

    def convert_date_column(self):
        if 'Date' in self.df.columns:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df.set_index('Date', inplace=True)
        else:
            raise KeyError("The 'Date' column is missing from the DataFrame.")
        return self.df

    def add_missing_dates(self, start_date, end_date):
        all_dates = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
        self.df = self.df.reindex(all_dates)
        return self.df

    def add_technical_indicators(self):
        self.df['SMA_50'] = self.df['Close'].rolling(window=50).mean()  # Simple Moving Average
        self.df['RSI'] = 100 - (100 / (1 + (self.df['Close'].diff(1).clip(lower=0).rolling(window=14).mean() /
                                    self.df['Close'].diff(1).clip(upper=0).abs().rolling(window=14).mean())))
        return self.df

    def remove_duplicates(self):
        self.df = self.df[~self.df.index.duplicated(keep='first')]
        return self.df

    def clean_data(self):
        self.df.sort_index(inplace=True)
        return self.df

    def preprocess_data(self, adjust_factor=1.0, start_date=None, end_date=None):
        # Drop first three rows
        self.df = self.df.iloc[3:].reset_index(drop=True)

        # Rename columns correctly
        self.df.columns = ["Date", "Adj Close", "Close", "High", "Low", "Open", "Volume"]

        # Convert Date column to datetime
        self.df["Date"] = pd.to_datetime(self.df["Date"])

        # Convert numerical columns to float
        numeric_cols = ["Adj Close", "Close", "High", "Low", "Open", "Volume"]
        self.df[numeric_cols] = self.df[numeric_cols].astype(float)

        self.df = self.handle_missing_values()
        self.df = self.adjust_prices(adjust_factor)
        self.df = self.convert_date_column()
        if start_date and end_date:
            self.df = self.add_missing_dates(start_date, end_date)
        self.df = self.remove_duplicates()
        self.df = self.add_technical_indicators()
        self.df = self.clean_data()
        self.df = self.df.ffill()
        self.df = self.df.bfill()
        return self.df
