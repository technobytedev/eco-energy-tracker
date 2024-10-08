import webview
import os
import sqlite3
import base64
import uuid

class Api:


    def delete_appliance_canvas(self, canvas_id):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
                
            # Insert the appliance and image path into the database
            query = "DELETE FROM canvas WHERE id = ?;"
            cursor.execute(query, (canvas_id,))
            connection.commit()  # Commit the transaction
                
            return {'message': 'Removed successfully.'}
            
        except sqlite3.Error as e:
            return {'error': 'Error occured please try again'}
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def update_appliance_canvas(self, simulation_id ,room_id, appliance_id, from_room, canvas_id):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
                
            # Insert the appliance and image path into the database
            query = "UPDATE canvas SET room_id = ? WHERE id = ?;"
            cursor.execute(query, (room_id, canvas_id))
            connection.commit()  # Commit the transaction
                
            return {'message': 'Transfered successfully.'}
            
        except sqlite3.Error as e:
            return {'error': 'Error occured please try again'}
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()



    def add_appliance_canvas(self, simulation_id ,room_id, appliance_id):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
                
            # Insert the appliance and image path into the database
            query = "INSERT INTO canvas(simulation_id, room_id, appliance_id) VALUES(?, ?, ?);"
            cursor.execute(query, (simulation_id, room_id, appliance_id))
            connection.commit()  # Commit the transaction
                
            return {'message': 'Appliance added to room.'}
            
        except sqlite3.Error as e:
            return {'error': 'Error occured please try again'}
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def create_room(self, room_name, simulation_id):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
                
            # Insert the appliance and image path into the database
            query = "INSERT INTO room(name, simulation_id) VALUES(?, ?);"
            cursor.execute(query, (room_name, simulation_id))
            connection.commit()  # Commit the transaction
                
            return {'message': 'Room created successfully.'}
            
        except sqlite3.Error as e:
            return {'error': 'Error occured please try again'}
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


    def create_simulation(self, name):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
                
            # Insert the appliance and image path into the database
            query = "INSERT INTO simulation(name) VALUES(?);"
            cursor.execute(query, (name,))
            connection.commit()  # Commit the transaction
            session_id = cursor.lastrowid
                
            return {'message': 'Simulation created successfully.', 'session_id': session_id}
            
        except sqlite3.Error as e:
            return {'error': 'Error occured please try again'}
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

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
                query = "INSERT INTO sub_appliance(appliance_id, image) VALUES(?, ?);"
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
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
            
            # Execute the query to get main appliance data
            appliance_query = "SELECT id, name, image FROM appliance;"
            cursor.execute(appliance_query)
            appliances = cursor.fetchall()
            appliance_columns = [description[0] for description in cursor.description]

            result = ""
            for appliance in appliances:
                appliance_data = {appliance_columns[i]: appliance[i] for i in range(len(appliance))}
                
                # Execute the query to get sub-appliance data for each appliance
                sub_appliance_query = """
                SELECT id, image
                FROM sub_appliance
                WHERE appliance_id = ?;
                """
                cursor.execute(sub_appliance_query, (appliance_data['id'],))
                sub_appliances = cursor.fetchall()
                sub_appliance_columns = [description[0] for description in cursor.description]

                # Generate the main image and dropdown structure
                result += f"""
                <div class="dropdown col-md-1 d-flex align-items-center">
                    <img draggable="false" data-is-update="0" id="s{appliance_data['id']}" data-bs-toggle="dropdown" aria-expanded="false" style="width:60px; height:60px; margin:15px;" src="assets/vectors/{appliance_data['image']}" />
                    <ul class="dropdown-menu" style="background:white" aria-labelledby="s{appliance_data['id']}">
                        <div class="d-flex p-4 text-center">
                """
                for sub_appliance in sub_appliances:
                    sub_appliance_data = {sub_appliance_columns[i]: sub_appliance[i] for i in range(len(sub_appliance))}
                    result += f"""
                            <div>
                                <img draggable="true" id="{sub_appliance_data['id']}" style="width:60px;margin:25px" src="assets/uploads/{sub_appliance_data['image']}"/>
                            </div>
                    """
                result += """
                        </div>
                    </ul>
                </div>
                """
            
            return {'message': result}
        
        except sqlite3.Error as e:
            return {'message': f"Error: {e}"}
        finally:
            cursor.close()
            connection.close()

    def navbar(self):

        # Connect to the SQLite database (it will create the file if it doesn't exist)
        connection = sqlite3.connect('ecoenergy.db')
        cursor = connection.cursor()
            
        # Execute the query
        cursor.execute("SELECT * FROM simulation;")
        rows = cursor.fetchall()  # Fetch all rows from the query result
        columns = [description[0] for description in cursor.description]  # Get column names

        # Return the fetched data as a string (for simplicity)

        r = ""

        simulations = ""

        for row in rows:
            row_data = {columns[i]: row[i] for i in range(len(row))}  # Create dict of column names and row values
            simulations += f"""
                         <li><p onclick="setID('{row_data['name']}', '{row_data['id']}');" class="text-white" >{row_data['name']}</p></li>
                        """
        r += """<div class="container-fluid">
            
            <div >
                <button class="navbar-toggler text-white" style="color:white" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon text-white" style="color:white"></span>
                </button>

            </div>
            
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav text-white">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="index.html">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="">Setting</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Recents
                        </a>
                        <ul class="dropdown-menu p-2 text-white" aria-labelledby="navbarDropdownMenuLink" style="background:#CE3A00">
                        """
        r +=   simulations

        r += """
                        </ul>
                    </li>
                </ul>
            </div>


            <div class="row">
            <div class="col-6">
            <button class="btn text-white" style="background:#CE3A00">Compute</button>
            </div>
            <div class="col-6">
            <div class="dropdown">
    
                    <button data-bs-toggle="dropdown" aria-expanded="false" class="btn text-white"><img style="width:25px" src="plus.png" class="fluid"></button>
                    <ul class="dropdown-menu" aria-labelledby="addRoom" style="background:#CE3A00">
                    <div class="p-2">
                        <input class="form-control" id="simulationName" placeholder="Simulation Label"  />
                        <input class="btn btn-light mt-2 form-control" type="submit" onclick="createSimulation()" value="+ Create" />
                    </div>
                    </ul>
             </div>
            </div>
            </div>
            
             <a class="navbar-brand text-white" href="index.html">Eco Energy Tracker</a>

        </div>"""


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

    def fetch_room(self, simulation_id):
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('ecoenergy.db')
            cursor = connection.cursor()
            
            # Query to fetch room and canvas details
            query = """SELECT room.id AS roomId, room.name AS roomName, sub_appliance.image AS applianceImage, 
            sub_appliance.id AS applianceImageId, simulation.*, canvas.id AS canvasRow
            FROM canvas 
            INNER JOIN room ON room.id = canvas.room_id
            INNER JOIN sub_appliance ON sub_appliance.id = canvas.appliance_id
            INNER JOIN simulation ON simulation.id = canvas.simulation_id 
            WHERE canvas.simulation_id = ?;"""
            cursor.execute(query, (simulation_id,))
            rows = cursor.fetchall()  # Fetch all rows from the query result

            columns = [description[0] for description in cursor.description]  # Get column names

            # Fetch all rooms
            query_rooms = """SELECT room.id AS roomId, room.name AS roomName FROM room
                             WHERE room.simulation_id = ?;"""
            cursor.execute(query_rooms, (simulation_id,))
            rooms = cursor.fetchall()

            # Group images by roomId
            grouped_data = {}
            for row in rows:
                row_data = {columns[i]: row[i] for i in range(len(row))}
                room_id = row_data['roomId']
                canvas_id = row_data['canvasRow']  # Fetch the canvas.id
                
                if room_id not in grouped_data:
                    grouped_data[room_id] = {
                        'roomName': row_data['roomName'],
                        'canvasRow': canvas_id,
                        'images': []
                    }
                # Append image, image_id, and canvas_id to the list of images
                grouped_data[room_id]['images'].append((row_data['applianceImage'], row_data['applianceImageId'], canvas_id))

            # Generate HTML
            result = ""
            for room in rooms:
                room_id = room[0]
                room_name = room[1]
                images_html = ""
                if room_id in grouped_data:
                    images_html = "".join(
                        f'<img draggable="true" data-is-update="1" data-canvas-id="{canvas_id}" data-custom-id="{room_id}" id="{image_id}" src="assets/uploads/{image}" style="width:60px; height:60px;" />' 
                        for image, image_id, canvas_id in grouped_data[room_id]['images']
                    )
                result += f"""<div class="col-3">
                                {room_name}
                                <div class="droptarget" id="{room_id}">
                                    {images_html}
                                </div>
                            </div>"""

            return {'message': result}
        
        except sqlite3.Error as e:
            return {'error': f"Error: {e}"}
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
