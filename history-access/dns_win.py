import subprocess

output_file = "win_dns_evidences.txt"

def dump_dns_win():
    print("Starting attack to DNS Windows")
    res = subprocess.run(["ipconfig", "/displaydns"], capture_output=True, text=True)

    output_res = res.stdout.split('\n')
    if output_res:
        for line in output_res:
            if "Record Name" in line:
                with open(output_file, "a", encoding="utf-8") as f:
                    site = line.split(":")[1].strip()
                    f.write(f"-> {site}\n")

        print(f"Success, saved to file: {output_file}")
    else:
        print("Nothing found in Windows DNS")