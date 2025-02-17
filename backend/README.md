# FastAPI Language Exercises API

This project is a learning practice for **FastAPI** and **Pydantic**, where I build a simple API to manage language exercise questions.

## 🚀 Features
- **CRUD operations**: Create, Read, Update, and Delete exercise questions.
- **Question Types**:
  - ✏️ **Fill-in-the-gap** (planned)
  - 🔘 **Multiple choice** (planned)

## 🛠 Tech Stack
- **FastAPI** (for the API backend)
- **Pydantic** (for data validation)
- **Python 3.12+**

## 🔧 Setup & Installation
1. **Create a new virtual environment**:
```sh
python -m venv <venv-name>
source ./fastapi-venv/Scripts/activate  # On Windows
pip install -r requirements.txt
```
2. **Run the localhost (on Windows)**:

Might not work because of the missing local db
```sh
\fastapi\backend uvicorn app.main:app --reload
```

## 🔧 Useful Commands
- Activate a virtual environment:
```cmd
cd .\backend\
.\fastapi-venv\Scripts\activate 
```

- Deactivate the virtual environment:
```cmd
deactivate
```

- Add installed package to `requirements.txt`:
```cmd
pip freeze > requirements.txt
```
