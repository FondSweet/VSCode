from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API URLs
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Weather code to description mapping
WEATHER_CODES = {
    0: ("Clear", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Foggy", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Moderate Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌦️"),
    61: ("Slight Rain", "🌧️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Slight Snow", "❄️"),
    73: ("Moderate Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    77: ("Snow Grains", "❄️"),
    80: ("Slight Rain Showers", "🌧️"),
    81: ("Moderate Rain Showers", "🌧️"),
    82: ("Violent Rain Showers", "🌧️"),
    85: ("Slight Snow Showers", "❄️"),
    86: ("Heavy Snow Showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Hail", "⛈️"),
    99: ("Thunderstorm with Hail", "⛈️"),
}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    """Fetch weather data for a city using Open-Meteo API"""
    try:
        data = request.get_json()
        city = data.get('city', '').strip()
        
        if not city:
            return jsonify({'error': 'Please enter a city name'}), 400
        
        # Step 1: Geocode the city name to get coordinates
        geocoding_params = {
            'name': city,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        
        geocoding_response = requests.get(GEOCODING_URL, params=geocoding_params)
        
        if geocoding_response.status_code != 200:
            return jsonify({'error': 'Unable to find city'}), 500
        
        geocoding_data = geocoding_response.json()
        
        if not geocoding_data.get('results') or len(geocoding_data['results']) == 0:
            return jsonify({'error': 'City not found'}), 404
        
        location = geocoding_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        city_name = location['name']
        country = location.get('country', '')
        
        # Step 2: Get weather data using coordinates
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,visibility,uv_index',
            'hourly': 'temperature_2m,weather_code,precipitation,wind_speed_10m,uv_index',
            'daily': 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum,sunrise,sunset,uv_index_max',
            'timezone': 'auto',
            'temperature_unit': 'celsius'
        }
        
        weather_response = requests.get(WEATHER_URL, params=weather_params)
        
        if weather_response.status_code != 200:
            return jsonify({'error': 'Unable to fetch weather data'}), 500
        
        weather_data = weather_response.json()
        current = weather_data['current']
        
        # Get weather description and emoji from weather code
        weather_code = current['weather_code']
        description, emoji = WEATHER_CODES.get(weather_code, ("Unknown", "❓"))
        
        # Parse hourly data (next 24 hours)
        hourly_data = weather_data.get('hourly', {})
        hourly_times = hourly_data.get('time', [])
        hourly_temps = hourly_data.get('temperature_2m', [])
        hourly_codes = hourly_data.get('weather_code', [])
        hourly_precip = hourly_data.get('precipitation', [])
        hourly_wind = hourly_data.get('wind_speed_10m', [])
        hourly_uv = hourly_data.get('uv_index', [])
        
        # Get next 24 hours
        hourly_forecast = []
        for i in range(min(24, len(hourly_times))):
            time = hourly_times[i]
            hour = time.split('T')[1].split(':')[0]  # Extract hour from "2024-01-01T14:00"
            code = hourly_codes[i]
            desc, emj = WEATHER_CODES.get(code, ("Unknown", "❓"))
            uv_value = hourly_uv[i] if i < len(hourly_uv) and hourly_uv[i] is not None else 'N/A'
            hourly_forecast.append({
                'time': f"{hour}:00",
                'temperature': round(hourly_temps[i]),
                'description': desc,
                'emoji': emj,
                'precipitation': round(hourly_precip[i], 1),
                'wind_speed': round(hourly_wind[i], 1),
                'uv_index': round(uv_value, 1) if isinstance(uv_value, (int, float)) else uv_value
            })
        
        # Parse daily data (7 days)
        daily_data = weather_data.get('daily', {})
        daily_times = daily_data.get('time', [])
        daily_max_temps = daily_data.get('temperature_2m_max', [])
        daily_min_temps = daily_data.get('temperature_2m_min', [])
        daily_codes = daily_data.get('weather_code', [])
        daily_precip = daily_data.get('precipitation_sum', [])
        daily_sunrise = daily_data.get('sunrise', [])
        daily_sunset = daily_data.get('sunset', [])
        daily_uv = daily_data.get('uv_index_max', [])
        
        # Get 7-day forecast
        daily_forecast = []
        for i in range(min(7, len(daily_times))):
            date = daily_times[i]
            code = daily_codes[i]
            desc, emj = WEATHER_CODES.get(code, ("Unknown", "❓"))
            sunrise_time = daily_sunrise[i].split('T')[1]  # Extract time
            sunset_time = daily_sunset[i].split('T')[1]
            daily_forecast.append({
                'date': date,
                'max_temp': round(daily_max_temps[i]),
                'min_temp': round(daily_min_temps[i]),
                'description': desc,
                'emoji': emj,
                'precipitation': round(daily_precip[i], 1),
                'sunrise': sunrise_time,
                'sunset': sunset_time,
                'uv_index': round(daily_uv[i], 1)
            })
        
        # Extract relevant data
        result = {
            'city': city_name,
            'country': country,
            'temperature': round(current['temperature_2m']),
            'description': description,
            'emoji': emoji,
            'humidity': current['relative_humidity_2m'],
            'wind_speed': round(current['wind_speed_10m'], 1),
            'visibility': round(current['visibility'] / 1000, 1),  # Convert to km
            'uv_index': round(current['uv_index'], 1),
            'coordinates': f"{latitude}, {longitude}",
            'hourly_forecast': hourly_forecast,
            'daily_forecast': daily_forecast
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
