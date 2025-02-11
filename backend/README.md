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
1. **Clone the repository**:
   ```sh
   python -m venv fastapi-venv
   source fastapi-venv/Scripts/activate  # On Windows
   pip install -r requirements.txt
   ```
1. **Run the localhost (on Windows)**:
   ```sh
   python main.py
   ```
   OR
   ```sh
   uvicorn main:app --reload
   ```

