import sqlite3
import requests
import hashlib
from datetime import datetime

API_VALIDAR_EMAIL = "https://api.eva.pingutil.com/email"

class SistemaUsuarios:
    def __init__(self, db_path="usuarios.db"):
        """Inicializa el sistema de usuarios con una conexión a la base de datos"""
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self._crear_tabla_usuarios()
        self._crear_tabla_logs()
        self.conexion.commit()

    def _crear_tabla_usuarios(self):
        """Crea la tabla de usuarios si no existe"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado BOOLEAN DEFAULT 1
            )
        """)

    def _crear_tabla_logs(self):
        """Crea la tabla de logs para auditoría"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                accion TEXT NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def _hash_password(self, password: str) -> str:
        """Hash de la contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _validar_email(self, email: str) -> bool:
        """Valida el formato del email"""
        if not email or "@" not in email:
            return False
        try:
            response = requests.get(f"{API_VALIDAR_EMAIL}?email={email}")
            response.raise_for_status()
            return response.json().get("status") == "valid"
        except:
            return False

    def registrar_usuario(self, nombre: str, email: str, password: str) -> bool:
        """
        Registra un nuevo usuario
        Args:
            nombre: Nombre del usuario
            email: Email del usuario
            password: Contraseña del usuario
        Returns:
            True si el registro es exitoso, False si hay un error
        """
        try:
            if not nombre or not email or not password:
                raise ValueError("Todos los campos son requeridos")
                
            if not self._validar_email(email):
                raise ValueError("Correo electrónico inválido")
                
            # Verificar si el usuario ya existe
            self.cursor.execute("SELECT id FROM usuarios WHERE email=?", (email,))
            if self.cursor.fetchone():
                raise ValueError("El email ya está registrado")
                
            # Hash de la contraseña
            hashed_password = self._hash_password(password)
            
            # Insertar usuario
            self.cursor.execute("""
                INSERT INTO usuarios (nombre, email, password) 
                VALUES (?, ?, ?)
            """, (nombre, email, hashed_password))
            
            # Registrar en logs
            self.cursor.execute("""
                INSERT INTO logs (email, accion) 
                VALUES (?, ?)
            """, (email, "registro"))
            
            self.conexion.commit()
            return True
            
        except Exception as e:
            self.conexion.rollback()
            raise ValueError(f"Error al registrar usuario: {str(e)}")

    def iniciar_sesion(self, email: str, password: str) -> bool:
        """
        Inicia sesión de un usuario
        Args:
            email: Email del usuario
            password: Contraseña del usuario
        Returns:
            True si el inicio de sesión es exitoso, False si falla
        """
        try:
            if not email or not password:
                return False
                
            # Hash de la contraseña
            hashed_password = self._hash_password(password)
            
            self.cursor.execute("""
                SELECT id FROM usuarios 
                WHERE email=? AND password=? AND estado=1
            """, (email, hashed_password))
            
            usuario = self.cursor.fetchone()
            
            # Registrar en logs
            accion = "iniciar_sesion_exitoso" if usuario else "iniciar_sesion_fallido"
            self.cursor.execute("""
                INSERT INTO logs (email, accion) 
                VALUES (?, ?)
            """, (email, accion))
            
            self.conexion.commit()
            return usuario is not None
            
        except Exception as e:
            self.conexion.rollback()
            return False

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        if self.conexion:
            self.conexion.close()
