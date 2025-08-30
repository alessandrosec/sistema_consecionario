from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # Crear instancia de la aplicación
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

# Importar modelos para que Flask-Migrate los detecte
from app import models