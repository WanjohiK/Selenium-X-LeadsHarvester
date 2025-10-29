from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sqlite3   # ✅ For saving to SQLite

# === Create a persistent Chrome profile ===
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Remove webdriver property for stealth
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 20)

# === Step 1: Open X and check login state ===
driver.get("https://x.com/home")
time.sleep(5)

# Try to detect login state
logged_out = False
try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Log in' or text()='Sign in']")))
    logged_out = True
except:
    logged_out = False

# === Step 2: Handle login ===
if logged_out:
    print("=" * 50)
    print("MANUAL LOGIN MODE - CLEAN PROFILE")
    print("=" * 50)
    print("Please log in manually in the browser window.")
    print("After you're logged in, press ENTER here to continue...")
    print("=" * 50)
    input()
    print("\n✅ Login successful! Redirecting to search...")
else:
    print("\n✅ You are already logged in. Redirecting to search...")

# === Step 3: Flexible search page ===
date_since = "2025-05-25"
date_until = "2025-10-27"
search_query = "looking for an AI engineering job opportunity"

search_url = f"https://x.com/search?q={search_query} since:{date_since} until:{date_until}&f=live"
driver.get(search_url)
time.sleep(10)

print(f"\n🎯 Reached search results page for '{search_query}' ({date_since} → {date_until}).")
print("You can now add scraping logic below this line.")

# === SQLite setup ===
conn = sqlite3.connect("machinelearningleads.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    text TEXT,
    displayed_time TEXT,
    datetime_value TEXT,
    search_query TEXT
)
''')
conn.commit()


def save_tweet_to_db(user, text, displayed_time, datetime_value, search_query):
    """Insert each tweet directly into SQLite."""
    cursor.execute('''
        INSERT INTO tweets (user, text, displayed_time, datetime_value, search_query)
        VALUES (?, ?, ?, ?, ?)
    ''', (user, text, displayed_time, datetime_value, search_query))
    conn.commit()


def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
        text = element.find_element(By.XPATH, ".//div[@lang]").text
        time_tag = element.find_element(By.XPATH, ".//time")
        displayed_time = time_tag.text
        datetime_value = time_tag.get_attribute("datetime")
        tweets_data = [user, text, displayed_time, datetime_value]
    except:
        tweets_data = ['user', 'text', 'displayed_time', 'datetime_value']
    return tweets_data


user_data = []
text_data = []
displayed_times = []
datetime_values = []
tweets_ids = set()

scrolling = True
while scrolling:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//article[@role='article']")))
    tweets = driver.find_elements(By.XPATH, "//article[@role='article']")
    for tweet in tweets[-15:]:
        tweet_list = get_tweet(tweet)
        tweet_id = "".join(tweet_list)
        if tweet_id not in tweets_ids:
            tweets_ids.add(tweet_id)
            user, text, displayed_time, datetime_value = tweet_list
            user_data.append(user)
            text_data.append(" ".join(text.split()))
            displayed_times.append(displayed_time)
            datetime_values.append(datetime_value)

            # 💾 Save immediately to SQLite
            save_tweet_to_db(user, text, displayed_time, datetime_value, search_query)
            print(f"💾 Saved tweet from {user}")

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight;")
    if new_height == last_height:
        scrolling = False
    else:
        last_height = new_height

driver.quit()

# === Save to CSV ===
df_tweets = pd.DataFrame({
    'user': user_data,
    'text': text_data,
    'displayed_time': displayed_times,
    'datetime_value': datetime_values
})
df_tweets.to_csv("AIEngineering.csv", index=False)
print(df_tweets.head())

conn.close()
print("\n✅ Tweets saved to both CSV and SQLite database 'AIEngineering.db'.")

time.sleep(5)
