import pandas as pd
import re

# Load the CSV file
processed_data = pd.read_csv("data_sources/problems_list_v1.csv")

# Function to wrap numbers and capitalized letter strings in $ if not already wrapped
def wrap_in_math_mode(text):
    if not isinstance(text, str):
        return text

    # Step 1: Protect math environments and curly-brace blocks
    # Match $...$, \(...\), \[...\], and {...}
    math_like_pattern = r"(\$.*?\$|\\\(.*?\\\)|\\\[.*?\\\]|\{[^{}]*\})"
    matches = re.findall(math_like_pattern, text)
    placeholder_template = "<<<BLOCK{}>>>"
    placeholders = {}

    # Replace each matched block with a unique placeholder
    for i, block in enumerate(matches):
        placeholder = placeholder_template.format(i)
        placeholders[placeholder] = block
        text = text.replace(block, placeholder)

    # Step 2: Wrap standalone numbers not in math-like blocks
    text = re.sub(r"\b\d+(\.\d+)?\b", lambda m: f"${m.group(0)}$", text)

    # Step 3: Wrap capitalized letter strings (2+ letters, not A or I)
    text = re.sub(r"\b(?![AI]\b)[A-Z]{2,}\b", lambda m: f"${m.group(0)}$", text)

    # Step 4: Restore original blocks
    for placeholder, original in placeholders.items():
        text = text.replace(placeholder, original)

    return text

# Apply the function to the "Problem" column
if "Problem" in processed_data.columns:
    processed_data["Problem"] = processed_data["Problem"].apply(
        lambda x: wrap_in_math_mode(x) if isinstance(x, str) else x
    )

# Save the updated CSV file
processed_data.to_csv("data_sources/mathv4_processed_3_updated.csv", index=False)
print("✅ Non-wrapped numbers and capitalized letter strings wrapped in $ and saved to mathv4_processed_3_updated.csv")