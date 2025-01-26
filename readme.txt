
# Inventory Management System

## Prerequisites

1. **Install Python**  
   Ensure you have Python installed. [Download Python](https://www.python.org/).
   
2. **Install Visual Studio Code (VS Code)**  
   [Download VS Code](https://code.visualstudio.com/).

3. **Install PostgreSQL**  
   Install PostgreSQL and pgAdmin. [Download PostgreSQL](https://www.postgresql.org/).

---

## Setup Instructions

### 1. Clone the Repository
Open a terminal and run:
```bash
git clone https://github.com/ash-pro007/Inventory
```

### 2. Create a Virtual Environment
Create a virtual environment for the project:
```bash
mkvirtualenv projectinventorymanager
```

### 3. Activate the Virtual Environment
Activate the virtual environment:
```bash
workon projectinventorymanager
```

### 4. Install Django
Install Django within the virtual environment:
```bash
pip install django
```

### 5. Navigate to the Project Directory
Change into the `Inventory` project directory. Inside, you’ll find:
- Folders: `Data_manager (app)`, `Inventory_manager (project)`, `static`, `templates`
- File: `manage.py`

---

## Required Libraries

### 6. Install Dependencies
Install the required libraries to run the project:
- **Pandas** and **OpenPyXL** for handling CSV and Excel files:
  ```bash
  pip install pandas openpyxl
  ```
- **Psycopg2** to connect Django with PostgreSQL:
  ```bash
  pip install psycopg2
  ```

---

## Database Setup

### 7. Create the Database
Using pgAdmin4 or the PostgreSQL command line, create a database named `Inventory`.

### 8. Apply Migrations
Generate and apply migrations to create the necessary database tables:
1. Generate SQL for migrations:
   ```bash
   python manage.py sqlmigrate Data_manager 0001
   ```
2. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

---

## Admin Setup

### 9. Create a Superuser
Create an admin user to access the Django Admin Panel:
```bash
python manage.py createsuperuser
```

---

## Run the Project

### 10. Start the Server
Run the Django development server:
```bash
python manage.py runserver
```

The project is now ready to use. Access it at `http://127.0.0.1:8000`.

---
