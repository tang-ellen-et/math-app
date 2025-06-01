import openai
import os

# Set your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)  # Ensure the key is set correctly

def rewrite_problem(problem, answer):
    system_prompt = """
You are an expert math competition problem editor. Your job is to rewrite math problems so they conform to the AIME format. Do not change the math content or the problem’s structure — only reword the final sentence or clause to match the desired answer form, and ensure clarity.

Do NOT invent new conditions, examples, or change the math logic.

If the original problem includes a phrase like "What is the value of x?" or "What is the answer?", change only that sentence.

Your rewrites must sound natural, consistent with AIME phrasing, and contain minimal changes to the original problem.

Apply the following rewriting rules to the problem:

1. If the answer is of the form \\( \\frac{m\\sqrt{n}}{k} \\), ask for \\( m + n + k \\).
2. If the answer is of the form \\( \\frac{m}{n} \\), ask for \\( m + n \\).
3. If the answer is of the form \\( a\\pi + b \\), ask for \\( a + b \\).
4. If the answer is of the form \\( a\\pi\\sqrt{b} + c \\), ask for \\( a + b + c \\).
5. If the answer is a combination like \\( \\frac{m}{n} + a\\sqrt{b} \\), ask for \\( m + n + a + b \\).
6. If the answer is a positive integer greater than 1000, ask for the answer modulo 1000.
7. If the answer is a negative integer, ask for its absolute value.
8. If the problem asks for the least or greatest integer with a property, rewrite it as:
   "Let \\( n \\) be the [original description]. Find \\( n \\)."
   Example: "What is the least positive integer that can be written as the sum of two cubes?"
   → "Let \\( n \\) be the least positive integer that can be written as the sum of two cubes. Find \\( n \\)."
9. If the answer is a positive integer between 000 and 999, do not change the problem statement.
Do not change the mathematical meaning of the problem. Preserve mathematical expressions and notation. Only return the rewritten problem with no explanation.
"""

    user_prompt = f"""
Original problem: {problem}

Original answer: {answer}
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ],
        temperature=0
    )
    rewritten = response.choices[0].message.content.strip()
    return rewritten

if __name__ == "__main__":
    problem_text = (
        "An ant in the xy-plane is at the origin facing in the positive x-direction. "
        "The ant then begins a progression of moves, on the n^{th} of which it first walks 1/5^{n} units in the direction it is facing "
        "and then turns 60^{\circ} degrees to the left. After a very large number of moves, the ant's movements begins to converge to a certain point. "
        "What is the y-value of this point?"
    )
    answer_text = "√3/42"

    rewritten_problem = rewrite_problem(problem_text, answer_text)
    print("Original problem:")
    print(problem_text)
    print("\nRewritten problem:")
    print(rewritten_problem)
