import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Smart Car Health Predictor", page_icon="🚗")

score_model = joblib.load("score_model.pkl")
part_model = joblib.load("part_model.pkl")

st.title("🚗 Smart Car Health Predictor")
st.write("Enter your car details to check its health.")

car_age = st.number_input("Car age (years)", 0, 15, 5)
km_driven = st.number_input("Total km driven", 0, 200000, 50000, step=1000)
km_since_service = st.number_input("Km since last service", 0, 15000, 5000, step=500)
style = st.selectbox("Driving style", ["Calm", "Normal", "Aggressive"])
traffic = st.selectbox("Traffic where you drive", ["Low", "Medium", "Heavy"])
road = st.selectbox("Road condition", ["Smooth", "Mixed", "Very rough"])

messages = {
    "Brakes": "Brake pads",
    "Engine oil": "Engine oil and filter",
    "Suspension": "Suspension",
    "Battery": "Battery",
}
costs = {  # (fix now, ignore and pay later) in Rs
    "Brakes": (1500, 8000),
    "Engine oil": (2500, 15000),
    "Suspension": (3000, 12000),
    "Battery": (4500, 9000),
}

if st.button("Check my car"):
    row = pd.DataFrame([{
        "car_age": car_age,
        "km_driven": km_driven,
        "km_since_service": km_since_service,
        "driving_style": ["Calm", "Normal", "Aggressive"].index(style),
        "traffic": ["Low", "Medium", "Heavy"].index(traffic),
        "rough_road": ["Smooth", "Mixed", "Very rough"].index(road),
    }])

    score = int(score_model.predict(row)[0])
    part = part_model.predict(row)[0]

    if score >= 70:
        st.success(f"Health score: {score}/100 🟢 Good")
    elif score >= 40:
        st.warning(f"Health score: {score}/100 🟡 Needs attention")
    else:
        st.error(f"Health score: {score}/100 🔴 Risky")

    if score >= 70:
        st.write("Your car looks healthy. Keep up regular servicing.")
    else:
        km_left = max(200, round(score * 15, -2))
        st.write(f"**{messages[part]} needs checking within {km_left} km.**")
        fix_now, later = costs[part]
        st.subheader("💰 Cost saver")
        c1, c2 = st.columns(2)
        c1.metric("Fix now", f"Rs {fix_now:,}")
        c2.metric("Ignore it, pay later", f"Rs {later:,}")
        st.info(f"Fixing now saves about Rs {later - fix_now:,}.")