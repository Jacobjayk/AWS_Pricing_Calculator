from flask import Flask
from app.routes.calculator_routes import calculator_bp
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(calculator_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 