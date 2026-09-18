import csv
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver_path = 'chromedriver.exe'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

url: str = 'https://www.digikala.com/'
driver.get(url=url)
driver.maximize_window()
time.sleep(5)

# Search (YOUR ORIGINAL WORKING SEARCH)
search_box = driver.find_element(
    by=By.XPATH,
    value='//*[@id="base_layout_desktop_fixed_header"]/header/div[2]/div/div/div[1]/div/div/div/div/span[1]/label/div',
)
search_box.click()
time.sleep(2)

input_search_box = driver.find_element(
    by=By.XPATH,
    value='/html/body/dk-teleport[2]/div/div/div[1]/div/div/span/label/div/div/input',
)
input_search_box.send_keys('iphone 18')
input_search_box.send_keys(Keys.RETURN)
time.sleep(10)

# Filter price accordion (YOUR ORIGINAL WORKING ACCORDION CLICK)
filter_price_icon = driver.find_element(
    by=By.XPATH,
    value='//*[@id="ProductListPagesWrapper"]/section[2]/div/div[1]/div/div[1]/div[3]/div/div[2]/div/div/div[3]',
)
filter_price_icon.click()
time.sleep(5)

# --- FIXED MIN & MAX PRICE INPUT LOGIC ---
js_set_input = """
let input = arguments[0];
let lastValue = input.value;
input.value = arguments[1];
let event = new Event('input', { bubbles: true });
let tracker = input._valueTracker;
if (tracker) {
    tracker.setValue(lastValue);
}
input.dispatchEvent(event);
input.dispatchEvent(new Event('change', { bubbles: true }));
input.dispatchEvent(new Event('blur', { bubbles: true }));
"""

# Min Price (Using input[name='min'] from DOM)
filter_min_price = driver.find_element(By.XPATH, "//input[@name='min']")
driver.execute_script(js_set_input, filter_min_price, '250000000')
time.sleep(2)

# Max Price (Using input[name='max'] from DOM)
filter_max_price = driver.find_element(By.XPATH, "//input[@name='max']")
driver.execute_script(js_set_input, filter_max_price, '450000000')
time.sleep(2)

# Commit price query
try:
    filter_max_price.send_keys(Keys.RETURN)
except Exception:
    pass

time.sleep(10)

# --- Data Extraction Setup (YOUR ORIGINAL LOOP) ---
collected_products = []
seen_titles = set()
no_new_item_count = 0
MAX_ITEMS = 500

while len(collected_products) < MAX_ITEMS:
    # Find all product cards
    product_cards = driver.find_elements(
        By.XPATH,
        "//*[@id='ProductListPagesWrapper']//article[contains(@class, 'ProductList__item')] | //*[@id='ProductListPagesWrapper']//div[contains(@class, 'ProductList')]//article",
    )

    new_items_found_in_this_step = 0

    for card in product_cards:
        if len(collected_products) >= MAX_ITEMS:
            break

        try:
            # 1. Title
            try:
                title_elem = card.find_element(By.XPATH, './/h3')
                title = title_elem.text.strip()
                if not title:
                    title = 'NULL'
            except Exception:
                title = 'NULL'

            # Avoid duplicates
            if title == 'NULL' or title in seen_titles:
                continue

            # 2. Price
            try:
                # Target price container span/div inside card
                price_elem = card.find_element(
                    By.XPATH,
                    './/div[contains(@class, "pt-1")]//span | .//span[contains(@data-testid, "price")] | .//div[contains(@class, "flex items-center justify-end")]/span',
                )
                price = price_elem.text.strip()
                price = price if price else 'NULL'
            except Exception:
                price = 'NULL'

            # 3. Point (Score/Rating)
            try:
                point_elem = card.find_element(
                    By.XPATH,
                    './/div[2]/div[2]/div[3]/div[2]/p | .//a/div/article/div[2]/div[2]/div[3]/div[2]/p',
                )
                point = point_elem.text.strip()
                point = point if point else 'NULL'
            except Exception:
                point = 'NULL'

            # 4. Image
            image = 'NULL'
            try:
                # Priority 1: Read high-res CDN url from <picture><source srcset="...">
                sources = card.find_elements(By.XPATH, './/picture/source')
                for s in sources:
                    srcset = s.get_attribute('srcset')
                    if (
                        srcset
                        and 'dkstatics-public.digikala.com' in srcset
                    ):
                        image = srcset.split(',')[0].strip().split(' ')[0]
                        break

                # Priority 2: Fallback to <img> tag src / data-src
                if image == 'NULL':
                    img_elem = card.find_element(
                        By.XPATH, './/picture/img | .//img'
                    )
                    img_src = (
                        img_elem.get_attribute('src')
                        or img_elem.get_attribute('data-src')
                        or ''
                    )
                    if (
                        img_src
                        and 'data:image' not in img_src
                        and 'blob:' not in img_src
                    ):
                        image = img_src.split(',')[0].strip().split(' ')[0]
            except Exception:
                image = 'NULL'

            seen_titles.add(title)
            collected_products.append(
                {'title': title, 'price': price, 'point': point, 'image': image}
            )
            new_items_found_in_this_step += 1

        except Exception:
            continue

    print(
        f'Total collected: {len(collected_products)} / {MAX_ITEMS} (New this scroll: {new_items_found_in_this_step})'
    )

    driver.execute_script('window.scrollBy(0, 800);')
    time.sleep(3)

    if new_items_found_in_this_step == 0:
        no_new_item_count += 1
    else:
        no_new_item_count = 0

    # If reached bottom or no new items after multiple scrolls
    if no_new_item_count >= 8:
        print('Reached bottom or no new products loading.')
        break

# --- Save to CSV ---
csv_filename = 'Digikala_Laptop.csv'
headers = ['title', 'price', 'point', 'image']

with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(collected_products)

print('=' * 60)
print(
    f'Saved {len(collected_products)} products successfully into {csv_filename}'
)
print('=' * 60)
