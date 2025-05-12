import asyncio
import csv
from twikit import Client
from configparser import ConfigParser

# Define the number of tweets you want to fetch
DESIRED_TWEETS = 900
QUERY = 'Tijuana River Sewage Crisis Pollution Mexico'

#* login credentials 
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

#. authenticate to X.com
client = Client(language='en-US')

async def login_to_client():
    result = await client.login(
        auth_info_1=username,
        auth_info_2=email,
        password=password,
        totp_secret=None,
        cookies_file=None,
        enable_ui_metrics=True
    )
    return result

async def get_tweets():
    tweet_count = 0
    all_tweets = []

    while tweet_count < DESIRED_TWEETS:
        print("Fetching tweets...")
        tweets = await client.search_tweet(query=QUERY, product='Top')
        all_tweets.extend(tweets)
        tweet_count = len(all_tweets)
        print(f"Fetched {tweet_count} tweets so far")

    with open('tweets.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Check if file is empty to write header
            writer.writerow(['Tweet Count', 'User Name', 'Tweet Text'])  # Write header
        
        for i, tweet in enumerate(all_tweets[:DESIRED_TWEETS]):
            tweet_data = [i + 1, tweet.user.name, tweet.text]
            writer.writerow(tweet_data)  # Write tweet data to CSV
            print(f"Writing tweet {i + 1} to CSV")

async def main():
    try:
        login_result = await login_to_client()
        print(f"Login result: {login_result}")
        
        # Save and load cookies
        client.save_cookies('cookies.json')
        client.load_cookies('cookies.json')
        
        # Get tweets and save to CSV
        await get_tweets()
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the main function
asyncio.run(main())
