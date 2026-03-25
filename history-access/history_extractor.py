import os
import sys
import shutil
import sqlite3
import tempfile

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(this_folder)
lookup_folder = os.path.join(root_folder, "local-lookup")
sys.path.append(lookup_folder)

from profile_hunter import find_history_databases

out_file = "history.txt"
out_forensics = "forensic.txt"

suspect_words = {
    "password and accounts" : ["reset-password", "forgot-password", "recover", "login", "signin", "auth", "token", "oauth"],
    "money and crypto": ["bank", "paypal", "binance", "metamask", "crypto", "wallet", "checkout", "mercadopago", "stripe", "banco"],
    "admin and infra": ["admin", "dashboard", "cpanel", "aws", "azure", "wp-admin", "phpmyadmin", "config", "localhost"],
    "work and communication": ["mail", "inbox", "slack", "discord", "whatsapp", "teams", "trello", "jira"]
}

def result_processing(res, history_db_path, motor):
    alerts = []
    for row in res:
        url = row[0]
        title = str(row[1]) if row[1] else "Untitled"
        visits = row[2]

        url_lower = url.lower()
        title_lower = title.lower()

        for category, words in suspect_words.items():
            if any(p in url_lower or p in title_lower for p in words):
                alerts.append((category, url, title, visits))
                break

    with open(out_forensics, "a", encoding="utf-8") as f:
        top = f"\nForensics resume - MOTOR: {motor.upper()}"
        f.write(top)
        f.write("\n" + "-" * 80 + "\n")
        alert_title = (f"\nRED FLAGS found ({len(alerts)}):")
        f.write(alert_title)
        f.write("\n" + "-" * 80 + "\n")
        if alerts:
            for category, url, title, visits in alerts:
                line_alerts = f"[{category}] Visits: {visits} \n -> {title}\n -> {url}\n"
                f.write(line_alerts + "\n")
        else:
            no_data = "No important data found\n"
            f.write(no_data)

    print(f"\nOutput file saved in: {out_forensics}")

def extract_chromium_history(history_db_path):
    print(f"\nExtracting DB from Chromium ({os.path.basename(os.path.dirname(history_db_path))})...")
    temp_db = os.path.join(tempfile.gettempdir(), "temp_history_db.sqlite")

    try:
        shutil.copy2(history_db_path, temp_db)
    except Exception as e:
        print(f"Error to copy database: {e}")
        return
    
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    try:
        query = """
        SELECT url, title, visit_count
        FROM urls
        ORDER BY visit_count DESC
        """
        cursor.execute(query)
        res = cursor.fetchall()

        with open(out_file, "a", encoding="utf-8") as f:
            top = f"\nOrdered by most visited websites (CHROMIUM) - Origin: {history_db_path}"
            f.write(top)
            f.write("\n" + "-" * 80 + "\n")
            for row in res:
                url = row[0]
                title = str(row[1]) if row[1] else "Untitled"
                visits = row[2]
                line = f"Visit count: {visits: <5} | Site: {title[:40]}... \nURL: {url}\n"
                f.write(line)
        print(f"\nHistory data from CHROMIUM saved in: {out_file}")
        
        result_processing(res, history_db_path, "Chromium")
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
    finally:
        conn.close()
        os.remove(temp_db)

def extract_firefox_history(history_db_path):
    print(f"\nExtracting DB from Firefox ({os.path.basename(os.path.dirname(history_db_path))})...")
    temp_db = os.path.join(tempfile.gettempdir(), "temp_firefox_db.sqlite")

    try:
        shutil.copy2(history_db_path, temp_db)
    except Exception as e:
        print(f"Error to copy db: {e}")
        return
    
    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()

    try:
        query = """
            SELECT url, title, visit_count
            FROM moz_places
            ORDER BY visit_count DESC
        """
        cursor.execute(query)
        res = cursor.fetchall()

        with open(out_file, "a", encoding="utf-8") as f:
            top = f"\nOrdered by most visited websites (FIREFOX) - Origin: {history_db_path}"
            f.write(top)
            f.write("\n" + "-" * 80 + "\n")
            for row in res:
                url = row[0]
                title = str(row[1]) if row[1] else "Untitled"
                visits = row[2]
                line = f"Visit count: {visits: <5} | Site: {title[:40]}... \nURL: {url}\n"
                f.write(line)
        print(f"\nHistory data from FIREFOX saved in: {out_file}")
        
        result_processing(res, history_db_path, "Firefox")
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
    finally:
        conn.close()
        os.remove(temp_db)

def main_history_extractor():
    print("\n" + "-"*50)
    print("Multi OS history stealer and forensic tool")
    print("-"*50)

    if os.path.exists(out_file): os.remove(out_file)
    if os.path.exists(out_forensics): os.remove(out_forensics)

    databases = find_history_databases()
    if not databases:
        print("\nNo databases found to extract")
    else:
        print("Starting extraction process\n")
        for my_db in databases:
            file_name = os.path.basename(my_db)
            if file_name == "places.sqlite":
                extract_firefox_history(my_db)
            elif file_name == "History":
                extract_chromium_history(my_db)
            else:
                print("Filename not recognized")

        print("\nSuccess: Extraction finished")
        print(f"    -> Full History Dump saved in: {out_file}")
        print(f"    -> Red Flags and Forensics saved in: {out_forensics}")