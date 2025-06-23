import os
import requests
import re
import sys

API_KEY = os.environ.get('GIPHY_API_KEY')
SEARCH_TAG = "anime"
README_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "README.md")
START_MARKER = "<!-- @START_ANIME_GIF -->"
END_MARKER = "<!-- @END_ANIME_GIF -->"
FALLBACK_GIF = "https://media.giphy.com/media/10SvWCbt1ytWCc/giphy.gif"


def get_random_gif_url():
    if not API_KEY:
        print("[Fehler] GIPHY_API_KEY Umgebungsvariable nicht gesetzt.")
        return FALLBACK_GIF
    url = f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={SEARCH_TAG}&rating=g"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        gif_url = data.get('data', {}).get('images', {}).get('original', {}).get('url')
        if not gif_url:
            print("[Warnung] Keine GIF-URL von Giphy erhalten. Fallback wird verwendet.")
            return FALLBACK_GIF
        return gif_url
    except Exception as e:
        print(f"[Fehler] Problem beim Abrufen des GIFs: {e}. Fallback wird verwendet.")
        return FALLBACK_GIF

def update_readme_with_gif(gif_url):
    if not os.path.isfile(README_FILE):
        print(f"[Fehler] README.md nicht gefunden unter {README_FILE}")
        sys.exit(1)
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_gif_block = f'\n<p align="center"><img src="{gif_url}" alt="random anime gif" width="600px"></p>\n'
    pattern = re.compile(rf"({re.escape(START_MARKER)})(.*?)(" + re.escape(END_MARKER) + ")", re.DOTALL)
    match = pattern.search(content)

    if match:
        updated_content = pattern.sub(rf"\g<1>{new_gif_block}\g<3>", content)
        print("[Info] GIF-Block zwischen Markern aktualisiert.")
    else:
        print("[Warnung] Marker nicht gefunden. GIF-Block wird am Anfang eingefügt.")
        updated_content = f"{START_MARKER}{new_gif_block}{END_MARKER}\n" + content

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("[Info] README.md erfolgreich aktualisiert.")

if __name__ == "__main__":
    gif_url = get_random_gif_url()
    update_readme_with_gif(gif_url)