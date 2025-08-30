from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, Length

class VehiculoForm(FlaskForm):
    marca = StringField('Marca', validators=[DataRequired(), Length(max=50)])
    modelo = StringField('Modelo', validators=[DataRequired(), Length(max=50)])
    anio = IntegerField('Año', validators=[DataRequired(), NumberRange(min=1900, max=2100)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    disponibilidad = BooleanField('Disponible')
    submit = SubmitField('Guardar')

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    num_identificacion = StringField('Número de Identificación', validators=[DataRequired(), Length(max=20)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Guardar')

class VentaForm(FlaskForm):
    vehiculo_id = SelectField('Vehículo', coerce=int, validators=[DataRequired()])
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar Venta')
    
    def __init__(self, *args, **kwargs):
        super(VentaForm, self).__init__(*args, **kwargs)
        self.vehiculo_id.choices = []  # Se llenarán dinámicamente
        self.cliente_id.choices = []   # Se llenarán dinámicamente