# X (Twitter) Scraper with Selenium + SQLite

This project automates the scraping of tweets from **X (formerly Twitter)** using `Selenium WebDriver`, then saves results in both **SQLite** and **CSV** formats.

---

## 🚀 Features

- **Persistent Login Session**: Reuses a Chrome profile to avoid repeated logins.
- **Manual Login Fallback**: Detects if you're logged out and allows manual login.
- **Flexible Search Query**: Automatically loads a given search between specified date ranges.
- **Automatic Scrolling**: Loads more tweets as you scroll through results.
- **SQLite + CSV Storage**: Saves scraped tweets in both a database and CSV file.
- **Stealth Mode**: Hides automation flags to reduce bot detection.

---

## 🧠 Tech Stack

- **Python 3.9+**
- **Selenium**
- **Pandas**
- **SQLite3**
- **WebDriver Manager**

---

## 🛠️ Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/WanjohiK/Selenium-X-LeadsHarvester.git
   cd Selenium-X-LeadsHarvester
   ```

2. **Install dependencies:**

   ```bash
   pip install selenium pandas webdriver-manager
   ```

3. **(Optional) Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

---

## ⚙️ How It Works

1. When the script starts, it launches Chrome using a **persistent user profile** (`chrome_profile/` folder).
2. It checks whether you’re already logged into X (`https://x.com/home`).
3. If you’re **not logged in**, the script pauses and lets you **log in manually**.
4. Once logged in, it navigates to a **search page** such as:

   ```text
   https://x.com/search?q=looking for an AI engineering job opportunity since:2025-05-25 until:2025-10-27&f=live
   ```

5. It scrolls automatically, extracting tweets containing:
   - Username
   - Tweet text
   - Displayed time
   - Datetime attribute

6. Each tweet is **immediately saved to a SQLite database** and later exported to CSV.

---

## 💾 Output Files

| File | Description |
|------|--------------|
| `AIEngineering.csv` | All scraped tweets in CSV format |
| `machinelearningleads.db` | SQLite database storing tweets |
| `chrome_profile/` | Persistent browser session data |

---

## 📂 SQLite Database Schema

| Column | Type | Description |
|---------|------|-------------|
| `id` | INTEGER | Primary key |
| `user` | TEXT | Username (e.g., @example) |
| `text` | TEXT | Tweet text |
| `displayed_time` | TEXT | Displayed timestamp (relative) |
| `datetime_value` | TEXT | ISO datetime string |
| `search_query` | TEXT | Search phrase used |

---

## 🧩 Key Functions

### `save_tweet_to_db()`
Inserts each tweet directly into the SQLite database.

### `get_tweet()`
Extracts username, text, and time data from each tweet element.

---

## 🧰 Example Use Case

You can modify the following variables to target different search queries or date ranges:

```python
date_since = "2025-01-01"
date_until = "2025-02-01"
search_query = "machine learning engineer"
```

---

## 🧑‍💻 Author

**Kelvin Nyawira**  
AI Engineer | Data Scientist  
📧 [Your Email Here]  
🌐 [Your LinkedIn or GitHub Link]

---

## 🪪 License

This project is licensed under the **MIT License** — you are free to use and modify it as long as you provide attribution.

---

### ⭐ If you find this useful, don’t forget to star the repo!

