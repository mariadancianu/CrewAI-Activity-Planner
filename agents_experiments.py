import os

from autogen import ConversableAgent, initiate_chats, register_function
from dotenv import load_dotenv

load_dotenv()

# source: https://bryananthonio.com/blog/autogen-weather-chatbot/

llm_config = {
    "config_list": [
        {"model": "gpt-4o-mini", "api_key": os.environ.get("OPENAI_API _KEY")}
    ],
    "cache_seed": None,
}

weather_assistant = ConversableAgent(
    name="WeatherAssistant",
    system_message="You are a helpful AI weather assistant. "
    "You can help with providing recommendations to the user based on available weather data. "
    "Return 'TERMINATE' when the task is done.",
    llm_config=llm_config,
    is_termination_msg=lambda msg: "terminate" in msg.get("content").lower(),
)

weather_api_proxy = ConversableAgent(
    name="WeatherAPIProxy",
    llm_config=False,
    default_auto_reply="Make an API request to get the latest weather as needed",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
)


def get_current_weather():
    response = []

    return response.json()


register_function(
    get_current_weather,
    caller=weather_assistant,
    executor=weather_api_proxy,
    description="A tool for obtaining weather information. Units are given in metric.",
)


user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None
    or "terminate" in msg.get("content").lower(),
    human_input_mode="ALWAYS",
)


chats = [
    {
        "sender": weather_assistant,
        "recipient": user_proxy,
        "message": "Hello, I'm here to provide recommendations based on the current weather."
        "How may I help you?",
        "summary_method": "reflection_with_llm",
        "max_turns": 2,
    }
]

# initiate_chats(chats)
