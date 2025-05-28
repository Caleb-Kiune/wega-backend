from flask import Flask
from models.user import db
from routes.user_routes import user_bp
from flask_migrate import Migrate

def create_app():
    """
    Create and configure the Flask application
    """
    app = Flask(__name__)
    
    # Configure SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 