from flask import Flask, request, render_template, send_file
import requests
from bs4 import BeautifulSoup
import io

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=["POST"])
def download():
    url = request.form.get("url")
    if not url:
        return "Instagram URL required", 400

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")
    video_tag = soup.find("meta", property="og:video")

    if not video_tag:
        return "Video not found or private post"

    video_url = video_tag["content"]
    video_data = requests.get(video_url).content

    return send_file(
        io.BytesIO(video_data),
        mimetype="video/mp4",
        as_attachment=True,
        download_name="reel.mp4"
    )

if __name__ == "__main__":
    app.run()

