#!/usr/bin/env python
"""
This is the main file that runs the weather forecasting system.
Make sure to have the necessary environment variables set up for the API keys and other configurations.
"""

import warnings
from typing import List

from src.weather_crew.crew import WeatherCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(
    city: str = "Milan",
    country: str = "IT",
    administrative_area: str = "Lombardy",
    start_date: str = "2024-03-27",
    end_date: str = "2024-03-29",
    user_interests: List = None,
):  # TODO: add support for user interests, this is just a placeholder for now
    """
    Run the weather forecast crew.

    Args:
      location: str, optional, Default = 'Milan'
        Desired city location.
      country: str, optional, Default = 'IT'
        Country ID of the country where of the city.
      administrative_area: str, optional, Default = 'Lombardy'
        Administrative area of the city.
      start_date: str, optional, Default = '2024-03-20'
        Desired start date for the weather forecast.
      end_date: str, optional, Default = '2024-03-20'
        Desired end date for the weather forecast.
      user_interests: List[str], optional, Default = None
        List of personal interests for the activities planner.
    """

    inputs = {
        "city": city,
        "country": country,
        "administrative_area": administrative_area,
        "start_date": start_date,
        "end_date": end_date,
        "user_interests": user_interests,
    }

    output = ""

    # Create and run the crew
    try:
        output = WeatherCrew().crew().kickoff(inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    return output


if __name__ == "__main__":
    run()
