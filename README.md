# FastAPI CRUD

A REST API built with FastAPI and MongoDB.

## Tech Stack

| Package | Purpose |
| --- | --- |
| `fastapi` | Build REST APIs |
| `uvicorn` | Run the FastAPI server |
| `pymongo` | Connect Python to MongoDB |
| `python-dotenv` | Read environment variables from `.env` |

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sanju1098/python-fastapi.git
cd fastapi-crud
git checkout fastapi-crud
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate with `venv\Scripts\activate` instead.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values (for example, your MongoDB connection string).

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. Interactive docs are available at `http://localhost:8000/docs`.

## Project Structure

```
fastapi-crud/
├── main.py            # FastAPI application
├── .env               # Environment variables (not committed)
├── .env.example       # Template for .env
└── requirements.txt   # Python dependencies
```

## Setting Up From Scratch

If you are creating this project fresh rather than cloning it:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install fastapi "uvicorn[standard]" pymongo python-dotenv
pip freeze > requirements.txt
```

Then create `main.py`, `.env` and `requirements.txt`.