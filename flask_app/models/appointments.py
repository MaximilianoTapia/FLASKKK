from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Appointment:

    def __init__(self, data):
        self.id = data ['id']
        self.name = data ['name']
        self.status = data ['status']
        self.user_id = data ['user_id']
        self.date_made = data ['date_made']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO appointments (name, status, date_made, user_id) VALUES (%(name)s, %(status)s, %(date_made)s, %(user_id)s);"
        nuevoId = connectToMySQL('esquema_citas').query_db(query, data)
        return nuevoId

    @staticmethod
    def valida_appointment(formulario):
# falta
        es_valido = True

        if len(formulario['name']) < 3:
            flash("El nombre de la cita debe tener al menos 3 caracteres", "cita")
            es_valido = False
        
        if formulario['date_made'] == "":
            flash("Ingrese una fecha", "cita")
            es_valido = False
        
        return es_valido
#
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM appointments"
        results = connectToMySQL('esquema_citas').query_db(query)
        appointments = []
        for appointment in results:
            appointments.append(cls(appointment))

        return appointments

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('esquema_citas').query_db(query, data)
        cita = cls(result[0])

        return cita

    @classmethod
    def update(cls, data):
        query = "UPDATE appointments SET name = %(name)s, status = %(status)s, date_made = %(date_made)s WHERE (id = %(id)s);"
        result = connectToMySQL('esquema_citas').query_db(query, data)

        return result
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        
        return connectToMySQL('esquema_citas').query_db(query, data)

