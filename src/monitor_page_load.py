import json
import time

from datetime import datetime, timezone
from playwright.sync_api import sync_playwright

SITE = "https://cathwalk.app"

try:
    with open("generated/page_load_times.json") as f:
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

if len(results) > 240:
    first_240 = results[:240]
    total = 0.0
    count = 0
    for item in first_240:
        try:
            val = float(item.get("load_time", 0))
        except Exception:
            val = 0.0
        total += val
        count += 1
    avg_load = total / count if count > 0 else 0.0

    # Use the timestamp and url from the original 240th entry
    timestamp_240 = results[239].get("timestamp")
    url_240 = results[239].get("url", SITE)

    averaged_entry = {
        "timestamp": timestamp_240,
        "url": url_240,
        "load_time": avg_load
    }

    # Keep averaged entry followed by any entries after the original 240th
    results = [averaged_entry] + results[240:]

with open("generated/page_load_times.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Page load time: {load_time:.2f} seconds")