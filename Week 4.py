# rebuild_and_save_models.py
import pandas as pd
import statsmodels.formula.api as smf
import pickle
import os
import statsmodels.api as sm

# Load cleaned data
data = pd.read_csv("C:/Users/HP/Desktop/Python Project/data/clean/uganda_health_claims_clean.csv")
data["Gender"] = data["Gender"].astype("category")
data["Region"] = data["Region"].astype("category")
data["Hospitalization"] = data["Hospitalization"].astype(int)

# Frequency model
freq_model = smf.glm(
    formula="Hospitalization ~ Age + Gender + Region",
    data=data,
    family=sm.families.Poisson()
).fit()

# Severity model
severity_data = data[data["Hospitalization"] == 1].copy()
sev_model = smf.glm(
    formula="ClaimCost ~ Age + Gender + Region",
    data=severity_data,
    family=sm.families.Gamma(link=sm.families.links.log())
).fit()

# Save models
os.makedirs("models", exist_ok=True)
with open("C:/Users/HP/Desktop/Python Project/data/ml/frequency_model.pkl", "wb") as f:
    pickle.dump(freq_model, f)

with open("C:/Users/HP/Desktop/Python Project/data/ml/severity_model.pkl", "wb") as f:
    pickle.dump(sev_model, f)

print("✅ Models saved to models/")
