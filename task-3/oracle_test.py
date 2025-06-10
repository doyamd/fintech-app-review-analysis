import cx_Oracle
import pandas as pd
from config import username, password, dsn


connection = None
cursor = None
try:
    # Establish connection
    print("Connecting to Oracle Database...")
    print("Using DSN:", dsn, "Username:", username, "Password:", password)
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    print("Connected to Oracle Database successfully!")

    # Drop tables if they exist
    try:
        cursor.execute("DROP TABLE Reviews PURGE")
    except cx_Oracle.DatabaseError:
        pass
    try:
        cursor.execute("DROP TABLE Banks PURGE")
    except cx_Oracle.DatabaseError:
        pass

    # Create Banks table
    cursor.execute("""
        CREATE TABLE Banks (
            bank_id NUMBER PRIMARY KEY,
            bank_name VARCHAR2(100) NOT NULL,
            headquarters VARCHAR2(150),
            established_year NUMBER(4),
            website VARCHAR2(100)
        )
    """)

    # Create Reviews table with new columns
    cursor.execute("""
        CREATE TABLE Reviews (
            review_id NUMBER PRIMARY KEY,
            bank_id NUMBER,
            review_text VARCHAR2(4000),
            rating NUMBER(2,1) CHECK (rating >= 0 AND rating <= 5),
            review_date DATE,
            reviewer_name VARCHAR2(100),
            source VARCHAR2(100),              -- New column
            sentiment_label VARCHAR2(50),      -- New column
            sentiment_score NUMBER(5,4),       -- New column
            themes VARCHAR2(4000),             -- New column for themes
            FOREIGN KEY (bank_id) REFERENCES Banks(bank_id)
        )
    """)

    # Commit changes
    connection.commit()
    print("Tables created successfully!")

    # Verify tables
    cursor.execute("SELECT table_name FROM user_tables")
    tables = cursor.fetchall()
    print("Tables in schema:", tables)

    # Load data from CSV
    df = pd.read_csv('data/reviews_with_themes.csv')  # Adjust path if needed
    # Map bank names to bank_ids
    bank_ids = {}
    for index, row in df.iterrows():
        bank_name = row['bank']
        if bank_name not in bank_ids:
            cursor.execute("SELECT MAX(bank_id) FROM Banks")
            max_id = cursor.fetchone()[0] or 0
            new_bank_id = max_id + 1
            cursor.execute("""
                INSERT INTO Banks (bank_id, bank_name, headquarters, established_year, website)
                VALUES (:1, :2, :3, :4, :5)
            """, (new_bank_id, bank_name, None, None, None))
            bank_ids[bank_name] = new_bank_id

        # Insert review data
        cursor.execute("""
            INSERT INTO Reviews (review_id, bank_id, review_text, rating, review_date, reviewer_name, source, sentiment_label, sentiment_score, themes)
            VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9, :10)
        """, (index + 1, bank_ids[bank_name], row['review'], row['rating'], row['date'], None, row['source'], row['sentiment_label'], row['sentiment_score'], row['themes']))

    connection.commit()
    print("CSV data inserted successfully!")

except cx_Oracle.DatabaseError as e:
    print("Database error:", e)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()