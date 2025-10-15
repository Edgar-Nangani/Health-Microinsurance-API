# Week 10: Predictive Modeling & Advanced Dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Week 10: Predictive Modeling Dashboard", layout="wide", page_icon="🤖")

st.title("🤖 Week 10: Predictive Modeling & Premium Prediction")
st.markdown("This dashboard trains a model to predict insurance claims and estimate future premiums.")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ExpectedClaims.csv")

data = load_data()

# Clean and prepare
data = data.dropna(subset=["Expected_Claim"])
data = data[data["Expected_Claim"] > 0]

# Encode categorical variables
data_encoded = pd.get_dummies(data, columns=["Gender", "Region"], drop_first=True)

# -----------------------------
# Split and Train Model
# -----------------------------
X = data_encoded.drop(columns=["Expected_Claim"])
y = data_encoded["Expected_Claim"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# -----------------------------
# Metrics
# -----------------------------
st.subheader("📊 Model Performance Metrics")
col1, col2 = st.columns(2)
col1.metric("Mean Absolute Error", f"${mae:,.2f}")
col2.metric("R² Score", f"{r2:.3f}")

# -----------------------------
# Feature Importance
# -----------------------------
importance_df = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

st.subheader("🔍 Feature Importance")
fig = px.bar(importance_df, x="Importance", y="Feature", orientation="h", title="Feature Importance for Expected Claims")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# User Prediction Interface
# -----------------------------
st.subheader("🧾 Predict Expected Claim & Premium")

col1, col2, col3 = st.columns(3)

age = col1.number_input("Enter Age:", min_value=18, max_value=90, value=30)
gender = col2.selectbox("Select Gender:", data["Gender"].unique())
region = col3.selectbox("Select Region:", data["Region"].unique())

premium_rate = st.slider("Select Loading Factor (for admin + profit):", 0.0, 0.5, 0.1, step=0.01)

# Prepare input for prediction
input_dict = {
    "Age": [age],
    "Gender": [gender],
    "Region": [region]
}

input_df = pd.DataFrame(input_dict)
input_encoded = pd.get_dummies(input_df, columns=["Gender", "Region"], drop_first=True)

# Align with training columns
for col in X_train.columns:
    if col not in input_encoded.columns:
        input_encoded[col] = 0
input_encoded = input_encoded[X_train.columns]

predicted_claim = model.predict(input_encoded)[0]
predicted_premium = predicted_claim * (1 + premium_rate)

st.write(f"### 🧮 Predicted Expected Claim: *${predicted_claim:,.2f}*")
st.write(f"### 💰 Recommended Premium (with {premium_rate*100:.0f}% loading): *${predicted_premium:,.2f}*")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("🧠 Developed for Week 10: Advanced Predictive Modeling in Microinsurance")

