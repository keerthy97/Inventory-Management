# Inventory Management System

## Project Overview
This project is a Simple Inventory Management System built using Django Rest Framework, PostgreSQL for database management, Redis for caching, and a logging system for tracking API usage and errors.

## Setup Instructions

### Prerequisites:
- Python 3.x
- PostgreSQL
- Redis
- pip (Python package manager)

### Steps to Set Up:
1. Clone the repository:
   ```bash
   git clone https://github.com/keerthy97/Inventory-Management.git
   cd inventory-management-system
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure the database:
   - Create a PostgreSQL database and update `DATABASES` settings in `settings.py`:
     ```python
     DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
     }
     ```

6. Run database migrations:
   ```bash
   python manage.py migrate
   ```

7. Set up Redis for caching:
   Ensure Redis is running on your machine:
   ```bash
   redis-server
   ```

8. Create a superuser to access the Django admin:
   ```bash
   python manage.py createsuperuser
   ```

9. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

- **Authentication**:
  - Register: `POST /api/register/`
  - Example payload:
    ```json
    {
      "username": "newuser",
      "password": "newpassword",
      "email": "newuser@example.com"
    }
    ```

- **Item Management**:
  - Retrieve items: `GET /api/items/`
  - Retrieve item by ID: `GET /api/items/{id}/`
  - Create new item: `POST /api/items/`
  - Update item: `PUT /api/items/{id}/`
  - Delete item: `DELETE /api/items/{id}/`

## Usage Examples

### Retrieve All Items
```bash
curl -X GET http://127.0.0.1:8000/api/items/
