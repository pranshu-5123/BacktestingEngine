import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA

# def forecast_prices(data, order=(5, 1, 0), steps=10):
#     """
#     Forecast future prices using ARIMA.
#     Args:
#         data (pd.DataFrame): Historical price data.
#         order (tuple): ARIMA order (p, d, q).
#         steps (int): Number of steps to forecast.
#     Returns:
#         pd.Series: Forecasted prices.
#     """
#     model = ARIMA(data['Close'], order=order)
#     model_fit = model.fit()
#     forecast = model_fit.forecast(steps=steps)
#     return pd.Series(forecast, index=pd.date_range(data.index[-1], periods=steps+1, freq='D')[1:])

from statsmodels.tsa.holtwinters import ExponentialSmoothing

def forecast_ets(data, seasonal='add', trend='add', steps=10):
    """
    Forecast future prices using Exponential Smoothing.
    Args:
        data (pd.DataFrame): Historical price data with datetime index
        seasonal (str): Seasonal component type ('add' or 'mul')
        trend (str): Trend component type ('add' or 'mul')
        steps (int): Number of steps to forecast
    Returns:
        pd.Series: Forecasted prices with proper date index
    """
    # Fit the model
    model = ExponentialSmoothing(
        data['Close'],
        trend=trend,
        seasonal=seasonal,
        seasonal_periods=min(12, len(data) // 2)  # Dynamic seasonal period
    )
    model_fit = model.fit()
    
    # Generate forecast with proper date index
    last_date = data.index[-1]
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=steps,
        freq='B'  # Business days
    )
    forecast = model_fit.forecast(steps)
    forecast.index = forecast_dates
    
    return forecast
