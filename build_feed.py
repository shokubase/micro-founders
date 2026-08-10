import json
from xml.sax.saxutils import escape

SITE_URL = "https://YOUR-GITHUB-USERNAME.github.io/YOUR-REPO-NAME/"  # TODO: 실제 배포 URL로 교체

cases = json.load(open("data/cases.json", encoding="utf-8"))
cases.sort(key=lambda c: c.get("ingested_at", ""), reverse=True)

items = []
for c in cases:
    title = escape(f"{c['product']} — {', '.join(c.get('founders') or [])}")
    desc = escape(c.get("one_liner", ""))
    link = SITE_URL
    guid = f"{SITE_URL}#{c['id']}"
    pub_date = c.get("ingested_at", "")
    items.append(f"""  <item>
    <title>{title}</title>
    <link>{link}</link>
    <guid isPermaLink="false">{guid}</guid>
    <description>{desc}</description>
    <pubDate>{pub_date}</pubDate>
  </item>""")

rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>바이브코딩 창업 사례 DB — 신규 사례</title>
  <link>{SITE_URL}</link>
  <description>1인/소규모 팀 AI 창업 사례 아카이브에 새로 추가된 사례</description>
{chr(10).join(items)}
</channel>
</rss>
"""

with open("feed.xml", "w", encoding="utf-8") as f:
    f.write(rss)

print(f"Wrote feed.xml with {len(cases)} items")
