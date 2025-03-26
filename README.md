# CrewAI Agentic AI - Activity Planner based on Weather Forecast

![CrewAI Agentic AI - Weather Assistant](images/img.png)


## 📌 Project Overview


This project explores basic agentic AI workflows using [CrewAI](https://www.crewai.com/) as a hands-on learning experiment. The primary goal is to learn by doing—testing how AI agents can autonomously retrieve and process weather data through API calls while leveraging CrewAI's capabilities for multi-agent collaboration and decision-making. Additionally, the experiment includes web search and scraping for activity planning, where an agent suggests engaging indoor or outdoor activities for a given date and city based on real-time weather forecasts.

## 🎯 Objectives

- Understand CrewAI’s agent-based AI framework, including Crews, Agents, Tasks and Tools.
- Implement a simple AI agent that uses a custom Tool for weather data API calls.
- Explore collaborative agent workflows for enhanced decision-making.

## 🛠️ Tech Stack

- Python (3.12+ recommended)
- CrewAI
- OpenAI API
- [AccuWeather API](https://developer.accuweather.com/) (or any weather API of choice)
- Streamlit


## Details

Key Components:

    src/weather_crew/main.py:
    -> Main script file.


    src/weather_crew/crew.py:
    -> Main crew file where agents and tasks come together, and the main logic is executed.


    src/weather_crew/config/agents.yaml:
    -> Configuration file for defining agents.


    src/weather_crew/config/tasks.yaml:
    -> Configuration file for defining tasks.


    src/weather_crew/tools/custom_tools.py:
    -> Contains custom tools used by the agents.

Upon running the main.py script, the following results are saved:

    src/weather_crew/results/weather_forecast.md:
    -> Weather forecast for the specified location and date.


    src/weather_crew/results/activities_suggestion.md:
    -> Suggested activities for the location, date based on the weather forecast, including a brief description of the activities, why the activity is suitable for the weather forecast, and potential reviews/ratings.

## 🔄 Status

Project is: In Progress


#

📝 Author: Maria Dancianu

📅 Last Updated: March 2025
