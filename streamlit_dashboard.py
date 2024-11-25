import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# App Configuration
st.set_page_config(
    page_title="Ghosts of War Crimes Dashboard",
    layout="wide",
)

# App Title
st.title("Ghosts of War Crimes")
st.caption("A dashboard visualizing war crimes and crimes against humanity.")

# Data Loading
@st.cache_data
def load_data():
    file_path = "./data/processed_data/processed_data.csv"
    data = pd.read_csv(file_path)
    return data

# Load processed data
df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
incident_filter = st.sidebar.multiselect(
    "Select Incident Type(s)", options=df["Incident Type"].unique(), default=df["Incident Type"].unique()
)
location_filter = st.sidebar.multiselect(
    "Select Location(s)", options=df["Location"].unique(), default=df["Location"].unique()
)
party_filter = st.sidebar.multiselect(
    "Select Responsible Party(s)", options=df["Responsible Party"].unique(), default=df["Responsible Party"].unique()
)

# Apply Filters
filtered_data = df[
    (df["Incident Type"].isin(incident_filter)) &
    (df["Location"].isin(location_filter)) &
    (df["Responsible Party"].isin(party_filter))
]

# Dynamic Chart Selector
chart_type = st.sidebar.radio("Select Chart Type", options=["Bar", "Pie", "Line"])

# Tabs for Layout
tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "📜 Insights"])

# Tab 1: Data Overview
with tab1:
    st.subheader("Filtered Data Overview")
    st.write(f"Total Records: {len(filtered_data)}")
    st.dataframe(filtered_data)

    st.subheader("Summary Statistics")
    st.write(filtered_data.describe())

    st.subheader("Download Filtered Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")

# Tab 2: Visualizations
with tab2:
    # Dynamic Chart Based on User Selection
    st.subheader(f"{chart_type} Chart: Victims by Incident Type")
    chart_data = filtered_data.groupby("Incident Type")["Number of Victims"].sum().sort_values()

    if chart_type == "Bar":
        st.bar_chart(chart_data)
    elif chart_type == "Pie":
        fig = px.pie(
            filtered_data,
            names="Incident Type",
            values="Number of Victims",
            title="Victims by Incident Type",
        )
        st.plotly_chart(fig)
    elif chart_type == "Line":
        line_data = filtered_data.groupby("Date")["Number of Victims"].sum()
        st.line_chart(line_data)

    # Heatmap: Victims by Incident Type and Responsible Party
    st.subheader("Heatmap: Victims by Type and Responsible Party")
    if not filtered_data.empty:
        pivot = filtered_data.pivot_table(
            index="Incident Type", columns="Responsible Party", values="Number of Victims", aggfunc="sum", fill_value=0
        )
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot, cmap="Blues", annot=True, fmt="g", ax=ax)
        st.pyplot(fig)

    # Map: Incident Locations
    st.subheader("Incident Map")
    if "Latitude" in filtered_data.columns and "Longitude" in filtered_data.columns:
        fig_map = px.scatter_mapbox(
            filtered_data,
            lat="Latitude",
            lon="Longitude",
            size="Number of Victims",
            color="Incident Type",
            hover_name="Location",
            title="Incident Locations (OpenStreetMap)",
            zoom=1,
            mapbox_style="open-street-map"
        )
        st.plotly_chart(fig_map)

# Tab 3: Insights
with tab3:
    st.subheader("Key Insights")
    st.markdown(
        """
        - **Incident Type Trends**: Examine which incident types contribute most to victim counts.
        - **Geographic Analysis**: Identify regions with the highest concentration of incidents.
        - **Party Responsibility**: Analyze which responsible parties are linked to the most incidents.
        """
    )
    if not filtered_data.empty:
        top_incident = filtered_data.groupby("Incident Type")["Number of Victims"].sum().idxmax()
        top_location = filtered_data.groupby("Location")["Number of Victims"].sum().idxmax()
        st.write(f"Top Incident Type by Victims: {top_incident}")
        st.write(f"Top Location by Victims: {top_location}")