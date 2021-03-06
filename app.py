import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    counter = ("https://api.countapi.xyz/hit/xactweather.herokuapp.com/" + count_key() + "?callback=cb")
    return render_template('home.html',counter=counter)


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
    description = data["weather"][0]["description"]
    country = data["sys"]["country"]
    icon = data["weather"][0]["icon"]
    icon_link = ("http://openweathermap.org/img/wn/" + icon + ".png")
    return render_template('results.html',
                           location=location, tempf=temp,tempc=celcius, country=country, icon=icon_link,
                           wind=wind,feel_like=feel_like,feels_like=feels_like, weather=weather, description=description)
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def count_key():
    config = configparser.ConfigParser()
    config.read('config.ini') 
    a = config['hit']['api']
    return str(a)

def get_weather_results(area, api_key):
    api_url= 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}'.format(area,api_key)
    
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.debug = True
    app.run()
#https://api.openweathermap.org/data/2.5/weather?q=bela&units=imperial&APPID=9ae2293a430331f38fc645ca26d6b271