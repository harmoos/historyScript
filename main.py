import os
import sys
import glob
import platform

root_folder = os.path.dirname(os.path.abspath(__file__))
lookup_folder = os.path.join(root_folder, "history-access")
sys.path.append(lookup_folder)

from history_extractor import main_history_extractor
from dns_ram_dumper import start_dns_attack
from dns_win import dump_dns_win

def clean_old_logs():
    txt_files = glob.glob("*.txt")
    if not txt_files:
        return
    for file in txt_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to remove {file}: {e}")

def check_admin_privileges():
    if sys.platform == "win32":
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    elif sys.platform == "linux" or sys.platform == "darwin":
        return os.geteuid() == 0
    return False

def run_windows_routine():
    print("Windows OS detected, executing...")
    main_history_extractor()
    dump_dns_win()


def run_linux_routine():
    print("Linux OS detected, executing...")
    main_history_extractor()

    if check_admin_privileges():
        print("Root privileges confirmed, ready to extract DNS cache")
        start_dns_attack()
    else:
        print("WARNING: if you want to extract DNS cache history please execute the script with 'sudo'")

def main():
    clean_old_logs()
    system = platform.system()
    if system == "Windows":
        run_windows_routine()
    elif system == "Linux":
        run_linux_routine()
    else:
        print(f"OS not supported: {system}")

if __name__ == "__main__":
    main()