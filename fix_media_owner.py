import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute(
    """
    UPDATE media
    SET owner_id = 1
    WHERE owner_id IS NULL
"""
)

conn.commit()
conn.close()

print("owner_id успешно проставлен для всех медиа без пользователя.")
