import shutil
import os

def get_installed_browsers():

    browsers = {
        "chrome": {
            "exec": "google-chrome",
            "config": os.path.expanduser("~/.config/google-chrome/"),
            "type": "chromium"
        },
        "firefox": {
            "exec": "firefox",
            "config": os.path.expanduser("~/.mozilla/firefox/"),
            "type": "firefox"
        },
        "brave": {
            "exec": "brave-browser",
            "config": os.path.expanduser("~/.config/BraveSoftware/"),
            "type": "chromium"
        },
        "chromium": {
            "exec": "chromium",
            "config": os.path.expanduser("~/.config/chromium/"),
            "type": "chromium"
        },
        "opera": {
            "exec": "opera",
            "config": os.path.expanduser("~/.config/opera/"),
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