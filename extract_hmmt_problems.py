import os
import PyPDF2
import pandas as pd
from openai import OpenAI
import json
from typing import List, Dict
import time
import re

# Initialize OpenAI client
client = OpenAI()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                # Extract text and clean it up
                page_text = page.extract_text()
                if page_text:
                    # Remove header/footer text that might interfere with problem matching
                    lines = page_text.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        # Skip lines that look like headers/footers
                        if any(skip in line.lower() for skip in ['hmmt', 'page', 'organization team']):
                            continue
                        cleaned_lines.append(line)
                    text += '\n'.join(cleaned_lines) + '\n'
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return ""

def clean_math_text(text: str) -> str:
    """Clean and format mathematical expressions in LaTeX format."""
    if not text:
        return text
        
    # First, standardize math delimiters
    text = text.replace('\\\\(', '$')
    text = text.replace('\\\\)', '$')
    text = text.replace('\\\\[', '$$')
    text = text.replace('\\\\]', '$$')
    
    # Remove extra backslashes that might interfere with LaTeX
    text = text.replace('\\\\', '\\')
    
    # Ensure proper LaTeX formatting for common mathematical expressions
    # Fractions
    text = text.replace('\\frac', '\\frac')
    text = text.replace('\\dfrac', '\\frac')
    
    # Square roots
    text = text.replace('\\sqrt', '\\sqrt')
    
    # Greek letters
    greek_letters = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 
                    'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 
                    'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega']
    for letter in greek_letters:
        text = text.replace(f'\\{letter}', f'\\{letter}')
        text = text.replace(f'\\{letter.capitalize()}', f'\\{letter.capitalize()}')
    
    # Common mathematical operators
    operators = ['sum', 'prod', 'int', 'lim', 'inf', 'sup', 'max', 'min']
    for op in operators:
        text = text.replace(f'\\{op}', f'\\{op}')
    
    # Ensure proper spacing around operators
    operators_with_spaces = ['+', '-', '=', '\\times', '\\div', '\\pm', '\\mp']
    for op in operators_with_spaces:
        text = text.replace(f'{op}', f' {op} ')
    
    # Clean up multiple spaces
    text = ' '.join(text.split())
    
    # Ensure proper LaTeX formatting for subscripts and superscripts
    text = text.replace('_', '_{')
    text = text.replace('^', '^{')
    
    # Add closing braces for subscripts and superscripts if missing
    text = text.replace('_{', '_{')
    text = text.replace('^{', '^{')
    
    # Ensure proper LaTeX formatting for fractions
    text = text.replace('\\frac{', '\\frac{')
    text = text.replace('}{', '}{')
    
    # Ensure proper LaTeX formatting for square roots
    text = text.replace('\\sqrt{', '\\sqrt{')
    
    # Clean up any remaining double spaces
    text = ' '.join(text.split())
    
    return text

def process_chunk(problems_chunk: str, solutions_chunk: str, start_index: int) -> List[Dict]:
    """Process a chunk of problems and solutions text."""
    prompt = f"""
    Extract math problems and their solutions from this section of the HMMT November 2025 Guts round.
    IMPORTANT RULES:
    1. ONLY extract the solution from the solutions text, DO NOT try to solve the problems
    2. For geometry problems with diagrams, mark them as "geometry problem, to be processed"
    3. Format ALL mathematical expressions in proper LaTeX:
       - Use $ for inline math and $$ for display math
       - Use \\frac{{numerator}}{{denominator}} for fractions
       - Use \\sqrt{{expression}} for square roots
       - Use proper LaTeX commands for Greek letters (e.g., \\alpha, \\beta)
       - Use proper LaTeX commands for operators (e.g., \\sum, \\int, \\lim)
       - Use proper LaTeX commands for subscripts and superscripts
       - Use proper LaTeX commands for special symbols (e.g., \\times, \\div, \\pm)
    4. Extract ALL problems in the chunk, not just a few
    5. Make sure problem numbers match between problems and solutions

    Return an array of problems, where each problem has:
    1. Problem number (as a string)
    2. Complete problem text with proper LaTeX formatting
    3. The final answer (from solutions only) with proper LaTeX formatting
    4. The detailed solution (from solutions only) with proper LaTeX formatting

    The response MUST be a JSON array of objects with this exact structure:
    [
        {{
            "id": "1",
            "problem": "Problem text here with $\\LaTeX$ formatting",
            "answer": "Answer here with $\\LaTeX$ formatting",
            "solution": "Solution here with $\\LaTeX$ formatting"
        }}
    ]

    Problems text:
    {problems_chunk}

    Solutions text:
    {solutions_chunk}
    """

    try:
        print(f"\nProcessing problems {start_index}...")
        
        # Save the prompt for debugging
        os.makedirs('model_responses', exist_ok=True)
        with open(f'model_responses/prompt_{start_index}.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
            
        # Try with different models and increasing timeouts
        models = ["gpt-4-turbo-preview", "gpt-4o", "gpt-3.5-turbo"]
        timeouts = [60, 90, 120]  # Increasing timeouts in seconds
        
        for model_name, timeout in zip(models, timeouts):
            try:
                print(f"Trying with model {model_name} (timeout: {timeout}s)...")
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts structured data from math competition problems and solutions. Always return data as a JSON array. DO NOT solve problems, only extract solutions from the solutions text. Format ALL mathematical expressions in proper LaTeX."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    timeout=timeout  # Dynamic timeout
                )
                
                content = response.choices[0].message.content
                print(f"\nReceived response for problem {start_index} using {model_name}")
                
                # Save the response for debugging
                with open(f'model_responses/response_{start_index}.json', 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # If we got here, we have a valid response
                break
                
            except Exception as e:
                print(f"Error with {model_name}: {str(e)}")
                # If this is the last model, save the error
                if model_name == models[-1]:
                    with open(f'model_responses/error_{start_index}.txt', 'w', encoding='utf-8') as f:
                        f.write(str(e))
                    return []
                # Otherwise, continue to the next model
                continue
            
        # Parse the JSON response
        data = json.loads(content)
        
        # Handle different response formats
        problems = []
        if isinstance(data, dict):
            if "problems" in data:
                problems = data["problems"]
            else:
                # If it's a single problem, wrap it in a list
                problems = [data]
        elif isinstance(data, list):
            problems = data
            
        # Clean and format the problems
        for problem in problems:
            problem["problem"] = clean_math_text(problem.get("problem", ""))
            problem["answer"] = clean_math_text(problem.get("answer", ""))
            problem["solution"] = clean_math_text(problem.get("solution", ""))
            
        return problems
            
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error for problem {start_index}: {str(e)}")
        # Save the error and raw content for debugging
        with open(f'model_responses/json_error_{start_index}.txt', 'w', encoding='utf-8') as f:
            f.write(f"Error: {str(e)}\nRaw content: {content}")
        return []
    except Exception as e:
        print(f"Error processing problem {start_index}: {str(e)}")
        # Save the error for debugging
        with open(f'model_responses/error_{start_index}.txt', 'w', encoding='utf-8') as f:
            f.write(str(e))
        return []

def extract_problems_and_solutions(problems_text: str, solutions_text: str) -> List[Dict]:
    """Use OpenAI to extract problems and solutions from the text."""
    if not problems_text or not solutions_text:
        print("Error: Missing problems or solutions text")
        return []
        
    print(f"\nProblems text length: {len(problems_text)} characters")
    print(f"Solutions text length: {len(solutions_text)} characters")
    
    all_problems = []
    skipped_problems = []
    
    # Split text into individual problems
    problem_chunks = {}
    solution_chunks = {}
    
    # Split problems text by problem numbers
    current_chunk = ""
    current_problem_num = None
    
    for line in problems_text.split('\n'):
        # Match pattern like "1. [5]" or "7. [6]"
        match = re.match(r'^(\d+)\.\s*\[(\d+)\]', line)
        if match:
            if current_chunk and current_problem_num:
                problem_chunks[current_problem_num] = current_chunk.strip()
            current_problem_num = int(match.group(1))
            current_chunk = line
        else:
            current_chunk += '\n' + line
    if current_chunk and current_problem_num:
        problem_chunks[current_problem_num] = current_chunk.strip()
    
    # Split solutions text similarly, but be more lenient with matching
    current_chunk = ""
    current_problem_num = None
    
    for line in solutions_text.split('\n'):
        # Match pattern like "1.[5]" or "7.[6]" or just "1." or "7."
        match = re.match(r'^(\d+)\.(?:\s*\[(\d+)\])?', line)
        if match:
            if current_chunk and current_problem_num:
                solution_chunks[current_problem_num] = current_chunk.strip()
            current_problem_num = int(match.group(1))
            current_chunk = line
        else:
            current_chunk += '\n' + line
    if current_chunk and current_problem_num:
        solution_chunks[current_problem_num] = current_chunk.strip()
    
    print(f"\nFound {len(problem_chunks)} problems and {len(solution_chunks)} solutions")
    
    # Get all unique problem numbers
    all_problem_nums = sorted(set(list(problem_chunks.keys()) + list(solution_chunks.keys())))
    
    # Process each problem individually
    for problem_num in all_problem_nums:
        print(f"\nProcessing problem {problem_num}")
        
        # Check if we have both problem and solution
        if problem_num not in problem_chunks:
            print(f"Warning: Missing problem text for problem {problem_num}")
            skipped_problems.append(problem_num)
            continue
            
        if problem_num not in solution_chunks:
            print(f"Warning: Missing solution text for problem {problem_num}")
            # Try to find the solution in the full text
            solution_match = re.search(
                rf"{problem_num}\.[\s\[]*\d*[\s\]]*.*?(?=\d+\.|$)",
                solutions_text,
                re.DOTALL
            )
            if solution_match:
                solution_chunks[problem_num] = solution_match.group(0).strip()
                print(f"Found solution for problem {problem_num} using regex search")
            else:
                skipped_problems.append(problem_num)
                continue
            
        problems = process_chunk(problem_chunks[problem_num], solution_chunks[problem_num], problem_num)
        if problems:
            all_problems.extend(problems)
            print(f"Successfully processed problem {problem_num}")
        else:
            print(f"Failed to process problem {problem_num}")
            skipped_problems.append(problem_num)
            
    # Print summary
    print("\nProcessing complete!")
    print(f"Successfully processed {len(all_problems)} problems")
    if skipped_problems:
        print(f"Skipped problems: {skipped_problems}")
    
    return all_problems

def main():
    # Paths to PDF files
    problems_pdf = "datasets/pdf/hmmt_nov_2025_guts/problems.pdf"
    solutions_pdf = "datasets/pdf/hmmt_nov_2025_guts/solutions.pdf"

    # Extract text from PDFs
    print("\nExtracting text from PDFs...")
    problems_text = extract_text_from_pdf(problems_pdf)
    solutions_text = extract_text_from_pdf(solutions_pdf)

    if not problems_text or not solutions_text:
        print("Error: Failed to extract text from PDFs")
        return

    print("\nProblems Text Preview (first 500 chars):")
    print(problems_text[:500])
    print("\nSolutions Text Preview (first 500 chars):")
    print(solutions_text[:500])

    # Extract problems and solutions
    print("\nExtracting problems and solutions...")
    problems_data = extract_problems_and_solutions(problems_text, solutions_text)

    # Create DataFrame and save to CSV
    if problems_data:
        df = pd.DataFrame(problems_data)
        # Ensure columns are in the correct order
        df = df[["id", "problem", "answer", "solution"]]
        
        # Clean up the data
        df = df.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with single space
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strip whitespace
        
        # Sort by problem number
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        df = df.sort_values('id')
        df['id'] = df['id'].astype(str)
        
        output_path = "datasets/csv/hmmt_nov_2025_guts.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save with proper encoding and quoting
        df.to_csv(output_path, index=False, quoting=1, encoding='utf-8')
        print(f"\nSaved {len(problems_data)} problems to {output_path}")
        
        # Print summary
        print("\nSummary of extracted problems:")
        print(f"Total problems extracted: {len(problems_data)}")
        print("\nFirst few rows of the CSV file:")
        pd.set_option('display.max_colwidth', None)
        print(df.head().to_string())
        
        # Check for missing problems
        expected_problems = set(str(i) for i in range(1, 37))
        extracted_problems = set(df['id'].unique())
        missing_problems = expected_problems - extracted_problems
        if missing_problems:
            print("\nWarning: Missing problems:", sorted(missing_problems))
            
        # Generate a report of model responses
        print("\nModel Response Summary:")
        model_responses_dir = "model_responses"
        if os.path.exists(model_responses_dir):
            response_files = [f for f in os.listdir(model_responses_dir) if f.startswith("response_")]
            error_files = [f for f in os.listdir(model_responses_dir) if f.startswith("error_")]
            print(f"Successful responses: {len(response_files)}")
            print(f"Failed responses: {len(error_files)}")
            
            # Check which models were used
            models_used = set()
            for file in response_files:
                with open(os.path.join(model_responses_dir, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "gpt-4-turbo-preview" in content:
                        models_used.add("gpt-4-turbo-preview")
                    elif "gpt-4o" in content:
                        models_used.add("gpt-4o")
                    elif "gpt-3.5-turbo" in content:
                        models_used.add("gpt-3.5-turbo")
            
            print(f"Models used: {', '.join(models_used)}")
    else:
        print("\nNo problems were extracted.")

if __name__ == "__main__":
    main() 