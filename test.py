import os
from groq import Groq
import re
import ast
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not set.")


# api_key = os.environ.get("GROQ_API_KEY")
# if not api_key:
#     raise ValueError("GROQ_API_KEY not set.")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = (
    "You are a strict unit test generator tool. "
    "Generate ONLY valid Python unittest test cases for the given function. "
    "Output code only. No explanations. No markdown. No comments."
)

def remove_comments(code : str):
    code = re.sub(r"#.*", "", code)
    code = re.sub(r'"""[\s\S]*?"""', "", code)
    code = re.sub(r"'''[\s\S]*?'''", "", code)
    return code

def extract_function(code : str):
    tree = ast.parse(code)

    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]
    if len(functions) != 1:
        return None
    return functions[0]



def generate_tests(input_code : str):
    sanitized = remove_comments(input_code)

    func = extract_function(sanitized)

    if func is None:
        return KeyError

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

    source_code = """def add(a, b):
    return a + b"""

    tests = generate_tests(source_code)
    print(tests)

if __name__ == "__main__":
    main()


