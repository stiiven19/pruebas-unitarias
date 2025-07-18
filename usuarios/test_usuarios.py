import unittest
from unittest.mock import MagicMock
from Usuarios import UsuarioRepository  # Asegúrate de importar correctamente

class TestUsuarioRepository(unittest.TestCase):

    def setUp(self):
        self.mock_db = MagicMock()  # Creamos un mock de la base de datos
        self.repo = UsuarioRepository(self.mock_db)  # Pasamos el mock al repositorio

    def test_crear_usuario(self):
        usuario = {"id": 1, "nombre": "Juan"}
        self.mock_db.insertar.return_value = True  # Simulamos inserción exitosa

        resultado = self.repo.crear_usuario(usuario)

        self.mock_db.insertar.assert_called_once_with(usuario)  # Verificamos que se llamó correctamente
        self.assertTrue(resultado)

    def test_obtener_usuario_por_id(self):
        usuario = {"id": 1, "nombre": "Juan"}
        self.mock_db.consultar.return_value = usuario  # Simulamos respuesta de la DB

        resultado = self.repo.obtener_usuario_por_id(1)

        self.mock_db.consultar.assert_called_once_with(1)
        self.assertEqual(resultado, usuario)

    def test_actualizar_usuario(self):
        usuario_id = 1
        datos_actualizados = {"nombre": "Juan Pérez"}
        self.mock_db.actualizar.return_value = True  # Simulamos actualización exitosa

        resultado = self.repo.actualizar_usuario(usuario_id, datos_actualizados)

        self.mock_db.actualizar.assert_called_once_with(usuario_id, datos_actualizados)
        self.assertTrue(resultado)

    def test_eliminar_usuario(self):
        usuario_id = 1
        self.mock_db.eliminar.return_value = True  # Simulamos eliminación exitosa

        resultado = self.repo.eliminar_usuario(usuario_id)

        self.mock_db.eliminar.assert_called_once_with(usuario_id)
        self.assertTrue(resultado)

if __name__ == "__main__":
    unittest.main()
