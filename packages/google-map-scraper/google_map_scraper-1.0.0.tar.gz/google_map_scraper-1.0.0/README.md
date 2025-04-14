# 🗺️ Google Maps Business Scraper Appication

This project is a **Web application** that allows users to scrape business information from Google Maps based on a search keyword. The extracted data includes the business name, website, Google Maps link, phone number, and ratings. The results are downloadable in both **JSON** and **CSV** formats.

---

## 🚀 Features

- 🔍 Input any business search keyword (e.g., `restaurant in India`)
- 🧠 Automatically scrapes:
  - Business Name
  - Website
  - Google Maps Link
  - Phone Number
  - Rating & Review Count
- 📁 Downloadable output in both:
  - `results.json`
  - `results.csv`
- ✅ Clean and simple
- 🕵️ Built-in support for scrolling Google Maps listings

---

## Prerequisites

Before running this project, ensure you have the following installed:
- Python (3.6 or higher recommended)
- pip (usually comes with Python)

## 🛠 Installation

1. **Clone this repository**

   ```bash
   git clone https://github.com/mukhtar-ul-islam88/google_map_scraper.git
   
   ```

2.   ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate      
        ```
3. Navigate to the project directory:
   ```bash
   cd Leads_generation_gmap_business
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```



## ✨ Usage Instructions
Type your search keyword (e.g., restaurant India) in the input box.




```bash
from google_maps_scraper import GoogleMapsScraper

scraper = GoogleMapsScraper()
results = scraper.scrape("CA in Hyderabad India")

```

## 📁 Output
-  results.json — full list of businesses

-  results.csv — same in spreadsheet form


## 🧪 Testing
```bash
python tests/test_scraper.py

```

# ❗ Notes
- The scraper uses Selenium with ChromeDriver, make sure Google Chrome is installed.

- Google Maps may temporarily block access if too many requests are made in a short time.

- The scraping process scrolls through Google Maps listings and collects visible information only.