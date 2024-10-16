# Pizza Delivery API

# Description

A simple FastAPI application for managing pizaa delivery using MySQL

# Requirements
- Python 3.10
- FastAPI
- SQLAlchemy
- Uvicorn

## Setup Instructions

1. Clone the repository
    ```bash:
        git clone <repository-url>

2. Navigate to the project directory
    ```bash:
        cd <repository-directory>

3. Install Poetry(if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   
4. Install the project dependencies:
   ```bash
     poetry install
     poetry shell

5. Run the Application:
   ```bash
    cd app
    poetry run uvicorn main:app --reload

6. Access the API:
    Navigate to http://127.0.0.1:8000/docs

# Examples
You can interact with the API using tools like Postman or curl. Here are some example requests.

# Get Root
```bash
curl -X GET http://127.0.0.1:8000/
