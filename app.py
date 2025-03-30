# __import__("pysqlite3")
# import sys

# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import datetime
import json

import streamlit as st

from src.weather_crew.main import run
from src.weather_crew.tools.custom_tool import get_supported_locations

accuweather_endpoint = "http://dataservice.accuweather.com"

# Title of the app
st.title("🌤️ Activity Planner")

today = datetime.date.today()
max_date = today + datetime.timedelta(
    days=5
)  # Limit the date range to 5 days due to free option weather API limitations

# Expander for user inputs
with st.expander("Select Your Preferences"):
    # Dropdown menu
    options = get_supported_locations(accuweather_endpoint)
    options = [
        f"{option['city_name']}, {option['country_name']}, {option['administrative_area_name']}"
        for option in options
    ]

    selected_option = st.selectbox(
        "Choose one of the supported cities:", ["None"] + options
    )

    # Date selection
    st.markdown("#### Select a date range for your activity:")
    start_date = st.date_input(
        "Start Date:", value=None, min_value=today, max_value=max_date, key="start_date"
    )

    end_date = st.date_input(
        "End Date:", value=None, min_value=today, max_value=max_date, key="end_date"
    )

    # Multiple options checkbox
    checkbox_options = [
        "Photography",
        "Art",
        "Food",
        "Nature",
        "Sports",
        "Technology",
        "Cooking",
        "Music",
        "Dancing",
    ]
    selected_interests = st.multiselect("Select your interests:", checkbox_options)

# Display user selections
st.markdown("### Your Selections")
if selected_option != "None":
    st.write(f"**Location:** {selected_option}")
if start_date and end_date:
    st.write(f"**Date Range:** {start_date} to {end_date}")
if selected_interests:
    st.write(f"**Interests:** {', '.join(selected_interests)}")

# Confirm button to trigger the run function
if st.button("Confirm and Run"):
    if (
        selected_option == "None"
        or not start_date
        or not end_date
        or not selected_interests
    ):
        st.error(
            "Please select a location, date, and at least one interest before proceeding."
        )
    else:
        with st.spinner("Running the activity planner..."):
            output = run(
                city=selected_option.split(",")[0],
                country=selected_option.split(",")[1],
                administrative_area=selected_option.split(",")[2],
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
                user_interests=selected_interests,
            )

        st.markdown("### Weather Forecast")

        filename = "results/weather_forecast.json"

        with open(filename, "r") as f:
            weather_data = json.load(f)

        for day in weather_data:
            condition_icon = (
                "☀️"
                if "sunny" in day["weather_text"].lower()  # == "Sunny"
                else "🌧️"
                if "rainy" in day["weather_text"].lower()  # == "Rainy"
                else "☁️"
            )
            st.write(
                f"{day['date']}: {condition_icon} {day['weather_text']}, Mimimum temperature: {day['temperature_min']}, Maximum temperature: {day['temperature_max']}"
            )

        st.markdown("### Activity Planner Output")
        st.markdown(output)

        # Ensure output is a string
        if not isinstance(output, str):
            output = str(output)

        # Add a download button for the output
        st.download_button(
            label="Download Activity Plan",
            data=output,
            file_name="activity_planner_output.txt",
            mime="text/plain",
        )
