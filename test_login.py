import mysql.connector
import unittest

def login(conn, username, password):
    cursor = conn.cursor()

    query = "SELECT * FROM usuarios WHERE usuario = %s AND contraseña = %s"
    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()

    return user is not None

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="micro_x" 
        )

    def tearDown(self):
        self.conn.close() #Cierre de conexión

    def test_login_correcto(self):
        # Aquí se ingresa el usaurio y contraseña correctos, en caso de que sean incorrectos la prueba no pasa
        self.assertTrue(login(self.conn, "tao", "123"))

    def test_login_incorrecto(self):
        # Por otro lado, aquí se hace el test de inicio de sesión incorrecto, En caso de ingresar los datos correctos no se pasa la prueba xD
        self.assertFalse(login(self.conn, "Furina", "contraseña_incorrecta"))

if __name__ == '__main__':
    unittest.main()
