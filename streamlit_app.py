import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from geopy.distance import geodesic

# App Configuration
st.set_page_config(
    page_title="Ghosts of War Crimes Dashboard",
    layout="wide",
)

# App Title
st.title("Ghosts of War Crimes")
st.markdown("*Visualizing the impacts of war crimes and crimes against humanity.*")

# Load Dataset
@st.cache_data
def load_data():
    try:
        file_path = "./data/processed_data/processed_data.csv"
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# Proximity Filters
st.sidebar.subheader("Proximity Filter")
latitude = st.sidebar.number_input("Latitude", value=31.5, format="%.2f")
longitude = st.sidebar.number_input("Longitude", value=34.5, format="%.2f")
radius = st.sidebar.slider("Radius (km)", 0, 1000, 50)

# Filter by Proximity
def filter_by_radius(lat, lon, radius_km):
    def is_within_radius(row):
        return geodesic((lat, lon), (row["Latitude"], row["Longitude"])).km <= radius_km
    return df[df.apply(is_within_radius, axis=1)]

filtered_data = filter_by_radius(latitude, longitude, radius)

# Incident Type Filter
incident_types = st.sidebar.multiselect(
    "Select Incident Types", options=df["Incident Type"].unique(), default=df["Incident Type"].unique()
)
filtered_data = filtered_data[filtered_data["Incident Type"].isin(incident_types)]

# Responsible Party Filter
responsible_parties = st.sidebar.multiselect(
    "Select Responsible Parties", options=df["Responsible Party"].unique(), default=df["Responsible Party"].unique()
)
filtered_data = filtered_data[filtered_data["Responsible Party"].isin(responsible_parties)]

# Date Range Filter
st.sidebar.subheader("Date Filter")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("1980-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2024-12-31"))
filtered_data = filtered_data[
    (pd.to_datetime(filtered_data["Date"]) >= start_date)
    & (pd.to_datetime(filtered_data["Date"]) <= end_date)
]

# Display Filtered Data
st.subheader("Filtered Data")
st.write(f"Total Records: {len(filtered_data)}")
st.dataframe(filtered_data)

# Map Visualization
if not filtered_data.empty:
    st.subheader("Incident Locations Map")
    fig = px.scatter_mapbox(
        filtered_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Location",
        hover_data=["Incident Type", "Number of Victims", "Responsible Party", "Date"],
        color="Number of Victims",
        size="Number of Victims",
        zoom=5,
        mapbox_style="open-street-map",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No incidents match your filters.")

# Footer Disclaimer and Contact Info
st.markdown("---")
st.markdown("""
    <div style='background-color: #E3F2FD; padding: 1rem; border-radius: 4px; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);'>
        <h3 style='margin-top: 0; color: #1976D2;'>Documentation & Disclaimer</h3>
        <p>This dashboard visualizes publicly available data and is meant for informational purposes only. 
        The creators do not endorse or support any specific political stance.</p>
        
        <p>For more details, please refer to our <a href='https://github.com/musha1140/README.md' target='_blank'>documentation</a>.</p>
        
        <p><strong>Contact:</strong> <a href='mailto:musherz@gas-lighting.com'>musherz@gas-lighting.com</a></p>
    </div>
    """, unsafe_allow_html=True)
