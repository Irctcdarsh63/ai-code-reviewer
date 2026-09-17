import sqlite3

def find_user_by_name(username):
    # Critical Flaw: SQL Injection vulnerability via string formatting
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE name = '{username}'")
    return cursor.fetchall()

def remove_duplicates(items):
    # Performance Flaw: Inefficient O(N^2) loop
    unique = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique