from bs4 import BeautifulSoup
import re


def html_to_lines(html):
    soup = BeautifulSoup(html, "html.parser")

    lines = []

    for item in soup.find_all(["p", "li"]):
        text = item.get_text(strip=True)

        if text:
            lines.append(text)

    return lines


def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\|?*]', "-", filename)
    filename = re.sub(r"\s+", " ", filename)

    return filename.strip()
