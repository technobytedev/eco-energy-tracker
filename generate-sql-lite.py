import sqlite3

# Connect to SQLite (it will create the database file if it doesn't exist)
connection = sqlite3.connect('ecoenergy.db')

# Create a cursor object
cursor = connection.cursor()

# Create a `users` table if it doesn't exist
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS appliance (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     image TEXT NOT NULL
# );
# ''')

# Insert some sample data (optional)
# cursor.execute("delete from appliance;")
# cursor.execute("INSERT INTO users (firstname, lastname) VALUES ('Jane', 'Smith');")
cursor.execute("SELECT * FROM simulation")

# Commit changes and close the connection
connection.commit()
cursor.close()
connection.close()

print("Database and table created successfully!")
