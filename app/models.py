from datetime import datetime
from app import db

class Vehiculo(db.Model):
    __tablename__ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)  # 10 dígitos en total, 2 decimales
    disponibilidad = db.Column(db.Boolean, default=True)
    
    # Relación con ventas (un vehículo puede tener una venta)
    venta = db.relationship('Venta', backref='vehiculo', uselist=False)
    
    def __repr__(self):
        return f'<Vehiculo {self.marca} {self.modelo} ({self.anio})>'

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    num_identificacion = db.Column(db.String(20), nullable=False, unique=True)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    
    # Relación con ventas (un cliente puede tener múltiples ventas)
    ventas = db.relationship('Venta', backref='cliente')
    
    def __repr__(self):
        return f'<Cliente {self.nombre} ({self.num_identificacion})>'

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Venta #{self.id} - Vehículo: {self.vehiculo_id}, Cliente: {self.cliente_id}>'