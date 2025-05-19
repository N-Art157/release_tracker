import re, datetime as dt, requests, pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support      import expected_conditions as EC

URL_LIST = "https://www.coca-cola.com/jp/ja/media-center"
CARD_CSS = "li.search__list-item"
TITLE_CSS = "h3.single-item__header"
DATE_RE  = re.compile(r'発売日\s*[:：]\s*(\d{4}年\d{1,2}月\d{1,2}日)')
PROD_RE  = re.compile(r'製品名\s*[:：]\s*(.+)')
KIND_RE  = re.compile(r'^品名\s*[:：]\s*(.+)', re.M)

def collect_release_links() -> list[str]:
    """一覧ページを開き『発売』を含むカードのリンクを返す。"""
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    driver = webdriver.Chrome(options=opts)
    wait   = WebDriverWait(driver, 20)

    try:
        driver.get(URL_LIST)

        # Cookie モーダルを閉じる（存在しない場合はスルー）
        try:
            btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'すべて許可する')]")))
            btn.click()
            wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'privacy-settings-modal')]")))
        except Exception:
            pass

        # カード読み込みを待機
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, CARD_CSS)))
        cards = driver.find_elements(By.CSS_SELECTOR, CARD_CSS)

        links: list[str] = []
        for card in cards:
            title = card.find_element(By.CSS_SELECTOR, TITLE_CSS).text
            if "発売" not in title:
                continue
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(link)

        return links
    finally:
        driver.quit()


def parse_detail(url: str) -> dict | None:
    """詳細ページを解析し dict を返す（該当しなければ None）。"""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except requests.RequestException:
        return None

    soup = BeautifulSoup(r.text, "html.parser")
    for block in soup.select("div.text"):
        text = block.get_text("\n", strip=True)
        if not re.match(r'^(?:＜|<)?製品概要', text):
            continue

        product = PROD_RE.search(text)
        kind    = KIND_RE.search(text)
        date    = DATE_RE.search(text)

        if not (product and kind):
            continue
        return {
            "発売日": date.group(1) if date else "",
            "商品名": product.group(1).strip(),
            "品目"  : kind.group(1).strip(),
            "リンク": url,
        }
    return None

def fetch() -> pd.DataFrame:
    """『発売日・商品名・品目・リンク』列の DataFrame を返す。"""
    rows: list[dict] = []

    for url in collect_release_links():
        rec = parse_detail(url)     # 詳細ページを辞書に変換
        if rec is not None:         # 解析に成功した場合だけ追加
            rows.append(rec)

    return pd.DataFrame(rows)
