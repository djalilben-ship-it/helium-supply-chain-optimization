# src/forecast.py
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import argparse

def forecast(datafile, periods=5):
    """Forecast helium production with Exponential Smoothing"""
    df = pd.read_csv(datafile)
    series = df['production']

    model = ExponentialSmoothing(series, trend="add", seasonal=None)
    fit = model.fit()

    forecast = fit.forecast(periods)
    return forecast, series, fit.fittedvalues

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="CSV file with 'year' and 'production'")
    args = parser.parse_args()

    forecast_values, series, fitted = forecast(args.data)

    plt.plot(series, label="Actual")
    plt.plot(fitted, label="Fitted")
    plt.plot(range(len(series), len(series) + len(forecast_values)), forecast_values, label="Forecast")
    plt.legend()
    plt.show()

    print("Forecasted Production:", forecast_values.values)
