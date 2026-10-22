
import time
import webbrowser
import urllib.request
import uvicorn
import threading


def open_browser():
    url = "http://127.0.0.1:8000/docs"

    while True:
        try:
            urllib.request.urlopen(url, timeout=1)
            webbrowser.open(url)
            break
        except Exception:
            time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
