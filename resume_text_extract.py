from pdfminer.high_level import extract_text
import os
import pandas as pd

PDF_DIR = "data/resumes_pdf"
OUT_PATH = "data/processed/resumes_text.csv"

rows = []

for fname in os.listdir(PDF_DIR):
    if fname.lower().endswith(".pdf"):
        path = os.path.join(PDF_DIR, fname)
        try:
            text = extract_text(path)
            rows.append({
                "filename": fname,
                "text": text.replace("\n", " ").strip()
            })
            print(f"Extracted: {fname}")
        except Exception as e:
            print(f"Failed to extract {fname}: {e}")

df = pd.DataFrame(rows)
df.to_csv(OUT_PATH, index=False)

print(f"Saved extracted resume text to {OUT_PATH}")
print(df.head())
