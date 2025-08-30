import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://aless:aless@Alessandro\SQLEXPRESS/sistema_consecionario?driver=SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False