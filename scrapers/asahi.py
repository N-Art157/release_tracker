import feedparser
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

RSS_URL   = "https://www.asahibeer.co.jp/news.rdf"
DATE_RE   = re.compile(r'\d{1,2}月\d{1,2}日')
TABLE_SEL = 'div.news_content_table.is-pattern-B table'


def parse_release_page(url: str) -> dict | None:
    """
    アサヒのリリース HTML を解析し、
    {'発売日', '商品名', '品目', 'リンク'} を返す。
    不要／失敗時は None。
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        res.encoding = 'shift_jis'
    except requests.RequestException:
        return None

    soup  = BeautifulSoup(res.text, 'html.parser')
    table = soup.select_one(TABLE_SEL)
    if not table:
        return None

    data = {'発売日': '', '商品名': '', '品目': '', 'リンク': url}

    for tr in table.find_all('tr'):
        label = tr.th.get_text(strip=True)
        value = ', '.join(td.get_text(strip=True) for td in tr.find_all('td'))

        match label:
            case '商品名':
                data['商品名'] = value
            case '品目':
                data['品目'] = value
            case '発売日':
                data['発売日'] = value
            case '発売地域' if not data['発売日']:
                dates = DATE_RE.findall(value)
                if dates:
                    data['発売日'] = ', '.join(dates)

    return data if DATE_RE.search(data['発売日']) else None


def fetch() -> pd.DataFrame:
    """
    Asahi (アサヒ) の新発売情報を取得して DataFrame を返す。
    列は ['発売日', '商品名', '品目', 'リンク']。
    """
    rows = []
    for entry in feedparser.parse(RSS_URL).entries:
        if '発売' not in entry.get('title', ''):
            continue
        rec = parse_release_page(entry.get('link', ''))
        if rec:
            rows.append(rec)

    return pd.DataFrame(rows)
