import requests
import os
import datetime as dt

from flask import Flask, render_template
from config import *

API_KEY = os.environ["API_KEY"]

app = Flask(__name__,
            static_url_path="",
            static_folder="static",
            template_folder="templates")


@app.route("/")
def initial():
    return render_template("index.html", message="This is my weather application on Flask.")


@app.route("/current")
def current():
    try:
        response = requests.get(f"{BASE_URL}/weather?q={CITY}&units=metric&appid={API_KEY}")
        response.raise_for_status()
        data = response.json()

        weather = {
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "name": data["name"],
            "temperature": data["main"]["temp"],
            "wind": data["wind"]["speed"]
        }

        return render_template("index.html", weather=weather)
    except (requests.exceptions.RequestException, requests.exceptions.RequestException) as error:
        return f"Error: {error}"


@app.route("/forecast")
def forecast():
    try:
        response = requests.get(f"{BASE_URL}/forecast?lat={LAT}&lon={LON}&units=metric&appid={API_KEY}")
        response.raise_for_status()
        data = response.json()

        for block in data["list"]:
            date = dt.datetime.strptime(block["dt_txt"], "%Y-%m-%d %H:%M:%S")
            if date < dt.datetime.now() or str(date)[-8:] != "15:00:00":
                data["list"].remove(block)

        forecast_list = []

        for block in data["list"]:
            block_dict = {
                "datetime": block["dt_txt"],
                "temperature": block["main"]["temp"],
                "wind": block["wind"]["speed"],
                "description": block["weather"][0]["description"].title(),
                "icon": block["weather"][0]["icon"]
            }
            forecast_list.append(block_dict)

        return render_template("index.html", forecast_list=forecast_list)
    except (requests.exceptions.RequestException, requests.exceptions.RequestException) as error:
        return f"Error: {error}"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html", message=error), 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
