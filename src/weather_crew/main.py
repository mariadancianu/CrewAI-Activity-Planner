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
    location: str = "Milan",
    date: str = "2024-03-20",  # TODO: add support for dates input, this is just a placeholder for now):
    user_interests: List = None,
):  # TODO: add support for user interests, this is just a placeholder for now
    """
    Run the weather forecast crew.

    Args:
      location: str, optional, Default = 'Milan'
        Desired city location.
      date: str, optional, Default = '2024-03-20'
        Desired date for the weather forecast.
      user_interests: List[str], optional, Default = None
        List of personal interests for the activities planner.
    """

    inputs = {
        "location": location,
        "date": date,
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
