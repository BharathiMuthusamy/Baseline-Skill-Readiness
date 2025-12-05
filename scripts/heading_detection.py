# Phase 2 — Text Extraction and Structural Analysis
import fitz
import re
import json
import os
import csv


# Extract PDF text
def extract_pdf_text(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text

# Clean text
def clean_text(text):
    return "\n".join(line.strip() for line in text.split("\n") if line.strip() != "")

# Check if a line is a heading using regex and some conditions
def is_heading(line):
    line = line.strip()
    
    if len(line) < 4:
        return False
    if re.match(r"^\d+\s*/\s*\d+$", line):
        return False
    if re.match(r"^[\d\W_]+$", line):
        return False
    if any(c in line for c in "[]()/"):
        return False
    if line.isupper():
        return True
    m = re.match(r"^(\d+)\.\s+(.*)", line)
    if m:
        num, title = m.groups()
        num = int(num)
        if num < 10 and sum(title.count(c) for c in ",.;") <= 2:
            return True
        else:
            return False
    if line.istitle() and 2 <= len(line.split()) <= 7:
        return True
    return False

# Extract headings
def extract_headings(cleaned_text):
    headings = []
    lines = cleaned_text.split("\n")
    
    for line in lines:
        if is_heading(line):
            headings.append(line)
            if line.lower() in ["references", "acknowledgements"]:  # for this pdf
                break
    return headings

# Detect tables
def is_table(line):
    return line.startswith("Table") or re.match(r"^Table\s*\d+", line)

# Detect figures
def is_figure(line):
    return line.startswith(("Fig", "Figure")) or re.match(r"^(Fig|Figure)\s*\d+", line)

# Count structural elements
def count_structural_elements(cleaned_text):
    counts = {
        "headings": 0,
        "tables": 0,
        "figures": 0,
        "paragraphs": 0,
        "lines": 0
    }
    headings_list = []
    tables = []
    figures = []
    
    # Approx paragraphs by splitting on double newlines
    paragraphs = cleaned_text.split("\n\n")
    counts["paragraphs"] = len(paragraphs)

    for line in cleaned_text.split("\n"):
        counts["lines"] += 1
        if is_heading(line):
            counts["headings"] += 1
            headings_list.append(line)
        elif is_table(line):
            counts["tables"] += 1
            tables.append(line)
        elif is_figure(line):
            counts["figures"] += 1
            figures.append(line)
            
    return counts, headings_list, tables, figures

# --- Pipeline ---
pdf_path = "../DATA/yeshan.pdf"
raw_text = extract_pdf_text(pdf_path)
cleaned_text = clean_text(raw_text)

# Output folder
output_folder = "../outputs/text"
os.makedirs(output_folder, exist_ok=True)

# --- Task 1: Save full text ---
full_text_file = os.path.join(output_folder, "full_text.txt")
with open(full_text_file, "w", encoding="utf-8") as f:
    f.write(cleaned_text)
print(f"Full text saved to {full_text_file}")

# --- Task 2: Extract and save headings ---
detected_headings = extract_headings(cleaned_text)
with open(os.path.join(output_folder, "headings.json"), "w", encoding="utf-8") as f:
    json.dump(detected_headings, f, ensure_ascii=False, indent=4)
print(f"Extracted headings saved to {os.path.join(output_folder, 'headings.json')}")

# --- Task 3: Count structural elements ---
counts, headings_list, tables, figures = count_structural_elements(cleaned_text)

# Save tables and figures JSON
with open(os.path.join(output_folder, "tables.json"), "w", encoding="utf-8") as f:
    json.dump(tables, f, ensure_ascii=False, indent=4)

with open(os.path.join(output_folder, "figures.json"), "w", encoding="utf-8") as f:
    json.dump(figures, f, ensure_ascii=False, indent=4)

# Save stats JSON
with open(os.path.join(output_folder, "stats.json"), "w", encoding="utf-8") as f:
    json.dump(counts, f, ensure_ascii=False, indent=4)

# Save counts CSV
csv_file = os.path.join(output_folder, "counts.csv")
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=counts.keys())
    writer.writeheader()
    writer.writerow(counts)

# --- Print summary ---
print("\nPDF Structural Elements Summary:")
for key, value in counts.items():
    print(f"{key.capitalize()}: {value}")

print(f"\nAll outputs saved in: {output_folder}")
