# from groq import Groq
# import os
# from dotenv import load_dotenv
# load_dotenv(dotenv_path="../.env")

from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, columns, rows):

    data_string = ""

    for row in rows:
        data_string += str(row) + "\n"

    prompt = f"""
You are a financial analyst assistant.

User Question:
{question}

Database Columns:
{columns}

Database Results:
{data_string}

Explain the financial result clearly in natural language.
If there are multiple companies, compare them.
If it is a single company, summarize the result.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content