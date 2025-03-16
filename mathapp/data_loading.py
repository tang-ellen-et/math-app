import csv
import pandas as pd
from datetime import date, datetime

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
            # Create an instance of Model using dictionary unpacking
            data_tuple = row.to_dict()
            item = model(**data_tuple)
            session.add(item)
        session.commit()


def generate_user_problem_sets(user: str, problems_df: pd.DataFrame) -> pd.DataFrame:
    
    test_date = datetime.today()
    problem_set = str(round(datetime.now().timestamp() * 1000))
    
    problems_df['pid'] = problems_df.index + 1 

    # Randomly select 20 problems from problems_df with different difficulty levels
    # user_problems_df = problems_df
    user_problems_df = problems_df.sample(n=20, random_state=1)
    # print(user_problems_df.head(2))
    
    user_problems_df ['User'] = user
    user_problems_df['ProblemSet'] = problem_set 
    user_problems_df["ProblemId"] = problems_df['pid']
    user_problems_df["TestDate"] = test_date.strftime("%Y-%m-%d")
    user_problems_df["Response"] = '' 
    user_problems_df["Result"] = '' 


    return user_problems_df

def load_all_problems(data_file_path :str, math_model: rx.Model)->pd.DataFrame:
    df_problems = pd.read_csv(data_file_path, header=0)
    print(f'====== df columns: {df_problems.columns} ===')
    
    add_pandas_data_to_db(df_problems, math_model)
    return df_problems 

def load_user_problems(user: str,  df_problems: pd.DataFrame, user_problems_model: rx.Model):
    # df = pd.read_csv(data_file_path, header=0)
    # print(f'====== df columns: {df.columns} ===')
    
    user_problems_df = generate_user_problem_sets (user, df_problems)
    add_pandas_data_to_db(user_problems_df, user_problems_model)
    