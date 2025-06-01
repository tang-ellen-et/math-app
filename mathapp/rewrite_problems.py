import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
import glob

load_dotenv()  # Load .env file

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Prompt map
prompt_map = {
    "aime_ready_integers": "Do not modify the problem statement. Keep the original problem exactly as is.",
    "large_integers": (
        "Your task is to rewrite a problem so that it matches the AIME format. "
        "This problem's answer is a large integer (over 1000). Do not change the core computation or mathematical structure of the problem. "
        "Modify the original problem statement as little as possible—ideally only the final instruction. "
        "If the original problem ends by asking for a specific named value (such as T(15), a count of things, a variable already defined in the problem, or a function evaluation), "
        "do not introduce a new variable. Simply rephrase the problem naturally to end with something like: 'Find the remainder when that quantity is divided by 1000.', but of course replace 'that quantity' with the actual quantity being asked for. "
        "Only introduce a variable such as $n$ if the quantity being asked for is not already explicitly named or defined as a function or a variable in the problem. "
        "Generally, if you introduce a variable, modify the original problem statement so that you set a variable, such as n, equal to the answer. Try to integrate this into the problem statement and not just append it at the end. It can be at the start of the problem statement. Always end the problem by asking to find the remainder when $n$ is divided by $1000$.'"
        "Also, make sure the variable you define does not conflict with any existing variables in the problem. "
        "Only use the phrases 'Let n be...' or 'Denote by n', replacing n with whatever variable you are using to define a variable. Make sure the revised problem flows naturally and does not add unnecessary words such as he, she, or we. "
    ),
    "negative_integers": (
        "Your goal is to rewrite a problem so that it matches the AIME format. "
        "This problem's answer is a negative integer. Modify the original problem statement so that you set a variable, such as n, equal to the answer "
        "and then ask the user to find the absolute value of n. "
        "If the absolute value is greater than 1000, instead ask: 'Find the remainder when the variable is divided by $1000$.' "
        "Do not say 'which we'll denote as $n$' or 'denote this quantity as $n$' — directly use 'Let $n$ be...' or 'denote by $n$...'. "
        "Do not alter the core context or intent of the problem."
    ),
    "fractions": (
        "Your task is to rewrite a problem so that it matches the AIME format. "
        "This problem's answer is a reduced fraction. Do not change the setting or add fictional contexts. "
        "Modify the original problem statement minimally."
        "Rewrite the problem so that it naturally introduces a variable (such as 'Let $s$ be the [quantity]') and states that $s$ can be expressed as $m/n$, "
        "where $m$ and $n$ are relatively prime positive integers. In the final sentence, ask for $m + n$. "
        "If the final instruction is a question, rephrase it into a statement before introducing a variable. "
        "Also, make sure the variable you define does not conflict with any existing variables in the problem. "
        "If $m + n$ exceeds $1000$, ask instead for the remainder when $m + n$ is divided by $1000$.\n\n"
        "Do not start a sentence with 'This [quantity] $s$ can be expressed as...' or 'The answer can be expressed as...'. "
        "Integrate the phrasing smoothly by using: 'Let $s$ be the [quantity]. If $s$ can be expressed as $m/n$, where $m$ and $n$ are...' — use that exact structure.\n\n"
        "Avoid phrases like 'this probability $p$' or 'this value $s$'; always refer to the variable by its name alone."
    ),
    "roots": (
        "Your task is to rewrite a math problem in the style of an AIME problem. "
        "You must not solve, explain, or comment on the problem. Your goal is to minimally edit the original problem so that its answer naturally involves a square root, and it matches AIME formatting.\n\n"
        "Keep the original problem's mathematical context and structure intact. Do not add new elements such as extra diagrams, labels, commentary, or clarification. "
        "Modify only what is necessary—ideally just the final sentence—to introduce a variable (e.g., x) and ask for a quantity derived from its square root form.\n\n"
        "Use one of the following formats, depending on the form of the answer:\n"
        "- If the answer is of the form √n and n is square-free, integrate some variation of: 'Let $x$ be [what the problem is asking for]' into the problem. End with 'If $x$ can be written as √n, where $n$ is not divisible by the square of a prime, find $n$.'\n"
        "- If the answer is of the form m√n/k, integrate some variation of: 'Let $x$ be [what the problem is asking for]' into the problem statement. End with 'If $x$ can be written as m√n/k, where $m$ and $k$ are relatively prime positive integers and $n$ is not divisible by the square of a prime, find $m + n + k$.'\n"
        "- If the answer is of the form m√n ± c, integrate some variation of: 'Let $x$ be [what the problem is asking for].' End with 'If $x$ can be written as m√n ± c, where $m$, $n$, and $c$ are positive integers and $n$ is not divisible by the square of a prime, find $m + n + c$.'\n"
        "- For any other square root expression, define x accordingly and ask for the sum of all constants and radicals involved.\n\n Of course, if $x$ is already defined in the problem statement, use another variable such as $n$ or $s$ instead.\n\n"
        "Always begin the final instruction with 'Let $x$ be [what the problem is asking for].' Place this sentence at the end of the problem. "
        "Do not use informal language such as 'we are interested in...' and do not say 'the answer is' or 'denote as'. Keep the voice formal and concise."
    ),
    "pi": (
        "Your task is to rewrite a problem to match the AIME format."
        "This problem's answer involves a simple expression with π (such as π, 2π + 1, or π√3). "
        "Modify the original problem statement minimally."
        "Generally, introduce a variable (such as n) to represent the quantity the problem is asking for and specify how it can be written. "
        "If the answer can be written as aπ + b, integrate some variation of 'Let $n$ be [the quantity]' into the problem statement. End with 'If $n$ can be written as aπ + b, where $a$ and $b$ are positive integers, find $a + b$.' "
        "If the answer can be written as aπ/b + c, integrate some variation of 'Let $n$ be [the quantity]' into the problem statement. End with 'If $n$ can be written as aπ/b + c, where $a$, $b$, and $c$ are positive integers, find $a + b + c$.' "
        "Try to make the phrasing as natural as possible, and do not add fictional contexts or change the mathematical structure of the problem. "
        "If the variable $n$ is used, use another variable not defined in the problem, such as $s$ or $t$, to avoid conflicts. "
        "If the sum $a + b$ exceeds $1000$, ask for the remainder when $a + b$ is divided by $1000$. "
    ),
    "powers": (
        "Your task is to rewrite a problem to match the AIME format. "
        "This problem's answer is an integer power or product involving a power (e.g., a·b^c for integers a, b, and c). Modify the original problem statement minimally."
        "" "Introduce a variable (such as n) to represent the quantity the problem is asking for, then specify how it can be written. "
        "Generally, if the answer can be expressed as a·b^c, integrate some variation of 'Let $n$ be [the quantity].' into the problem. End with 'If $n$ can be written as a·b^c, where $a$, $b$, and $c$ are positive integers, find $a + b + c$.' "
        "If the answer is of the form a^b, just end with 'If the answer can be written as a^b, where $a$ and $b$ are positive integers, find $a$ + $b$.' "
        "Do not alter the core mathematical intent of the problem."
    ),
    "misc": ""
}

def process_file(input_path, output_dir, top_n=50):
    print(f"========== Processing {input_path}... ==========")
    df = pd.read_csv(input_path)
    types_to_exclude = ["aime_ready_integers", "misc"]
    modified_problems = []
    processed_count = 0
    for i, row in df.iterrows():
        ans_type = row["AnswerType"]
        if ans_type in types_to_exclude:
            modified_problems.append("N/A")
        elif top_n == -1 or processed_count < top_n:
            prob = row["Problem"]
            ans = row["Answer"]
            prompt = (
                f"Original problem:\n{prob}\n\n"
                f"The answer is: {ans}\n\n"
                f"{prompt_map.get(ans_type, '')}"
            )
            print(f"------------------------------------------[{i}]------------------------------------------")
            print(f"\nPrompt to GPT:\n{prompt}")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            print(f"\nOriginal Problem:\n{prob}")
            print(f"\nModified Problem:\n{response.choices[0].message.content}")
            modified_problems.append(response.choices[0].message.content)
            processed_count += 1
        else:
            modified_problems.append("To be Processed")
    df["modified_problem"] = modified_problems
    df["review_status"] = ""
    output_path = os.path.join(output_dir, os.path.basename(input_path))
    df.to_csv(output_path, index=False)
    print(f"Saved modified problems to {output_path}")

if __name__ == "__main__":
    input_dir = "data_sources/inputs"
    output_dir = "data_sources/problem_modified"
    os.makedirs(output_dir, exist_ok=True)
    top_n = -1  # Or -1 for all
    for input_path in glob.glob(os.path.join(input_dir, "*.csv")):
        print(f"Processing {input_path}")
        process_file(input_path, output_dir, top_n=top_n)
    
