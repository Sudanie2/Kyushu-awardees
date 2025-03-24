import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone  # ← 追加
import hashlib
from feedgen.feed import FeedGenerator

URL = 'https://pr-platform.kyushu-u.ac.jp/research/research-topics/research-results/'

res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

fg = FeedGenerator()
fg.id('https://example.com/research-feed')
fg.title('九州大学 研究成果 新着RSS')
fg.link(href='https://pr-platform.kyushu-u.ac.jp/research/research-topics/research-results/')
fg.language('ja')

fg.description('九州大学の研究成果に関する新着情報フィード')

for title_main, title_sub in zip(
    soup.select('.c-title__main'),
    soup.select('.c-title__sub')
):
    full_title = title_main.text.strip()
    sub_title = title_sub.text.strip()
    full_text = f"{full_title}｜{sub_title}"

    fe = fg.add_entry()
    fe.id(hashlib.md5(full_text.encode()).hexdigest())
    fe.title(full_title)
    fe.description(sub_title)
    fe.link(href='https://pr-platform.kyushu-u.ac.jp/research/research-topics/research-results/')
    fe.pubDate(datetime.now(timezone.utc))  # ← 修正

fg.rss_file('rss.xml')
