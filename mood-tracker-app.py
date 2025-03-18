import streamlit as st
import pandas as pd
import datetime
import csv
import os

MOOD_FILE = "mood_log.csv"

# Function to load mood data safely
def load_mood_data():
    # If file does not exist or is empty, return empty DataFrame with correct columns
    if not os.path.exists(MOOD_FILE) or os.stat(MOOD_FILE).st_size == 0:
        return pd.DataFrame(columns=["Date", "Mood"])
    
    # Try reading CSV
    try:
        data = pd.read_csv(MOOD_FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Mood"])
    
    # Debug: Print column names for verification
    st.write("Columns in DataFrame (Before Fixing):", data.columns.tolist())

    # Strip spaces and standardize column names
    data.columns = data.columns.str.strip()  

    # Ensure both "Date" and "Mood" columns exist
    if not {"Date", "Mood"}.issubset(data.columns):
        st.error("Error: 'Date' or 'Mood' column is missing. Fixing it now...")
        
        # Rename if there is a case issue (e.g., "date" instead of "Date")
        column_mapping = {col.strip().lower(): col.strip() for col in data.columns}
        
        if "date" in column_mapping and "mood" in column_mapping:
            data.rename(columns={column_mapping["date"]: "Date", column_mapping["mood"]: "Mood"}, inplace=True)
        else:
            # If columns are still incorrect, recreate CSV with headers
            st.warning("Resetting CSV file due to incorrect format.")
            reset_csv()
            return pd.DataFrame(columns=["Date", "Mood"])

    return data

# Function to reset CSV file with correct headers
def reset_csv():
    with open(MOOD_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Mood"])

# Function to save new mood entry
def save_mood_data(date, mood):
    file_exists = os.path.exists(MOOD_FILE)

    with open(MOOD_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        
        # Ensure headers exist if file is empty
        if not file_exists or os.stat(MOOD_FILE).st_size == 0:
            writer.writerow(["Date", "Mood"])

        writer.writerow([date, mood])

# Streamlit App Title
st.title("Mood Tracker")

# Get Today's Date
today = datetime.date.today()

# User Mood Input
st.subheader("How are you feeling today?")
mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

# Button to Save Mood
if st.button("Log Mood"):
    save_mood_data(today, mood)
    st.success("Mood Logged Successfully!")

# Load and Display Mood Data
data = load_mood_data()

if not data.empty:
    st.subheader("Mood Trends Over Time")

    # Ensure Date column is properly formatted
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")  # Convert to datetime
        data = data.dropna(subset=["Date"])  # Remove rows with invalid dates
    else:
        st.error("Error: 'Date' column not found.")
    
    # Display Mood Counts as a Bar Chart
    mood_counts = data["Mood"].value_counts()
    st.bar_chart(mood_counts)





# import streamlit as st # For creating web interface
# import pandas as pd # For data manipulation
# import datetime # For handling dates
# import csv # For reading and writing CSV file
# import os # For file operations

# # Define the file name for storing mood data
# MOOD_FILE = "mood_log.csv"

# # Function to read mood data from the CSV file
# def load_mood_data():
#     # Check if the file exists
#     if not os.path.exists(MOOD_FILE):
#         # If no file, create empty DataFrame with columns
#         return pd.DataFrame(columns=["Date", "Mood"])
#     # Read and return existing mood data
#     return pd.read_csv(MOOD_FILE)

# # Function to add new mood entry to CSV file
# def save_mood_data(date, mood):
#     # Open file in append mode
#     with open(MOOD_FILE, "a") as file:

#         # Create CSV writer
#         writer = csv.writer(file)

#         # Add new mood entry
#         writer.writerow([date, mood])

# # Streamlit app title
# st.title("Mood Tracker")

# # Get today's date
# today = datetime.date.today()

# # Create subheader for mood input
# st.subheader("How are your feeling today?")

# # Create dropdown for mood selection
# mood = st.selectbox("Select your mood", ["Happy", "Sad", "Angry", "Neutral"])

# # Create button to save mood
# if st.button("Log Mood"):
    
#     # Save mood when button is clicked
#     save_mood_data(today, mood)

#     # Show success message
#     st.success("Mood Logged Successfully!")

# # Load existing mood data
# data = load_mood_data()

# # If there is data to display
# if not data.empty:

#     # Create section for Visualization
#     st.subheader("Mood Trends Over Time")

#     # Convert date stings to datetime Objects
#     data["Date"] = pd.to_datetime(data["Date"])

#     # Count frequency of each mood
#     mood_counts = data.groupby("Mood").count()["Date"]

#     # Display bar chart of mood frequencies
#     st.bar_chart(mood_counts)
