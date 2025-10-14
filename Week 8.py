# ================================
# WEEK 8: Health Micro-Insurance Dashboard (Streamlit)
# ================================


#Import the necessary libraries
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Step 1: Load the processed data
data_path = "C:/Users/HP/Desktop/Python Project/data/processed/ExpectedClaims.csv"
if not os.path.exists(data_path):
    st.error("ExpectedClaims.csv not found ")
    st.stop()

data = pd.read_csv(data_path)

# Step 2: Sidebar filters
st.set_page_config(page_title="Health Micro-Insurance Dashboard", layout="wide")
st.title("Health Micro-Insurance Dashboard")

region = st.sidebar.selectbox("Select Region:", sorted(data["Region"].unique()))
gender = st.sidebar.selectbox("Select Gender:", sorted(data["Gender"].unique()))
age_range = st.sidebar.slider("Select Age Range:",
                              int(data["Age"].min()), int(data["Age"].max()),
                              (int(data["Age"].min()), int(data["Age"].max())))

# Step 3: Filtered data
filtered = data[
    (data["Region"] == region) &
    (data["Gender"] == gender) &
    (data["Age"] >= age_range[0]) &
    (data["Age"] <= age_range[1])
]


# Step 4: Overview tab
st.subheader("Expected Claim by Age")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(filtered["Age"], filtered["Expected_Claim"], color="steelblue", linewidth=2)
ax.scatter(filtered["Age"], filtered["Expected_Claim"], color="darkred", s=30)
ax.set_title("Expected Claim by Age")
ax.set_xlabel("Age")
ax.set_ylabel("Expected Claim (UGX)")
st.pyplot(fig)

st.subheader("Summary Statistics")
st.text(filtered["Expected_Claim"].describe().to_string())



# Step 5: Raw Data tab
st.subheader("Raw Data")
st.dataframe(filtered)


# Step 6: Download report
st.sidebar.markdown("### ⬇ Download Summary Report")
st.sidebar.download_button(
    label="Download CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name=f"HealthInsurance_Report_{pd.Timestamp.today().date()}.csv",
    mime="text/csv"
)


