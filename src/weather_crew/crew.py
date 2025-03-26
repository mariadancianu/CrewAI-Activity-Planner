"""
Creates the crew of agents and tasks for the weather forecasting system,
with the provided tools and configurations.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from src.weather_crew.tools.custom_tool import get_weather


@CrewBase
class WeatherCrew:
    """WeatherCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def weather_assistant(self) -> Agent:
        """
        Creates the Weather Assistant agent.
        """
        return Agent(
            config=self.agents_config["weather_assistant"],
            verbose=True,
            tools=[get_weather],  # use the custom tool for weather forecast API calls
            max_iter=3,  # Maximum iterations before the agent must provide its best answer. Default is 20.
            # allow_delegation=False,
        )

    @agent
    def activities_planner(self) -> Agent:
        """
        Creates the Activities Searcher agent.
        """
        return Agent(
            config=self.agents_config["activities_planner"],
            verbose=True,
            max_iter=3,  # Maximum iterations before the agent must provide its best answer. Default is 20.
            tools=[
                SerperDevTool(),  # search the internet and return the most relevant results.
                ScrapeWebsiteTool(),
            ],
            # allow_delegation=False,
        )

    @task
    def weather_collection(self) -> Task:
        """
        Creates the weather_collection task.
        """
        return Task(
            config=self.tasks_config["weather_collection_task"],
            output_file="/results/weather_forecast.md",
        )

    @task
    def activities_planning_task(self) -> Task:
        """
        Creates the activities_suggestion task.
        """
        return Task(
            config=self.tasks_config["activities_planning_task"],
            output_file="/results/activities_suggestion.md",
        )

    @crew
    def crew(self) -> Crew:
        """
        Creates the WeatherCrew with the agents and tasks.
        """

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,  # or Process.hierarchical
            verbose=True,
        )
