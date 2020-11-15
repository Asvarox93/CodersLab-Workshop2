from models import User, Message
from create_db import connect_db, close_connect_db
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='username')
parser.add_argument('-p','--password', help='password')
parser.add_argument('-t','--to', help='to user')
parser.add_argument('-s','--send', help='text to user')
parser.add_argument('-l','--list', help='get user text', action="store_true")

args = parser.parse_args()

u = args.username
p = args.password
t = args.to
s = args.send
l = args.list

if(u is not None and
   p is not None and
   t is None and
   s is None and
   l is True):

    user = User(u, p)
    cursor = connect_db()

    sql = f"SELECT id FROM users WHERE username='{u}' and hashed_password='{user.hashed_password}'"
    cursor.execute(sql)

    if cursor.rowcount==0:
        raise ValueError('Username or password is incorrect')

    user = User.load_user_by_name(cursor, u)

    msgs = Message.load_all_messages(cursor)

    print("Massages for you:")
    for msg in msgs:
        if msg is None:
            print(f"Empty")
        if msg.to_id == user.id:
            sql = f"SELECT username FROM users Where id={msg.from_id}"
            cursor.execute(sql)
            print(f"From {cursor.fetchall()[0][0]}:\n{msg.creation_date}\n{msg.text}")
        
    
    close_connect_db()
    
elif(u is not None and
   p is not None and
   t is not None and
   s is not None and
   l is False):

    user = User(u, p)
    cursor = connect_db()

    sql = f"SELECT id FROM users WHERE username='{u}' and hashed_password='{user.hashed_password}'"
    cursor.execute(sql)

    if cursor.rowcount==0:
        raise ValueError('Username or password is incorrect')
    
    user = User.load_user_by_name(cursor, u)

    sql = f"SELECT * FROM users WHERE id={t}"

    if cursor.rowcount==0:
        raise IndexError('Your recipient does not exist')

    if len(s) > 255:
        raise ValueError('Your messange is to long (max 255 characters)')

    msg = Message(user.id, t, s)
    msg.safe_to_db(cursor)
    print('Messange has been send')
    close_connect_db()
else:
    parser.print_help()