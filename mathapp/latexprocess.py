import pandas as pd

data_file_path = 'data_sources/mathv4.csv'

df = pd.read_csv(data_file_path, header=0)

print("==== Before ====")
print(df.head(10))

# Use str.replace with regex=True for more robust replacements
df['Problem'] = df['Problem latex'].str.replace(r'\\[', '$$', regex=True) \
    .str.replace(r'\\]', '$$', regex=True) \
    .str.replace(r'\\(', '$', regex=True) \
    .str.replace(r'\\)', '$', regex=True) \
    .str.replace(r'\\%', '%', regex=True)

print("==== After ====")
print(df.head(5))

df.drop(columns=['Problem latex'], inplace=True)

output_file_path = 'data_sources/mathv4_processed.csv'
df.to_csv(output_file_path, index=False)
