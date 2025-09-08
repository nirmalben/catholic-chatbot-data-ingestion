import pandas as pd
import matplotlib.pyplot as plt
import json

with open("generated/page_load_times.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])

plt.style.use('dark_background')
plt.figure(figsize=(10, 4))

for url in df["url"].unique():
    subset = df[df["url"] == url]
    avg_time = subset["load_time"].mean()
    plt.plot(subset["timestamp"], subset["load_time"], marker="o", linestyle="-", label=f"{url} (avg: {avg_time:.2f}s)")

plt.title("Page Load Times")
plt.xlabel("Time")
plt.ylabel("Load Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("generated/page_load_times.png")