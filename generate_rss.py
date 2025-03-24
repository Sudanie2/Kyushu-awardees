import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
    fe.pubDate(datetime.now().isoformat())

fg.rss_file('rss.xml')
