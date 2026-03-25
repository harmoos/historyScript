import os
import sys
import time
import subprocess

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(this_folder)
lookup_folder = os.path.join(root_folder, "local-lookup")

sys.path.append(lookup_folder)

from dns_detector import detect_dns_config

output_file = "dns_evidences.txt"

def dump_systemd_resolved():
    print("Starting attack to systemd-resolved for RAM extraction")
    try:
        subprocess.run(["killall", "-USR1", "systemd-resolved"], check=True, capture_output=True)
        time.sleep(2)

        res = subprocess.run(
            ["journalctl", "-u", "systemd-resolved", "--since", "10 seconds ago"],
            capture_output=True, text=True, check=True
        )

        dominios = []
        for line in res.stdout.split('\n'):
            if "IN A" in line or "IN AAAA" in line:
                try:
                    cut_line = line.split("]:")[1].strip() if "]:" in line else line
                    dominio = cut_line.split("IN A")[0].strip()
                    if dominio and dominio not in dominios:
                        dominios.append(dominio)
                except Exception:
                    continue
            
        if dominios:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Got {len(dominios)} websites extracteds from RAM:\n")
                f.write(("-" * 50) + "\n")
                for d in dominios:
                    f.write(f"-> {d}\n")
                f.write(("-" * 50) + "\n")

            print(f"Success, saved to file: {output_file}")
        else:
            print("Empty cache, no websites to extract")
            
    except subprocess.CalledProcessError:
        print("Attack to systemd-resolved failed")


def dump_networkmanager_dnsmasq():
    print("Starting attack to dnsmasq used by Network Manager for RAM extraction")
    try:
        subprocess.run(["killall", "-USR1", "dnsmasq"], check=True, capture_output=True)
        time.sleep(2)

        res = subprocess.run(
            ["journalctl", "-t", "dnsmasq", "--since", "10 seconds ago"],
            capture_output=True, text=True, check=True
        )

        output_log = res.stdout.strip()
        if output_log:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write("Cache DNSMASQ extracted from RAM:\n")
                f.write(("-" * 50) + "\n")
                f.write(output_log)
                f.write(("-" * 50) + "\n")

            print(f"Success, saved to file: {output_file}")
        else:
            print("Empty cache log")
    
    except subprocess.CalledProcessError:
        print("Attack to dnsmasq failed")


def start_dns_attack():
    if os.geteuid() != 0:
        print("ERROR: Access to RAM denied.")
        print("Try again with sudo")
        return
    
    dns_config = detect_dns_config()
    config = dns_config.get("manager", "Unknown")

    print(f"DNS detected: {config}")

    if config == "systemd-resolved":
        dump_systemd_resolved()
    
    elif config == "NetworkManager":
        dump_networkmanager_dnsmasq()

    else:
        print("DNS not recognized or no local cache. \nNo attack can be executed")


if __name__ == "__main__":
    start_dns_attack()