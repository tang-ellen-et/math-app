import csv
import pandas as pd
from datetime import datetime
from mathapp.utils import get_aime_problems
import reflex as rx

def add_csv_data_to_db(data_file_path: str, model: rx.Model) -> None:
    with open(data_file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        with rx.session() as session:
            for row in reader:
                session.add(model(**row))
            session.commit()

def add_pandas_data_to_db(df: pd.DataFrame, model: rx.Model) -> None:
    with rx.session() as session:
        # for _, row in df.iterrows():
        #     session.add(model(**row.to_dict()))
        for index, row in df.iterrows():
            # Create an instance of Model using dictionary unpacking
            data_tuple = row.to_dict()
            item = model(**data_tuple)
            session.add(item)
            
        session.commit()

def generate_user_problem_sets(user: str, problem_set: str, problems_df: pd.DataFrame) -> pd.DataFrame:
    test_date = datetime.today()
    problems_df['pid'] = problems_df.index + 1
    
    user_problems_df = get_aime_problems(problems_df, difficulty=5)
    
    # user_problems_df.assign(
    #     User=user,
    #     ProblemSet=problem_set,
    #     ProblemId=problems_df['pid'],
    #     TestDate=test_date.strftime("%Y-%m-%d"),
    #     Response='',
    #     Result=''
    # )
    user_problems_df ['User'] = user
    user_problems_df['ProblemSet'] = problem_set 
    user_problems_df["ProblemId"] = problems_df['pid']
    user_problems_df["TestDate"] = test_date.strftime("%Y-%m-%d")
    user_problems_df["Response"] = '' 
    user_problems_df["Result"] = '' 
    
    return user_problems_df

def load_all_problems(data_file_path: str, math_model: rx.Model, load_to_db: bool = False) -> pd.DataFrame:
    df_problems = pd.read_csv(data_file_path, header=0)
    print(f'====== df columns: {df_problems.columns} ===')
    
    if load_to_db:
        add_pandas_data_to_db(df_problems, math_model)
    return df_problems

def load_user_problems(user: str, df_problems: pd.DataFrame, user_problems_model: rx.Model) -> str:
    problem_set = str(round(datetime.now().timestamp() * 1000))
    user_problems_df = generate_user_problem_sets(user, problem_set, df_problems)
    add_pandas_data_to_db(user_problems_df, user_problems_model)
    return problem_set