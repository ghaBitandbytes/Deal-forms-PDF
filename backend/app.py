from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv
import os

load_dotenv()

# Import config
from config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()   # ← NEW

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- EMAIL CONFIGURATION ---
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = "syeda.ghazia@bitandbytes.net"
    app.config['MAIL_PASSWORD'] = "woolfcgnpvkcdtzm"  
    app.config['MAIL_DEFAULT_SENDER'] = ('DealForms PDF', "syeda.ghazia@bitandbytes.net")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)   # ← NEW

    # Register Blueprints
    from routes.loi_routes import loi_bp
    app.register_blueprint(loi_bp)

    from routes.cim_routes import cim_bp
    app.register_blueprint(cim_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/health')
    def health_check():
        return "Flask + PostgreSQL + SQLAlchemy + Migrations + Mail working fine!"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
