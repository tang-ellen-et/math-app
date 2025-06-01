import pandas as pd
import openai  # Requires openai Python SDK
from test_AIME_formatter import rewrite_problem
import csv
import os

if __name__ == "__main__":
    # Set your API key here or export as environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")
    #change this later
    csv_filename = "data_sources/problems_list_v1.csv"

    # Adjust these column names/indexes depending on your CSV structure
    # If header row exists, use header names like "problem" and "answer"
    problem_column = "Problem"
    answer_column = "Answer"

    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Using DictReader assumes header row
        for i, row in enumerate(reader):
            if i >= 10:
                break  # stop after first 10 rows
            problem = row[problem_column]
            answer = row[answer_column]

            rewritten = rewrite_problem(problem, answer)
            print(f"Problem {i+1} rewritten:\n{rewritten}\n{'-'*40}\n")