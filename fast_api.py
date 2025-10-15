import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm

# Load training data
data = pd.read_csv("C:/Users/HP/Desktop/Python Project/data/clean/uganda_health_claims_clean.csv")
data["Gender"] = data["Gender"].astype("category")
data["Region"] = data["Region"].astype("category")
data["Hospitalization"] = data["Hospitalization"].astype(int)

# Rebuild frequency model
freq_model = smf.glm(
    formula="Hospitalization ~ Age + Gender + Region",
    data=data,
    family=sm.families.Poisson()
).fit()

from fastapi import FastAPI

app = FastAPI(title="Health Microinsurance API")

from fastapi import FastAPI

app = FastAPI(title="Health Microinsurance API")

# ✅ Root route for homepage
@app.get("/")
def read_root():
    return {"message": "Welcome to the Health Microinsurance API"}

# ✅ Prediction route
@app.get("/predict")
async def predict_claim(Age: int, Gender: str, Region: str):
    gender_map = {
        "Male": "M", "male": "M", "MALE": "M",
        "Female": "F", "female": "F", "FEMALE": "F"
    }
    region_map = {
        "CENTRAL": "Central", "central": "Central", "Central": "Central",
        "EASTERN": "Eastern", "eastern": "Eastern", "Eastern": "Eastern",
        "NORTHERN": "Northern", "northern": "Northern", "Northern": "Northern",
        "WESTERN": "Western", "western": "Western", "Western": "Western"
    }

    Gender = gender_map.get(Gender, Gender)
    Region = region_map.get(Region, Region)

    input_df = pd.DataFrame({
        "Age": [Age],
        "Gender": pd.Categorical([Gender], categories=["F", "M"]),
        "Region": pd.Categorical([Region], categories=["Central", "Eastern", "Northern", "Western"])
    })

    predicted_freq = freq_model.predict(input_df)[0]

    return {
        "predicted_frequency": round(predicted_freq, 4),
        "parameters": {"Age": Age, "Gender": Gender, "Region": Region}
    }
