# app.py
from flask import Flask, render_template, request
import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_12")

app = Flask(__name__)

# Configurar la cadena de conexión
user = 'x7944486'
password = 'x7944486'
host = 'oracle0.ugr.es'
port = '1521'
service_name = 'practbd.oracle0.ugr.es'

dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
connection = cx_Oracle.connect(user, password, dsn)

# Crear un cursor para ejecutar consultas
cursor = connection.cursor()

borrartablas = [
    "Cliente",
    "Empleado",
    "Asignado",
    "De",
    "Alerta",
    "Revision",
    "Solicita",
    "SistemaDeVigilancia",
    "Instalacion",
    "Proveedor"
]

# Borrar las tablas si existen
for tabla in borrartablas:
    cursor.execute(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {tabla} CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;")


# Lista de sentencias SQL
sentencias_sql = [
    """
    CREATE TABLE Cliente (
        DNI VARCHAR(10) PRIMARY KEY,
        Nombre VARCHAR(50),
        Apellidos VARCHAR(50),
        Telefono VARCHAR(15),
        Direccion VARCHAR(100),
        IDTecnico INT,
        UNIQUE (Nombre, Apellidos)
    )
    """,
    """
    CREATE TABLE Empleado (
        IDE INT PRIMARY KEY,
        Usuario VARCHAR(20),
        Contraseña VARCHAR(20),
        Nombre VARCHAR(50),
        Apellidos VARCHAR(50),
        Telefono VARCHAR(15),
        UNIQUE (Nombre, Apellidos)
    )
    """,
    """
    CREATE TABLE Asignado (
        DNI VARCHAR(10) PRIMARY KEY,
        IDTecnico INT,
        FOREIGN KEY (DNI) REFERENCES Cliente(DNI)
    )
    """,
    """
    CREATE TABLE De (
        DNI VARCHAR(10) PRIMARY KEY,
        Direccion VARCHAR(100),
        FOREIGN KEY (DNI) REFERENCES Cliente(DNI),
        FOREIGN KEY (Direccion) REFERENCES SistemaDeVigilancia(Direccion),
        UNIQUE (Direccion)
    )
    """,
    """
    CREATE TABLE Alerta (
        DNI VARCHAR(10) PRIMARY KEY,
        IDE INT,
        Fecha DATE,
        Estado VARCHAR(10) CHECK (Estado IN ('Confirmada', 'Rechazada')),
        FOREIGN KEY (DNI) REFERENCES Cliente(DNI),
        FOREIGN KEY (IDE) REFERENCES Empleado(IDE),
        UNIQUE (IDE)
    )
    """,
    """
    CREATE TABLE Revision (
        IDE INT PRIMARY KEY,
        Direccion VARCHAR(100),
        FOREIGN KEY (IDE) REFERENCES Empleado(IDE),
        FOREIGN KEY (Direccion) REFERENCES SistemaDeVigilancia(Direccion)
    )
    """,
    """
    CREATE TABLE Solicita (
        IDE INT PRIMARY KEY,
        Direccion VARCHAR(100),
        FOREIGN KEY (IDE) REFERENCES Empleado(IDE),
        FOREIGN KEY (Direccion) REFERENCES SistemaDeVigilancia(Direccion)
    )
    """,
    """
    CREATE TABLE SistemaDeVigilancia (
        Direccion VARCHAR(100) PRIMARY KEY
    )
    """,
    """
    CREATE TABLE Instalacion (
        Direccion VARCHAR(100) PRIMARY KEY,
        Estado VARCHAR(500),
        Componentes VARCHAR(500),
        FOREIGN KEY (Direccion) REFERENCES SistemaDeVigilancia(Direccion)
    )
    """,
    """
    CREATE TABLE Proveedor (
        Nombre VARCHAR(50) PRIMARY KEY,
        Direccion VARCHAR(100),
        Telefono VARCHAR(15),
        email VARCHAR(50)
    )
    """
]

# Imprimir cada sentencia SQL
for sentencia in sentencias_sql:
    cursor.execute(sentencia)


# Guardar los cambios
connection.commit()

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar las acciones
@app.route('/accion', methods=['POST'])
def accion():
    opcion = request.form['opcion']

    if opcion == 'añadir':
        return render_template('añadirUser.html')
    elif opcion == 'modificar':
        return render_template('editarUser.html')
    elif opcion == 'eliminar':
        return render_template('eliminarUser.html')
    elif opcion == 'consultar':
        # Ejemplo: Ejecutar una consulta SELECT
        query = 'SELECT * FROM tu_tabla'
        cursor.execute(query)
        data = cursor.fetchall()
        return render_template('consultarUser.html', data=data)
    else:
        return "Opción no válida"
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

