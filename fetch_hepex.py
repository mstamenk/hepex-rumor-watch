#!/usr/bin/env python3
import requests

URL = "https://sites.google.com/site/hepexrumor/2025-2026"

def main():
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    html = resp.text

    # Save raw HTML snapshot
    with open("hepexrumor.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()

