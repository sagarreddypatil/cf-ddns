import os
import requests as re
from cloudflare import Cloudflare
from dotenv import load_dotenv

load_dotenv()

DOMAIN_NAME = os.getenv("CF_DOMAIN_NAME")
ZONE_ID = os.getenv("CF_ZONE_ID")
DNS_RECORD_ID = os.getenv("CF_DNS_RECORD_ID")

client = Cloudflare()


def get_ip() -> str:
    resp = re.get("https://cloudflare.com/cdn-cgi/trace")
    if resp.status_code != 200:
        raise Exception("Failed to retrieve IP address")
    data = resp.text.splitlines()
    ip_info = {
        v[0]: v[1] for v in (line.strip().split("=", 1) for line in data if "=" in line)
    }
    if "ip" not in ip_info:
        raise Exception("IP address not found in response")
    return ip_info["ip"]


def update_dns(ip: str) -> None:
    _ = client.dns.records.update(
        dns_record_id=DNS_RECORD_ID,
        zone_id=ZONE_ID,
        name=DOMAIN_NAME,
        content=ip,
        ttl=60,  # seconds
        proxied=False,
        type="A",
        comment="Scripted DDNS update",
    )


def main():
    try:
        ip_address = get_ip()
        print(f"Current IP address: {ip_address}")
        update_dns(ip_address)
        print("DNS record updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
