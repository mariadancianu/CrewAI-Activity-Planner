import streamlit as st

from src.weather_crew.main import run
from src.weather_crew.tools.custom_tool import get_supported_locations

accuweather_endpoint = "http://dataservice.accuweather.com"

# Title of the app
st.title("🌤️ Activity Planner")

# Expander for user inputs
with st.expander("Select Your Preferences"):
    # Dropdown menu
    options = get_supported_locations(accuweather_endpoint)
    options = [f"{option['city_name']}, {option['country_name']}" for option in options]

    selected_option = st.selectbox(
        "Choose one of the supported cities:", ["None"] + options
    )

    # Date selection
    # TODO: add support for user-defined date range in the activity planner agent
    # This is just a placeholder for now
    st.markdown("#### Select a date range for your activity:")
    start_date = st.date_input("Start Date:", value=None, key="start_date")
    end_date = st.date_input("End Date:", value=None, key="end_date")

    # Multiple options checkbox
    # TODO: add support for user personal interests in the activity planner agent
    # This is just a placeholder for now
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
            output = run()

        st.markdown("### Weather Forecast")
        # TODO: this is a placeholder, replace with actual weather data retrieval
        weather_data = [
            {"Date": "2025-03-26", "Condition": "Sunny"},
            {"Date": "2025-03-27", "Condition": "Rainy"},
            {"Date": "2025-03-28", "Condition": "Cloudy"},
        ]

        for day in weather_data:
            condition_icon = (
                "☀️"
                if day["Condition"] == "Sunny"
                else "🌧️"
                if day["Condition"] == "Rainy"
                else "☁️"
            )
            st.write(f"{day['Date']}: {condition_icon} {day['Condition']}")

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
