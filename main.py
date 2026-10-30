from dotenv import load_dotenv
from datetime import date
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, model_validator
import uvicorn
from agents import run_agent

load_dotenv()

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/run")
def run_endpoint(prompt: str = Query(...)):
    return run_agent(prompt)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
