import re, feedparser, requests, pandas as pd
from bs4 import BeautifulSoup

RSS_URL   = "https://www.kirinholdings.com/jp/newsroom/rss.php"
TABLE_SEL = "table.m-table-common"
DATE_YMD  = re.compile(r"\d{4}年\d{1,2}月\d{1,2}日")
DATE_MD   = re.compile(r"\d{1,2}月\d{1,2}日")


# ------------------------------------------------------------
def parse_kirin_detail(url: str) -> dict | None:
    """詳細ページを解析して dict を返す。失敗時は None。"""
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
    except requests.RequestException:
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # 商品名を含む表を探す
    for table in soup.select(TABLE_SEL):
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if any("商品名" in h for h in headers):
            break
    else:
        return None  # 該当表なし

    product = kind = launch = ""

    for tr in table.find_all("tr"):
        key   = tr.th.get_text(strip=True)
        value = tr.td.get_text("\n", strip=True)

        if "商品名" in key:
            product = value
        elif "品目" in key:
            kind = value
        elif "発売日" in key:
            launch = ", ".join(DATE_YMD.findall(value) or DATE_MD.findall(value))
        elif "販売期間" in key and not launch:
            launch = ", ".join(DATE_YMD.findall(value) or DATE_MD.findall(value))

    return {
        "発売日": launch,
        "商品名": product,
        "品目": kind,
        "リンク": url,
    }


# ------------------------------------------------------------
def fetch() -> pd.DataFrame:
    """Kirin の新発売情報を DataFrame で返す。"""
    rows: list[dict] = []

    for entry in feedparser.parse(RSS_URL).entries:
        if "発売" not in entry.get("title", ""):
            continue
        rec = parse_kirin_detail(entry.get("link", ""))
        if rec:
            rows.append(rec)

    return pd.DataFrame(rows)
