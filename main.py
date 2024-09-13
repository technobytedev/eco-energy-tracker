import webview
import os
import sqlite3

class Api:
    def fetch_data(self):
        try:
            # Connect to the SQLite database (it will create the file if it doesn't exist)
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()  # Fetch all rows from the query result
            columns = [description[0] for description in cursor.description]  # Get column names

            # Return the fetched data as a string (for simplicity)
            result = ""
            for row in rows:
                row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                result += f"ID: {row_data['id']}, Firstname: {row_data['firstname']}, Lastname: {row_data['lastname']}\n"
            
            return {'message': result}
        
        except sqlite3.Error as e:
            return {'message': f"Error: {e}"}
        finally:
            cursor.close()
            connection.close()

    def search_data(self, searchByName):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()

            # Query to search name
            query = "SELECT * FROM users WHERE firstname LIKE ? OR lastname LIKE ?;"
            search_pattern = f"%{searchByName}%"  # Add wildcard characters before and after the search term
            cursor.execute(query, (search_pattern, search_pattern))

            rows = cursor.fetchall()  # Fetch all rows from the query result
            columns = [description[0] for description in cursor.description]  # Get column names

            # Return the fetched data as a string (for simplicity)
            result = ""
            for row in rows:
                row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                result += f"ID: {row_data['id']}, Firstname: {row_data['firstname']}, Lastname: {row_data['lastname']}\n"
            
            return {'message': result}
        
        except sqlite3.Error as e:
            return {'message': f"Error: {e}"}
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    api = Api()
    
    # Get the path to the HTML file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(current_dir, 'index.html')

    # Create the window using the external HTML file
    window = webview.create_window('ECO ENEGERY', html_path, js_api=api)
    webview.start()
