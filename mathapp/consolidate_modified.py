import pandas as pd
import glob
import os
import re

def replace_fraction(text):
    if not isinstance(text, str):
        return text
    # Only replace the exact text 'm/n' with '\\frac{m}{n}'
    return text.replace('m/n', '\\frac{m}{n}')

# 1. Consolidate all files in the correct order
input_dir = 'data_sources/problem_modified'
# Explicitly specify the order
ordered_files = [
    os.path.join(input_dir, f'problems_list_v1_with_types_part1.csv'),
    os.path.join(input_dir, f'problems_list_v1_with_types_part2.csv'),
    os.path.join(input_dir, f'problems_list_v1_with_types_part3.csv'),
    os.path.join(input_dir, f'problems_list_v1_with_types_part4.csv'),
]
# Only include files that actually exist
ordered_files = [f for f in ordered_files if os.path.exists(f)]

df_list = [pd.read_csv(f) for f in ordered_files]
df = pd.concat(df_list, ignore_index=True)

# 2. Process the 'modified_problem' field
if 'modified_problem' in df.columns:
    df['modified_problem'] = df['modified_problem'].apply(replace_fraction)

# 3. Save as a single file
output_path = 'data_sources/problems_list_modified.csv'
df.to_csv(output_path, index=False)
print(f'Saved consolidated file to {output_path}') 