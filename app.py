import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    area = request.form['Area']

    api_key = get_api_key()
    data = get_weather_results(area, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    celcius=str(round((float(temp)-32)/2))
    feel_like =str(round((float(feels_like)-32)/2))
    wind = data["wind"]["speed"]
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html',
                           location=location, tempf=temp,tempc=celcius,
                           wind=wind,feel_like=feel_like,feels_like=feels_like, weather=weather)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(area, api_key):
    api_url= 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}'.format(area,api_key)
    
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.debug = True
    app.run()