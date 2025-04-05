import pandas as pd

data_file_path = 'data_sources/mathv5_raw.csv'

df = pd.read_csv(data_file_path, header=0)

df['Problem'] = df['Problem latex'].str.replace(r'\\\[' , '$$', regex=True) \
    .str.replace(r'\\\]', '$$', regex=True) \
    .str.replace(r'\\\(', '$', regex=True) \
    .str.replace(r'\\\)', '$', regex=True) \
    .str.replace(r'\\%', '%', regex=True) \
    .str.replace(r'&=', '=', regex=True) 

df.drop(columns=['Problem latex'], inplace=True)

output_file_path = 'data_sources/mathv5_processed.csv'
df.to_csv(output_file_path, index=False)

print("Processed file saved successfully!")