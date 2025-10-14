# Week 9: Microinsurance Claims Prediction Dashboard with Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Week 9: Microinsurance Claims Prediction Dashboard",
    layout="wide",
    page_icon="📊"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    data = pd.read_csv("C:/Users/HP/Desktop/Python Project/data/processed/ExpectedClaims.csv")
    return data

df = load_data()

# -----------------------------
# Dashboard Header
# -----------------------------
st.title("📊 Week 9: Microinsurance Claims Prediction Dashboard")
st.markdown("Use the filters in the sidebar to explore the microinsurance claims data and estimate premiums.")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Options")

regions = st.sidebar.multiselect(
    "Select Region:",
    options=sorted(df["Region"].dropna().unique()),
    default=[]
)

age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

genders = st.sidebar.multiselect(
    "Select Gender:",
    options=sorted(df["Gender"].dropna().unique()),
    default=[]
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if regions:
    filtered_df = filtered_df[filtered_df["Region"].isin(regions)]
filtered_df = filtered_df[(filtered_df["Age"] >= age_range[0]) & (filtered_df["Age"] <= age_range[1])]
if genders:
    filtered_df = filtered_df[filtered_df["Gender"].isin(genders)]

# -----------------------------
# Summary Statistics
# -----------------------------
st.subheader("📈 Summary Statistics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", f"{len(filtered_df):,}")
col2.metric("Average Expected Claim", f"${filtered_df['Expected_Claim'].mean():,.2f}")
col3.metric("Total Expected Claims", f"${filtered_df['Expected_Claim'].sum():,.2f}")

# -----------------------------
# Visualizations
# -----------------------------
st.subheader("📊 Claims Visualization")

tab1, tab2, tab3 = st.tabs(["By Region", "By Gender", "By Age"])

with tab1:
    if "Region" in filtered_df.columns:
        fig_region = px.bar(
            filtered_df.groupby("Region", as_index=False)["Expected_Claim"].mean(),
            x="Region",
            y="Expected_Claim",
            title="Average Expected Claim by Region",
            color="Region"
        )
        st.plotly_chart(fig_region, use_container_width=True)

with tab2:
    if "Gender" in filtered_df.columns:
        fig_gender = px.box(
            filtered_df,
            x="Gender",
            y="Expected_Claim",
            color="Gender",
            title="Claim Distribution by Gender"
        )
        st.plotly_chart(fig_gender, use_container_width=True)

with tab3:
    fig_age = px.scatter(
        filtered_df,
        x="Age",
        y="Expected_Claim",
        color="Gender",
        title="Expected Claim vs Age"
    )
    st.plotly_chart(fig_age, use_container_width=True)

# -----------------------------
# Premium Calculation Section
# -----------------------------
st.subheader("💰 Premium Estimation")

premium_rate = st.slider(
    "Select Loading Factor (for administrative cost & profit margin):",
    0.0, 0.5, 0.1, step=0.01
)

filtered_df["Premium_to_Pay"] = filtered_df["Expected_Claim"] * (1 + premium_rate)

st.write("### Calculated Premiums")
st.dataframe(
    filtered_df[["Region", "Age", "Gender", "Expected_Claim", "Premium_to_Pay"]]
    .head(20)
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("Developed for Week 9: The Python Path — Building Dashboards with Streamlit")

#week 9 streamlit app
