// DOM Elements
const weatherForm = document.getElementById('weatherForm');
const cityInput = document.getElementById('cityInput');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const weatherContainer = document.getElementById('weatherContainer');

// Event Listeners
weatherForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }
    
    await fetchWeather(city);
});

/**
 * Fetch weather data from the Flask backend
 */
async function fetchWeather(city) {
    try {
        // Show loading state
        showLoading(true);
        hideError();
        weatherContainer.classList.add('hidden');
        
        // Make API request to Flask backend
        const response = await fetch('/get_weather', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ city: city })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'Unable to fetch weather data');
            showLoading(false);
            return;
        }
        
        // Display weather data
        displayWeather(data);
        showLoading(false);
        
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred. Please try again.');
        showLoading(false);
    }
}

/**
 * Display weather data in the UI
 */
function displayWeather(data) {
    // Update location
    document.getElementById('cityName').textContent = data.city;
    document.getElementById('countryCode').textContent = data.country;
    
    // Update temperature
    document.getElementById('temperature').textContent = data.temperature;
    document.getElementById('weatherDescription').textContent = data.description;
    
    // Update weather emoji
    document.getElementById('weatherEmoji').textContent = data.emoji;
    
    // Update current details
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} km/h`;
    document.getElementById('visibility').textContent = `${data.visibility} km`;
    document.getElementById('uvIndex').textContent = data.uv_index;
    document.getElementById('coordinates').textContent = data.coordinates;
    
    // Update sunrise/sunset from first day of forecast (today)
    if (data.daily_forecast && data.daily_forecast.length > 0) {
        const today = data.daily_forecast[0];
        document.getElementById('sunrise').textContent = today.sunrise;
        document.getElementById('sunset').textContent = today.sunset;
    }
    
    // Display hourly forecast
    if (data.hourly_forecast) {
        displayHourlyForecast(data.hourly_forecast);
    }
    
    // Display daily forecast
    if (data.daily_forecast) {
        displayDailyForecast(data.daily_forecast);
    }
    
    // Show weather container
    weatherContainer.classList.remove('hidden');
    
    // Clear input
    cityInput.value = '';
    cityInput.focus();
}

/**
 * Display hourly forecast
 */
function displayHourlyForecast(hourlyData) {
    const container = document.getElementById('hourlyContainer');
    container.innerHTML = '';
    
    hourlyData.forEach(hour => {
        const card = document.createElement('div');
        card.className = 'hourly-card';
        card.innerHTML = `
            <div class="hourly-time">${hour.time}</div>
            <div class="hourly-emoji">${hour.emoji}</div>
            <div class="hourly-temp">${hour.temperature}°C</div>
            <div class="hourly-desc">${hour.description}</div>
            <div class="hourly-precip">💧 ${hour.precipitation}mm</div>
            <div class="hourly-wind">💨 ${hour.wind_speed}km/h</div>
        `;
        container.appendChild(card);
    });
}

/**
 * Display 7-day forecast
 */
function displayDailyForecast(dailyData) {
    const container = document.getElementById('dailyContainer');
    container.innerHTML = '';
    
    dailyData.forEach(day => {
        const date = new Date(day.date);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        const monthDay = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        
        const card = document.createElement('div');
        card.className = 'daily-card';
        card.innerHTML = `
            <div class="daily-date">${dayName}<br>${monthDay}</div>
            <div class="daily-emoji">${day.emoji}</div>
            <div class="daily-description">${day.description}</div>
            <div class="daily-temps">
                <div class="temp-max">↑ ${day.max_temp}°</div>
                <div class="temp-min">↓ ${day.min_temp}°</div>
            </div>
            <div class="daily-details">
                <div class="daily-detail-row">
                    <span>💧 Precip:</span>
                    <span>${day.precipitation}mm</span>
                </div>
                <div class="daily-detail-row">
                    <span>☀️ UV:</span>
                    <span>${day.uv_index}</span>
                </div>
                <div class="daily-detail-row">
                    <span>🌅</span>
                    <span>${day.sunrise}</span>
                </div>
                <div class="daily-detail-row">
                    <span>🌇</span>
                    <span>${day.sunset}</span>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

/**
 * Show loading spinner
 */
function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    errorContainer.classList.add('hidden');
    errorMessage.textContent = '';
}
