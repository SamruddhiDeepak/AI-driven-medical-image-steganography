from flask import Flask
from flask_cors import CORS
import backend1
import backend2
import backend3  # Import backend3

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register Blueprints from backend1, backend2, and backend3
app.register_blueprint(backend1.backend1, url_prefix='/backend1')
app.register_blueprint(backend2.backend2, url_prefix='/backend2')
app.register_blueprint(backend3.backend3, url_prefix='/backend3')  # Register backend3

if __name__ == "__main__":
    app.run(debug=True)
