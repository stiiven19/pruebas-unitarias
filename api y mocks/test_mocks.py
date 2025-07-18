class ClienteRepository:
    """
    Repositorio de clientes que maneja la persistencia de datos
    """
    def __init__(self):
        self.clientes = {}

    def obtener_cliente_por_id(self, cliente_id):
        """
        Obtiene un cliente por su ID
        
        Args:
            cliente_id (int): ID del cliente
            
        Returns:
            dict: Datos del cliente o None si no existe
        """
        return self.clientes.get(cliente_id)

    def agregar_cliente(self, cliente_id, cliente):
        """
        Agrega un cliente al repositorio
        
        Args:
            cliente_id (int): ID del cliente
            cliente (dict): Datos del cliente
        """
        self.clientes[cliente_id] = cliente

def calcular_total(items):
    """
    Calcula el total de una lista de items
    Args:
        items: Lista de diccionarios con 'precio' y 'cantidad'
    Returns:
        float: Total redondeado a 2 decimales
    """
    if not isinstance(items, list):
        raise ValueError("La orden debe ser una lista de items.")
    
    total = 0
    for item in items:
        if 'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada item debe tener 'precio' y 'cantidad'.")
        total += item['precio'] * item['cantidad']
        
    return round(total, 2)

def crear_orden(cliente_id, items, repo):
    """
    Crea una orden para un cliente
    Args:
        cliente_id: ID del cliente
        items: Lista de items
        repo: Repositorio de clientes
    Returns:
        dict: Orden creada
    Raises:
        ValueError: Si el cliente no existe o está inactivo
    """
    cliente = repo.obtener_cliente_por_id(cliente_id)
    if cliente is None:
        raise ValueError("Cliente no encontrado")
    if not cliente.get("activo", False):
        raise ValueError("Cliente inactivo.")
    
    total = calcular_total(items)
    
    orden = {
        "id": cliente_id,
        "total": total
    }
    return orden

import unittest

class TestOrden(unittest.TestCase):
    def setUp(self):
        self.repo = ClienteRepository()
        self.cliente_activo = {
            "id": 1,
            "nombre": "Juan",
            "activo": True
        }
        self.cliente_inactivo = {
            "id": 2,
            "nombre": "Maria",
            "activo": False
        }
        self.repo.agregar_cliente(1, self.cliente_activo)
        self.repo.agregar_cliente(2, self.cliente_inactivo)

    def test_calcular_total_exitoso(self):
        """Test para calcular total exitoso"""
        items = [
            {"precio": 100.0, "cantidad": 2},
            {"precio": 50.0, "cantidad": 3}
        ]
        resultado = calcular_total(items)
        self.assertEqual(resultado, 350.0)

    def test_calcular_total_item_invalido(self):
        """Test para cuando un item tiene formato inválido"""
        items = [
            {"precio": 100.0, "cantidad": 2},
            {"precio": 50.0}  # Falta cantidad
        ]
        with self.assertRaises(ValueError):
            calcular_total(items)

    def test_calcular_total_no_lista(self):
        """Test para cuando se pasa un objeto no lista"""
        items = "no soy una lista"
        with self.assertRaises(ValueError):
            calcular_total(items)

    def test_crear_orden_exitoso(self):
        """Test para crear orden exitosa"""
        items = [
            {"precio": 100.0, "cantidad": 2},
            {"precio": 50.0, "cantidad": 3}
        ]
        orden = crear_orden(1, items, self.repo)
        self.assertEqual(orden["id"], 1)
        self.assertEqual(orden["total"], 350.0)

    def test_crear_orden_cliente_no_existe(self):
        """Test para cuando el cliente no existe"""
        items = [{"precio": 100.0, "cantidad": 2}]
        with self.assertRaises(ValueError):
            crear_orden(999, items, self.repo)

    def test_crear_orden_cliente_inactivo(self):
        """Test para cuando el cliente está inactivo"""
        items = [{"precio": 100.0, "cantidad": 2}]
        with self.assertRaises(ValueError):
            crear_orden(2, items, self.repo)

    def test_crear_orden_item_invalido(self):
        """Test para cuando hay un item inválido en la orden"""
        items = [
            {"precio": 100.0, "cantidad": 2},
            {"precio": 50.0}  # Falta cantidad
        ]
        with self.assertRaises(ValueError):
            crear_orden(1, items, self.repo)

if __name__ == "__main__":
    unittest.main()