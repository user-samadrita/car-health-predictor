import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000  # number of imaginary cars

df = pd.DataFrame({
    "car_age": rng.integers(0, 15, n),
    "km_driven": rng.integers(2000, 200000, n),
    "km_since_service": rng.integers(0, 15000, n),
    "driving_style": rng.integers(0, 3, n),  # 0 calm, 1 normal, 2 aggressive
    "traffic": rng.integers(0, 3, n),        # 0 low, 2 heavy
    "rough_road": rng.integers(0, 3, n),     # 0 smooth, 2 very rough
})

# Health score: start at 100, subtract for wear
penalty = (df.km_since_service / 15000 * 30 + df.car_age * 1.5
           + df.km_driven / 200000 * 20 + df.driving_style * 5
           + df.traffic * 3 + df.rough_road * 5)
df["health_score"] = (100 - penalty + rng.normal(0, 3, n)).clip(0, 100).round()

# Risky part: whichever part has the highest risk points
risk = pd.DataFrame({
    "Brakes": df.driving_style * 3 + df.traffic * 3 + df.km_since_service / 3000,
    "Engine oil": df.km_since_service / 1500,
    "Suspension": df.rough_road * 4 + df.car_age / 2,
    "Battery": df.car_age * 0.8,
})
df["risky_part"] = risk.idxmax(axis=1)

df.to_csv("car_data.csv", index=False)
print(df.head())