import sqlite3
con = sqlite3.connect('users.db', check_same_thread=False)
# con.execute("create table users (user_id, temp, light, name, picture)")
# con.execute("insert into users values(123,10,100,Name, PicturePath)")

def getUser(userId):
    cur = con.cursor()
    cur.execute("select * from users where user_id=:user_id", {"user_id": userId})
    results = cur.fetchone()
    return results
