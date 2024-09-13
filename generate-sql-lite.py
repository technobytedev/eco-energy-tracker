import sqlite3

# Connect to SQLite (it will create the database file if it doesn't exist)
connection = sqlite3.connect('ecoenergy.db')

# Create a cursor object
cursor = connection.cursor()

# Create a `users` table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);
''')

# Insert some sample data (optional)
cursor.execute("INSERT INTO users (firstname, lastname) VALUES ('John', 'Doe');")
cursor.execute("INSERT INTO users (firstname, lastname) VALUES ('Jane', 'Smith');")
cursor.execute("INSERT INTO users (firstname, lastname) VALUES ('Alice', 'Johnson');")

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Database and table created successfully!")
