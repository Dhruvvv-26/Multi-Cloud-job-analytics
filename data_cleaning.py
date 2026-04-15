import pandas as pd
import re

RAW_PATH = "data/job_postings_raw.csv"
OUT_PATH = "data/processed/job_postings_clean.csv"

df = pd.read_csv(RAW_PATH)

print("Columns found:", df.columns.tolist())

# Rename columns to standard names
df = df.rename(columns={
    "Job Title": "title",
    "Job Description": "description",
    "skills": "skills",
    "Role": "role"
})

# Keep only required columns
required_cols = ["title", "description", "skills", "role"]
df = df[required_cols].dropna()

def is_relevant(title, role):
    text = f"{str(title)} {str(role)}".lower()

    cloud_whitelist = [
        "cloud engineer", "devops engineer", "site reliability engineer", "sre",
        "platform engineer", "infrastructure engineer", "cloud architect",
        "aws engineer", "azure engineer", "gcp engineer"
    ]

    cyber_whitelist = [
        "cybersecurity", "security engineer", "security analyst",
        "soc analyst", "security operations", "incident response",
        "penetration tester", "pentester", "threat analyst",
        "network security", "information security"
    ]

    blacklist = [
        "software engineer", "software architect", "frontend", "backend",
        "full stack", "mobile", "android", "ios",
        "network administrator", "network technician"
    ]

    if any(bad in text for bad in blacklist):
        return False

    return any(k in text for k in cloud_whitelist) or any(k in text for k in cyber_whitelist)


df = df[df.apply(lambda row: is_relevant(row["title"], row["role"]), axis=1)]

# Clean text fields
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z0-9\s,]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["description"] = df["description"].apply(clean_text)
df["skills"] = df["skills"].apply(clean_text)

# Save cleaned dataset
df.to_csv(OUT_PATH, index=False)

print(f"Cleaned dataset saved to: {OUT_PATH}")
print("Sample rows:")
print(df.head())
print("Total rows after filtering:", len(df))
