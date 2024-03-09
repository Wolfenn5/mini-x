import mysql.connector

def conectar():
    # Establecer conexión a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="log_micro_x"
    )
    return conexion

def insertar_registro_log(id_usuario, accion, detalle):
    try:
        # Conectar a la base de datos
        conexion = conectar()
        cursor = conexion.cursor()

        # Insertar registro en la tabla de log
        query = "INSERT INTO log_actividad (id_usuario, accion, detalle) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_usuario, accion, detalle))

        # Confirmar la transacción y cerrar la conexión
        conexion.commit()
        cursor.close()
        conexion.close()
    except mysql.connector.Error as error:
        print("Error al insertar registro en el log:", error)

# Código para crear la tabla de log_actividad si no existe
def crear_tabla_log():
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_actividad (
                id INT AUTO_INCREMENT PRIMARY KEY,
                accion VARCHAR(50),
                id_usuario INT,
                detalle TEXT,
                fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_usuario) REFERENCES micro_x.usuarios(id)
            );
        """)

        conexion.commit()
        cursor.close()
        conexion.close()
    except mysql.connector.Error as error:
        print("Error al crear tabla de log_actividad:", error)

# Ejecutar la función para crear la tabla de log si no existe
crear_tabla_log()
