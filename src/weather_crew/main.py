#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from crew import WeatherCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the research crew.
    """
    inputs = {
        "location": "Milan",  # This will be passed directly to the get_weather function
        "date": "today",
    }

    # Create and run the crew
    try:
        output = WeatherCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # Print the result
    print(output)


if __name__ == "__main__":
    run()
