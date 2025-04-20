import time
import logging
import requests
from collections import defaultdict
from urllib.parse import urlparse
import json

logger = logging.getLogger(__name__)

def extract_domain(url):
    return urlparse(url).hostname

def parse_body(body):
    if not body:
        return None
    if isinstance(body, dict):
        return body
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return body

def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = parse_body(endpoint.get('body'))

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=1)
        response_time = time.time() - start

        if 200 <= response.status_code < 300 and response_time < 0.5:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException as e:
        logger.error(f"[DOWN] {url} → Request failed: {e}")
        return "DOWN"

def monitor_endpoints(config):
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    logger.info("Starting endpoint monitoring...")

    while True:
        cycle_start = time.time()

        for endpoint in config:
            domain = extract_domain(endpoint["url"])
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        for domain, stats in domain_stats.items():
            availability = int(100 * stats["up"] / stats["total"])
            logger.info(f"[{domain}] Availability: {availability}%")

        elapsed = time.time() - cycle_start
        time.sleep(max(0, 15 - elapsed))
