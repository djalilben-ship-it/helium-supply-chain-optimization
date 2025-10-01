import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# ---------------------------------------------------------------------
# Ensure results folder exists
# ---------------------------------------------------------------------
RESULTS_DIR = os.path.join("..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------
# Example Port Ranking Results (AHP + TOPSIS)
# ---------------------------------------------------------------------
ports = ["Oran", "Algiers", "Skikda"]
scores = [0.85, 0.72, 0.65]
ranking_df = pd.DataFrame({"Port": ports, "Score": scores})
ranking_path = os.path.join(RESULTS_DIR, "port_ranking.csv")
ranking_df.to_csv(ranking_path, index=False)

# ---------------------------------------------------------------------
# Example Forecasting Results
# ---------------------------------------------------------------------
years = [2021, 2022, 2023, 2024, 2025]
production = [400, 420, 460, 500, 540]
model = ExponentialSmoothing(production, trend="add").fit()
forecast = model.forecast(2)  # forecast 2026–2027
forecast_df = pd.DataFrame({"Year": [2026, 2027], "Forecast": forecast})
forecast_path = os.path.join(RESULTS_DIR, "forecast.csv")
forecast_df.to_csv(forecast_path, index=False)

# Plot forecast curve
plt.plot(years, production, label="Actual")
plt.plot([2026, 2027], forecast, label="Forecast", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Truckloads")
plt.legend()
plt.title("Helium Production Forecast")
plot_path = os.path.join(RESULTS_DIR, "forecast.png")
plt.savefig(plot_path)
plt.close()

# ---------------------------------------------------------------------
# Example TSP Route Results
# ---------------------------------------------------------------------
route = [0, 3, 2, 1, 0]
route_str = " → ".join(map(str, route))

# ---------------------------------------------------------------------
# Write Summary File
# ---------------------------------------------------------------------
summary = f"""
Helium Supply Chain Optimization - Simulation Results

📌 Optimal Port: {ports[0]} (Score: {scores[0]})
📊 Forecast: +35% shipments (≈ 550 truckloads/year by 2025)
🚚 Optimal Route: {route_str}
"""

summary_path = os.path.join(RESULTS_DIR, "simulation_summary.txt")
with open(summary_path, "w", encoding="utf-8") as f:
    f.write(summary)

print("✅ Results generated in 'results/' folder:")
print(f"- {ranking_path}")
print(f"- {forecast_path}")
print(f"- {plot_path}")
print(f"- {summary_path}")
