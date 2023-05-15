import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username
    cursor.execute(query)
    result = cursor.fetchone()
    return result
