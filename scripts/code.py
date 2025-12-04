# reading the file
path = '../DATA/practice_file.txt'
with open(path, 'r') as file:
    content = file.read()

# counting the number of lines
lines = content.split('\n')
num_lines = len(lines)
print(f'Number of lines: {num_lines}')

# printing five largest words
words = content.split()
words.sort(key=len, reverse=True)
largest_five_words = words[:5]
print('five largest words in the file are:', largest_five_words)

# counting headings (ending with :)
count = 0
for title in words:
    if title.endswith(":"):
        count += 1
print("\nNumber of headings in the file:", count)

# finding lines containing Figure or Table
lines_mentioning = []
for line in lines:
    if "Figure" in line or "Table" in line:
        lines_mentioning.append(line)

print("\nLines mentioning figures or tables:")
for l in lines_mentioning:
    print(l)

# using regex to extract figure/table references
import re
references = re.findall(r'(Figure|Table)\s*\d+(\.\d+)*', content)

# Count figure/table references
figure = sum(1 for r in references if r[0] == "Figure")
table = sum(1 for r in references if r[0] == "Table")

print(f'\nNumber of Figure references: {figure}')
print(f'Number of Table references: {table}')

# create metadata.json
import json, os, shutil, pandas as pd

metadata = {
    "number_of_lines": num_lines,
    "five_largest_words": largest_five_words,
    "number_of_headings": count,
    "lines_mentioning_figures_or_tables": [l for l in lines_mentioning],
    "number_of_figure_references": figure,
    "number_of_table_references": table
}

os.makedirs('../outputs', exist_ok=True)

# write json file
with open('../outputs/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)

# read it back safely
with open('../outputs/metadata.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame([data])
print(df)

# save CSV
df.to_csv('../outputs/metadata.csv', index=False)
print("metadata.csv file created successfully")
