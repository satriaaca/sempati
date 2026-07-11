from bs4 import BeautifulSoup
import re
from datetime import datetime


def html_to_lines(html):
    soup = BeautifulSoup(html, "html.parser")

    lines = []

    for item in soup.find_all(["p", "li"]):
        text = item.get_text(strip=True)

        if text:
            lines.append(text)

    return lines


def sanitize_filename(filename):
    # 1. Bersihkan karakter ilegal bawaan sistem operasi
    filename = re.sub(r'[<>:"/\\|?*]', "-", filename)
    filename = re.sub(r"\s+", " ", filename).strip()

    # 2. Ambil tanggal hari ini dengan format YYYY-MM-DD (contoh: 2026-07-11)
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 3. Gabungkan tanggal di depan nama file
    formatted_filename = f"{today_str} - {filename}"

    return formatted_filename
