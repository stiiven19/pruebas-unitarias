class UsuarioRepository:
    def __init__(self, db):
        self.db = db  # La base de datos es un objeto simulado

    def crear_usuario(self, usuario):
        return self.db.insertar(usuario)

    def obtener_usuario_por_id(self, usuario_id):
        return self.db.consultar(usuario_id)

    def actualizar_usuario(self, usuario_id, datos):
        return self.db.actualizar(usuario_id, datos)

    def eliminar_usuario(self, usuario_id):
        return self.db.eliminar(usuario_id)
