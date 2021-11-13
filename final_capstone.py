"""
Aaron Quiroz
Mini Capstone

"""



import requests
from discord_webhook import DiscordEmbed, DiscordWebhook
import time
import json
from datetime import datetime
from dateutil import tz

# METHOD 1: Hardcode zones:
from_zone = tz.gettz('UTC')
to_zone = tz.gettz('America/New_York')


alreadydonelist = []
counter = 0
def sendwebhook(content = None):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/904473988128989184/ToNx5U82pxiEiW4gSDdZL2fmUyGi8NcTdb1IJ24gX1pfKBRlgs_JuFPBqQBAq5a9kzYB',rate_limit_retry=True)
    embed = DiscordEmbed(title='NFT Sniping Monitor', color='ee82ee')
    embed.set_footer(text='smkrgroup', icon_url='https://cdn.discordapp.com/attachments/860707974355091456/879584512810573854/png-01.png')
    if content:
        embed.add_embed_field(name="Name", value=content['Name'])
        embed.add_embed_field(name="Category", value=content['Category'], )
        embed.add_embed_field(name="Price", value=content['Price'], )
        embed.add_embed_field(name="Monitor Price", value=content['MonitorPrice'], )
        embed.add_embed_field(name="URL", value=content['URL'], )
        embed.add_embed_field(name="Listing Time", value=content['Time'], )


    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()

def search(previoustime = 1630890535, cap = 10500000000000000000, category = "neo-tokyo-identities"):
    global counter
    headers = {
    "Accept": "application/json",
    "X-API-KEY": "011fdef55779420aaa44553a7b9158f3"}
    proxies = {"http": "http://sub_1jhtaalnflrqhw4aliumdvyh:villain138@139.190.228.85:3190/", "https" : "http://sub_1jhtaalnflrqhw4aliumdvyh:villain138@139.190.228.85:3190"}
    response = requests.get(f"https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=300&occurred_after={previoustime}&event_type=created&collection_slug={category}",headers=headers, proxies=proxies).text
    current_time = time.time()
    if "<title>Server Error (500)" in response: return previoustime
    containerobject = json.loads(response)
    if 'detail' in containerobject: 
        time.sleep(1)
        print(f"Rate limited at {current_time}.")
        counter = counter + 1
    else:
        print(f"{current_time} pinged for {counter}.")
        for transaction in containerobject["asset_events"]:
            if transaction['payment_token']['symbol'] == 'ETH' and transaction["starting_price"] == transaction["ending_price"] and int(transaction["starting_price"]) < cap and transaction['asset']['permalink'] not in alreadydonelist:
                msg = f"Found {transaction['asset']['name']} under cap value. Price: {int(transaction['starting_price'])} Link: {transaction['asset']['permalink']} "
                listingtime = transaction['created_date'].replace("T"," ")
                newlistingtime = listingtime.split(".")
                utc = datetime.strptime(newlistingtime[0], '%Y-%m-%d %H:%M:%S')
                utc = utc.replace(tzinfo=from_zone)
                # Convert time zone
                central = utc.astimezone(to_zone)
                sendwebhook(content={'Name': transaction['asset']['name'], 'Category': transaction['collection_slug'], 'Price': str(int(transaction['ending_price']) / 1000000000000000000) + " ETH", 'MonitorPrice': str(cap / 1000000000000000000) + " ETH", 'URL': transaction['asset']['permalink'], 'Time': str(central) + " EST"})
                print(msg)
                alreadydonelist.append(transaction['asset']['permalink'])
        counter = counter + 1
        time.sleep(0.6)

        return current_time
    return previoustime

timevar = 1635328215 


while True:
    try:timevar = search(previoustime=timevar)
    except Exception as e: print(f"Error due to: {e}.")

    