import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.server = os.getenv('DB_SERVER')
        self.database = os.getenv('DB_DATABASE')
        self.username = os.getenv('DB_USERNAME')
        self.password = os.getenv('DB_PASSWORD')
        self.connection_string = None
        self.setup_connection_string()
    
    def setup_connection_string(self):
        """Setup database connection string"""
        self.connection_string = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password};'
            f'Encrypt=yes;'
            f'TrustServerCertificate=no;'
            f'Connection Timeout=30;'
        )
    
    def get_connection(self):
        """Get database connection"""
        try:
            connection = pyodbc.connect(self.connection_string)
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def create_ticket(self, user_phone, issue_description, category="General"):
        """Create a new service desk ticket"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor()
            
            # Example SQL - adjust based on your database schema
            sql = """
            INSERT INTO Tickets (UserPhone, Description, Category, Status, CreatedDate)
            VALUES (?, ?, ?, 'Open', GETDATE())
            """
            
            cursor.execute(sql, (user_phone, issue_description, category))
            connection.commit()
            
            # Get the ticket ID
            ticket_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            return ticket_id
            
        except Exception as e:
            print(f"Error creating ticket: {e}")
            return None
    
    def get_ticket_status(self, ticket_id):
        """Get status of a specific ticket"""
        try:
            connection = self.get_connection()
            if not connection:
                return None
            
            cursor = connection.cursor()
            
            sql = "SELECT Status, Description, CreatedDate FROM Tickets WHERE TicketID = ?"
            cursor.execute(sql, (ticket_id,))
            
            result = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if result:
                return {
                    'status': result[0],
                    'description': result[1],
                    'created_date': result[2]
                }
            return None
            
        except Exception as e:
            print(f"Error getting ticket status: {e}")
            return None