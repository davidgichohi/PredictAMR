from flask import Flask
import dash
import os
from dashboard import create_dashboard, register_callbacks

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]

)
app.title = "PredictAMR Dashboard"

# Set layout and register callbacks
app.layout = create_dashboard(app)
register_callbacks(app)

# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

