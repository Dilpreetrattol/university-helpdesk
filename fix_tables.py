import pymupdf
import os

# Run this to inspect where the fee table lives in your PDF
doc = pymupdf.open("./pdfs/TUITION FEE AND OTHER DUES.pdf")
for i, page in enumerate(doc):
    text = page.get_text()
    print(f"\n--- PAGE {i+1} ---")
    print(text)