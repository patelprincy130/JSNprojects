# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to My Financial Planner!"

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db' 
    db.init_app(app)

    from .routes import main_bp 
    app.register_blueprint(main_bp) 

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
