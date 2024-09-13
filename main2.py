import webview
import os
import mysql.connector
from mysql.connector import Error

class Api:
    def fetch_data(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jocos_payroll',
                user='jocos_payroll_user',
                password='cedrickarldb',
                port=3308  # Your MySQL port
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM users;")
                rows = cursor.fetchall()  # Fetch all rows from the query result
                columns = cursor.description  # Get column names

                # Extract column names
                column_names = [column[0] for column in columns]

                # Return the fetched data as a string (for simplicity)
                result = ""
                for row in rows:
                    row_data = {column_names[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                    result += f"ID: {row_data['id']}, Firstname: {row_data['firstname']}, Lastname: {row_data['lastname']}\n"
                
                return {'message': result}
        
        except Error as e:
            return {'message': f"Error: {e}"}
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def search_data(self, searchByName):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='jocos_payroll',
                user='jocos_payroll_user',
                password='cedrickarldb',
                port=3308  # Your MySQL port
            )
            
            if connection.is_connected():
                cursor = connection.cursor()

                # query to search name
                query = "SELECT * FROM users WHERE firstname LIKE %s;"
                search_pattern = f"%{searchByName}%"  # Add wildcard characters before and after the search term
                cursor.execute(query, (search_pattern,))

                rows = cursor.fetchall()  # Fetch all rows from the query result
                columns = cursor.description  # Get column names

                # Extract column names
                column_names = [column[0] for column in columns]

                # Return the fetched data as a string (for simplicity)
                result = ""
                for row in rows:
                    row_data = {column_names[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                    result += f"ID: {row_data['id']}, Firstname: {row_data['firstname']}, Lastname: {row_data['lastname']}\n"
                
                return {'message': result}
        
        except Error as e:
            return {'message': f"Error: {e}"}
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    api = Api()
    
    # Get the path to the HTML file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(current_dir, 'index.html')

    # Create the window using the external HTML file
    window = webview.create_window('JS API example', html_path, js_api=api)
    webview.start()
