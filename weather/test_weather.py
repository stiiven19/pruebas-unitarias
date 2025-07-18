import unittest
from unittest.mock import patch, MagicMock
from weather import obtener_clima, obtener_ubicacion, guardar_datos_en_bd, procesar_datos

class TestAPIs(unittest.TestCase):

    @patch("weather.requests.get")
    def test_obtener_clima(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 22.5},
            "weather": [{"description": "cielo despejado"}],
        }
        mock_get.return_value = mock_response

        resultado = obtener_clima("Bogotá")
        self.assertEqual(resultado, {"temperatura": 22.5, "descripcion": "cielo despejado"})
        mock_get.assert_called_once()

    @patch("weather.requests.get")
    def test_obtener_ubicacion(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"lat": "4.6097", "lon": "-74.0817"}]
        mock_get.return_value = mock_response

        resultado = obtener_ubicacion("Plaza de Bolívar")
        self.assertEqual(resultado, {"latitud": 4.6097, "longitud": -74.0817})
        mock_get.assert_called_once()

class TestBaseDeDatos(unittest.TestCase):

    @patch("weather.sqlite3.connect")
    def test_guardar_datos_en_bd(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        guardar_datos_en_bd("Bogotá", "Plaza de Bolívar", 4.6097, -74.0817, 22.5, "cielo despejado")

        mock_connect.assert_called_once_with("datos.db")
        mock_cursor.execute.assert_called()  # Verifica que se ejecutaron consultas SQL
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
