import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import hashlib
from feedgen.feed import FeedGenerator

# 対象ページ（九州大学 研究成果）
URL = 'https://pr-platform.kyushu-u.ac.jp/research/research-topics/research-results/'
KEYWORD = '受賞'  # 抽出対象キーワード

# ページ取得＆解析
res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

# フィード基本情報
fg = FeedGenerator()
fg.id('https://your-domain.example/rss')  # 固有ID（ダミーでもOK）
fg.title('九州大学 研究成果 RSS - 受賞のみ')
fg.link(href=URL)
fg.language('ja')
fg.description('九州大学 研究成果ページから「受賞」に関する記事だけを配信するRSSフィード')

# 記事の抽出とフィルター
for title_main, title_sub in zip(
    soup.select('.c-title__main'),
    soup.select('.c-title__sub')
):
    full_title = title_main.text.strip()
    sub_title = title_sub.text.strip()
    full_text = f"{full_title} {sub_title}"

    # 「受賞」が含まれないものはスキップ
    if KEYWORD not in full_text:
        continue

    fe = fg.add_entry()
    fe.id(hashlib.md5(full_text.encode()).hexdigest())
    fe.title(full_title)
    fe.description(sub_title)
    fe.link(href=URL)  # 個別記事リンクがあればここに差し替え可
    fe.pubDate(datetime.now(timezone.utc))

# RSSファイルとして出力
fg.rss_file('rss.xml')
