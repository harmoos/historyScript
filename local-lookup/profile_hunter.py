import os

from browser_detector import get_installed_browsers

def find_history_databases():
    browsers = get_installed_browsers()
    db_list = []

    for name, data in browsers.items():
        base_path = data["config"]
        b_type = data["type"]

        print(f"Looking for databases at: {name}")

        if b_type == "chromium":
            if os.path.exists(base_path):
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)

                    if os.path.isdir(item_path) and (item == "Default" or item.startswith("Profile")):
                        history_file = os.path.join(item_path, "History")
                        if os.path.exists(history_file):
                            print(f"  -> Profile found: {item}")
                            print(f"     DB: {history_file}")
                            db_list.append(history_file)

        elif b_type == "firefox":
            if os.path.exists(base_path):
                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)

                    if os.path.isdir(item_path):
                        history_file = os.path.join(item_path, "places.sqlite")

                        if os.path.exists(history_file):
                            print(f"  -> Profile found: {item}")
                            print(f"     DB: {history_file}")
                            db_list.append(history_file)

    print(f"Number of databases found: {len(db_list)}")

    return db_list

if __name__ == "__main__":
    print("Starting")
    databases = find_history_databases()
    print("Done")