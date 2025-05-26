import requests as re

def get_ip() -> str:
    resp = re.get("https://cloudflare.com/cdn-cgi/trace")
    if resp.status_code != 200:
        raise Exception("Failed to retrieve IP address")
    data = resp.text.splitlines()
    ip_info = {v[0]: v[1] for v in (line.strip().split('=', 1) for line in data if '=' in line)}
    if "ip" not in ip_info:
        raise Exception("IP address not found in response")
    return ip_info["ip"]