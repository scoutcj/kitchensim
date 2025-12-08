# Kitchen Simulator 🍳

Restaurant service flow simulator with agent orchestration. Built with FastAPI, LangGraph, React, and TypeScript.

**Website:** willdinnergowell.com

## Project Structure

```
kitchensim/
├── backend/          # FastAPI backend
│   ├── main.py       # FastAPI app entry point
│   └── requirements.txt
├── frontend/         # React + TypeScript frontend
│   ├── src/
│   └── package.json
└── phase1.md         # Implementation plan
```

## Setup

### Backend

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY
```

4. Run the server:
```bash
python main.py
# Or: uvicorn main:app --reload
```

Backend runs on http://localhost:8000

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

Frontend runs on http://localhost:5173

## Development

- Backend API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/api/health

## Phase 1 Status

✅ PR 1: Project Foundation - Complete

See `phase1.md` for full implementation plan.

