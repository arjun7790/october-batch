
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear Sky ☀️",
    1: "Mainly Clear 🌤️",
    2: "Partly Cloudy ⛅",
    3: "Overcast ☁️",
    45: "Fog 🌫️",
    48: "Fog 🌫️",
    51: "Light Drizzle 🌦️",
    53: "Moderate Drizzle 🌦️",
    55: "Heavy Drizzle 🌧️",
    61: "Light Rain 🌧️",
    63: "Moderate Rain 🌧️",
    65: "Heavy Rain ⛈️",
    71: "Light Snow ❄️",
    73: "Moderate Snow ❄️",
    75: "Heavy Snow ❄️",
    80: "Rain Showers 🌦️",
    81: "Moderate Showers 🌧️",
    82: "Heavy Showers ⛈️",
    95: "Thunderstorm ⛈️",
    96: "Thunderstorm with Hail ⛈️",
    99: "Severe Thunderstorm ⛈️"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeatherNow | Live Weather Report</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            padding: 35px 18px;
            color: white;
            background: linear-gradient(135deg, #101b35, #243b63, #436b91);
        }

        .container {
            max-width: 850px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        header h1 {
            font-size: 34px;
            margin-bottom: 12px;
        }

        header p, .subtitle {
            color: #d3e0f2;
            line-height: 1.6;
        }

        .card {
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 22px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }

        h2 {
            margin-bottom: 10px;
        }

        .subtitle {
            margin-bottom: 22px;
        }

        form {
            display: flex;
            gap: 12px;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 15px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
        }

        button {
            padding: 15px 22px;
            border: none;
            border-radius: 12px;
            background: #f7c969;
            color: #17243c;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
        }

        button:hover {
            background: #ffdc8f;
        }

        .error {
            margin-top: 18px;
            color: #ffd0d0;
            line-height: 1.5;
        }

        .location {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }

        .location p {
            color: #d3e0f2;
            margin-top: 6px;
        }

        .icon {
            font-size: 60px;
        }

        .temperature {
            text-align: center;
            padding: 25px 0;
        }

        .temperature .degrees {
            font-size: 76px;
            font-weight: 300;
        }

        .temperature p {
            margin-top: 8px;
            font-size: 19px;
        }

        .temperature .feels {
            color: #d3e0f2;
            font-size: 14px;
        }

        .details, .forecast {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-top: 20px;
        }

        .detail, .forecast-item {
            background: rgba(255, 255, 255, 0.09);
            border-radius: 15px;
            padding: 20px 10px;
            text-align: center;
            overflow-wrap: anywhere;
        }

        .detail .symbol {
            font-size: 25px;
        }

        .detail p, .forecast-item p {
            color: #d3e0f2;
            font-size: 13px;
            margin: 10px 0;
        }

        .detail h3, .forecast-item h3 {
            font-size: 18px;
        }

        .section-title {
            margin-top: 30px;
        }

        .welcome {
            text-align: center;
            line-height: 1.8;
        }

        .welcome .globe {
            font-size: 55px;
            margin-bottom: 15px;
        }

        .welcome p {
            color: #d3e0f2;
        }

        footer {
            text-align: center;
            color: #d3e0f2;
            font-size: 13px;
            padding: 15px 0;
        }

        @media (max-width: 550px) {
            body {
                padding: 20px 12px;
            }

            .card {
                padding: 20px 15px;
            }

            form {
                flex-direction: column;
            }

            button {
                width: 100%;
            }

            .temperature .degrees {
                font-size: 62px;
            }

            .icon {
                font-size: 43px;
            }

            .details, .forecast {
                gap: 8px;
            }

            .detail, .forecast-item {
                padding: 14px 5px;
            }

            .detail h3, .forecast-item h3 {
                font-size: 14px;
            }

            .detail p, .forecast-item p {
                font-size: 12px;
            }
        }
    </style>
</head>

<body>
    <main class="container">

        <header>
            <h1>☀️ WeatherNow</h1>
            <p>Live weather reports for cities around the world</p>
        </header>

        <section class="card">
            <h2>Check Your Weather</h2>
            <p class="subtitle">Enter a city name to get its live weather.</p>

            <form method="POST">
                <input
                    type="text"
                    name="city"
                    placeholder="Enter city, e.g. Bengaluru"
                    value="{{ city }}"
                    aria-label="City name"
                    required
                >
                <button type="submit">Search Weather</button>
            </form>

            {% if error %}
                <p class="error">{{ error }}</p>
            {% endif %}
        </section>

        {% if weather %}
        <section class="card">

            <div class="location">
                <div>
                    <h2>{{ weather.city }}</h2>
                    <p>{{ weather.country }}</p>
                    <p>Local time: {{ weather.time }}</p>
                </div>
                <div class="icon">{{ weather.icon }}</div>
            </div>

            <div class="temperature">
                <div class="degrees">{{ weather.temperature }}°C</div>
                <p>{{ weather.condition }}</p>
                <p class="feels">
                    Feels like {{ weather.feels_like }}°C
                </p>
            </div>

            <div class="details">
                <div class="detail">
                    <div class="symbol">💧</div>
                    <p>Humidity</p>
                    <h3>{{ weather.humidity }}%</h3>
                </div>

                <div class="detail">
                    <div class="symbol">🌬️</div>
                    <p>Wind Speed</p>
                    <h3>{{ weather.wind }} km/h</h3>
                </div>

                <div class="detail">
                    <div class="symbol">🌧️</div>
                    <p>Precipitation</p>
                    <h3>{{ weather.rain }} mm</h3>
                </div>
            </div>

            <h2 class="section-title">Today's Forecast</h2>

            <div class="forecast">
                <div class="forecast-item">
                    <p>Highest Temperature</p>
                    <h3>{{ weather.max_temp }}°C</h3>
                </div>

                <div class="forecast-item">
                    <p>Lowest Temperature</p>
                    <h3>{{ weather.min_temp }}°C</h3>
                </div>

                <div class="forecast-item">
                    <p>Rain Probability</p>
                    <h3>{{ weather.rain_chance }}{% if weather.rain_chance != 'N/A' %}%{% endif %}</h3>
                </div>
            </div>

        </section>
        {% else %}
        <section class="card welcome">
            <div class="globe">🌍</div>
            <h2>Your City's Weather, At a Glance</h2>
            <p>
                Search any city to discover its current temperature,
                weather conditions, humidity, wind speed and forecast.
            </p>
        </section>
        {% endif %}

        <footer>
            Powered by Open-Meteo | Free Weather Data
        </footer>

    </main>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                # Find the city
                geo_response = requests.get(
                    GEO_URL,
                    params={
                        "name": city,
                        "count": 1,
                        "language": "en",
                        "format": "json"
                    },
                    timeout=10
                )
                geo_response.raise_for_status()

                locations = geo_response.json().get("results", [])

                if not locations:
                    error = "City not found. Please try another city."
                else:
                    place = locations[0]

                    # Fetch current weather and today's forecast
                    response = requests.get(
                        WEATHER_URL,
                        params={
                            "latitude": place["latitude"],
                            "longitude": place["longitude"],
                            "current": (
                                "temperature_2m,relative_humidity_2m,"
                                "apparent_temperature,precipitation,"
                                "weather_code,wind_speed_10m"
                            ),
                            "daily": (
                                "temperature_2m_max,temperature_2m_min,"
                                "precipitation_probability_max"
                            ),
                            "timezone": "auto",
                            "forecast_days": 1
                        },
                        timeout=10
                    )
                    response.raise_for_status()

                    data = response.json()
                    current = data["current"]
                    daily = data["daily"]

                    code = current["weather_code"]
                    condition = WEATHER_CODES.get(
                        code, "Other Weather Conditions"
                    )

                    if code == 0:
                        icon = "☀️"
                    elif code in (1, 2):
                        icon = "🌤️"
                    elif code in (3, 45, 48):
                        icon = "☁️"
                    elif code in (71, 73, 75):
                        icon = "❄️"
                    elif code >= 95:
                        icon = "⛈️"
                    elif code in (51, 53, 55, 61, 63, 65, 80, 81, 82):
                        icon = "🌧️"
                    else:
                        icon = "🌦️"

                    rain_chance = daily[
                        "precipitation_probability_max"
                    ][0]

                    weather = {
                        "city": place["name"],
                        "country": place.get("country", ""),
                        "time": current["time"].replace("T", " "),
                        "temperature": current["temperature_2m"],
                        "feels_like": current["apparent_temperature"],
                        "humidity": current["relative_humidity_2m"],
                        "wind": current["wind_speed_10m"],
                        "rain": current["precipitation"],
                        "condition": condition,
                        "icon": icon,
                        "max_temp": daily["temperature_2m_max"][0],
                        "min_temp": daily["temperature_2m_min"][0],
                        "rain_chance": (
                            rain_chance if rain_chance is not None
                            else "N/A"
                        )
                    }

            except requests.RequestException:
                error = (
                    "Unable to connect to the weather service. "
                    "Check your internet connection and try again."
                )
            except (KeyError, IndexError, TypeError, ValueError):
                error = "Unable to process weather data. Please try again."

    return render_template_string(
        HTML,
        weather=weather,
        error=error,
        city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
