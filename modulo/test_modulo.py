from modulo import *
import pytest
from unittest.mock import MagicMock

#importamos la funcion a probar

def test_es_par():
    # Arrange
    numero1 = 4
    numero2 = 7
    
    # Act
    resultado1 = es_par(numero1)
    resultado2 = es_par(numero2)
    
    # Assert
    assert resultado1 is True
    assert resultado2 is False
    
def test_es_primo():
    # Arrange
    numero1 = 3
    numero2 = 5
    
    # Act
    resultado1 = es_primo(numero1)
    resultado2 = es_primo(numero2)
    
    # Assert
    assert resultado1 is True
    assert resultado2 is True
    
    
def test_error_precio_negativo():
    items = [{'precio': -10, 'cantidad': 2}]
    with pytest.raises(ValueError, match="El precio debe ser un numero positivo"):
        calcular_total(items)

def test_calcular_total_valido():
    items = [{'precio': 10.5, 'cantidad': 2}, {'precio': 5, 'cantidad': 3}]
    assert calcular_total(items) == 36.0

def test_calcular_total_un_item():
    items = [{'precio': 20, 'cantidad': 1}]
    assert calcular_total(items) == 20.0

def test_calcular_total_sin_items():
    items = []
    assert calcular_total(items) == 0.0

def test_calcular_total_decimales():
    items = [{'precio': 3.333, 'cantidad': 3}]
    assert calcular_total(items) == round(9.999, 2)

def test_calcular_total_cantidad_invalida():
    items = [{'precio': 10, 'cantidad': 0}]
    with pytest.raises(ValueError, match="La cantidad debe ser un entero mayor a cero"):
        calcular_total(items)


def test_error_precio_negativo_iva():
    with pytest.raises(ValueError, match="Cada item debe tener 'precio' y 'cantidad'"):
        tasas_iva([{"precio": -100, "cantidad": 2}])

def test_error_cantidad_invalida_iva():
    with pytest.raises(ValueError, match="Cada item debe tener 'precio' y 'cantidad'"):
        tasas_iva([{"precio": 1000, "cantidad": 0}])

def test_cliente_exento_iva():
    items = [{'precio': 100, 'cantidad': 2}]
    assert tasas_iva(items, "Colombia", exento=True) == 200.0

def test_descuento_por_monto_alto():
    items = [{'precio': 50000, 'cantidad': 3}]
    assert tasas_iva(items, "Mexico") == 156600.0  # 150000 - 10%

def test_cliente_vip_descuento_adicional():
    items = [{'precio': 50000, 'cantidad': 3}]
    assert tasas_iva(items, "Mexico", vip=True) == 133110.0  # 150000 - 10% - 15%
    

def test_crear_orden_exitosa():
    items = [{"precio":1000,"cantidad":2}]
#    resultado
def test_cliente_inexistente():
    repo_mock = MagicMock()
    repo_mock.obtener_cliente_por_id.return_value = None
    items = [{'precio': 500, 'cantidad': 1}]
    
 #   with pytest.raises(ValueError, match="Cliente")
#def test_cliente_inactivo()



    

