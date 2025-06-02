import pandas as pd

# Read the original CSV
input_path = 'data_sources/problems_list_v1_with_types.csv'
df = pd.read_csv(input_path)

# Calculate the number of rows per split
n = len(df)
rows_per_part = n // 4

# Split and save
for i in range(4):
    start = i * rows_per_part
    # For the last part, include all remaining rows
    end = (i + 1) * rows_per_part if i < 3 else n
    df_part = df.iloc[start:end]
    output_path = f'data_sources/problems_list_v1_with_types_part{i+1}.csv'
    df_part.to_csv(output_path, index=False)
    print(f'Saved {output_path} with {len(df_part)} rows.') 