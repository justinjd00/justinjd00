import os
import requests
import re

API_KEY = os.environ['GIPHY_API_KEY']
SEARCH_TAG = "anime"
README_FILE = "README.md"
START_MARKER = "@START_ANIME_GIF"
END_MARKER = "@END_ANIME_GIF"

def get_random_gif_url():
    url = f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={SEARCH_TAG}&rating=g"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['data']['images']['original']['url']

def update_readme_with_gif(gif_url):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_gif_block = f'\n<p align="center"><img src="{gif_url}" alt="random anime gif" width="600px"></p>\n'
    
    pattern = re.compile(rf"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})", re.DOTALL)
    
    match = pattern.search(content)

    if match:
        updated_content = pattern.sub(rf"\g<1>{new_gif_block}\g<3>", content)
        
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.write(updated_content)
    else:
        print(f"Warning: Markers '{START_MARKER}' and '{END_MARKER}' not found in '{README_FILE}'. README will not be updated.")

if __name__ == "__main__":
    try:
        gif_url = get_random_gif_url()
        update_readme_with_gif(gif_url)
    except Exception as e:
        print(f"Error during GIF update: {e}")