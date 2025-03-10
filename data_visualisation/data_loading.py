import csv
import pandas as pd
import json

import reflex as rx


def add_csv_data_to_db(data_file_path: str, model: rx.Model):
    with open(data_file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(
            file
        )  # This automatically uses the first row as header names

        with rx.session() as session:
            for row in reader:
                # Create an instance of Model using dictionary unpacking
                item = model(**row)
                session.add(item)
            session.commit()


def add_pandas_data_to_db(df: pd.DataFrame, model: rx.Model):
    with rx.session() as session:
        for index, row in df.iterrows():
            data_tuple = row.to_dict()
            # Create an instance of Model using dictionary unpacking
            item = model(**data_tuple)
            session.add(item)
        session.commit()


def loading_data(data_file_path: str, model: rx.Model):
    try:
        if data_file_path.endswith(".csv"):
            # Open your CSV file
            add_csv_data_to_db(data_file_path, model)

        if data_file_path.endswith(".xlsx"):
            # Open your excel file
            df = pd.read_excel(data_file_path)
            add_pandas_data_to_db(df, model)

        if data_file_path.endswith(".json"):
            # Open your json file
            with open(data_file_path, "r") as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                add_pandas_data_to_db(df, model)

    except Exception as e:
        print(
            f"An error occurred! You might have the wrong datafile for your Model. Here is the error: {e}"
        )


from datetime import date

def _generate_user_problem_sets(user: str, problems_df: pd.DataFrame) -> pd.DataFrame:
    test_date = datetime.today()
    problem_set = str(round(datetime.now().timestamp() * 1000))

    # Randomly select 20 problems from problems_df with different difficulty levels
    user_problems_df = problems_df.sample(n=20, replace=False)
    user_problems_df.head(20)
    
    user_problems_df ['User'] = user
    user_problems_df['ProblemSet'] = problem_set 
    user_problems_df["ProblemId"] = user_problems_df["id"]
    user_problems_df["TestDate"] = test_date 
    user_problems_df["Response"] = None 
    user_problems_df["Result"] = None 
    
    user_problems_df = user_problems_df.drop("Id")

    return user_problems_df


def load_user_problems(user: str,  data_file_path: str, model: rx.Model):
    with open(data_file_path, mode="r", newline="", encoding="utf-8") as file:
        # reader = csv.DictReader(
        #     file
        # )  # This automatically uses the first row as header names

        problems_df = pd.read_csv(data_file_path, header=True)
        user_problems_df = _generate_user_problem_sets (user, problems_df)

        add_pandas_data_to_db(user_problems_df, model)
    