import sqlite3
import shutil
import os

def extract_chromium_history(history_db_path):
    temp_db = '/tem/temp_history_db.sqlite'

    try:
        shutil.copy2(history_db_path, temp_db)
    except Exception as e:
        print(f"Error to copy database: {e}")
        return
    
    connect = sqlite3.connect(temp_db)
    cursor = connect.cursor

    try:
        query = """
        SELECT url, title, visit_count
        FROM urls
        ORDER BY visit_count DESC
        """
        cursor.execute(query)
        res = cursor.fetchall()

        print("Ordered by most visited websites")
        print("-" * 50)
        for row in res:
            url = row[0]
            title = row[1]
            visits = row[2]
            print(f"Visit count: {visits: <5} | Site: {title[:40]}... \nURL: {url}\n")
        
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
    finally:
        connect.close()
        os.remove(temp_db)

if __name__ == "__main__":
    my_db = input("Paste your web brower db path here: ")
    if os.path.exists(my_db):
        extract_chromium_history(my_db)
    else:
        print("File not found")