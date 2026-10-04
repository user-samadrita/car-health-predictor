import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("car_data.csv")

features = ["car_age", "km_driven", "km_since_service",
            "driving_style", "traffic", "rough_road"]
X = df[features]

X_train, X_test, y_score_train, y_score_test, y_part_train, y_part_test = train_test_split(
    X, df["health_score"], df["risky_part"], test_size=0.2, random_state=42
)

score_model = RandomForestRegressor(n_estimators=100, random_state=42)
score_model.fit(X_train, y_score_train)

part_model = RandomForestClassifier(n_estimators=100, random_state=42)
part_model.fit(X_train, y_part_train)

print("Health score accuracy (R2):", round(score_model.score(X_test, y_score_test), 3))
print("Risky part accuracy:", round(part_model.score(X_test, y_part_test), 3))

joblib.dump(score_model, "score_model.pkl")
joblib.dump(part_model, "part_model.pkl")
print("Models saved!")