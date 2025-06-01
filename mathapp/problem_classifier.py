import pandas as pd
import re

def classify_answer(ans):
    ans = str(ans).strip()

    # Integer
    try:
        val = int(ans)
        if 0 <= val <= 999:
            return 'aime_ready_integers'
        elif val > 999:
            return 'large_integers'
        elif val < 0:
            return 'negative_integers'
    except ValueError:
        pass

    # Fractions
    if re.fullmatch(r'-?\d+\s*/\s*\d+', ans):
        return 'fractions'

    # Simple pi expressions (max 1 operator, max 2 terms, at most 1 sqrt, no parentheses)
    if 'pi' in ans.lower() or 'π' in ans:
        ops = re.findall(r'[+\-/]', ans)
        terms = re.split(r'[+\-/]', ans)
        if len(ops) <= 1 and len(terms) <= 2 and ans.lower().count('sqrt') + ans.count('√') <= 1 and '(' not in ans:
            return 'pi'

    # Simple root expressions (exactly 1 root, max 1 operator, no parentheses)
    if 'sqrt' in ans.lower() or '√' in ans:
        root_count = ans.lower().count('sqrt') + ans.count('√')
        ops = re.findall(r'[+\-/]', ans)
        if root_count == 1 and len(ops) <= 1 and '(' not in ans:
            return 'roots'

    # Powers like 2^800
    if re.fullmatch(r'\d+\s*\^\s*-?\d+', ans):
        return 'powers'

    return 'misc'

def main():
    input_path = "/Users/jasonyuan/Documents/git/math-app/data_sources/problems_list_v1.csv"
    df = pd.read_csv(input_path)

    df['AnswerType'] = df['Answer'].apply(classify_answer)

    # (Optional) Save to new file
    output_path = input_path.replace(".csv", "_with_types.csv")
    df.to_csv(output_path, index=False)

    print("Answer type classification complete.")
    print(df['AnswerType'].value_counts())

if __name__ == "__main__":
    main()
