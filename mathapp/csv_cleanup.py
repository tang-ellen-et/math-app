import pandas as pd
from generate_images import add_line_breaks

def preprocess_csv(input_file: str, output_file: str, max_length: int = 80):
    """Preprocess the CSV file to fix long LaTeX strings."""
    df = pd.read_csv(input_file)

    def fix_latex_string(latex_string):
        if pd.isna(latex_string):
            return latex_string
        latex_string = " ".join(latex_string.split())  # Remove extra spaces
        latex_string = add_line_breaks(latex_string, max_length=80)  # Add line breaks and wrap in \text{}
        return latex_string

    # Apply the fix to the "Problem" column
    df["Problem"] = df["Problem"].apply(fix_latex_string)

    # Save the updated CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Processed CSV saved to {output_file}")

# Run the script
preprocess_csv("/Users/jasonyuan/Documents/git/math-app/data_sources/mathv4_processed_3.csv", "/Users/jasonyuan/Documents/git/math-app/data_sources/mathv4_processed_3_fixed2.csv")