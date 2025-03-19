import json
import os
import urllib
from typing import Any, Dict, Optional

from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

ACCUWEATHER_API_KEY = os.environ.get("ACCUWEATHER_API_KEY")

# TODO: add support for multiple cities and dates


def get_json_data(url: str) -> Dict[str, Any]:
    """Gets the json data through an API.

    Args:
      url: str
        AccuWeather API endpoint URL.

    Returns:
      data: Dict[str, Any]
        Data returned by the API in the json format.
    """

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    return data


def accuweather_get_forecast_one_day(url: str, location_id: int) -> Dict[str, Any]:
    """Get the weather forecast for the next day.

    Args:
      url: str
        AccuWeather API endpoint URL.
      location_id: int
        AccuWeather location key.

    Returns:
      weather_forecast_dict: Dict[str, Any]
        Weather forecast for the next day, including:
            - "weather_text" (str): Text description of the weather.
            - "temperature_min" (int): Minimum temperature in Celsius.
            - "temperature_max" (int): Maximum temperature in Celsius.
    """

    url = f"{url}/forecasts/v1/daily/1day/{location_id}?apikey={ACCUWEATHER_API_KEY}"
    data = get_json_data(url)

    weather_text = data.get("Headline", {}).get("Text", None)
    daily_forecasts_list = data.get("DailyForecasts", [])

    if len(daily_forecasts_list) == 0:
        daily_forecasts_dict = {}
    else:
        daily_forecasts_dict = daily_forecasts_list[0]

    temperature_min = (
        daily_forecasts_dict.get("Temperature", {})
        .get("Minimum", {})
        .get("Value", None)
    )
    temperature_max = (
        daily_forecasts_dict.get("Temperature", {})
        .get("Maximum", {})
        .get("Value", None)
    )

    # convert fahrenheit to celsius
    if temperature_min is not None:
        temperature_min = (temperature_min - 32) * 5 / 9
        temperature_min = round(temperature_min)

    if temperature_max is not None:
        temperature_max = (temperature_max - 32) * 5 / 9
        temperature_max = round(temperature_max)

    weather_forecast_dict = {}
    weather_forecast_dict["weather_text"] = weather_text
    weather_forecast_dict["temperature_min"] = temperature_min
    weather_forecast_dict["temperature_max"] = temperature_max

    return weather_forecast_dict


def accuweather_get_city_location_key(
    url: str,
    city: str = "Milan",
    country_id: str = "IT",
    administrative_area_localized_name: str = "Lombardy",
) -> Optional[int]:
    """The AccuWeather API forecast searches require a location key.
    Here we get the location key for the desired city.

    Args:
      url: str
        AccuWeather API endpoint URL.
      city: str, optional, Default = 'Milan'
        Desired city location.
      country_id: str, optional, Default= 'IT'
        AccuWeather ID of the country where of the city. Here we limit
        the search to Italy only. To change this check out the AccuWeather
        API documentation.
      administrative_area_localized_name: str, optional, Default = 'Lombardy'
        AccuWeather localized name of the administrative area of the
        city. To change this check out the AccuWeather API documentation.

    Returns:
      location_id: Optional[int]
        AccuWeather location key or None if no matching location is found.
    """

    url = f"{url}/locations/v1/cities/{country_id}/search?apikey={ACCUWEATHER_API_KEY}&q={city}"

    location_id = None

    data = get_json_data(url)

    for found_cities in data:
        localized_name = found_cities.get("AdministrativeArea", {}).get(
            "LocalizedName", None
        )

        if localized_name == administrative_area_localized_name:
            location_id = found_cities["Key"]
            break

    return location_id


@tool("get_weather")
def get_weather(city: str = "Milan") -> Dict[str, Any]:
    """
    Get weather forecast for the given city.

    Args:
        city: str
          The name of the city to get weather for (e.g., "Milan", "Rome")

    Returns:
    result: Dict[str, Any]
        Weather forecast for the next day, including:
            - "weather_text" (str): Text description of the weather.
            - "temperature_min" (int): Minimum temperature in Celsius.
            - "temperature_max" (int): Maximum temperature in Celsius.
    """

    # endpoint = "http://dataservice.accuweather.com"
    # location_id = accuweather_get_city_location_key(endpoint, city=city)
    # result = accuweather_get_forecast_one_day(endpoint, location_id=location_id)

    result = {"temperature_min": "15", "temperature_max": "25", "weather_text": "Sunny"}

    return result


# result = get_weather.run("Milan")
# print(result)
