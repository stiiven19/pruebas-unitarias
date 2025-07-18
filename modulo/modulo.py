import pytest
def es_par(numero):
    """Retorna True si el numero es pas, False si es impar"""
    return numero % 2 == 0

def es_primo(numero):
    """Verifica si un número es primo."""
    if numero < 2:
        return False
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            return False
    return True

def calcular_total(items):
    
    if not isinstance(items,list):
        raise ValueError("La orden debe ser una lista de items.")
    
    total = 0
    for item in items:
        if'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada item debe tener 'precio', 'cantidad'.")
        if not isinstance(item['precio'],(int,float)) or item['precio'] < 0:
            raise ValueError("El precio debe ser un numero positivo")
        if not isinstance(item['cantidad'],int) or item['cantidad'] <= 0:
            raise ValueError("La cantidad debe ser un entero mayor a cero")
        
        total+=item['precio']* item['cantidad']
        
    return round(total,2)

def tasas_iva(items, pais="Colombia", exento=False, vip=False):
    tasas_iva = {
        "Colombia": 0.19,
        "Mexico": 0.16
    }
    if not isinstance(items, list):
        raise ValueError("La orden debe ser una lista de items.")
    
    subtotal = 0
    for item in items:
        if 'precio' not in item or 'cantidad' not in item:
            raise ValueError("Cada item debe tener 'precio' y 'cantidad'")
        subtotal += item['precio'] * item['cantidad']
    
    if exento:
        iva = 0
    else:
        iva = subtotal * tasas_iva.get(pais, 0)
    
    total = subtotal + iva
    
    if subtotal > 100000:
        total *= 0.9  # 10% de descuento
    
    if vip:
        total *= 0.85  # 15% de descuento adicional para clientes VIP
    
    return round(total, 2)