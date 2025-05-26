import pandas as pd
import os
import urllib.parse
import requests
import re

def add_line_breaks(latex: str, max_length: int) -> str:
    """Add line breaks to a LaTeX string while preserving math mode expressions."""
    # Split the LaTeX string into text and math mode parts
    parts = re.split(r"(\$.*?\$)", latex)  # Split by inline math mode ($...$)
    processed_parts = []

    for part in parts:
        if part.startswith("$") and part.endswith("$"):
            # Math mode part: leave it untouched
            processed_parts.append(part)
        else:
            # Plain text part: wrap in \text{} and add line breaks
            words = part.split(" ")  # Split by spaces
            lines = []
            current_line = []
            current_length = 0

            for word in words:
                if current_length + len(word) + 1 > max_length:  # +1 for the space
                    lines.append(" ".join(current_line))
                    current_line = []
                    current_length = 0
                current_line.append(word)
                current_length += len(word) + 1  # +1 for the space

            if current_line:
                lines.append(" ".join(current_line))

            # Wrap each line in \text{} and join with \\
            processed_parts.append(" \\\\ ".join([f"\\text{{{line}}}" for line in lines]))

    # Join all parts back together
    return " ".join(processed_parts)

def latex_image_save(latex_string: str, filename: str) -> str:
    """Generate and save a LaTeX-rendered image from codecogs URL to a local file.

    Args:
        latex_string: The LaTeX math string to render.
        filename: The filename (with path) to save the PNG image (e.g., 'images/problem1.png').

    Returns:
        The path to the saved image file.
    """
    # URL encode the LaTeX string for the URL
    encoded = urllib.parse.quote(latex_string)

    # Construct the URL for the PNG image
    url = f"https://latex.codecogs.com/png.latex?{encoded}"

    # Make sure the output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Download the image content
    response = requests.get(url)
    response.raise_for_status()  # Raise error if download failed

    # Save the image to file
    with open(filename, "wb") as f:
        f.write(response.content)

    return filename

if __name__ == "__main__":
    # Example code to generate images (only runs when this file is executed directly)
    df = pd.read_csv("data_sources/mathv4_processed_3_fixed2.csv")
    for idx, row in df.iterrows():
        latex_code = row.get("Problem", "")
        problem_id = row.get("idx", idx)  # Fallback to row index if no ID

        if pd.isna(latex_code) or latex_code.strip() == "":
            continue

        # Generate and save the image
        filename = f"images/problem_{problem_id}.png"
        latex_image_save(latex_code, filename)
        print(f"✅ Saved image for problem {problem_id} at {filename}")