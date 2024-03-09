import mysql.connector

class ConexionSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # Inicializar la conexión a la base de datos
            cls._instance.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="micro_x"
            )
        return cls._instance
