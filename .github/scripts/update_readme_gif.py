import os
import requests
import re

API_KEY = os.environ['GIPHY_API_KEY']
SEARCH_TAG = "anime"
README_FILE = "README.md"
START_MARKER = "" # Wichtig: Hier sind die Marker definiert
END_MARKER = ""     # Wichtig: Hier sind die Marker definiert

def get_random_gif_url():
    """Fetches a random GIF URL from Giphy."""
    url = f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={SEARCH_TAG}&rating=g"
    response = requests.get(url)
    response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()
    return data['data']['images']['original']['url']

def update_readme_with_gif(gif_url):
    """Updates the README.md file with the new GIF URL."""
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Der Block, der in die README eingefügt wird.
    # Beachte die Zeilenumbrüche (\n) für bessere Lesbarkeit in der Raw-Datei.
    new_gif_content = f'\n<p align="center"><img src="{gif_url}" alt="random anime gif" width="600px"></p>\n'
    
    # Regex, um den gesamten Bereich zwischen den Markern zu finden, einschließlich der Marker selbst
    # re.DOTALL ist wichtig, damit '.' auch Zeilenumbrüche matcht
    pattern = re.compile(rf"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})", re.DOTALL)
    
    match = pattern.search(content)

    if match:
        # Ersetze den gesamten gefundenen Bereich (inkl. Marker) durch die Marker + neuen GIF-Inhalt
        updated_content = pattern.sub(rf"\g<1>{new_gif_content}\g<3>", content)
    else:
        # Fallback-Logik (sollte nicht greifen, wenn die README korrekt ist)
        print("Warning: START_ANIME_GIF / END_ANIME_GIF markers not found in README. Falling back to inserting after title.")
        # Fügt das GIF nach der H3-Überschrift ein, wenn die Marker nicht gefunden werden.
        updated_content = content.replace(
            "### Ein leidenschaftlicher Entwickler mit ❤️ für sauberen Code und innovative Lösungen!", 
            "### Ein leidenschaftlicher Entwickler mit ❤️ für sauberen Code und innovative Lösungen!" + new_gif_content
        )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    try:
        gif_url = get_random_gif_url()
        update_readme_with_gif(gif_url)
    except Exception as e:
        print(f"Error during GIF update: {e}")
        # In GitHub Actions wird dieser Fehler im Log sichtbar sein.