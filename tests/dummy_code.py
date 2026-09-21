import sqlite3

def get_user_data(user_id):
    # Vulnerability: Direct SQL interpolation
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    return cur.fetchall()

def slow_duplicate_check(numbers):
    # Performance flaw: Nested loop O(N^2)
    duplicates = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] == numbers[j] and numbers[i] not in duplicates:
                duplicates.append(numbers[i])
    return duplicates