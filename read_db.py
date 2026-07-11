import sqlite3
import os

# მიუთითე გზა ბაზისკენ
db_path = os.path.join('instance', 'site.db')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM user") # მხოლოდ მეილების წამოღება
    emails = cursor.fetchall()
    print("ბაზაში დარეგისტრირებული მეილებია:")
    for email in emails:
        print(email[0])
    conn.close()
else:
    print("ბაზის ფაილი ვერ მოიძებნა!")