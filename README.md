# FinLume

🧾 FinLume – Personal Finance Tracker (Backend-Only)
🚀 Project Overview

FinLume is a backend-only personal finance tracker built using Python FastAPI. The aim is to provide a lightweight, secure, and scalable foundation for managing personal income, expenses, and savings—all through a clean API interface.

This project is part of my ongoing journey to deepen my backend development skills and understanding of building real-world applications with FastAPI, PostgreSQL, and token-based authentication.

🔧 Tech Stack

- Python 3.11+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Alembic (Migrations) # Work in progress
- Docker (Optional for Deployment) # Work in progress
- JWT Authentication

✨ Key Features

- User registration & login (JWT-based authentication)
- Add / edit / delete financial transactions (income, expense)
- Categorize transactions (Bills / Subscriptions)
- Data validation with Pydantic
- Environment-safe settings with .env
- Database migrations with Alembic (Coming Soon)

finlume/
├── app/
│ ├── crud/
│ ├── routers/
│ ├── tests/
│ ├── schemas/
│ └── main.py
├── auth_utils.py
├── database.py
├── requirements.txt
├── main.py
├── models.py
├── utils.py
└── README.md

Setup Instructions (Local Development)

Step 1 - clone the repo

"git clone https://github.com/YOURUSERNAME/finlume.git
cd finlume"

Step 2 - Create and activate the virtual enviroment

"python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows"

Step 3 - Install Dependencies

"pip install -r requirements.txt"

Step 4 - Set up the .env file

"Create a .env file using the provided .env.example as a template."

Step 5 - Run the app

"uvicorn app.main:app --reload"

🔒 Authentication

FinLume uses JWT tokens for user authentication. Upon login, you'll receive an access token to use in the Authorization header when making requests.

✅ Roadmap

User authentication (JWT)

Basic transaction CRUD

Financial reports / summaries

Docker containerization

Frontend (React or Next.js – future scope)

🧑‍💻 About Me

I'm Alex, a self-taught Python developer currently working towards a career tranistion. Running a gardening business at the moment until I can make the switch. Focused on backend development with FastAPI. This project reflects my interest in building real-world, useful tools while improving my architecture, testing, and deployment workflows.

Feel free to explore the code, raise issues, or offer suggestions!
