#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

URL = "https://sites.google.com/site/hepexrumor/"
OUTPUT_FILE = "hepexrumor.html"  # keep same name so the workflow doesn't change

def extract_summary(text: str) -> str:
    # Normalize whitespace and drop empty lines
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)

    # Find key anchors
    last_update_start = cleaned.find("Last update")
    random_notes_start = cleaned.find("Random Notes")

    # If for some reason we cannot find them, fall back to full text
    if last_update_start == -1 or random_notes_start == -1:
        return cleaned

    # ---- Last update block ----
    # From "Last update ..." down to just before the big tables,
    # which start at "Positions outside of the US"
    pos_outside_index = cleaned.find("Positions outside of the US", last_update_start)
    if pos_outside_index == -1:
        # Fallback: stop right before Random Notes if we don't find the table title
        pos_outside_index = random_notes_start

    last_update_block = cleaned[last_update_start:pos_outside_index].strip()

    # ---- Random Notes block ----
    # From "Random Notes" down to the footer ("Google Sites")
    google_sites_index = cleaned.find("Google Sites", random_notes_start)
    if google_sites_index == -1:
        google_sites_index = len(cleaned)

    random_notes_block = cleaned[random_notes_start:google_sites_index].strip()

    summary = last_update_block + "\n\n" + random_notes_block + "\n"
    return summary

def main():
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()

    # Parse HTML and get visible text
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text("\n")

    summary = extract_summary(text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(summary)

if __name__ == "__main__":
    main()

