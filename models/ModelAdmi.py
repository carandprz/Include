#usuario , nombre_completo ,correo, contrasena
# models/ModelAdmi.py
from models.entities.Admi import Admi
import database as db

class ModelAdmi:
    @classmethod
    def login(cls, db_connection, user, password):
        try:
            cursor = db_connection.cursor()
            sql = "SELECT * FROM administradores WHERE usuario = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None:
                user_db = Admi(row[0],row[3],row[1])
                if user.password == user_db.password:
                    return user_db
                #if password == row[3]:  # Comparar la contraseña directamente
                #    return Admi(row[0], row[3], row[1])  # usuario, contrasena, nombre_completo
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(f'Error en la consulta: {str(ex)}')

    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.database.cursor()
            sql = "SELECT usuario, nombre_completo FROM administradores WHERE usuario = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                return Admi(row[0], None, row[1])  # usuario, contrasena (None), nombre_completo
            else:
                return None
        except Exception as ex:
            raise Exception(f'Error en la consulta: {str(ex)}')
