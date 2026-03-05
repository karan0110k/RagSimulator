import requests
import time

time.sleep(2) # Give server time to start

print("--- Uploading sample.pdf ---")
url_upload = "http://127.0.0.1:5001/api/upload"
with open("sample.pdf", "rb") as f:
    files = {"file": ("sample.pdf", f, "application/pdf")}
    try:
        res = requests.post(url_upload, files=files)
        print("Upload Response:", res.json())
    except Exception as e:
        print("Upload error:", e)

print("\n--- Asking question ---")
url_ask = "http://127.0.0.1:5001/api/ask"
try:
    res = requests.post(url_ask, json={"query": "What is the answer to life according to the uploaded document?"})
    print("Ask Response:", res.json())
except Exception as e:
    print("Ask error:", e)
