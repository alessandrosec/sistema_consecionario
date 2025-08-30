CREATE DATABASE sistema_consecionario;

use sistema_consecionario;
 
-- Crear tabla de vehículos
CREATE TABLE vehiculos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    marca NVARCHAR(50) NOT NULL,
    modelo NVARCHAR(50) NOT NULL,
    anio INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    disponibilidad BIT DEFAULT 1
);

-- Crear tabla de clientes
CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    num_identificacion NVARCHAR(20) NOT NULL UNIQUE,
    correo NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(20) NOT NULL
);

-- Crear tabla de ventas
CREATE TABLE ventas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    cliente_id INT NOT NULL,
    fecha_venta DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_ventas_vehiculos FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
    CONSTRAINT FK_ventas_clientes FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);