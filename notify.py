import requests, os
from bs4 import BeautifulSoup

URL = "https://www.kgrowth.or.kr/notice.asp?str_type=1&tab=1"
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

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
    posts = get_latest_posts()
    target_posts = posts[2:5]   # 3번째~5번째 글만

    for idx, title, link in target_posts:
        send_telegram(f"[출자공고] {title}\n{link}")

if __name__ == "__main__":
    main()
