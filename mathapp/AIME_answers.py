import pandas as pd
from fractions import Fraction
import re

# --- COMPONENT EXTRACTOR --- #

def sum_of_numeric_components(expr: str) -> int:
    numbers = re.findall(r'\d+', expr)
    return sum(int(num) for num in numbers)

# --- HANDLER FUNCTIONS --- #

def handle_integer(ans_str):
    try:
        val = int(ans_str)
        return abs(val) % 1000
    except:
        return None

def handle_fraction(ans_str):
    try:
        frac = Fraction(ans_str)
        return (frac.numerator + frac.denominator) % 1000
    except:
        return None

def handle_decimal(ans_str):
    try:
        # Remove commas, handle decimals like 3.14
        ans_str = ans_str.replace(',', '')
        val = float(ans_str)
        # Treat it like an integer for modulus (e.g., take floor or round?)
        return int(abs(val)) % 1000
    except:
        return None

def handle_symbolic(ans_str):
    try:
        return sum_of_numeric_components(ans_str) % 1000
    except:
        return None

def fallback_handler(ans_str):
    # If everything else fails, just return None
    return None

# --- MAIN LOGIC --- #

def compute_updated_answer(ans_str):
    if pd.isnull(ans_str):
        return None
    ans_str = str(ans_str).strip()
    for handler in [handle_integer, handle_fraction, handle_decimal, handle_symbolic]:
        result = handler(ans_str)
        if result is not None:
            return result
    return fallback_handler(ans_str)

# --- APPLY TO CSV --- #

df = pd.read_csv("data_sources/problems_list_v1_with_types.csv")
df['updated_answer'] = df['Answer'].apply(compute_updated_answer)

# --- SAVE & PREVIEW --- #

df['updated_answer'].to_csv("updated_answers_only.csv", index=False, header=True)

