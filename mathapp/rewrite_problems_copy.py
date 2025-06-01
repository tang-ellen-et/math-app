import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")
# Load the data
df = pd.read_csv("/Users/jasonyuan/Documents/git/math-app/data_sources/problems_list_v1_with_types.csv")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Prompt map
prompt_map = prompt_map = {
    "aime_ready_integers": "Do not modify the problem statement. Keep the original problem exactly as is.",

    "large_integers": (
        "This problem's answer is a large integer (over 1000). Do not change the core computation or mathematical structure of the problem. "
        "Modify the original problem statement as little as possible—ideally only the final instruction. "
        "If the problem already defines a variable (such as x) and the final instruction asks you to compute something based on that variable "
        "(e.g., the sum of its prime factors), then let n be that final quantity (not x itself). "
        "Generally, replace the final instruction with: 'Let n be [the final quantity asked for]. Find the remainder when n is divided by 1000.' "
        "Do not say 'which we'll denote as n' or 'denote this quantity as n' — directly use 'Let n be...'. "
        "Make sure the rephrasing is natural and flows smoothly within the original problem context. "
        "Do not invent new scenarios or reword anything other than the final sentence."
    ),

    "negative_integers": (
        "This problem's answer is a negative integer. Modify the original problem statement so that you set a variable, such as n, equal to the answer "
        "and then ask the user to find the absolute value of n. "
        "If the absolute value is greater than 1000, instead ask: 'Find the remainder when the variable is divided by 1000.' "
        "Do not alter the core context or intent of the problem."
    ),

    "fractions": (
        "This problem's answer is a reduced fraction. Do not change the setting or add fictional contexts. Modify the original problem statement as little as possible—ideally only the final question. "
        "Rephrase the final sentence so that it naturally introduces a variable (such as 'Let s be the [quantity]') and states that it can be expressed as m/n, "
        "where m and n are relatively prime positive integers. Then ask for m + n. "
        "If m + n is greater than 1000, ask for the remainder when m + n is divided by 1000. "
        "Do not append a new sentence starting with 'The answer can be expressed as...'; instead, integrate this information smoothly into the existing question."
    ),

    "roots": (
        "This problem's answer involves square roots. Modify the original problem statement as little as possible so that the square root form arises naturally from the context. "
        "Do not change the core mathematical setup or invent new values, diagrams, or scenarios. "

        "In the rewrite of the problem, define a variable (such as x) to represent the answer, and describe its form depending on the type:\n"
        
        "- If the answer is √n and n is square-free, write: 'Let x be [what the problem is asking for]. If x = √n, where n is not divisible by the square of a prime, find n.'\n"
        
        "- If the answer is m√n/k, write: 'Let x be [what the problem is asking for]. If x = m√n/k, where m and k are relatively prime positive integers and n is not divisible by the square of a prime, find m + n + k.'\n"
        
        "- If the answer is of the form m√n ± c, write: 'Let x be [what the problem is asking for]. If x = m√n ± c, where m, n, and c are positive integers and n is not divisible by the square of a prime, find m + n + c.'\n"
        
        "- For other forms involving square roots, define x appropriately, clearly state its algebraic form, and ask for the sum of all constants and radicals involved."

        "Always begin the final instruction with 'Let x be [what the problem is asking for].' Then clearly define x algebraically. Do not say 'the answer is' or 'which we'll denote as'—just define x directly. "
        "Ensure the rephrased problem flows naturally from the original without altering its structure or introducing extraneous information."
    ),


    "pi": (
        "This problem's answer involves a simple expression with π (such as π, 2π + 1, or π√3). Modify the original problem statement as little as possible—preferably just the final question—so that the form arises naturally. "
        "In general, set a variable such as n equal to the answer and then ask for the sum of all components. "
        "If the answer can be written as aπ + b, where a and b are real numbers, ask: 'Find a + b.' "
        "If the answer is aπ√n, treat it as aπ with b = 0. Only use this format if the components are clearly defined and the sum is meaningful. "
        "Define the components of the answer and ask for the sum of all components. "
        "If the answer is greater than 1000, ask for the remainder when the sum is divided by 1000. "
        "Do not change the mathematical structure or create a fictional context."
    ),

    "powers": (
        "This problem's answer is an integer power or product involving a power (e.g., a·b^c for integers a, b, and c). Modify the original problem statement as little as possible—preferably just the final instruction. "
        "Then end the problem with: 'If the answer is of the form a·b^c, find a + b + c.' "
        "Make sure the exponential form arises naturally from the context. Do not alter the core mathematical intent of the problem."
    ),

    "misc": ""

}

# Loop through first 20
for i, row in df.iloc[70:80].iterrows():
    prob = row["Problem"]
    ans = row["Answer"]
    ans_type = row["AnswerType"]

    if ans_type in ["aime_ready_integers", "misc"]:
        print("No prompt applied.")
        continue

    prompt = (
        f"Original problem:\n{prob}\n\n"
        f"The answer is: {ans}\n\n"
        f"{prompt_map.get(ans_type, '')}"
    )
    print(f"\nPrompt to GPT:\n{prompt}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    print(f"\nModified Problem:\n{response.choices[0].message.content}")
