# Django Project Setup Guide

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:
- Python 3.8 or higher
- pip (Python package manager)
- Redis Server
- Microsoft SQL Server
- Git (optional, for version control)

## Step 1: Database Setup

### Microsoft SQL Server Configuration
1. Install Microsoft SQL Server if not already installed
2. Create a new database for the project named 'ETL_DB':
   ```sql
   CREATE DATABASE ETL_DB;
   ```
## Step 2: Redis Setup

### Redis Installation and Configuration
1. Install Redis Server:
   - For Windows: Download and install from [Redis Windows Downloads](https://github.com/microsoftarchive/redis/releases)
   - For Linux: `sudo apt-get install redis-server`
   - For macOS: `brew install redis`

2. Start Redis Server:
   - Windows: Start Redis service from Services
   - Linux/macOS: `sudo service redis start` or `redis-server`

3. Verify Redis is running:
   ```bash
   redis-cli ping
   ```
   Should return "PONG"



## Step 3: Project Setup

### Virtual Environment Creation
1. Extract the project zip file to your desired location
2. Open terminal/command prompt and navigate to the project directory
3. Create a virtual environment using command:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

### Dependencies Installation
1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Environment Configuration
1. Create a `.env` file in the project root directory
2. Add the following configurations (modify as needed):
   
### Database Configuration
```
TIMEZONE=<your_timezone>
DATABASE_NAME=ETL_DB
DATABASE_PASS=<your_database_password>
DATABASE_USER=<your_database_username>
```



## Step 4: Django Setup

### Database Migration
1. Run migrations:
```
python manage.py migrate
```

2. Create a superuser (admin):
```
python manage.py createsuperuser
```


## Step 5: Celery Configuration

### Starting Celery Worker
1. Open a new terminal window
2. Activate the virtual environment
3. Start Celery worker:
### Windows
```
celery -A projectroot worker --pool=solo -l info
```

### Linux/macOS
```
celery -A projectroot worker -l info
```

## Step 6: Running the Application

1. Start the Django development server:
   ```
   python manage.py runserver
   ```
2. Access the application at `http://localhost:8000`
3. Access the API interface at `http://localhost:8000/api/docs`
