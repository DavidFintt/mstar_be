from flask_cors import CORS

def configure_cors(app, origins=None):
    if origins is None:
        origins = ["http://localhost:3000"]

    CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)