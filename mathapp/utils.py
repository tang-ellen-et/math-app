import pandas as pd

def get_sample_sizes(difficulty):
    sample_sizes = {
        1: (6, 5, 4, 0),
        2: (5, 5, 5, 0),
        3: (5, 5, 4, 1),
        4: (5, 5, 3, 2),
        5: (5, 4, 4, 2),
        6: (5, 4, 3, 3),
        7: (4, 5, 3, 3),
        8: (4, 4, 4, 3),
        9: (4, 4, 3, 4),
        10: (3, 4, 4, 4)
    }
    return sample_sizes.get(difficulty, (5, 5, 4, 1))

def get_aime_problems(df_problems: pd.DataFrame, difficulty:int)->pd.DataFrame:
    # problems = pd.read_csv('data_sources/mathv4_processed.csv')
    problems = df_problems 
    
    df_3_3_5 = problems[(problems['Difficulty'] >= 3) & (problems['Difficulty'] <= 3.5)]
    df_4_4_5 = problems[(problems['Difficulty'] >= 4) & (problems['Difficulty'] <= 4.5)]
    df_5_5_5 = problems[(problems['Difficulty'] >= 5) & (problems['Difficulty'] <= 5.5)]
    df_6_7 = problems[(problems['Difficulty'] >= 6) & (problems['Difficulty'] <= 7)]
    
    sample_sizes = get_sample_sizes(difficulty)
    
    sample_3_3_5 = df_3_3_5.sample(n=sample_sizes[0])
    sample_4_4_5 = df_4_4_5.sample(n=sample_sizes[1])
    sample_5_5_5 = df_5_5_5.sample(n=sample_sizes[2])
    sample_6_7 = df_6_7.sample(n=sample_sizes[3])
    
    aime_problems = pd.concat([sample_3_3_5, sample_4_4_5, sample_5_5_5, sample_6_7])
    max_category_count = 6
    problems = problems.groupby('Type').apply(lambda x: x.sample(min(len(x), max_category_count))).reset_index(drop=True)
   
    while any(aime_problems['Type'].value_counts() > max_category_count):
        for problem_type, count in aime_problems['Type'].value_counts().items():
            if count > max_category_count:
                problem_to_replace = aime_problems[aime_problems['Type'] == problem_type].sample(n=1)
                aime_problems = aime_problems.drop(problem_to_replace.index)
                
                same_difficulty_problems = problems[(problems['Difficulty'] == problem_to_replace['Difficulty'].values[0]) & (problems['Type'] != problem_type)]
                print("Same difficulty problems:")
                print(same_difficulty_problems.head(20))
                if not same_difficulty_problems.empty:
                    replacement_problem = same_difficulty_problems.sample(n=1)
                    aime_problems = pd.concat([aime_problems, replacement_problem])
                    break
                else:
                    print(f"No replacement found for {problem_type} with difficulty {problem_to_replace['Difficulty'].values[0]}")


    # aime_problems = aime_problems.sort_values(by='Difficulty').reset_index(drop=True)
    return aime_problems