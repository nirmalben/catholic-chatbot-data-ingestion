import time, os, requests
from playwright.sync_api import sync_playwright

URL = os.environ["GRAFANA_OTLP_URL"]
API_KEY = os.environ["GRAFANA_OTLP_API_KEY"]
SITE = "https://cathwalk.app"

# Measure load time with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    start = time.time()
    page.goto(SITE, wait_until="networkidle")
    end = time.time()
    browser.close()

load_time = end - start
print(f"Page load time: {load_time:.2f} seconds")

# Current time in nanoseconds
timestamp_ns = int(time.time() * 1e9)

# OTLP JSON body
body = {
    "resourceMetrics": [{
        "scopeMetrics": [{
            "metrics": [{
                "name": "page_load_seconds",
                "unit": "s",
                "description": "Page Load Time in Seconds",
                "gauge": {
                    "dataPoints": [
                        {
                            "asDouble": load_time,
                            "timeUnixNano": timestamp_ns,
                            "attributes": [
                                {
                                    "key": "site",
                                    "value": {
                                        "stringValue": SITE
                                    }
                                }
                            ]
                        }
                    ]
                }
            }]
        }]
    }]
}

# Send to Grafana OTLP endpoint
resp = requests.post(
    URL,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    },
    json=body
)

print("Response:", resp.status_code, resp.text)
