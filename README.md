# SpendWise — Expense Tracker API

SpendWise is a REST API built with Python and FastAPI that helps users manage expenses, track spending, and view financial summaries. It includes JWT authentication and user-level data isolation.

## Features

- **User authentication:** Register and log in with secure password hashing.
- **JWT authorization:** Protect endpoints with expiring access tokens.
- **Expense management:** Create, view, update, and delete expenses.
- **Expense filtering:** Filter records by category and date range.
- **Spending analytics:** View overall, monthly, and category-wise summaries.
- **Data persistence:** Store users and expenses in SQLite.
- **Input validation:** Validate amounts, dates, and required fields.
- **Automated tests:** Test API functionality and access control using pytest.

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- PyJWT
- Argon2 password hashing via `pwdlib`
- pytest and FastAPI TestClient

## Project Structure

```text
SpendWise/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routers/
│       ├── auth_routes.py
│       ├── expenses.py
│       └── analytics.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SpendWise
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Generate a secret key:

```powershell
py -c "import secrets; print(secrets.token_urlsafe(48))"
```

Add the generated key to `.env`:

```dotenv
DATABASE_URL=sqlite:///./spendwise_v5.db
SPENDWISE_SECRET_KEY=your_generated_secret
```

Keep `.env` private and never commit it to GitHub.

### 5. Start the API

```powershell
py -m uvicorn app.main:app --reload
```

Interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/auth/register` | Register a user |
| POST | `/auth/login` | Obtain an access token |
| POST | `/expenses` | Create an expense |
| GET | `/expenses` | List and filter your expenses |
| GET | `/expenses/{expense_id}` | Retrieve an expense |
| PUT | `/expenses/{expense_id}` | Update an expense |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/summary` | View overall spending |
| GET | `/summary/monthly` | View monthly spending |
| GET | `/summary/categories` | View category-wise spending |

Expense and summary endpoints require a valid bearer token.

## Running Tests

Run the automated test suite:

```powershell
py -m pytest -v
```

The tests cover expense operations, validation, authentication, and user-level access control.

## Security Notes

- Passwords are stored as Argon2 hashes, not plain text.
- JWT access tokens expire after 30 minutes.
- Expense queries are restricted to the authenticated user.
- Secrets and local database files should be excluded from version control.
- Use HTTPS and production-grade configuration before deployment.

## Future Improvements

- Alembic database migrations
- Pagination and sorting
- Expense budgets and spending limits
- API rate limiting
- Continuous integration with GitHub Actions
- Deployment with a production database

## Author

Built as a backend development portfolio project to practice REST API design, authentication, database management, and automated testing.
