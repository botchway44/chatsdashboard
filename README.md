# Chats Dashboard

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.10+
- `pip` (Python package installer)
- `venv` (for creating virtual environments)

## Project Setup

Follow these steps to get your development environment set up and running.

**1. Clone the Repository**

```bash
git clone [url]
cd app-dir
```

**2. Create and Activate a Virtual Environment**
It is highly recommended to use a virtual environment to manage project dependencies.

- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**3. Install Dependencies**
Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**4. Run Database Migrations**
Apply the initial database schema and any subsequent model changes.

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a Superuser Account**
You'll need a superuser account to access the Django admin dashboard.

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin username, email, and password.

**6. Run the Development Server**
You're all set! Start the development server.

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`. You can access the Django admin panel at `http://127.0.0.1:8000/admin/`.

---

## API Endpoints

- `/api/auth/`: User registration, login, and token management.
