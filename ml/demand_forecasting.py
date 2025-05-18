# backend/ml/demand_forecasting.py

import pandas as pd
from prophet import Prophet
import numpy as np
from datetime import datetime, timedelta

def simulate_ticket_sales(event_id: int, days: int = 60):
    """
    Simulate daily ticket sales data for an event for the past `days`.
    """
    dates = [datetime.today() - timedelta(days=x) for x in reversed(range(days))]
    # Simulate sales with some random walk + weekly seasonality
    np.random.seed(event_id)  # seed for reproducibility
    base_sales = np.maximum(5 + np.random.randn(days).cumsum() + 3 * np.sin(np.arange(days) * 2 * np.pi / 7), 0).astype(int)
    data = pd.DataFrame({'ds': dates, 'y': base_sales})
    return data

def train_forecast_model(sales_data: pd.DataFrame):
    """
    Train Prophet model and return it.
    """
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(sales_data)
    return model

def forecast_sales(model, periods: int = 30):
    """
    Forecast sales for the next `periods` days.
    """
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == '__main__':
    event_id = 1
    sales_data = simulate_ticket_sales(event_id)
    model = train_forecast_model(sales_data)
    forecast = forecast_sales(model)
    print(forecast.tail(10))
