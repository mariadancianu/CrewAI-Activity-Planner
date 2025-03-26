# CrewAI Agentic AI - Activity Planner based on Weather Forecast

![CrewAI Agentic AI - Weather Assistant](images/img.png)


## 📌 Project Overview


This project takes a hands-on approach to explore the power of agentic AI workflows using [CrewAI](https://www.crewai.com/). The main objective is to learn by doing and test how AI agents can autonomously retrieve and process weather data via API calls while leveraging CrewAI’s capabilities for multi-agent collaboration and decision-making.

Additionally, the project includes an Activity Planner, where an AI agent suggests indoor or outdoor activities based on real-time weather forecasts, user interests, and a selected date range and city.

The Streamlit application provides an interactive experience, allowing users to input their preferences, view weather forecasts, and receive activity recommendations, with the option to download the suggested activities.

<!--
You can access the deployed app [here](https://crewai-activity-planner-aujjnndpfyz9lpfzkxvlmg.streamlit.app/).
-->

Below is a preview of the application interface. Please note that the discrepancies related to the city and dates are temporary and due to ongoing development.

![](images/activity_planner_1.png)
![](images/activity_planner_2.png)
![](images/activity_planner_3.png)

As this project is still in progress, there may be occasional performance inconsistencies. However, I'm actively working on fine-tuning the system for a more optimized and seamless user experience.

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
