import pandas as pd

# Load original rewritten problems CSV
original_df = pd.read_csv("data_sources/problems_list_modified (1).csv")

# Load updated answers CSV (with just the updated_answer column)
updated_answers_df = pd.read_csv("data_sources/updated_answers_only.csv")  # assuming it has updated_answer column

# Add/replace the 'Answer' column in original_df with updated_answer from updated_answers_df
# (If you want to append as a new column with a different name, change 'Answer' to that name)
original_df['AIME_Answer'] = updated_answers_df['updated_answer']

# Drop the 'review_status' column if it exists
if 'review_status' in original_df.columns:
    original_df = original_df.drop(columns=['review_status'])

# Save to a new CSV (or overwrite)
original_df.to_csv("data_sources/final_final_problems_list.csv", index=True)
