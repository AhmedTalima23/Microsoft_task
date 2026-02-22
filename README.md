# Microsoft Task - Python Unit Test Generator CLI

This is a **CLI-based Python developer tool** that automatically generates **unit tests** for a single Python function using the **Groq LLM API**.

The tool enforces strict constraints:  

- Accepts **Python source code with exactly one function**.  
- Rejects any other input with the error message:  
  `Error: This tool only generates unit tests for functions.`  
- Sanitizes comments to prevent prompt injection.  
- Outputs **only valid Python `unittest` code** (no explanations, markdown, or extra text).  
- Deterministic output (`temperature=0`).  

---

## 🔹 Prerequisites

- Python 3.10+  
- [Groq API Key](https://console.groq.ai/)  
- `python-dotenv` package

---

## 🔹 Installation

1. Clone this repository:

```bash
git clone https://github.com/AhmedTalima23/Microsoft_task.git
cd Microsoft_task
```

2. Install dependencies:

```bash
pip install groq python-dotenv
```

## 🔹 Setup API Key

Create a .env file in the project root:
GROQ_API_KEY=your_api_key_here

🔹 How to Run
1️⃣ Using a Python File
```bash
python test.py -f path/to/your_function.py
```
Example:

python test.py -f my_function.py

2️⃣ Manual Input via CLI

python test.py

Then type or paste your function:

```bash
def add(a, b):
    return a + b
```
End input with Ctrl+D (Linux/macOS) or Ctrl+Z (Windows).

The tool will print only the generated unit tests.

🔹 Example Output

For the function add(a, b), the tool may generate:

import unittest

class TestAdd(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-1, -1), -2)

if __name__ == "__main__":
    unittest.main()

