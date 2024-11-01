import sqlite3

def initialize_db():
    conn = sqlite3.connect('database/prescriptions.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL
                      )''')
    
    # Create prescriptions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions (
                      id INTEGER PRIMARY KEY,
                      user_id INTEGER,
                      name TEXT,
                      content TEXT,
                      FOREIGN KEY (user_id) REFERENCES users(id)
                      )''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
