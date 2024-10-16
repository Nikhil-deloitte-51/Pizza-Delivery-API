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
    bash:
        cd <repository-directory>

3. Install dependencies:
    Using poetry:
        bash:
            poetry install
            poetry shell

4. Run the Application:
    cd app
    poetry run uvicorn main:app --reload

5. Access the API:
    Navigate to http://127.0.0.1:8000/docs
