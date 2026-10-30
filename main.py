from dotenv import load_dotenv
from datetime import date
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, model_validator
import uvicorn

load_dotenv()

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

class DateRange(BaseModel):
    start_date: date = Field(default_factory=date.today)
    end_date: date | None = None

    @model_validator(mode='after')
    def set_end_date(self):
        if self.end_date is None:
            self.end_date = self.start_date
        elif self.end_date < self.start_date:
            raise ValueError(f"end_date {self.end_date} cannot be before start_date {self.start_date}")
        return self
    

@app.get("/run")
def run_endpoint(date_range: DateRange = Query()):
    start_date = date_range.start_date
    end_date = date_range.end_date
    return f"Fetch calendar events from {start_date} to {end_date}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)