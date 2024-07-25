import os
import requests
import uuid

import sqlite3
from flask import Flask, render_template, request, session, jsonify
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
WEATHER_FORECAST_API_URL = 'http://api.weatherapi.com/v1/forecast.json'
API_KEY = os.getenv('API_KEY')
app.secret_key = os.getenv('SECRET_KEY')

@app.before_request
def ensure_user_id():
    if not 'user_id' in session:
        session['user_id'] = str(uuid.uuid4())


def insert_data(user_id, city):
    try:
        conn = sqlite3.connect('search_history.db')
        cursor = conn.cursor()
        query = 'INSERT INTO user_search (user_id, city) VALUES (?, ?)'
        cursor.execute(query, (user_id, city))
        conn.commit()
        session['last_city'] = city
    except Exception as e:
        print('Error: ', e)
    finally:
        conn.close()

def fetch_weather(city):
    response = requests.get(
        WEATHER_FORECAST_API_URL, 
        params={'key': API_KEY, 'q': city}
    )
    if response.status_code == 200:
        return response.json()
    return None

def parse_weather_data(data):
    forecast = {}
    current_weather = data.get('current')
    if current_weather:
        forecast['текущая погода'] = {
            'температура': current_weather.get('temp_c'), 
            'время последнего обновления': current_weather.get('last_updated'), 
            'состояние': current_weather.get('condition').get('text')
        }
    
    forecast_data = data.get('forecast')
    if forecast_data:
        forecastday = forecast_data.get('forecastday')
        if forecastday:
            time = [x.get('time')[-5:] for x in forecastday[0].get('hour')]
            cast = [x.get('temp_c') for x in forecastday[0].get('hour')]
            forecast['прогноз'] = {k: v for k, v in zip(time, cast)}
    return forecast

@app.route('/')
def index():
    last_city = session.get('last_city')
    return render_template('index.html', last_city=last_city)

@app.route('/forecast/', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        city: str = request.form['city']
        weather_data = fetch_weather(city)
        if weather_data:
            forecast = parse_weather_data(weather_data)
            insert_data(session.get('user_id'), city)
            return render_template('weather.html', forecast=forecast, city=city)
        return render_template('weather.html', forecast=None, city=city)

    elif request.method == "GET":
        city = request.args['city']
        weather_data = fetch_weather(city)
        if weather_data:
            insert_data(session.get('user_id'), city)
            forecast = parse_weather_data(weather_data)
            return render_template('weather.html', forecast=forecast, city=city)
        return render_template('weather.html', forecast=None, city=city)
    

@app.get('/api/get_stats')
def get_stats():
    try:
        conn = sqlite3.connect('search_history.db')
        cursor = conn.cursor()
        cursor.execute('SELECT city, COUNT(*) as count FROM user_search GROUP BY city')
        stats = cursor.fetchall()
    except Exception as e:
        print('Error: ', e)
    finally:
        conn.close()
    return jsonify([{'city': city, 'count': count} for city, count in stats])


if __name__ == '__main__':
    app.run(debug=False)
