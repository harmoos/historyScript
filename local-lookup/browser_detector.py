import os
import pwd
import shutil

def get_real_home():
    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        return pwd.getpwnam(sudo_user).pw_dir
    else:
        return os.path.expanduser("~")

def get_installed_browsers():
    browsers = {}

    if os.name == 'nt':
        local_appdata = os.getenv('LOCALAPPDATA')
        roaming_appdata = os.getenv('APPDATA')

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

    found = []
    found_config = {}

    for browser_name, data in browsers.items():
        exec_found = shutil.which(data["exec"])
        config_found = os.path.exists(data["config"])

        if exec_found or config_found:
            found.append(browser_name)
        if config_found:
            found_config[browser_name] = data

    print("Detected Browsers:")
    if len(found) > 0:
        for b in found:
            print(f"\n- {b}")
    else:
        print("No browsers detected.")

    return found_config