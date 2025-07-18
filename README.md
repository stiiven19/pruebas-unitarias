# Proyectos de Pruebas Unitarias

Este repositorio contiene varios proyectos de pruebas unitarias en Python, cada uno enfocado en diferentes aspectos de la automatización de pruebas.

## Estructura del Proyecto

```
pruebas-unitarias/
├── api y mocks/
│   ├── test_SimulaAPI.py
│   └── test_mocks.py
├── modulo/
│   ├── modulo.py
│   └── test_modulo.py
├── sistema_usuarios/
│   ├── sistema_usuarios.py
│   └── test_sistema_usuarios.py
└── weather/
    ├── weather.py
    └── test_weather.py
```

## Requisitos

- Python 3.x
- pytest
- requests
- unittest.mock
- sqlite3

## Instalación

```cmd
# Instalar dependencias
pip install pytest requests

# Verificar instalación
pytest --version
```

# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest api\test_SimulaAPI.py
pytest api\test_mocks.py
pytest sistema_usuarios\test_sistema_usuarios.py

# Ejecutar con verbosidad
pytest -v

# Ejecutar con cobertura
pytest --cov=api --cov=sistema_usuarios

## Proyectos Incluidos

### 1. Sistema de Usuarios

- **Descripción**: Sistema completo de gestión de usuarios con autenticación
- **Características**:
  - Registro de usuarios
  - Inicio de sesión
  - Validación de emails con API externa
  - Sistema de logs
  - Manejo de estados de usuario
- **Tecnologías**: Python, SQLite, requests

### 2. Sistema de Mocks y APIs

- **Descripción**: Pruebas con mocks y simulación de APIs
- **Características**:
  - Simulación de llamadas a APIs
  - Manejo de diferentes estados de respuesta
  - Pruebas de errores de conexión
  - Validación de respuestas
- **Tecnologías**: Python, unittest.mock, requests

### 3. Sistema de Módulos

- **Descripción**: Pruebas básicas de funciones y módulos
- **Características**:
  - Validación de números
  - Cálculos y operaciones matemáticas
  - Manejo de errores
  - Pruebas de cobertura
- **Tecnologías**: Python, pytest

### 4. Sistema de Clima

- **Descripción**: Integración con servicios de clima
- **Características**:
  - Consulta de datos meteorológicos
  - Manejo de respuestas de API
  - Pruebas de integración
- **Tecnologías**: Python, requests

## Guía de Contribución

1. Clona el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT - consulta el archivo LICENSE para más detalles.

## Autores

- Stiiven19 - Desarrollador principal

## Acknowledgments

- Recursos de aprendizaje de Python y pruebas