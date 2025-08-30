from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Vehiculo, Cliente, Venta
from app.forms import VehiculoForm, ClienteForm, VentaForm
from datetime import datetime

# Crear el blueprint
main_bp = Blueprint('main', __name__)

# Ruta principal
@main_bp.route('/')
def index():
    vehiculos_count = Vehiculo.query.count()
    clientes_count = Cliente.query.count()
    ventas_count = Venta.query.count()
    return render_template('index.html', 
                          vehiculos_count=vehiculos_count,
                          clientes_count=clientes_count,
                          ventas_count=ventas_count)

# Rutas para vehículos
@main_bp.route('/vehiculos')
def lista_vehiculos():
    # Obtener parámetros de filtro
    marca = request.args.get('marca', '')
    modelo = request.args.get('modelo', '')
    anio = request.args.get('anio', '')
    
    # Construir consulta base
    query = Vehiculo.query
    
    # Aplicar filtros si están presentes
    if marca:
        query = query.filter(Vehiculo.marca.like(f'%{marca}%'))
    if modelo:
        query = query.filter(Vehiculo.modelo.like(f'%{modelo}%'))
    if anio and anio.isdigit():
        query = query.filter(Vehiculo.anio == int(anio))
    
    # Ejecutar consulta
    vehiculos = query.all()
    
    return render_template('vehiculos/lista.html', vehiculos=vehiculos)

@main_bp.route('/vehiculos/crear', methods=['GET', 'POST'])
def crear_vehiculo():
    form = VehiculoForm()
    
    if form.validate_on_submit():
        vehiculo = Vehiculo(
            marca=form.marca.data,
            modelo=form.modelo.data,
            anio=form.anio.data,
            precio=form.precio.data,
            disponibilidad=form.disponibilidad.data
        )
        
        db.session.add(vehiculo)
        db.session.commit()
        
        flash('Vehículo agregado exitosamente!', 'success')
        return redirect(url_for('main.lista_vehiculos'))
    
    return render_template('vehiculos/crear.html', form=form)

@main_bp.route('/vehiculos/editar/<int:id>', methods=['GET', 'POST'])
def editar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    form = VehiculoForm(obj=vehiculo)
    
    if form.validate_on_submit():
        vehiculo.marca = form.marca.data
        vehiculo.modelo = form.modelo.data
        vehiculo.anio = form.anio.data
        vehiculo.precio = form.precio.data
        vehiculo.disponibilidad = form.disponibilidad.data
        
        db.session.commit()
        
        flash('Vehículo actualizado exitosamente!', 'success')
        return redirect(url_for('main.lista_vehiculos'))
    
    return render_template('vehiculos/editar.html', form=form, vehiculo=vehiculo)

@main_bp.route('/vehiculos/eliminar/<int:id>')
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    
    # Validar que no tenga ventas asociadas
    if vehiculo.venta:
        flash('No se puede eliminar un vehículo que ya ha sido vendido!', 'error')
        return redirect(url_for('main.lista_vehiculos'))
    
    db.session.delete(vehiculo)
    db.session.commit()
    
    flash('Vehículo eliminado exitosamente!', 'success')
    return redirect(url_for('main.lista_vehiculos'))

# Rutas para clientes
@main_bp.route('/clientes')
def lista_clientes():
    # Obtener parámetros de filtro
    nombre = request.args.get('nombre', '')
    num_identificacion = request.args.get('num_identificacion', '')
    
    # Construir consulta base
    query = Cliente.query
    
    # Aplicar filtros si están presentes
    if nombre:
        query = query.filter(Cliente.nombre.like(f'%{nombre}%'))
    if num_identificacion:
        query = query.filter(Cliente.num_identificacion.like(f'%{num_identificacion}%'))
    
    # Ejecutar consulta
    clientes = query.all()
    
    # Crear un formulario para los filtros
    form = ClienteForm()
    
    return render_template('clientes/lista.html', clientes=clientes, form=form)


@main_bp.route('/clientes/crear', methods=['GET', 'POST'])
def crear_cliente():
    form = ClienteForm()
    
    if form.validate_on_submit():
        cliente = Cliente(
            nombre=form.nombre.data,
            num_identificacion=form.num_identificacion.data,
            correo=form.correo.data,
            telefono=form.telefono.data
        )
        
        db.session.add(cliente)
        try:
            db.session.commit()
            flash('Cliente agregado exitosamente!', 'success')
            return redirect(url_for('main.lista_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar cliente: {str(e)}', 'error')
    
    return render_template('clientes/crear.html', form=form)

@main_bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    
    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.num_identificacion = form.num_identificacion.data
        cliente.correo = form.correo.data
        cliente.telefono = form.telefono.data
        
        try:
            db.session.commit()
            flash('Cliente actualizado exitosamente!', 'success')
            return redirect(url_for('main.lista_clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'error')
    
    return render_template('clientes/editar.html', form=form, cliente=cliente)

@main_bp.route('/clientes/eliminar/<int:id>')
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    
    # Validar que no tenga ventas asociadas
    if cliente.ventas:
        flash('No se puede eliminar un cliente que tiene ventas registradas!', 'error')
        return redirect(url_for('main.lista_clientes'))
    
    db.session.delete(cliente)
    db.session.commit()
    
    flash('Cliente eliminado exitosamente!', 'success')
    return redirect(url_for('main.lista_clientes'))

# Rutas para ventas
@main_bp.route('/ventas')
def lista_ventas():
    ventas = Venta.query.order_by(Venta.fecha_venta.desc()).all()
    return render_template('ventas/lista.html', ventas=ventas)

@main_bp.route('/ventas/crear', methods=['GET', 'POST'])
def crear_venta():
    form = VentaForm()
    
    # Cargar vehículos disponibles
    vehiculos_disponibles = Vehiculo.query.filter_by(disponibilidad=True).all()
    form.vehiculo_id.choices = [(v.id, f"{v.marca} {v.modelo} ({v.anio})") for v in vehiculos_disponibles]
    
    # Cargar todos los clientes
    clientes = Cliente.query.all()
    form.cliente_id.choices = [(c.id, f"{c.nombre} ({c.num_identificacion})") for c in clientes]
    
    if form.validate_on_submit():
        vehiculo = Vehiculo.query.get(form.vehiculo_id.data)
        
        # Verificar nuevamente que el vehículo esté disponible
        if not vehiculo or not vehiculo.disponibilidad:
            flash('El vehículo seleccionado ya no está disponible', 'error')
            return redirect(url_for('main.crear_venta'))
        
        # Crear la venta
        venta = Venta(
            vehiculo_id=form.vehiculo_id.data,
            cliente_id=form.cliente_id.data,
            fecha_venta=datetime.utcnow()
        )
        
        # Marcar el vehículo como vendido
        vehiculo.disponibilidad = False
        
        db.session.add(venta)
        db.session.commit()
        
        flash('Venta registrada exitosamente!', 'success')
        return redirect(url_for('main.lista_ventas'))
    
    return render_template('ventas/crear.html', form=form)

@main_bp.route('/ventas/detalles/<int:id>')
def detalles_venta(id):
    venta = Venta.query.get_or_404(id)
    return render_template('ventas/detalles.html', venta=venta)

