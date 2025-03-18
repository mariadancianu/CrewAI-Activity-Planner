import json
import os
import urllib
from typing import Type

from crewai.tools import BaseTool, tool
from crewai.tools.structured_tool import CrewStructuredTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

ACCUWEATHER_API_KEY = os.environ.get("ACCUWEATHER_API_KEY")


def accuweather_get_forecast_one_day(url, location_id):
    """Get the weather forecast for the next day.

    Args:
      location_id: int
          AccuWeather location key.

    Returns:
      weather_text_to_speech: string
          Weather forecast for the next day and the desired city.
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


def get_json_data(url):
    """Gets the json data through an API.

    Args:
      url: string
          URL of the API.

    Returns:
      data: json
          Data returned by the API in the json format.
    """

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    return data


def accuweather_get_city_location_key(
    url,
    city="Milan",
    country_id="IT",
    administrative_area_localized_name="Lombardy",
):
    """The AccuWeather API forecast searches require a location key.
    Here we get the location key for the desired city.

    Args:
      city: string, optional, Default = 'Milan'
          Desired city location.
      country_id: str, optional, Default= 'IT'
          AccuWeather ID of the country where of the city. Here we limit
          the search to Italy only. To change this check out the AccuWeather
          API documentation.
      administrative_area_localized_name: str, optional, Default = 'Lombardy'
          AccuWeather localized name of the administrative area of the
          city. To change this check out the AccuWeather API documentation.

    Returns:
      location_id: int
          AccuWeather location key.
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


"""
# Define the schema for the tool's input using Pydantic
class APICallInput(BaseModel):
    endpoint: str
    parameters: dict

# Wrapper function to execute the API call
def tool_wrapper(*args, **kwargs):
    # Here, you would typically call the API using the parameters
    # For demonstration, we'll return a placeholder string

    city = kwargs.get("parameters", {}).get("location", "Milan")
    location_id = accuweather_get_city_location_key(kwargs["endpoint"], city=city)
    result = accuweather_get_forecast_one_day(kwargs["endpoint"], location_id=location_id)

    return result

# Create and return the structured tool
def create_structured_tool():
    return CrewStructuredTool.from_function(
        name='Wrapper API',
        description="A tool to wrap API calls with structured input.",
        args_schema=APICallInput,
        func=tool_wrapper,
    )

weather_api_tool = create_structured_tool()

# Execute the tool with structured input
# TODO: allow date input
result = weather_api_tool._run(**{
    "endpoint": "http://dataservice.accuweather.com",
    "parameters": {"location": "Milan",
                  # "key2": "value2"
                  }
})

print("*** Result 1")
print(result) """


@tool("get_weather")
def get_weather(city: str = "Milan") -> dict:
    """
    Get weather forecast for the given city.

    Args:
        city (str): The name of the city to get weather for (e.g., "Milan", "Rome")

    Returns:
        dict: Weather information including temperature and conditions
    """

    # endpoint = "http://dataservice.accuweather.com"
    # location_id = accuweather_get_city_location_key(endpoint, city=city)
    # result = accuweather_get_forecast_one_day(endpoint, location_id=location_id)

    result = {"forecast": "sunny"}

    return result


# print("*** Result 2")
# result = get_weather.run("Milan")
# print(result)
