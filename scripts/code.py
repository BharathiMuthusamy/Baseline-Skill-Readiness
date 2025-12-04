# reading the file

path = '../DATA/practice_file.txt'
with open(path, 'r') as file:
    content = file.read()
    #print(content)

# counting the number of lines
lines = content.split('\n')
num_lines = len(lines)
print(f'Number of lines: {num_lines}')

#printing five largest words in the text file
words = content.split()
words.sort(key=len, reverse = True)
largest_five_words = words[:5]
print('five largest words in the file are:', largest_five_words)

#counting the headings in the text file
count = 0
for title in words:
    if title.endswith(":"):
        count += 1
print("\nNumber of headings in the file:")
print("\n",count)

#finding lines that mentioning fig or tables
lines = content.split("\n")
print("\nLines mentioning figures or tables:")
for line in lines:
    if "Figure" in line or "Table" in line:
        print("\n",line)
        
#using regrex to extract the refernces section from the text file
import re
references = re.findall(r'(figure|Table)\s*\d+',content)
figure = 0
table = 0
for reference in references:
    if "Figure" in reference:
        figure += 1
    elif "Table" in reference:
        table += 1  
print(f'Number of Figure references: {figure}')
print(f'Number of Table references: {table}')

# creating metadata.json 
import re
import json
import os
import shutil
import pandas as pd
metadata = {
    "number_of_lines": num_lines,
    "five_largest_words": largest_five_words,
    "number_of_headings": count,
    "lines_mentioning_figures_or_tables": references,
    "number_of_figure_references": figure,
    "number_of_table_references": table
}
os.makedirs('../outputs',exist_ok=True)
# creating a pandas dataframe from metadata.json (FIXED)
with open('../outputs/metadata.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame([data])  # Wrap dictionary inside a list
print(df)

# save CSV
df.to_csv('../outputs/metadata.csv', index=False)
print("metadata.csv file created successfully")

