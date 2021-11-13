# Aaron Quiroz
# Mini Capstone
# NFT search using opensea API

# readme stuff to add - python environment, list imports, link open api documentation. 


import requests
import json
import time


def search(category="neo-tokyo-identities"):

    headers = {
        "Accept": "application/json"}

    response = requests.get(
        f"https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&event_type=created&collection_slug={category}&occurred_before={time.time()}", headers=headers).text

    if "<title>Server Error (500)" in response:
        return "Error"
    containerobject = json.loads(response)

    if 'asset_events' not in containerobject:
        return "Category could not be found."
    elif len(containerobject['asset_events']) == 0:
        return "Category listings could not be found."
    elif 'detail' in containerobject:
        return "Error due to rate limiting."
    else:
        return containerobject['asset_events'][0]['asset']['permalink']


while True:
    try:
        params = ""
        while params == "":
            params = input("Enter category for search: ").strip(" ")
        print(search(category=params))
    except Exception as e:
        print(f"Error due to: {e}.")
    # break  # optional if you want to keep searching remove "break"
