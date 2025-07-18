import unittest
from unittest.mock import patch, MagicMock
from sistema_usuarios import SistemaUsuarios
import sqlite3
import hashlib

class TestSistemaUsuarios(unittest.TestCase):
    def setUp(self):
        # Usar base de datos en memoria para pruebas
        self.conexion = sqlite3.connect(":memory:")
        self.cursor = self.conexion.cursor()
        self.sistema = SistemaUsuarios(":memory:")
        self.sistema.conexion = self.conexion
        self.sistema.cursor = self.cursor
        self.sistema._crear_tabla_usuarios()
        self.sistema._crear_tabla_logs()
        self.conexion.commit()

    def tearDown(self):
        self.conexion.close()

    @patch("sistema_usuarios.requests.get")
    def test_registrar_usuario_exitoso(self, mock_get):
        """Test para registro exitoso de usuario"""
        # Configurar el mock de la API
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "valid"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Intentar registrar usuario
        resultado = self.sistema.registrar_usuario("Juan", "juan@email.com", "password123")
        self.assertTrue(resultado)

        # Verificar que el usuario se guardó correctamente
        self.cursor.execute("SELECT * FROM usuarios WHERE email = ?", ("juan@email.com",))
        usuario = self.cursor.fetchone()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario[1], "Juan")
        self.assertEqual(usuario[2], "juan@email.com")

        # Verificar que se registró en logs
        self.cursor.execute("SELECT * FROM logs WHERE email = ?", ("juan@email.com",))
        log = self.cursor.fetchone()
        self.assertIsNotNone(log)
        self.assertEqual(log[2], "registro")

    @patch("sistema_usuarios.requests.get")
    def test_registrar_usuario_email_invalido(self, mock_get):
        """Test para registro con email inválido"""
        # Configurar el mock de la API para retornar email inválido
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "invalid"}
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError) as context:
            self.sistema.registrar_usuario("Maria", "emailinvalido", "password123")
        self.assertTrue("Correo electrónico inválido" in str(context.exception))

    def test_iniciar_sesion_exitoso(self):
        """Test para inicio de sesión exitoso"""
        # Insertar usuario de prueba
        hashed_password = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute("""
            INSERT INTO usuarios (nombre, email, password) 
            VALUES (?, ?, ?)
        """, ("Ana", "ana@email.com", hashed_password))
        self.conexion.commit()

        # Intentar iniciar sesión
        resultado = self.sistema.iniciar_sesion("ana@email.com", "password123")
        self.assertTrue(resultado)

        # Verificar que se registró en logs
        self.cursor.execute("SELECT * FROM logs WHERE email = ?", ("ana@email.com",))
        log = self.cursor.fetchone()
        self.assertIsNotNone(log)
        self.assertEqual(log[2], "iniciar_sesion_exitoso")

    def test_iniciar_sesion_contraseña_incorrecta(self):
        """Test para inicio de sesión con contraseña incorrecta"""
        # Insertar usuario de prueba
        hashed_password = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute("""
            INSERT INTO usuarios (nombre, email, password) 
            VALUES (?, ?, ?)
        """, ("Ana", "ana@email.com", hashed_password))
        self.conexion.commit()

        # Intentar iniciar sesión con contraseña incorrecta
        resultado = self.sistema.iniciar_sesion("ana@email.com", "incorrecta")
        self.assertFalse(resultado)

        # Verificar que se registró en logs
        self.cursor.execute("SELECT * FROM logs WHERE email = ?", ("ana@email.com",))
        log = self.cursor.fetchone()
        self.assertIsNotNone(log)
        self.assertEqual(log[2], "iniciar_sesion_fallido")

    def test_iniciar_sesion_usuario_inexistente(self):
        """Test para inicio de sesión con usuario inexistente"""
        resultado = self.sistema.iniciar_sesion("noexiste@email.com", "password123")
        self.assertFalse(resultado)

    def test_iniciar_sesion_usuario_desactivado(self):
        """Test para inicio de sesión con usuario desactivado"""
        # Insertar usuario desactivado
        hashed_password = hashlib.sha256("password123".encode()).hexdigest()
        self.cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, estado) 
            VALUES (?, ?, ?, ?)
        """, ("Ana", "ana@email.com", hashed_password, 0))
        self.conexion.commit()

        resultado = self.sistema.iniciar_sesion("ana@email.com", "password123")
        self.assertFalse(resultado)

if __name__ == "__main__":
    unittest.main()
