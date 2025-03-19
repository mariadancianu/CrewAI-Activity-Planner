#!/usr/bin/env python
"""
This is the main file that runs the weather forecasting system.
Make sure to have the necessary environment variables set up for the API keys and other configurations.
"""

import warnings

from crew import WeatherCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the weather forecast crew.
    """

    inputs = {
        "location": "Milan",  # This will be passed directly to the get_weather function
        "date": "2024-03-20",  # TODO: add support for dates input, this is just a placeholder for now
    }

    # Create and run the crew
    try:
        output = WeatherCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
