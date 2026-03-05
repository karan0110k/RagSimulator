import requests

print("--- Uploading document ---")
url_upload = "http://127.0.0.1:5001/api/upload"
with open("test_rag.py", "rb") as f:
    files = {"file": ("test_rag.txt", f, "text/plain")} # Fake PDF upload to trigger logic
    try:
        res = requests.post(url_upload, files=files)
        print(res.json())
    except Exception as e:
        print("Upload error:", e)

print("\n--- Asking question ---")
url_ask = "http://127.0.0.1:5001/api/ask"
try:
    res = requests.post(url_ask, json={"query": "What is the answer to life?"})
    print(res.json())
except Exception as e:
    print("Ask error:", e)
