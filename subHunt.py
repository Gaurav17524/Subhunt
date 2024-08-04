import subprocess
from termcolor import colored
import json

def print_banner():
    banner = """
  ____        _     _   _             _   
 / ___| _   _| |__ | | | |_   _ _ __ | |_ 
 \___ \| | | | '_ \| |_| | | | | '_ \| __|
  ___) | |_| | |_) |  _  | |_| | | | | |_ 
 |____/ \__,_|_.__/|_| |_|\__,_|_| |_|\__|
                                          
    """
    print(colored(banner, "cyan"))

def run_command(command):
    print(colored(f"Running command: {command}", "blue"))
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.stderr:
        print(colored(f"Error: {process.stderr}", "red"))
    return process.stdout.splitlines()

def enumerate_subdomains(domain):
    print(colored(f"Enumerating subdomains for {domain}...", "green"))
    subdomains = run_command(f"subfinder -d {domain} -all -silent")
    print(colored(f"Found subdomains: {len(subdomains)}", "green"))
    return subdomains

def get_cname_records(subdomains):
    print("Checking CNAME records...")
    cname_records = {}
    for subdomain in subdomains:
        print(f"Processing subdomain: {subdomain}")
        output = run_command(f"dig cname +short {subdomain}")
        if output:
            cname_records[subdomain] = output[0]
    print(colored(f"Found CNAME records for {len(cname_records)} subdomains", "green"))
    return cname_records

def check_service_status(cname_records):
    print("Checking service status with httpx...")
    potentially_vulnerable = []

    # Prepare the input file for httpx
    with open('subdomains.txt', 'w') as f:
        for cname in cname_records.values():
            f.write(cname + '\n')

    # Run httpx to check the status
    command = "httpx -status-code -title -json -l subdomains.txt"
    httpx_output = run_command(command)
    
    for line in httpx_output:
        if not line.strip():
            continue  # Skip empty lines
        try:
            result = json.loads(line)
            cname = result.get("input")
            status_code = result.get("status_code")
            title = result.get("title")

            # Find the subdomain corresponding to this CNAME
            subdomain = next(key for key, value in cname_records.items() if value == cname)

            # Check for common signs of a potentially vulnerable subdomain
            if status_code == 404 or (title and ("not found" in title.lower() or "error" in title.lower())):
                potentially_vulnerable.append((subdomain, cname, status_code, title))
        except (json.JSONDecodeError, StopIteration):
            print(colored(f"Error processing result: {line}", "red"))

    print(colored(f"Checked {len(cname_records)} subdomains with httpx", "green"))
    return potentially_vulnerable

def alert_vulnerable_subdomains(vulnerable_subdomains):
    print(colored("Potentially vulnerable subdomains found:", "red"))
    for subdomain, cname, status_code, title in vulnerable_subdomains:
        print(colored(f"{subdomain} -> {cname} (Status Code: {status_code}, Title: {title})", "red"))

def main():
    print_banner()  # Print the banner
    domain = input("Enter the domain name: ")
    subdomains = enumerate_subdomains(domain)
    cname_records = get_cname_records(subdomains)
    vulnerable_subdomains = check_service_status(cname_records)
    if vulnerable_subdomains:
        alert_vulnerable_subdomains(vulnerable_subdomains)
    else:
        print("No potentially vulnerable subdomains found.")

if __name__ == "__main__":
    main()
