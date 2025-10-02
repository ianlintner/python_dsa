import os
from flask import Flask, send_from_directory

app = Flask(__name__)

# Path to built MkDocs site
DOCS_BUILD_DIR = os.path.join(os.path.dirname(__file__), "..", "site")

@app.route("/docs/")
@app.route("/docs/<path:filename>")
def serve_docs(filename="index.html"):
    """
    Serve the built MkDocs documentation from /docs/ route.
    """
    return send_from_directory(DOCS_BUILD_DIR, filename)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)
