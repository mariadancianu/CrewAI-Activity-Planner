import streamlit as st

from src.weather_crew.main import run
from src.weather_crew.tools.custom_tool import get_supported_locations

accuweather_endpoint = "http://dataservice.accuweather.com"

# Title of the app
st.title("Activity Planner")

# Dropdown menu
options = get_supported_locations(accuweather_endpoint)
options = [f"{option['city_name']}, {option['country_name']}" for option in options]

selected_option = st.selectbox(
    "Choose one of the supported cities:", ["None"] + options
)

# Display the selected option
st.write(f"You selected: {selected_option}")

# Date selection
# TODO: add support for user-defined date range in the activity planner agent
# This is just a placeholder for now
selected_date = st.date_input("Select a date for your activity:", value=None)
if selected_date:
    st.write(f"You selected the date: {selected_date}")

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

# Display the selected interests
st.write(f"You selected the following interests: {', '.join(selected_interests)}")

# Confirm button to trigger the run function
if st.button("Confirm and Run"):
    if selected_option == "None" or not selected_date or not selected_interests:
        st.error(
            "Please select a location, date, and at least one interest before proceeding."
        )
    else:
        with st.spinner("Running the activity planner..."):
            output = run()

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
