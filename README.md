# Digikala Laptop Scraper 🛒💻

A Python web scraper that collects laptop listings (title, price, rating, and product images links) from Digikala search result pages, cleans the data, saves it to CSV, and shows a quick data-quality summary.

---

## ✨ Features

- Scrape laptop search results from Digikala (paginated).
- Extracts per product:
  - 🏷️ Title (Persian)
  - 💰 Price
  - ⭐ Rating
  - 🔗 Product URL
- Cleans and normalizes prices (removes separators, converts to numeric).
- Removes duplicates and empty rows.
- Saves results to a timestamped **CSV** file.

---

## 📁 Project Structure

```
digikala-laptop-scraper/
│
├── Digikala.py            # Main scraping script
├── requirements.txt      # Python dependencies
├── Digikala_Laptop.csv           # Output data (generated)
└── README.md             # This file
```

---

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/ArtaMohammadbeigi/digikala-scraper.git
cd digikala-laptop-scraper
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the scraper:

```bash
python scraper.py
```

Example output:

```
Scraping page 1 ... done (24 items)
Scraping page 2 ... done (24 items)
Saved 48 rows to laptops.csv
```

The results are saved as `Digikala_Laptop.csv` in the project folder.

---

## 📊 Output Format (`Digikala_Laptop.csv`)

| Column      | Type   | Description                          |
|-------------|--------|--------------------------------------|
| `title`     | str    | Laptop name (Persian)                |
| `price`     | int    | Price in Toman (numeric)             |
| `rating`    | float  | Average user rating                  |
| `url`       | str    | Link to the product page on Digikala |

---

## 🧰 Tech Stack

- **Python 3.9+**
- `requests` – HTTP requests
- `BeautifulSoup4` – HTML parsing
- `pandas` – data cleaning & CSV export
- `time` / `random` – polite scraping delays

---

## 📦 requirements.txt

```text
requests
beautifulsoup4
pandas
lxml
```

---

## 🔧 Configuration

At the top of `Digikala.py` you can adjust:

```python
BASE_URL   = "https://www.digikala.com/"
```

- Increase `MAX` for more data.
- Keep the delay reasonable — don't hammer the server.
---

## 🧪 Data Cleaning Steps

1. Strip whitespace from text fields.
2. Convert price strings like `"45,500,000"` to integers.
3. Drop rows with missing titles or prices.
4. Drop duplicate products (by URL).
5. Reset the DataFrame index and export to CSV with `utf-8` encoding (so Persian text opens correctly in Excel).

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

Created by **<Arta Mohammadbeigi>** — feel free to reach out!

- GitHub: `https://github.com/ArtaMohammadbeigi/`
- Email: `artamohammadbeigi@gmail.com`
- LinkedIn: `https://www.linkedin.com/in/arta-mohammadbeigi/`
