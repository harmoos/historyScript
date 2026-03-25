import os
import glob
import shutil

if os.name != "nt":
    import pwd

def get_real_home():
    if os.name == "nt":
        return os.path.expanduser("~")
    
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return pwd.getpwnam(sudo_user).pw_dir
    else:
        return os.path.expanduser("~")

def get_installed_browsers():
    browsers = {}

    if os.name == 'nt':
        user_home = os.path.expanduser("~")
        local_appdata = os.path.join(user_home, "AppData", "Local")
        roaming_appdata = os.path.join(user_home, "AppData", "Roaming")
        packages_path = os.path.join(local_appdata, "Packages")

        browsers = {
            "chrome": {
                "exec": "chrome", 
                "config": os.path.join(local_appdata, "Google", "Chrome", "User Data"),
                "type": "chromium"
            },
            "firefox": {
                "exec": "firefox",
                "config": os.path.join(roaming_appdata, "Mozilla", "Firefox"),
                "type": "firefox"
            },
            "brave": {
                "exec": "brave",
                "config": os.path.join(local_appdata, "BraveSoftware", "Brave-Browser", "User Data"),
                "type": "chromium"
            },
            "chromium": {
                "exec": "chromium",
                "config": os.path.join(local_appdata, "Chromium", "User Data"),
                "type": "chromium"
            },
            "opera": {
                "exec": "opera",
                "config": os.path.join(roaming_appdata, "Opera Software", "Opera Stable"),
                "type": "chromium"
            },
            "edge": {
                "exec": "msedge",
                "config": os.path.join(local_appdata, "Microsoft", "Edge", "User Data"),
                "type": "chromium"
            }
        }


    else:
        home_path = get_real_home()
        browsers = {
            "chrome": {
                "exec": "google-chrome",
                "config": os.path.join(home_path, ".config/google-chrome/"),
                "type": "chromium"
            },
            "firefox": {
                "exec": "firefox",
                "config": os.path.join(home_path, ".mozilla/firefox/"),
                "type": "firefox"
            },
            "brave": {
                "exec": "brave-browser",
                "config": os.path.join(home_path, ".config/BraveSoftware/"),
                "type": "chromium"
            },
            "chromium": {
                "exec": "chromium",
                "config": os.path.join(home_path, ".config/chromium/"),
                "type": "chromium"
            },
            "opera": {
                "exec": "opera",
                "config": os.path.join(home_path, ".config/opera/"),
                "type": "chromium"
            }
        }

    store_mappings = {
        "firefox": "Mozilla.Firefox_*",
        "edge":    "Microsoft.MicrosoftEdge.Stable_*",
    }

    found = []
    found_config = {}

    for browser_name, data in browsers.items():
        exec_found = shutil.which(data["exec"])
        config_found = os.path.exists(data["config"])

        if config_found:
            found.append(browser_name)
            found_config[browser_name] = data
        elif os.name == 'nt' and browser_name in store_mappings:
            search_pattern = os.path.join(packages_path, store_mappings[browser_name])
            matches = glob.glob(search_pattern)

            if matches:
                store_root = matches[0]
                store_config = os.path.join(store_root, "LocalCache", "Roaming", "Mozilla", "Firefox")
                if os.path.exists(store_config):
                    data["config"] = store_config
                    found.append(browser_name)
                    found_config[browser_name] = data
        elif exec_found:
            pass

    print("Detected Browsers:")
    if len(found) > 0:
        for b in found:
            print(f"\n- {b}")
        print("\n")
    else:
        print("No browsers detected.")
    print(found_config)

    return found_config