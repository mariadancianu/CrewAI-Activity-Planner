import datetime
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


def get_supported_locations(url: str) -> Dict[str, Any]:
    """Gets the supported cities for which the activity planner is available.

    Args:
      url: str
        AccuWeather API endpoint URL.
    Returns:
      supported_cities_dict: Dict[str, Any]
        Supported cities with their location keys and localized names.

    """

    url = f"{url}/locations/v1/topcities/150?apikey={ACCUWEATHER_API_KEY}"

    top_cities_data = get_json_data(url)

    supported_locations = [
        {
            "city_name": city["LocalizedName"],
            "country_name": city["Country"]["LocalizedName"],
            "administrative_area_name": city["AdministrativeArea"]["LocalizedName"],
        }
        for city in top_cities_data
    ]
    return supported_locations


def accuweather_get_forecast(url: str, location_id: int) -> Dict[str, Any]:
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

    days = 5
    url = (
        f"{url}/forecasts/v1/daily/{days}day/{location_id}?apikey={ACCUWEATHER_API_KEY}"
    )
    data = get_json_data(url)

    # with open(f"test_weather_data_{days}day.json", "w") as f:
    #    json.dump(data, f, indent=4)

    daily_forecasts_list = data.get("DailyForecasts", [])

    weather_forecast_list = []

    for daily_forecast in daily_forecasts_list:
        date = daily_forecast["Date"]
        date_format = "%Y-%m-%dT%H:%M:%S%z"

        date = datetime.datetime.strptime(date, date_format).strftime("%Y-%m-%d")

        daily_weather_text = daily_forecast["Day"]["IconPhrase"]

        temperature_min = (
            daily_forecast.get("Temperature", {}).get("Minimum", {}).get("Value", None)
        )
        temperature_max = (
            daily_forecast.get("Temperature", {}).get("Maximum", {}).get("Value", None)
        )

        # convert fahrenheit to celsius
        if temperature_min is not None:
            temperature_min = (temperature_min - 32) * 5 / 9
            temperature_min = round(temperature_min)

        if temperature_max is not None:
            temperature_max = (temperature_max - 32) * 5 / 9
            temperature_max = round(temperature_max)

        weather_forecast_list.append(
            {
                "Date": date,
                "temperature_min": temperature_min,
                "temperature_max": temperature_max,
                "weather_text": daily_weather_text,
            }
        )

    # weather_forecast_dict["weather_text"] = daily_weather_text
    # weather_forecast_dict["temperature_min"] = temperature_min
    # weather_forecast_dict["temperature_max"] = temperature_max

    return weather_forecast_list


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
def get_weather(
    city: str = "Milan",
    country: str = "IT",
    administrative_area_localized_name: str = "Lombardy",
    start_date: str = "2025-03-27",
    end_date: str = "2025-03-29",
) -> Dict[str, Any]:
    """
    Get weather forecast for the given city.

    Args:
        city: str
          The name of the city to get weather for (e.g., "Milan", "Rome")
        country_id: str, optional, Default= 'IT'
          AccuWeather ID of the country where of the city. Here we limit
          the search to Italy only. To change this check out the AccuWeather
          API documentation.
        administrative_area_localized_name: str, optional, Default = 'Lombardy'
          AccuWeather localized name of the administrative area of the
          city. To change this check out the AccuWeather API documentation.
        start_date: str, optional, Default = '2024-03-20'
          Desired start date for the weather forecast.
        end_date: str, optional, Default = '2024-03-20'
          Desired end date for the weather forecast.

    Returns:
    result: Dict[str, Any]
        Weather forecast for the next day, including:
            - "weather_text" (str): Text description of the weather.
            - "temperature_min" (int): Minimum temperature in Celsius.
            - "temperature_max" (int): Maximum temperature in Celsius.
    """

    # The weather forecast must be in the future from today and not more than 5 days in the future.
    # (due to free AccuWeather API's limitations)
    start_date_min = datetime.date.today()
    end_date_max = datetime.date.today() + datetime.timedelta(days=5)

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    print(f"Start date min allowed {start_date_min}")
    print(f"End date max allowed {end_date_max}")

    if start_date < start_date_min or start_date > end_date_max:
        print(f"Start date must be between {start_date_min} and {end_date_max}")
        start_date = start_date_min

    if end_date < start_date_min or end_date > end_date_max:
        print(f"End date must be between {start_date_min} and {end_date_max}")
        end_date = end_date_max

    print(
        f"Getting weather forecast for {city}, {country}, {administrative_area_localized_name} between {start_date} and {end_date}"
    )

    endpoint = "http://dataservice.accuweather.com"

    location_id = accuweather_get_city_location_key(
        endpoint,
        city=city,
        country_id=country,
        administrative_area_localized_name=administrative_area_localized_name,
    )
    result = accuweather_get_forecast(endpoint, location_id=location_id)

    for idx, res in enumerate(result):
        date = res["Date"]

        if date < start_date or date > end_date:
            del result[idx]

    # TODO: remove, testing purposes only
    # result = {"temperature_min": "15", "temperature_max": "25", "weather_text": "Rainy"}

    return result


# result = get_weather.run("Milan")
# print(result)
