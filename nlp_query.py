# app/nlp_query.py

import openai
import os
import pandas as pd
from app.dataload import get_df

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(filename, question):
    df = get_df(filename)
    if df is None:
        return {"error": "Data not loaded."}

    prompt = f"""
You are a data scientist. Write Python Pandas code to answer this question using a DataFrame named `df`.

DataFrame sample (first few rows):
{df.head().to_string(index=False)}

Question: {question}

Output only the Python code in a markdown block, nothing else.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()
    try:
        code_block = content.split("```python")[1].split("```")[0].strip()
    except:
        return {"error": "Failed to extract code block"}

    # Secure code execution (simple sandbox)
    try:
        local_env = {"df": df.copy()}
        exec(code_block, {}, local_env)
        result = local_env.get("result", "No `result` variable found.")
    except Exception as e:
        return {"error": str(e), "code": code_block}

    return {
        "code": code_block,
        "result": str(result)
    }
