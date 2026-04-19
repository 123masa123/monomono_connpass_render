from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "DEMO_KEY"

@app.route("/", methods=["GET", "POST"])
def index():
    default_date = "2019-06-06"
    
    # 修正ポイント: フォームから送られてきた値が「空（None or ""）」の場合にデフォルト値を使う
    date = request.form.get("date")
    if not date:
        date = default_date

    url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
    # cameraパラメータを追加すると、より確実に画像を取得しやすくなります（例: mast）
    params = {
        "earth_date": date, 
        "api_key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # エラーがあれば例外を発生させる
        data = response.json()
        # photosキーが存在するかチェック
        photos = [photo["img_src"] for photo in data.get("photos", [])[:4]]
    except Exception as e:
        print(f"Error: {e}")
        photos = []

    return render_template("index.html", photos=photos, date=date)

if __name__ == "__main__":
    app.run(debug=True)