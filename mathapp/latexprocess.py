import pandas as pd


data_file_path = '../data_sources/mathv2.csv'

df = pd.read_csv(data_file_path, header=0)
print (df.head(10))


# df['Problem latex_2'] = df['Problem latex'].replace('\[', '$$').replace('\(', '$ ').replace('\%', '%')
print('==== after === ')

df['Problem latex_2'] = df['Problem latex'].str.replace('\\[', '$$').replace('\\( ', '$ ' ) \
    .replace('\\%', '%').replace('\\]', '$$'). replace(' \\)', ' $')
print(df.head(5))


output_file_path = '../data_sources/mathv2_processed.csv'
df.to_csv(output_file_path, index=False)

