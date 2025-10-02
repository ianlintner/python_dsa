## Brief overview
  Guidelines for managing the Flask development server in this project. These rules ensure smooth testing of navigation, filtering, and UI features by avoiding port conflicts and ensuring the correct environment is used.

## Development workflow
  - Always kill any existing process running on port 5000 before starting a new Flask server.
  - Use the command:  
    ```bash
    lsof -ti:5002 | xargs kill -9 && cd flask_app && python app.py --host=127.0.0.1 --port=5002
    ```
  - This ensures no stale processes interfere with the new server instance.

## Virtual environment usage
  - Always activate the local virtual environment before running the Flask app to ensure dependencies are correctly loaded.
  - Example:  
    ```bash
    source .venv/bin/activate
    ```
  - This avoids issues with missing or mismatched dependencies.

## Testing guidelines
  - After starting the server, verify navigation and filtering in the browser at `http://127.0.0.1:5000`.
  - Ensure that **All Content**, **Algorithms**, **LeetCode Problems**, and **Visualizations** tabs display the correct cards.
  - Confirm that the **category filter dropdown** works in combination with the view tabs.

## Other guidelines
  - Keep the server running in debug mode for development, but remember this is not suitable for production.
  - If Tailwind warnings appear in the console, they can be ignored for development but should be addressed before production deployment.
