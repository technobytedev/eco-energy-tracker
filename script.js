        window.addEventListener('pywebviewready', async function() {
            try {
                const data = await pywebview.api.backend;  // Fetch the 'db_data' from Python
                document.getElementById('dbData').innerText = data;
            } catch (error) {
                console.error("Error fetching data from PyWebView API:", error);
            }
        });