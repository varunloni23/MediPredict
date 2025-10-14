import psycopg2
from psycopg2 import sql

def test_database_connection():
    # Database connection parameters
    DB_HOST = "db.ylnfooqviyusdjeymyka.supabase.co"
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "MediPredict"
    DB_PORT = "5432"
    
    try:
        # Establish connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        
        # Create cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        
        print("Database connection successful!")
        if db_version:
            print(f"PostgreSQL version: {db_version[0]}")
        else:
            print("Could not retrieve PostgreSQL version")
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()