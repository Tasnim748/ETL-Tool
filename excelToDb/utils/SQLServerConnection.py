import pyodbc
from django.db import connections
from django.conf import settings

class SQLServerConnection:
    def __init__(self, server, database, user_id, password):
        """
        Initialize connection parameters for SQL Server
        
        Args:
            server (str): SQL Server IP address/hostname
            database (str): Database name
            user_id (str): SQL Server username
            password (str): SQL Server password
        """
        self.server = server
        self.database = database
        self.user_id = user_id
        self.password = password
        self.connection = None
        
    def connect(self):
        """
        Establish connection to SQL Server
        
        Returns:
            pyodbc.Connection: Database connection object
        
        Raises:
            Exception: If connection fails
        """
        try:
            # Connection string for SQL Server
            conn_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.user_id};"
                f"PWD={self.password};"
                "Trusted_Connection=no;"
                "TrustServerCertificate=yes;"
                "Connection Timeout=30;" 
            )
            
            # Establish connection
            self.connection = pyodbc.connect(conn_str)
            return self.connection
            
        except Exception as e:
            raise Exception(f"Failed to connect to SQL Server: {str(e)}")
    
    def create_table_if_not_exists(self, table_name, columns_definition):
        """
        Create table if it doesn't exist
        
        Args:
            table_name (str): Name of the table to create
            columns_definition (str): SQL column definitions
            
        Returns:
            bool: True if successful
        """
        try:
            cursor = self.connection.cursor()
            
            # Check if table exists
            check_query = f"""
            IF NOT EXISTS (
                SELECT 1
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = '{table_name}'
            )
            BEGIN
                CREATE TABLE {table_name} (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    {columns_definition},
                    created_at DATETIME DEFAULT GETDATE()
                );
            END;
            """

            cursor.execute(check_query)
            self.connection.commit()
            return True
            
        except Exception as e:
            raise Exception(f"Failed to create table: {str(e)}")
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager enter"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()