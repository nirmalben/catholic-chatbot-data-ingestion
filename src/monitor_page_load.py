import json
import time

from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

SITE = "https://cathwalk.app"

try:
    with open("metrics.json") as f:
        results = json.load(f)
except FileNotFoundError:
    results = []

# Measure load time with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    start = time.time()
    page.goto(SITE, wait_until="networkidle")
    end = time.time()
    browser.close()

load_time = end - start
results.append({
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "url": SITE,
    "load_time": load_time
})

with open("metrics.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Page load time: {load_time:.2f} seconds")