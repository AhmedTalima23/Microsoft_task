import os
import re
import ast
from groq import Groq
from dotenv import load_dotenv
import argparse

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    api_key = input("Enter your Groq API Key: ").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = (
    "You are a strict unit test generator tool. "
    "Generate ONLY valid Python unittest test cases for the given function. "
    "Output code only. No explanations. No markdown. No comments."
)

# Helper Functions

def remove_comments(code: str) -> str:
    code = re.sub(r"#.*", "", code)
    code = re.sub(r'"""[\s\S]*?"""', "", code)
    code = re.sub(r"'''[\s\S]*?'''", "", code)
    return code

def extract_function(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    if len(functions) != 1:
        return None
    return functions[0]

def generate_tests(input_code: str):
    sanitized = remove_comments(input_code)
    func = extract_function(sanitized)

    if func is None:
        return "Error: This tool only generates unit tests for functions."

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_completion_tokens=1024,
        top_p=1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": sanitized},
        ],
    )
    return response.choices[0].message.content.strip()



def main():
    parser = argparse.ArgumentParser(description="CLI Unit Test Generator")
    parser.add_argument("-f", "--file", help="Python file containing a single function")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                source_code = f.read()
        except Exception:
            print("Error: Cannot read file.")
            return
    else:
        print("Enter your Python function (end with EOF / Ctrl+D or Ctrl+Z):")
        source_code = ""
        try:
            while True:
                line = input()
                source_code += line + "\n"
        except EOFError:
            pass

    tests = generate_tests(source_code)
    print(tests)

if __name__ == "__main__":
    main()
