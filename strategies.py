import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data, params):
        self.data = data  # Historical OHLC data
        self.params = params  # Strategy-specific parameters
        self.signals = pd.DataFrame(index=data.index)  # Signal storage

    def generate_signals(self):
        """
        Abstract method to generate buy/sell signals.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
class MovingAverageCrossover(Strategy):
    def generate_signals(self):
        short_window = self.params['short_window']
        long_window = self.params['long_window']
        
        # Calculate moving averages
        self.data['Short_MA'] = self.data['Close'].rolling(window=short_window).mean()
        self.data['Long_MA'] = self.data['Close'].rolling(window=long_window).mean()

        # Generate buy/sell signals
        self.signals['Signal'] = 0
        self.signals['Signal'] = np.where(
            self.data['Short_MA'] > self.data['Long_MA'], 1, -1
        )
        return self.signals

class RSIStrategy(Strategy):
    def generate_signals(self):
        period = self.params['rsi_period']
        overbought = self.params['overbought']
        oversold = self.params['oversold']
        
        # Calculate RSI
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        rs = gain / loss
        self.data['RSI'] = 100 - (100 / (1 + rs))
        
        # Generate buy/sell signals
        self.signals['Signal'] = 0
        self.signals['Signal'] = np.where(
            self.data['RSI'] < oversold, 1, 
            np.where(self.data['RSI'] > overbought, -1, 0)
        )
        return self.signals
    
class BollingerBands(Strategy):
    def generate_signals(self):
        period = self.params['period']
        std_dev = self.params['std_dev']

        # Calculate Bollinger Bands
        self.data['MA'] = self.data['Close'].rolling(window=period).mean()
        self.data['Upper_Band'] = self.data['MA'] + (self.data['Close'].rolling(window=period).std() * std_dev)
        self.data['Lower_Band'] = self.data['MA'] - (self.data['Close'].rolling(window=period).std() * std_dev)

        # Generate buy/sell signals
        self.signals['Signal'] = 0
        self.signals['Signal'] = np.where(
            self.data['Close'] < self.data['Lower_Band'], 1,
            np.where(self.data['Close'] > self.data['Upper_Band'], -1, 0)
        )
        return self.signals

class MACD(Strategy):
    def generate_signals(self):
        fast_period = self.params['fast_period']
        slow_period = self.params['slow_period']
        signal_period = self.params['signal_period']

        # Calculate MACD
        self.data['EMA_Fast'] = self.data['Close'].ewm(span=fast_period, adjust=False).mean()
        self.data['EMA_Slow'] = self.data['Close'].ewm(span=slow_period, adjust=False).mean()
        self.data['MACD'] = self.data['EMA_Fast'] - self.data['EMA_Slow']
        self.data['Signal_Line'] = self.data['MACD'].ewm(span=signal_period, adjust=False).mean()

        # Generate buy/sell signals
        self.signals['Signal'] = 0
        self.signals['Signal'] = np.where(
            self.data['MACD'] > self.data['Signal_Line'], 1, 
            np.where(self.data['MACD'] < self.data['Signal_Line'], -1, 0)
        )
        return self.signals

class Breakout(Strategy):
    def generate_signals(self):
        breakout_period = self.params['breakout_period']

        # Calculate breakout levels
        self.data['Recent_High'] = self.data['High'].rolling(window=breakout_period).max()
        self.data['Recent_Low'] = self.data['Low'].rolling(window=breakout_period).min()

        # Generate buy/sell signals
        self.signals['Signal'] = 0
        self.signals['Signal'] = np.where(
            self.data['Close'] > self.data['Recent_High'], 1,
            np.where(self.data['Close'] < self.data['Recent_Low'], -1, 0)
        )
        return self.signals



