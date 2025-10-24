from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

#.env must be loaded first (before importing config)
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize DB and migrations
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from routes.loi_routes import loi_bp
    app.register_blueprint(loi_bp)

    #from routes.cim_routes import cim_bp
    #app.register_blueprint(cim_bp)

    @app.route('/')
    def home():
        return render_template('index.html')
    
    # Health check route
    @app.route('/health')
    def health_check():
        return "Flask + PostgreSQL + SQLAlchemy + Migrations working fine!"

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
