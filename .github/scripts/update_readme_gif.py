import os
import requests
import re

API_KEY = os.environ['GIPHY_API_KEY']
SEARCH_TAG = "anime"
README_FILE = "README.md"
START_MARKER = "@START_ANIME_GIF"
END_MARKER = "@END_ANIME_GIF"

def get_random_gif_url():
    """Fetches a random GIF URL from Giphy."""
    url = f"https://api.giphy.com/v1/gifs/random?api_key={API_KEY}&tag={SEARCH_TAG}&rating=g"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['data']['images']['original']['url']

def update_readme_with_gif(gif_url):
    """Updates the README.md file with the new GIF URL."""
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    new_gif_block = f'\n<p align="center"><img src="{gif_url}" alt="random anime gif" width="600px"></p>\n'
    
    pattern = re.compile(rf"{START_MARKER}(.*?){END_MARKER}", re.DOTALL)
    
    if pattern.search(content):
        updated_content = pattern.sub(f"{START_MARKER}{new_gif_block}{END_MARKER}", content)
    else:

        print("Warning: START_ANIME_GIF / END_ANIME_GIF markers not found. Appending GIF after title.")
        updated_content = content.replace(new_gif_block)


    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    try:
        gif_url = get_random_gif_url()
        update_readme_with_gif(gif_url)
    except Exception as e:
        print(f"Error during GIF update: {e}")
