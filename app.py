import requests
import os

from flask import Flask, render_template

API_KEY = os.environ["API_KEY"]
BASE_URL = "https://api.openweathermap.org/data/2.5"
CITY = "minsk"
LAT = 53.8930
LON = 27.5674

app = Flask(__name__,
            static_url_path="",
            static_folder="static",
            template_folder="templates")


@app.route("/")
def initial():
    return render_template("index.html", message="This is my weather application of Flask.")


@app.route("/current")
def current():
    try:
        response = requests.get(f"{BASE_URL}/weather?q={CITY}&units=metric&appid={API_KEY}")
        response.raise_for_status()
        data = response.json()

        weather ={
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
        return data
    except (requests.exceptions.RequestException, requests.exceptions.RequestException) as error:
        return f"Error: {error}"


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html", message=error), 404


if __name__ == '__main__':
    app.run()
