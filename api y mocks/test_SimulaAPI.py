import unittest
from unittest.mock import patch, MagicMock
import requests

def get_data_from_api(url):
    """
    Obtiene datos de una API externa
    
    Args:
        url (str): URL de la API a consultar
        
    Returns:
        dict: Datos en formato JSON
        
    Raises:
        requests.exceptions.Timeout: Si hay timeout en la conexión
        requests.exceptions.ConnectionError: Si hay error de conexión
        ValueError: Si la respuesta no es JSON válido
    """
    response = requests.get(url)
    return response.json()

class TestAPI(unittest.TestCase):
    @patch('requests.get')
    def test_get_data_from_api_exitoso(self, mock_get):
        """Test para cuando la API responde exitosamente"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'key': 'value',
            'timestamp': '2023-07-18T21:54:09Z'
        }
        mock_get.return_value = mock_response

        url = "https://api.example.com/data"
        resultado = get_data_from_api(url)

        self.assertEqual(resultado['key'], 'value')
        self.assertIn('timestamp', resultado)
        mock_get.assert_called_once_with(url)

    @patch('requests.get')
    def test_get_data_from_api_error_404(self, mock_get):
        """Test para cuando la API devuelve 404"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            'error': 'Not Found',
            'message': 'Resource not found'
        }
        mock_get.return_value = mock_response

        url = "https://api.example.com/no-existe"
        with self.assertRaises(Exception) as context:
            get_data_from_api(url)

        self.assertTrue('404' in str(context.exception))
        mock_get.assert_called_once_with(url)

    @patch('requests.get')
    def test_get_data_from_api_timeout(self, mock_get):
        """Test para cuando hay timeout en la conexión"""
        mock_get.side_effect = requests.exceptions.Timeout

        url = "https://api.example.com/slow"
        with self.assertRaises(requests.exceptions.Timeout):
            get_data_from_api(url)

        mock_get.assert_called_once_with(url)

    @patch('requests.get')
    def test_get_data_from_api_conexion_fallida(self, mock_get):
        """Test para cuando hay error de conexión"""
        mock_get.side_effect = requests.exceptions.ConnectionError

        url = "https://api.example.com/error"
        with self.assertRaises(requests.exceptions.ConnectionError):
            get_data_from_api(url)

        mock_get.assert_called_once_with(url)

    @patch('requests.get')
    def test_get_data_from_api_respuesta_invalida(self, mock_get):
        """Test para cuando la respuesta no es JSON válido"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError  # Simulamos JSON inválido
        mock_get.return_value = mock_response

        url = "https://api.example.com/invalid"
        with self.assertRaises(ValueError):
            get_data_from_api(url)

        mock_get.assert_called_once_with(url)

if __name__ == "__main__":
    unittest.main()
