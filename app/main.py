# app/main.py

from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, SessionLocal
from .models import Company, Event, Person
import openai
import json
import subprocess
import os

app = FastAPI()

# Configure OpenAI
openai.api_key = 'your_openai_api_key'

# Load example queries
with open('queries.json') as f:
    example_queries = json.load(f)

async def ensure_database_setup():
    if not os.path.exists('data/company_info.csv'):
        subprocess.run(["python", "app/data_processing.py"])

@app.on_event("startup")
async def startup_event():
    await ensure_database_setup()

@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_query = data.get('query')

    # Use OpenAI to convert natural language query to SQL
    prompt = f"Convert the following natural language query to SQL:\n\nExamples:\n"
    for example in example_queries:
        prompt += f"Q: {example['natural_language']}\nA: {example['sql']}\n\n"
    prompt += f"Q: {user_query}\nA:"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    sql_query = response.choices[0].text.strip()

    try:
        async with SessionLocal() as session:
            result = await session.execute(sql_query)
            result_list = [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result_list

@app.post("/clear_context")
async def clear_context():
    return {"message": "Context cleared"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


