# Flask Weather App

A simple and elegant weather application built with Flask. Enter a city name and get current weather information with weather emojis. Powered by **Open-Meteo API** - completely free, no API key required!

## Features

- ✅ Search weather by city name
- ✅ Display current temperature, weather condition, humidity, wind speed
- ✅ Weather emojis for visual representation
- ✅ Responsive design for mobile and desktop
- ✅ Error handling and user feedback
- ✅ Beautiful gradient UI with animations
- ✅ **No API key needed!** Uses Open-Meteo free API

## Project Structure

```
Flask_Weather_App/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key)
├── .gitignore               # Git ignore file
├── README.md                # This file
├── templates/
│   └── index.html           # Main HTML template
└── static/
    ├── css/
    │   └── style.css        # Styling
    └── js/
        └── script.js        # Frontend logic
```

## Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd Flask_Weather_App

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Run the Flask development server
python app.py
```

The app will start on `http://localhost:5000`

## Usage

1. Open your browser and go to `http://localhost:5000`
2. Enter a city name in the search box (e.g., "London", "New York", "Tokyo")
3. Click the "Search" button
4. View the current weather with icon, temperature, and additional details

## Technologies Used

- **Backend**: Flask 2.3.3 (Python web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **APIs**: 
  - [Open-Meteo](https://open-meteo.com/) for weather data (free, no API key)
  - Open-Meteo Geocoding API for location lookup
- **No external dependencies for API calls!**

## API Endpoints

### GET `/`
Renders the main weather app page

### POST `/get_weather`
Fetches weather data for a specified city

**Request Body:**
```json
{
  "city": "London"
}
```

**Response (Success - 200):**
```json
{United Kingdom",
  "temperature": 15,
  "description": "Partly Cloudy",
  "emoji": "⛅",
  "humidity": 72,
  "wind_speed": 3.5,
  "coordinates": "51.5085, -0.1257: 3.5,
  "pressure": 1013,
  "icon": "04d"
}
```

**Response (Error - 404):**
```json
{
  "error": "City not found"
}
```

## Features Explained

### Frontend
- Clean, modern UI with gradient background
- Real-time weather icon display
- Responsive design that works on mobile and desktop
- Loading spinner duemoji display
- Responsive design that works on mobile and desktop
- Loading spinner during API calls
- Error handling with user-friendly messages
- Automatic input clearing after successful search

### Backend
- Flask routes for serving pages and API
- Open-Meteo API integration (no API key required!)
- Geocoding for city name to coordinates conversion
- Weather code to description mapping with emojis
- Error handling for invalid cities and API failures
- JSON response format for easy frontend integration

### Change Temperature Unit
In `app.py`, change the `units` parameter:
- `metric` = Celsius (deftemperature_unit` parameter:
- `celsius` = Celsius (default)
- `fahrenheit` = Fahrenheit

### Change Styling
Edit `static/css/style.css` to customize colors, fonts, and layout.

### Add More Weather Details
Modify the `WEATHER_CODES` dictionary in `app.py` to add more weather codes, or adjust which fields are returned in the API response
## Troubleshooting

### "City not found" error
- Check the spelling of the city name
- Try using the city's full name (e.g., "San Francisco" instead of "SF")

- Some small towns may not be in the database

### "Unable to fetch weather data" error
- Check your internet connection
- Open-Meteo API servers might be temporarily unavailable
- Try again in a few moments

### Port 5000 already in use
Flask defaults to port 5000. To use a different port, modify the last line in `app.py`:
```python
# Change to:
`

## Future Enhancements

- 🔄 Weather forecast for upcoming days
- 📍 Geolocation-based weather
- 💾 Search history
- ⭐ Save favorite cities
- 🌍 Multiple language support
- 📊 Weather charts and graphs
- 🔔 Weather alerts

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check:
1. Your API key is corr:
1. Check your internet connection
2. Verify city name spelling
3. Ensure Flask is running on the correct port
4. All dependencies are installed via `pip install -r requirements.txt`

## Why Open-Meteo?

Open-Meteo was chosen for this project because:
- ✅ **No API key required** - Start using immediately!
- ✅ **Free and open-source** - Sustainable and transparent
- ✅ **Excellent documentation** - Easy to understand and implement
- ✅ **Fast and reliable** - Built for performance
- ✅ **No rate limits** for reasonable use
- ✅ **Global coverage** - Access to weather data worldwide

Learn more at [open-meteo.com](https://open-meteo.com/)
Enjoy checking the weather! ☀️🌤️⛅
