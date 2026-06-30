import requests, os
from bs4 import BeautifulSoup

URL = "https://www.kgrowth.or.kr/notice.asp?str_type=1&tab=1"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
SEEN_FILE = "seen_idx.txt"

def get_latest_posts():
    res = requests.get(URL)
    res.encoding = "euc-kr"
    soup = BeautifulSoup(res.text, "html.parser")
    posts = []
    for a in soup.select("a[href*='notice_view.asp']"):
        href = a.get("href", "")
        if "idx=" in href:
            idx = href.split("idx=")[1].split("&")[0]
            title = a.get_text(strip=True)
            posts.append((idx, title, "https://www.kgrowth.or.kr/" + href))
    return posts

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

def main():
    try:
        with open(SEEN_FILE) as f:
            seen = set(f.read().split())
    except FileNotFoundError:
        seen = set()

    posts = get_latest_posts()
    new_posts = [p for p in posts if p[0] not in seen]

    for idx, title, link in new_posts:
        send_telegram(f"[출자공고] {title}\n{link}")
        seen.add(idx)

    with open(SEEN_FILE, "w") as f:
        f.write("\n".join(seen))

if __name__ == "__main__":
    main()
