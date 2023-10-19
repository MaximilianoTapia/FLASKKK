from flask_app.config.mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        nuevoId = connectToMySQL('esquema_citas').query_db(query, data)
        return nuevoId

    @staticmethod
    def valida_usuario(user):

        es_valido = True

        if len(user['first_name']) < 3:
            flash('Nombre debe de tener al menos 3 caracteres', 'registro')
            es_valido = False

        if len(user['last_name']) < 3:
            flash('Apellido debe de tener al menos 3 caracteres', 'registro')
            es_valido = False

        if not EMAIL_REGEX.match(user['email']):
            flash('E-mail inválido', 'registro')
            es_valido = False
        if len(user['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False
        if user['password'] != user['confirm']:
            flash('Contraseñas no coinciden', 'registro')
            es_valido = False
        
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_citas').query_db(query, user)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False

        return es_valido

    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_citas').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_citas').query_db(query, data)
        if len(result) < 1:
            return False
        else :
            usr = result[0]
            user = cls(usr)
            return user
