from flask import Flask
from app.routes import identify_blueprint  # ✅ Make sure this import is working
from app.database import init_db

app = Flask(__name__)

init_db(app)  # ✅ Pass the app to init DB

app.register_blueprint(identify_blueprint)  # ✅ Register the blueprint

if __name__ == "__main__":
    app.run(debug=True)
