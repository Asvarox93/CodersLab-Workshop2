from password import hash_password
import datetime

class User:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    
    def safe_to_db(self, cursor):
        if self._id == -1:
            sql = """INSERT INTO users(username, hashed_password)
                            VALUES(%s, %s) RETURNING id"""
            values = (self.username, self.hashed_password)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                           WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True
    
    @staticmethod
    def load_user_by_id(cursor, id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))  # (id_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_name(cursor, name_):
        sql = "SELECT id, username, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (name_,))  # (name_, ) - cause we need a tuple
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None
    
    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users
    
    def delete(self, cursor):
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (self.id,))
        self._id = -1
        return True


class Message:
    def __init__(self, from_id="", to_id="",text="", creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def safe_to_db(self, cursor):
        self.creation_date = datetime.datetime.now()
        if self._id == -1:
            sql = """INSERT INTO messages (from_id, to_id, creation_date, text)
                            VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.creation_date, self.text)
            cursor.execute(sql, values)
            self._id = cursor.fetchone()[0]  # or cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, creation_date=%s, text=%s
                           WHERE id=%s"""
            values = (self.from_id, self.to_id, self.creation_date, self.text, self.id)
            cursor.execute(sql, values)
            return True
    
    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT * FROM Messages"
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date, text = row
            loaded_messages = Message()
            loaded_messages._id = id_
            loaded_messages.from_id = from_id
            loaded_messages.to_id = to_id
            loaded_messages.creation_date = creation_date
            loaded_messages.text = text
            messages.append(loaded_messages)
        return messages


if __name__ == '__main__':

    from config import config   
    from psycopg2 import connect, OperationalError
    
    try:
        params = config(section='workshop')
        cnx = connect(**params)
        cnx.autocommit = True
        cursor = cnx.cursor()

        usr1 = User('user1','haslo1')
        usr2 = User('user2','haslo2')

        usr1.safe_to_db(cursor)
        usr2.safe_to_db(cursor)

        print(User.load_all_users(cursor))

        msg1 = Message(usr1.id,usr2.id,'Przykladowa wiadomosc')
        msg1.safe_to_db(cursor)

        print(Message.load_all_messages(cursor))


    except OperationalError:
        print("Błąd!")
    else:
        cursor.close()
        cnx.close()