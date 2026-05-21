import socket
import subprocess
import csv


def resolve_dns(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"Error for {domain}: {e}")
        return None

def run_traceroute(ip):
    cmd = ["tracert", "-d", "-h", "10", ip]
    try:
        result = subprocess.run(
            cmd, capture_output=True, 
            text=True, timeout=45, 
            check=False, encoding='cp866'
        )
        if result.returncode != 0:
            return f"traceroute завершился с кодом {result.returncode}"
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception as e:
        return f"Error: {e}"

def main():
    output_file = f"result.csv"
    domains = [
        "google.com",
        "github.com", 
        "temporary.com",
        "yandex.ru",
        "stackoverflow.com",
    ]
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["domain", "ip", "traceroute_result"])
        for domain in domains:
            ip = resolve_dns(domain)
            if ip:
                print(f"IP: {ip}")
                trace = run_traceroute(ip)
            else:
                trace = "Error DNS"
                print(f"Error DNS")
            writer.writerow([domain, ip or "N/A", trace])

if __name__ == "__main__":
    main()