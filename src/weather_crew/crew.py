"""
Creates the crew of agents and tasks for the weather forecasting system,
with the provided tools and configurations.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import get_weather


# TODO: experiment with addition of tool to save the weather results into a json file 


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
            tools=[get_weather], # use the custom tool for weather forecast API calls
            max_iter=3,  # Maximum iterations before the agent must provide its best answer. Default is 20.
            # allow_delegation=False,
        )

    @task
    def weather_collection(self) -> Task:
        """
        Creates the weather_collection task.
        """
        return Task(config=self.tasks_config["weather_collection"])

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
