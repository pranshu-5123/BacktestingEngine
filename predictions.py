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
    model = ExponentialSmoothing(data['Close'], trend=trend, seasonal=seasonal, seasonal_periods=12)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps)
    return forecast
