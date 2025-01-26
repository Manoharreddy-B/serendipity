import psycopg2
from psycopg2 import sql
import random
from datetime import date, timedelta

# Database connection parameters
DB_HOST = "localhost"
DB_PORT = "15432"
DB_NAME = "serendipitydb"
DB_USER = "serenbhai"
DB_PASSWORD = "serenbro"

# Function to generate random dates
def generate_random_date():
    start_date = date(1990, 1, 1)
    end_date = date(2000, 12, 31)
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)

def generate_phone_number():
  area_code = ''.join(random.choice('23456789') for _ in range(3)) 
  exchange_code = ''.join(random.choice('234567890') for _ in range(3)) 
  line_number = ''.join(random.choice('0123456789') for _ in range(4)) 

  return f'{area_code}-{exchange_code}-{line_number}'

# Function to create 1000 users, 10 stocks, and portfolios
def create_data():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    cursor = conn.cursor()

    try:
        # Check if users exist
        cursor.execute("SELECT COUNT(*) FROM UserTable")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            # Insert 1000 users
            users = [
                ('User' + str(i), f'user{i}@example.com', generate_random_date(), generate_phone_number())
                for i in range(1, 1001)
            ]
            cursor.executemany("""
                INSERT INTO UserTable (Name, Email, DOB, PhoneNo)
                VALUES (%s, %s, %s, %s)
            """, users)
            print("Inserted 1000 users into UserTable.")

        # Check if stocks exist
        cursor.execute("SELECT COUNT(*) FROM StockTable")
        stock_count = cursor.fetchone()[0]
        
        if stock_count == 0:
            # Insert 10 stocks
            stocks = [
                ('Stock' + str(i), float(100+(i*50)))
                for i in range(1, 11)
            ]
            cursor.executemany("""
                INSERT INTO StockTable (Price)
                VALUES (%s)
            """, [(price,) for _, price in stocks])
            print("Inserted 10 stocks into StockTable.")

        # Check if portfolios exist
        cursor.execute("SELECT COUNT(*) FROM PortfolioTable")
        portfolio_count = cursor.fetchone()[0]
        
        if portfolio_count == 0:
            # Get all users and stocks
            cursor.execute("SELECT UID FROM UserTable")
            users = [uid[0] for uid in cursor.fetchall()]

            cursor.execute("SELECT SID FROM StockTable")
            stocks = [sid[0] for sid in cursor.fetchall()]

            portfolios = []
            for user in users:
                num_stocks = random.randint(1, len(stocks))
                assigned_stocks = random.sample(stocks, num_stocks)

                for stock in assigned_stocks:
                    qty = random.randint(1, 100)
                    portfolios.append((user, stock, qty))
                    
            cursor.executemany("""
                INSERT INTO portfoliotable (UID, SID, Qty)
                VALUES (%s, %s, %s)
            """, portfolios)
            print("Inserted portfolios into portfoliotable.")

        # Commit changes
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_data()
