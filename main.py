import webview
import os
import sqlite3
import base64
import uuid

class Api:

    def upload_image(self, base64_image, appliance):
            try:
                # Decode the base64 image
                image_data = base64.b64decode(base64_image)
                image_name = f"{str(uuid.uuid4())}.png"
                
                # Specify the upload folder path
                upload_folder = os.path.join(os.getcwd(), 'assets/uploads')
                
                # Create the folder if it doesn't exist
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                # Full file path for the image
                file_path = os.path.join(upload_folder, image_name)
                
                # Write the image to the folder
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                
                # Connect to the SQLite database
                connection = sqlite3.connect('ecoenergy.db')
                cursor = connection.cursor()
                
                # Insert the appliance and image path into the database
                query = "INSERT INTO appliance(name, image) VALUES(?, ?);"
                cursor.execute(query, (appliance, image_name))
                connection.commit()  # Commit the transaction
                
                return f'file://{file_path}'
            
            except sqlite3.Error as e:
                return f"Error: {e}"
            
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

    def appliance_list(self):
        r = '<img src="monitor.png" class="fluid" draggable="true" id="dragtarget">'
        # r = '<p draggable="true" id="dragtarget">Drag me!</p>'
        return {'message': r}

    def navbar(self):
        r = ''' <div class="container-fluid">
            
            <div>
                <button class="navbar-toggler text-white" style="color:white" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon text-white" style="color:white"></span>
            </button>
            <button class="btn btn-light">Compute</button>
            </div>
            <a class="navbar-brand text-white" href="index.html">EcoEnergy Tracker</a>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav text-white">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="settings.html">Setting</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Dropdown link
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                            <li><a class="dropdown-item" href="#">Action</a></li>
                            <li><a class="dropdown-item" href="#">Another action</a></li>
                            <li><a class="dropdown-item" href="#">Something else here</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>'''
        return {'message': r}


    def fetch_appliance(self):
        try:
            # Connect to the SQLite database (it will create the file if it doesn't exist)
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute("SELECT * FROM appliance;")
            rows = cursor.fetchall()  # Fetch all rows from the query result
            columns = [description[0] for description in cursor.description]  # Get column names

            # Return the fetched data as a string (for simplicity)
            result = ""
            for row in rows:
                row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                result += f"""<tr>
                                <td>{row_data['id']}</td>
                                <td>{row_data['name']}</td>
                                <td> <img src="assets/uploads/{row_data['image']}" style="width:60px" />  </td>
                            </tr>"""
      
            return {'message': result}
        
        except sqlite3.Error as e:
            return {'message': f"Error: {e}"}
        finally:
            cursor.close()
            connection.close()
    
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
                result += f"""<tr>
                                <td>{row_data['id']}</td>
                                <td>{row_data['firstname']}</td>
                                <td>{row_data['lastname']}</td>
                            </tr>"""
      
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
            result = ""
            if not rows:
                result += f"""<tr>
                                <td style="text-align:center" colspan="3">No data found</td>
                              </tr>"""
            else:
                # Return the fetched data as a string (for simplicity)
                for row in rows:
                    row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
                    result += f"""<tr>
                                    <td>{row_data['id']}</td>
                                    <td>{row_data['firstname']}</td>
                                    <td>{row_data['lastname']}</td>
                                </tr>"""
            
            return {'message': result}
        
        except sqlite3.Error as e:
            return {'message': f"Error: {e}"}
        finally:
            cursor.close()
            connection.close()

def on_loaded():
    window.toggle_fullscreen()


if __name__ == '__main__':
    api = Api()
    
    # Get the path to the HTML file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(current_dir, 'index.html')

    # Create the window using the external HTML file
    window = webview.create_window('ECO ENEGERY', html_path, js_api=api, width=1000, height=700,)
    webview.start()
