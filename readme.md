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
1. Download and install (choose Developer version) [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) [ For linux: [Follow the instructions](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2204#install-sql-server) ]
2. Download and install [ODBC Driver 18 for SQL Server for Windows](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16#download-for-windows) [ For linux: [Follow the instructions](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-ver16&tabs=ubuntu2204#install-the-sql-server-command-line-tools) ]
3. Create some new databases

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
```
TIMEZONE=<your_timezone>
ODBC_DRIVER=ODBC Driver 18 for SQL Server
```



## Step 4: Django Setup

### Database Migration
1. Run migrations:
```
python manage.py migrate
```

2. Create a superuser (admin) (optional):
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
1. Open a new terminal tab or window
2. Start the Django development server:
   ```
   python manage.py runserver
   ```
3. Access the application at `http://localhost:8000`
4. Access the API interface at `http://localhost:8000/api/docs`
