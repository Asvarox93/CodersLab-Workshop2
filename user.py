from models import User, Message
from create_db import connect_db, close_connect_db
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username', help='username')
parser.add_argument('-p','--password', help='password')
parser.add_argument('-l','--list', help='list users', action="store_true")
parser.add_argument('-d','--delete', help='delete user', action="store_true")
parser.add_argument('-e','--edit', help='edit user', action="store_true")
parser.add_argument('-n','--new_pass', help='new password')

args = parser.parse_args()

u = args.username
p = args.password
l = args.list
d = args.delete
e = args.edit
np = args.new_pass


# When only username and password args
if(u is not None and
   p is not None and
   l is False and 
   d is False and
   e is False and
   np is None):
   
    if len(p) < 8:
        raise ValueError("Password is to short")

    cursor = connect_db()

    sql = f"SELECT * FROM users WHERE username='{u}'"
    cursor.execute(sql)

    if(cursor.rowcount>0):
        raise ValueError('A duplicated recrod already exists')
    
    user = User(u, p)
    user.safe_to_db(cursor)
    close_connect_db()
    print("User has been created")

elif(u is not None and
   p is not None and
   l is False and 
   d is False and
   e is True and
   np is not None):

    user = User(u, p)
    cursor = connect_db()

    sql = f"SELECT * FROM users WHERE username='{u}' and hashed_password='{user.hashed_password}'"
    cursor.execute(sql)

    if(cursor.rowcount==0):
        raise ValueError('Username or password is incorrect')
    
    if len(np) < 8:
        raise ValueError("Password is to short")

    user = User.load_user_by_name(cursor,u)
    user.hashed_password = p
    user.safe_to_db(cursor)
    close_connect_db()
    print("Password has been changed")

elif(u is not None and
   p is not None and
   l is False and 
   d is True and
   e is False and
   np is None):

    user = User(u, p)
    cursor = connect_db()

    sql = f"SELECT * FROM users WHERE username='{u}' and hashed_password='{user.hashed_password}'"
    cursor.execute(sql)

    if(cursor.rowcount==0):
        raise ValueError('Username or password is incorrect')
    
    user = User.load_user_by_name(cursor,u)
    user.delete(cursor)
    close_connect_db()
    print("User has been deleted")

elif(u is None and
   p is None and
   l is True and 
   d is False and
   e is False and
   np is None):

    cursor = connect_db()
    users = User.load_all_users(cursor)
    print("Current User List:", users)
    for user in users:
        print(f"{user.id} - {user.username}")
    close_connect_db()
else:
    parser.print_help()