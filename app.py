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

REQUIRED_HEADERS = [
    "Accept",
    "Accept-Language",
    "User-Agent",
    "Sec-Fetch-Site",
    "Sec-Fetch-Mode",
    "Sec-Fetch-Dest"
]

def is_bot(req):
    headers = req.headers
    ua = (headers.get("User-Agent") or "").lower()

    # 1. Missing required browser headers
    for h in REQUIRED_HEADERS:
        if not headers.get(h):
            return True

    # 2. Obvious bot keywords
    for word in BOT_KEYWORDS:
        if word in ua:
            return True

    # 3. Headless / automation hints
    if "headless" in ua:
        return True

    # 4. Programmatic Accept headers
    accept = headers.get("Accept", "")
    if accept in ["*/*", "application/json"]:
        return True

    # 5. Suspicious fetch behavior
    if headers.get("Sec-Fetch-Site") == "none":
        return True

    return False


@app.route("/")
def root():
    if is_bot(request):
        # BOT DESTINATION
        return redirect("https://azure.com", code=302)
    else:
        # HUMAN DESTINATION
        return redirect("https://www.google.com", code=302)


if __name__ == "__main__":
    app.run()
