from flask import Flask, request, redirect

app = Flask(__name__)

BOT_KEYWORDS = [
    "bot", "crawl", "spider", "slurp",
    "wget", "curl", "python", "httpclient",
    "headless", "playwright", "puppeteer",
    "selenium", "openai", "anthropic",
    "claude", "cohere", "ai", "llm",
    "monitor", "uptime", "checker"
]

def is_bot(req):
    h = req.headers
    ua = (h.get("User-Agent") or "").lower()

    # 1️⃣ Hard fail: no UA
    if not ua:
        return True

    # 2️⃣ Known bot / AI keywords
    for word in BOT_KEYWORDS:
        if word in ua:
            return True

    # 3️⃣ Must look like a real browser
    if not (
        h.get("Accept") and
        h.get("Accept-Language") and
        h.get("Upgrade-Insecure-Requests")
    ):
        return True

    # 4️⃣ Reject obvious non-browser Accepts
    if h.get("Accept") in ["*/*", "application/json"]:
        return True

    # 5️⃣ Browser engine sanity check
    if not any(x in ua for x in ["chrome", "safari", "firefox", "edg"]):
        return True

    return False


@app.route("/")
def root():
    if is_bot(request):
        return redirect("https://azure.com", code=302)
    else:
        return redirect("https://www.google.com", code=302)


if __name__ == "__main__":
    app.run()
