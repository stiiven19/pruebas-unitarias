import sqlite3
import requests

# URLS de ejemplo (debes usar claves reales si la API lo requiere)
API_CLIMA = "https://api.openweathermap.org/data/2.5/weather"
API_GEO = "https://nominatim.openstreetmap.org/search"

# 🔹 Obtener datos de clima desde la API
def obtener_clima(ciudad):
    params = {"q": ciudad, "appid": "TU_API_KEY", "units": "metric", "lang": "es"}
    respuesta = requests.get(API_CLIMA, params=params)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return {
            "temperatura": datos["main"]["temp"],
            "descripcion": datos["weather"][0]["description"]
        }
    else:
        raise ValueError("Error al obtener datos del clima")

# 🔹 Obtener datos de geolocalización desde la API
def obtener_ubicacion(direccion):
    params = {"q": direccion, "format": "json"}
    respuesta = requests.get(API_GEO, params=params)
    if respuesta.status_code == 200 and respuesta.json():
        datos = respuesta.json()[0]
        return {"latitud": float(datos["lat"]), "longitud": float(datos["lon"])}
    else:
        raise ValueError("Error al obtener datos de ubicación")

# 🔹 Guardar datos en SQLite
def guardar_datos_en_bd(ciudad, direccion, latitud, longitud, temperatura, descripcion):
    conexion = sqlite3.connect("datos.db")
    cursor = conexion.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciudad TEXT,
            direccion TEXT,
            latitud REAL,
            longitud REAL,
            temperatura REAL,
            descripcion TEXT
        )
        """
    )
    cursor.execute(
        "INSERT INTO datos (ciudad, direccion, latitud, longitud, temperatura, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
        (ciudad, direccion, latitud, longitud, temperatura, descripcion),
    )
    conexion.commit()
    conexion.close()

# 🔹 Función principal que integra todo
def procesar_datos(ciudad, direccion):
    try:
        clima = obtener_clima(ciudad)
        ubicacion = obtener_ubicacion(direccion)
        guardar_datos_en_bd(ciudad, direccion, ubicacion["latitud"], ubicacion["longitud"], clima["temperatura"], clima["descripcion"])
        return "Datos guardados correctamente"
    except ValueError as e:
        return str(e)

# 🔹 Prueba rápida
if __name__ == "__main__":
    print(procesar_datos("Bogotá", "Plaza de Bolívar"))
