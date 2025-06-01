import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load .env file

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")
# Load the data
df = pd.read_csv("data_sources/problems_list_v1_with_types.csv")

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
        "Use the appropriate final question based on the form of the answer:\n"
        "- If the answer is √n and n is square-free, ask: 'Find n.'\n"
        "- If the answer is m√n/k, ask: 'Find m + n + k.'\n"
        "- If the answer is m√n ± c, ask: 'Find m + n + c.'\n"
        "- In general, if the answer is a sum/difference/fraction involving square roots, extract all constants and radicals and ask for the sum of all components involved. "
        "Do not change the core setup or mathematical structure of the problem."
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

# Set how many problems to process
top_n = 5  # Change as needed

# Exclude certain answer types
types_to_exclude = ["aime_ready_integers", "misc"]

modified_problems = []
processed_count = 0

for i, row in df.iterrows():
    ans_type = row["AnswerType"]
    if ans_type in types_to_exclude:
        modified_problems.append("N/A")
    elif processed_count < top_n:
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
        # If we've already processed top_n, fill the rest with To be Processed
        modified_problems.append("To be Processed")

df["modified_problem"] = modified_problems

# Save to new CSV
output_path = "data_sources/problems_list_v1_with_modified.csv"
df.to_csv(output_path, index=False)
print(f"Saved modified problems to {output_path}")
 
    
