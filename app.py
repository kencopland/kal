from flask import Flask, request, redirect, abort, make_response
import time

app = Flask(__name__)

TARGET_URL = "https://www.google.com"

BOT_KEYWORDS = [
    "bot", "crawler", "spider", "scrapy",
    "curl", "wget", "python-requests",
    "httpclient", "go-http-client",
    "headless", "phantom", "selenium"
]

REQUIRED_HEADERS = [
    "User-Agent",
    "Accept",
    "Accept-Language",
    "Accept-Encoding",
]

def looks_like_bot(req):
    ua = req.headers.get("User-Agent", "").lower()

    if not ua:
        return True

    if any(b in ua for b in BOT_KEYWORDS):
        return True

    for h in REQUIRED_HEADERS:
        if h not in req.headers:
            return True

    now = time.time()
    last = req.cookies.get("t")
    if last:
        try:
            if now - float(last) < 0.3:
                return True
        except ValueError:
            return True

    return False


@app.route("/")
def main():
    if looks_like_bot(request):
        return abort(403)

    response = make_response(redirect(TARGET_URL, code=302))
    response.set_cookie("t", str(time.time()), httponly=True, secure=True)
    return response


@app.errorhandler(403)
def forbidden(_):
    return "Access denied", 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
