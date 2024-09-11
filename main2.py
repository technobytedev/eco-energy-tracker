import random
import sys
import threading
import time

import webview
import os
import mysql.connector
from mysql.connector import Error

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
<link href="assets/bootstrap.min.css" rel="stylesheet" >

<style>
    #response-container {
        display: none;
        padding: 1rem;
        margin: 3rem 5%;
        font-size: 120%;
        border: 5px dashed #ccc;
        word-wrap: break-word;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }

</style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Pricing</a>
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
      </div>
    </nav>

<h1>JS API Example</h1>
<p id='pywebview-status'><i>pywebview</i> is not ready</p>

<button onClick="showData()">Show Data</button><br/>

<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> is ready'
    })

    function showData() {
        pywebview.api.fetch_data().then(showResponse)
    }

</script>
<script src="assets/bootstrap.min.js"></script>
</body>
</html>
"""

class Api:

    def error(self):
        raise Exception('This is a Python exception')

    def fetch_data(self):

        try:
            connection = mysql.connector.connect(
                host='localhost',  # Your MySQL host
                database='jocos_payroll',  # Your MySQL database
                user='jocos_payroll_user',  # Your MySQL username
                password='cedrickarldb',  # Your MySQL password
                port=3308  # Your MySQL port (default is 3306)
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
                
                response = {'message': format(result)}
                return response
        
        except Error as e:
            return f"Error: {e}"

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == '__main__':
    api = Api()
    window = webview.create_window('JS API example', html=html, js_api=api)

    webview.start()