import pandas as pd
def backtest_strategy(data, signals, initial_balance=100000):
    """
    Backtest a strategy and calculate portfolio performance.
    Args:
        data (pd.DataFrame): Historical OHLC data.
        signals (pd.DataFrame): Generated buy/sell signals.
        initial_balance (float): Starting portfolio balance.
    Returns:
        dict: Performance metrics.
    """
    balance = initial_balance
    position = 0
    trades = []

    for i in range(len(signals)):
        if signals['Signal'].iloc[i] == 1:  # Buy Signal
            if balance > 0:  # Ensure funds are available
                position = balance / data['Close'].iloc[i]
                balance = 0  # Invest all money
        elif signals['Signal'].iloc[i] == -1:  # Sell Signal
            if position > 0:  # Ensure a position exists
                balance = position * data['Close'].iloc[i]
                position = 0  # Exit position
                trades.append(balance - initial_balance)  # Record trade profit/loss

    # Final portfolio value
    final_value = balance + (position * data['Close'].iloc[-1])

    # Calculate Metrics
    cagr = ((final_value / initial_balance) ** (1 / (len(data) / 252))) - 1 if final_value > 0 else -1
    returns = pd.Series(trades)
    sharpe_ratio = returns.mean() / returns.std() if not returns.empty and returns.std() != 0 else None
    drawdown = (returns.cumsum().max() - returns.cumsum().min()) / returns.cumsum().max() if not returns.empty else None
    win_rate = (returns > 0).sum() / len(returns) * 100 if len(returns) > 0 else None

    return {
        "Final Portfolio Value": final_value,
        "CAGR": cagr,
        "Sharpe Ratio": sharpe_ratio,
        "Max Drawdown": drawdown,
        "Win Rate": win_rate,
    }
