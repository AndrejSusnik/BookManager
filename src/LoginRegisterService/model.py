import marshmallow as ma
from config_managment import CustomConfigManager
from typing import Optional
import psycopg2 as ps
import logging
import time
import bcrypt

class EtcdDemoSchema(ma.Schema):
    path = ma.fields.String()
    value = ma.fields.String()

class EtcdQuerySchema(ma.Schema):
    path = ma.fields.String()

class ConfigQuerySchema(ma.Schema):
    key = ma.fields.String()

class ConfigDemoSchema(ma.Schema):
    key = ma.fields.String()
    value = ma.fields.String()
    
class UserSchema(ma.Schema):
    id = ma.fields.Integer()
    username = ma.fields.String()
    email = ma.fields.String()

class UserLoginSchema(ma.Schema):
    username = ma.fields.String()
    password = ma.fields.String()

class UserRegisterSchema(ma.Schema):
    username = ma.fields.String()
    password = ma.fields.String()
    email = ma.fields.String()

class UserUpdateSchema(ma.Schema):
    id = ma.fields.Integer()
    username = ma.fields.String()
    password = ma.fields.String()
    email = ma.fields.String()

class UserQuerySchema(ma.Schema):
    id = ma.fields.Integer()

class HealthSchema(ma.Schema):
    status = ma.fields.String()
    checks = ma.fields.List(ma.fields.Nested(lambda: SreviceHealthSchema()))

class SreviceHealthSchema(ma.Schema):
    name = ma.fields.String()
    status = ma.fields.String()
    data = ma.fields.Dict(keys=ma.fields.String(), values=ma.fields.String())

class UserNotFound(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class IncorrectUsernameOrPassword(Exception):
    pass

class CouldNotConnectToDatabase(Exception):
    pass

class _User:
    def __init__(self, config_manager: CustomConfigManager):
        self.host = config_manager.get("DB_URL", default="localhost")
        self.db_name = config_manager.get("DB_NAME", default="postgres")
        self.username = config_manager.get("DB_USER", default="postgres")
        self.password = config_manager.get("DB_PASSWORD", default="postgres")

        self.db_max_connection_attempts = config_manager.get("DB_MAX_CONNECTION_ATTEMPTS", default=5)
        self.db_connection_attempt_delay = config_manager.get("DB_CONNECTION_ATTEMPT_DELAY", default=1)

        self.has_error = False
        self.has_etcd_error = config_manager.has_etcd_error
        self.connection: Optional[ps.connection] = None

        self.writes = 0
        self.cursors = 0
        self.reads = 0

        self.try_reconnect()

    def login(self, user: UserLoginSchema) -> UserSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()
        self.cursors += 1
        cursor.execute("SELECT id, name, email, password FROM users WHERE name = %s", (user.username,))
        result = cursor.fetchone()
        cursor.close()
        self.cursors -= 1
        self.reads += 1

        if result is None:
            raise UserNotFound()

        if not bcrypt.checkpw(user.password.encode('utf-8'), result[3].encode('utf-8')):
            print(user.password.encode('utf-8'))
            raise IncorrectUsernameOrPassword()

        return (result[0], result[1], result[2])

    def get_all(self):
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()
        self.cursors += 1
        cursor.execute("SELECT id, name, email FROM users")
        self.reads += 1
        result = cursor.fetchall()
        cursor.close()
        self.cursors -= 1
        return result

    def get_by_id(self, user_id: int) -> UserSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()
        self.cursors += 1
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        self.reads += 1
        result = cursor.fetchone()
        cursor.close()
        self.cursors -= 1

        if result is None:
            raise UserNotFound()

        return result

    def add(self, user: UserUpdateSchema) -> UserSchema:
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()
        self.cursors += 1
        cursor.execute("SELECT id, name, email FROM users WHERE name = %s", (user.username,))
        self.reads += 1
        result = cursor.fetchone()

        if result is not None:
            raise UserAlreadyExists()

        cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s) RETURNING id", (user.username, bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(12)).decode(), user.email))
        self.writes += 1
        result = cursor.fetchone()
        self.connection.commit()

        user_id = result[0]

        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        self.reads += 1
        result = cursor.fetchone()

        cursor.close()
        self.cursors -= 1

        return result


    def update(self, user: UserUpdateSchema):
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (user.id,))
        self.reads += 1
        result = cursor.fetchone()
        if result is None:
            raise UserNotFound()

        cursor.execute("UPDATE users SET name = %s, password = %s, email = %s WHERE id = %s", (user.username, bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(12)).decode(), user.email, user.id))
        self.writes += 1
        self.connection.commit()
        cursor.close()

        return (user.id, user.username, user.email)

    def delete(self, user_id):
        if self.has_error:
            raise CouldNotConnectToDatabase()

        cursor = self.connection.cursor()

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        self.reads += 1
        result = cursor.fetchone()
        if result is None:
            raise UserNotFound()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.writes += 1
        self.connection.commit()
        cursor.close()

    def try_reconnect(self) -> bool:
        max_connection_attempts = self.db_max_connection_attempts
        while max_connection_attempts > 0:
            try:
                logging.info("Connecting to database %s on %s as %s", self.db_name, self.host, self.username)
                self.connection = ps.connect(host=self.host, database=self.db_name, user=self.username, password=self.password)

                return True
            except Exception as e:
                logging.error("Error while connecting to database: %s", str(e))
                max_connection_attempts -= 1
                if max_connection_attempts == 0:
                    self.has_error = True
                time.sleep(self.db_connection_attempt_delay)
        return False




UserDb = _User(CustomConfigManager())
