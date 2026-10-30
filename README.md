# AI Email Assistant

An intelligent email assistant powered by OpenAI's API with FastAPI backend, capable of fetching and analyzing calendar events within specified date ranges.

## Overview

This project demonstrates an AI agent that can intelligently process natural language requests and interact with external tools (like calendar services) to provide helpful responses. It uses OpenAI's function calling feature to enable the agent to make tool calls autonomously.

## Features

- 🤖 **AI Agent**: Powered by OpenAI's GPT API with function calling capabilities
- 📅 **Calendar Integration**: Fetch calendar events within specified date ranges
- 🔄 **Multi-turn Conversations**: Agent can iterate multiple times to refine responses
- 🚀 **FastAPI Server**: RESTful endpoints for health checks and date range queries
- 🔐 **Environment-based Configuration**: Uses `.env` for secure credential management

## Project Structure

```
├── main.py          # FastAPI application with REST endpoints
├── agents.py        # AI agent logic with OpenAI integration
├── tools.py         # Tool implementations (calendar event fetching)
├── pyproject.toml   # Project metadata and dependencies
└── README.md        # This file
```

## Requirements

- Python ≥ 3.12
- OpenAI API key

## Dependencies

- **fastapi** ≥ 0.162.0 - Web framework
- **uvicorn** ≥ 0.54.0 - ASGI server
- **python-dotenv** ≥ 1.2.4 - Environment variable management
- **openai** - OpenAI Python SDK (implied dependency)

## Installation

1. Clone the repository
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Start the Server

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000`

### API Endpoints

#### Health Check
```bash
GET /health
```
Returns `{"status": "ok"}`

#### Run Agent
```bash
GET /run?start_date=2024-01-01&end_date=2024-01-31
```
Fetches calendar events for the specified date range.

Query parameters:
- `start_date` (optional): Start date in YYYY-MM-DD format (defaults to today)
- `end_date` (optional): End date in YYYY-MM-DD format (defaults to start_date if not provided)

### Agent Example

```python
from agents import run_agent

response = run_agent("What events do I have scheduled for next week?")
print(response)
```

## How It Works

1. The AI agent receives a natural language prompt
2. The agent analyzes the request and determines if it needs to call tools
3. If tool calls are needed, the agent invokes `fetch_calendar_events` with appropriate date parameters
4. The tool returns calendar data, which is sent back to the agent
5. The agent processes the results and generates a natural language response
6. The process repeats up to 3 times to refine the answer if needed

## Future Enhancements

- Integrate with real calendar services (Google Calendar, Outlook)
- Add email composition and sending capabilities
- Support for natural language date parsing (e.g., "next week", "tomorrow")
- Multi-user support with authentication
- Email filtering and organization features
