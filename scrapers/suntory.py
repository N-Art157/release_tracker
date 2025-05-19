from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd

def fetch_news_urls():
    """
    サントリーのニュースページから「発売」を含む記事のURLを取得する。
    """
    URL = "https://www.suntory.co.jp/news"
    opts = webdriver.ChromeOptions()
    # opts.add_argument("--headless=new")  # バックグラウンド実行したい場合に有効化
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 20)

    driver.get(URL)
    CARD_CSS = "div.articles_list dl.article_wrap"
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CARD_CSS)))
    cards = driver.find_elements(By.CSS_SELECTOR, CARD_CSS)

    urls = []
    for card in cards:
        article_element = card.find_element(By.CSS_SELECTOR, "div.ttl_article a")
        title = article_element.text
        if "発売" in title:
            urls.append(article_element.get_attribute("href"))

    driver.quit()
    return urls

def extract_product_info(url):
    """
    記事ページから商品情報を抽出する。
    """
    opts = webdriver.ChromeOptions()
    # opts.add_argument("--headless=new")  # バックグラウンド実行したい場合に有効化
    driver = webdriver.Chrome(options=opts)
    wait = WebDriverWait(driver, 20)

    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 「記」を含む段落をゆるく探す
    marker = soup.find("p", string=lambda s: s and "記" in s.strip())
    if not marker:
        driver.quit()
        return None

    product = None
    kind = ""
    launch_date = ""

    for sib in marker.find_next_siblings():
        text = sib.get_text(" ", strip=True)
        if text.startswith("以上"):
            break

        if sib.name == "table":
            table_rows = sib.select("tr")
            headers = [th.get_text(strip=True) for th in table_rows[0].find_all("th")]

            if "商品名" in headers:
                product = " / ".join(
                    tr.find("td").get_text(strip=True)
                    for tr in table_rows[1:]
                    if tr.find("td")
                )

        elif text.startswith("▼商品"):
            m = re.search(r'「(.+?)」', text)
            if m:
                product = m.group(1)

        elif text.startswith("▼発売期日"):
            m = re.match(r"▼発売期日[\s　：]+(.+)", text)
            if m:
                launch_date = m.group(1)

        elif text.startswith("▼品目"):
            m = re.match(r"▼品目[\s　：]+(.+)", text)
            if m:
                kind = m.group(1)

    driver.quit()

    if product:
        return {
            '発売日': launch_date,
            '商品名': product,
            '品目': kind,
            'リンク': url
        }
    return None

def fetch():
    """
    サントリーのニュースページから「発売」を含む記事の商品情報を取得し、データフレームにまとめる。
    """
    urls = fetch_news_urls()
    rows = []

    for url in urls:
        product_info = extract_product_info(url)
        if product_info:
            rows.append(product_info)

    return pd.DataFrame(rows)

