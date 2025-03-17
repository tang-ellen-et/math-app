import pandas as pd

def get_aime_sample_sizes(difficulty):
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

def get_amc8_sample_sizes(difficulty):
    sample_sizes = {
        #1, 1.5, 2, 2.5
        1: (12, 10, 3, 0),
        2: (11, 9, 4, 1),
        3: (10, 9, 4, 2),
        4: (10, 9, 3, 3),
        5: (9, 9, 4, 3),
        6: (9, 8, 5, 3),
        7: (8, 8, 5, 4),
        8: (7, 9, 5, 4),
        9: (7, 8, 6, 4),
        10: (7, 7, 6, 5)
    }
    return sample_sizes.get(difficulty, (9, 9, 4, 3))

def get_amc10_sample_sizes(difficulty):
    sample_sizes = {
        #1-1.5, 1.5-2.5, 3-3.5, 4-4.5
        1: (12, 8, 4, 1),
        2: (11, 9, 3, 2),
        3: (11, 8, 4, 2),
        4: (10, 7, 6, 2),
        5: (10, 8, 5, 2),
        6: (9, 8, 6, 2),
        7: (9, 6, 7, 3),
        8: (8, 7, 7, 3),
        9: (8, 6, 8, 3),
        10: (7, 6, 9, 4)
    }
    return sample_sizes.get(difficulty, (10, 8, 5, 2))

def get_amc12_sample_sizes(difficulty):
    sample_sizes = {
        #1.5-2, 2.5-3.5, 3.5-4.5, 5-6
        1: (12, 8, 4, 1),
        2: (11, 8, 4, 2),
        3: (10, 8, 5, 2),
        4: (10, 7, 5, 3),
        5: (9, 7, 6, 3),
        6: (9, 6, 7, 3),
        7: (8, 6, 7, 4),
        8: (7, 7, 7, 4),
        9: (7, 5, 9, 4),
        10: (6, 5, 9, 5)
    }
    return sample_sizes.get(difficulty, (10, 8, 5, 2))

def get_aime_problems(df_problems: pd.DataFrame, difficulty:int)->pd.DataFrame:
    # problems = pd.read_csv('data_sources/mathv4_processed.csv')
    problems = df_problems 
    
    df_3_3_5 = problems[(problems['Difficulty'] >= 3) & (problems['Difficulty'] <= 3.5)]
    df_4_4_5 = problems[(problems['Difficulty'] >= 4) & (problems['Difficulty'] <= 4.5)]
    df_5_5_5 = problems[(problems['Difficulty'] >= 5) & (problems['Difficulty'] <= 5.5)]
    df_6_7 = problems[(problems['Difficulty'] >= 6) & (problems['Difficulty'] <= 7)]
    
    sample_sizes = get_aime_sample_sizes(difficulty)
    
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

def get_amc8_problems(df_problems: pd.DataFrame, difficulty:int)->pd.DataFrame:
    # problems = pd.read_csv('data_sources/mathv4_processed.csv')
    problems = df_problems 
    
    df_1 = problems[(problems['Difficulty'] == 1)]
    df_1_5 = problems[(problems['Difficulty'] == 1.5)]
    df_2 = problems[(problems['Difficulty'] == 2)]
    df_2_5 = problems[(problems['Difficulty'] == 2.5)]
    
    sample_sizes = get_amc8_sample_sizes(difficulty)
    
    sample_1 = df_1.sample(n=sample_sizes[0])
    sample_1_5 = df_1_5.sample(n=sample_sizes[1])
    sample_2 = df_2.sample(n=sample_sizes[2])
    sample_2_5 = df_2_5.sample(n=sample_sizes[3])
    
    amc8_problems = pd.concat([sample_1, sample_1_5, sample_2, sample_2_5])
    max_category_count = 10
    problems = problems.groupby('Type').apply(lambda x: x.sample(min(len(x), max_category_count))).reset_index(drop=True)
   
    while any(amc8_problems['Type'].value_counts() > max_category_count):
        for problem_type, count in amc8_problems['Type'].value_counts().items():
            if count > max_category_count:
                problem_to_replace = amc8_problems[amc8_problems['Type'] == problem_type].sample(n=1)
                amc8_problems = amc8_problems.drop(problem_to_replace.index)
                
                same_difficulty_problems = problems[(problems['Difficulty'] == problem_to_replace['Difficulty'].values[0]) & (problems['Type'] != problem_type)]
                print("Same difficulty problems:")
                print(same_difficulty_problems.head(20))
                if not same_difficulty_problems.empty:
                    replacement_problem = same_difficulty_problems.sample(n=1)
                    amc8_problems = pd.concat([amc8_problems, replacement_problem])
                    break
                else:
                    print(f"No replacement found for {problem_type} with difficulty {problem_to_replace['Difficulty'].values[0]}")

    # amc8_problems = amc8_problems.sort_values(by='Difficulty').reset_index(drop=True)
    return amc8_problems

def get_amc10_problems(df_problems: pd.DataFrame, difficulty:int)->pd.DataFrame:
    # problems = pd.read_csv('data_sources/mathv4_processed.csv')
    problems = df_problems 
    
    df_1_1_5 = problems[(problems['Difficulty'] >= 1) & (problems['Difficulty'] <= 1.5)]
    df_2_2_5 = problems[(problems['Difficulty'] >= 2) & (problems['Difficulty'] <= 2.5)]
    df_3_3_5 = problems[(problems['Difficulty'] >= 3) & (problems['Difficulty'] <= 3.5)]
    df_4_4_5 = problems[(problems['Difficulty'] >= 4) & (problems['Difficulty'] <= 4.5)]
    
    sample_sizes = get_amc10_sample_sizes(difficulty)
    
    sample_1_1_5 = df_1_1_5.sample(n=sample_sizes[0])
    sample_2_2_5 = df_2_2_5.sample(n=sample_sizes[1])
    sample_3_3_5 = df_3_3_5.sample(n=sample_sizes[2])
    sample_4_4_5 = df_4_4_5.sample(n=sample_sizes[3])
    
    amc10_problems = pd.concat([sample_1_1_5, sample_2_2_5, sample_3_3_5, sample_4_4_5])
    max_category_count = 10
    problems = problems.groupby('Type').apply(lambda x: x.sample(min(len(x), max_category_count))).reset_index(drop=True)
   
    while any(amc10_problems['Type'].value_counts() > max_category_count):
        for problem_type, count in amc10_problems['Type'].value_counts().items():
            if count > max_category_count:
                problem_to_replace = amc10_problems[amc10_problems['Type'] == problem_type].sample(n=1)
                amc10_problems = amc10_problems.drop(problem_to_replace.index)
                
                same_difficulty_problems = problems[(problems['Difficulty'] == problem_to_replace['Difficulty'].values[0]) & (problems['Type'] != problem_type)]
                print("Same difficulty problems:")
                print(same_difficulty_problems.head(20))
                if not same_difficulty_problems.empty:
                    replacement_problem = same_difficulty_problems.sample(n=1)
                    amc10_problems = pd.concat([amc10_problems, replacement_problem])
                    break
                else:
                    print(f"No replacement found for {problem_type} with difficulty {problem_to_replace['Difficulty'].values[0]}")

    # amc10_problems = amc10_problems.sort_values(by='Difficulty').reset_index(drop=True)
    return amc10_problems

def get_amc12_problems(df_problems: pd.DataFrame, difficulty:int)->pd.DataFrame:
    # problems = pd.read_csv('data_sources/mathv4_processed.csv')
    problems = df_problems 
    
    df_1_5_2 = problems[(problems['Difficulty'] >= 1.5) & (problems['Difficulty'] <= 2)]
    df_2_5_3_5 = problems[(problems['Difficulty'] >= 2.5) & (problems['Difficulty'] <= 3.5)]
    df_3_5_4_5 = problems[(problems['Difficulty'] >= 3.5) & (problems['Difficulty'] <= 4.5)]
    df_5_6 = problems[(problems['Difficulty'] >= 5) & (problems['Difficulty'] <= 6)]
    
    sample_sizes = get_amc12_sample_sizes(difficulty)
    
    sample_1_5_2 = df_1_5_2.sample(n=sample_sizes[0])
    sample_2_5_3_5 = df_2_5_3_5.sample(n=sample_sizes[1])
    sample_3_5_4_5 = df_3_5_4_5.sample(n=sample_sizes[2])
    sample_5_6 = df_5_6.sample(n=sample_sizes[3])
    
    amc12_problems = pd.concat([sample_1_5_2, sample_2_5_3_5, sample_3_5_4_5, sample_5_6])
    max_category_count = 10
    problems = problems.groupby('Type').apply(lambda x: x.sample(min(len(x), max_category_count))).reset_index(drop=True)
   
    while any(amc12_problems['Type'].value_counts() > max_category_count):
        for problem_type, count in amc12_problems['Type'].value_counts().items():
            if count > max_category_count:
                problem_to_replace = amc12_problems[amc12_problems['Type'] == problem_type].sample(n=1)
                amc12_problems = amc12_problems.drop(problem_to_replace.index)
                
                same_difficulty_problems = problems[(problems['Difficulty'] == problem_to_replace['Difficulty'].values[0]) & (problems['Type'] != problem_type)]
                print("Same difficulty problems:")
                print(same_difficulty_problems.head(20))
                if not same_difficulty_problems.empty:
                    replacement_problem = same_difficulty_problems.sample(n=1)
                    amc12_problems = pd.concat([amc12_problems, replacement_problem])
                    break
                else:
                    print(f"No replacement found for {problem_type} with difficulty {problem_to_replace['Difficulty'].values[0]}")

    # amc12_problems = amc12_problems.sort_values(by='Difficulty').reset_index(drop=True)
    return amc12_problems