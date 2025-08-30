from app import create_app, db
from app.models import Vehiculo, Cliente, Venta

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()
    print("Base de datos inicializada con éxito.")