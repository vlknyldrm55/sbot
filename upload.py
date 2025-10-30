import requests
import base64

# 🔐 GitHub tokenın
import os
TOKEN = os.getenv("GITHUB_TOKEN")

# 📁 Repo bilgileri
USERNAME = "vlknyldrm55"
REPO = "sbot"
BRANCH = "main"
FILEPATH = "sbot.m3u"

# 📄 M3U dosyasını oku
with open(FILEPATH, "rb") as f:
    content = base64.b64encode(f.read()).decode("utf-8")

# 🔍 GitHub API URL
url = f"https://api.github.com/repos/{USERNAME}/{REPO}/contents/{FILEPATH}"

# 🔐 Header bilgisi
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# 🔄 Dosya var mı kontrol et
r = requests.get(url, headers=headers)
if r.status_code == 200 and "sha" in r.json():
    sha = r.json()["sha"]
    data = {
        "message": "update sbot.m3u",
        "content": content,
        "branch": BRANCH,
        "sha": sha
    }
else:
    data = {
        "message": "add sbot.m3u",
        "content": content,
        "branch": BRANCH
    }

# 🚀 Yükleme işlemi
r = requests.put(url, headers=headers, json=data)
print("Yükleme durumu:", r.status_code)
