import subprocess

output_file = "win_dns_evidences.txt"

def dump_dns_win():
    print("Starting attack to DNS Windows")

    ps_command = "Get-DnsClientCache | Select-Object -ExpandProperty Entry"

    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_command],
            capture_output=True, text=True
        )
        output_res = res.stdout.strip().split('\n')
        if output_res and output_res[0] != "":
            sites = set([site.strip() for site in output_res if site.strip()])

            with open(output_file, "a", encoding="utf-8") as f:
                f.write(f"Windows DNS cache dump ({len(sites)}) websites")
                f.write("-" * 50 + "\n")
                for site in sites:
                    f.write(f"-> {site}\n")
                f.write("-" * 50 + "\n")

            print(f"Success, saved to file: {output_file}")
        else:
            print("Nothing found in Windows DNS cache")
    except Exception as e:
        print(f"Error executing PowerShell extraction: {e}")

if __name__ == "__main__":
    dump_dns_win()