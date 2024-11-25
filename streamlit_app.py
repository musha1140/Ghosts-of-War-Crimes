import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# App Configuration
st.set_page_config(
    page_title="Ghosts of War Crimes Dashboard",
    layout="wide",
)

# Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        color: #1e1e1e;
    }
    .stApp {
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #34495e;
        color: white;
    }
    .stSelectbox {
        background-color: #ecf0f1;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("Ghosts of War Crimes Dashboard")
st.markdown("*Visualizing the impacts of war crimes and crimes against humanity.*")

# Data Loading Function
@st.cache_data
def load_data(file_path="./data/processed_data/processed_data.csv"):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# File Upload Section
st.header("Data Source")
uploaded_file = st.file_uploader("Upload a CSV file containing war crimes data", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = load_data()

if not df.empty:
    # Sidebar Filters
    st.sidebar.header("Data Filters")
    incident_filter = st.sidebar.multiselect(
        "Incident Type(s)", options=df["Incident Type"].unique(), default=df["Incident Type"].unique()
    )
    location_filter = st.sidebar.multiselect(
        "Location(s)", options=df["Location"].unique(), default=df["Location"].unique()
    )
    party_filter = st.sidebar.multiselect(
        "Responsible Party(s)", options=df["Responsible Party"].unique(), default=df["Responsible Party"].unique()
    )

    # Apply Filters
    filtered_data = df[
        (df["Incident Type"].isin(incident_filter)) &
        (df["Location"].isin(location_filter)) &
        (df["Responsible Party"].isin(party_filter))
    ]

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
        st.subheader("Victims by Incident Type")
        chart_data = filtered_data.groupby("Incident Type")["Number of Victims"].sum().sort_values()

        # Bar Chart
        st.bar_chart(chart_data)

        # Pie Chart
        st.subheader("Pie Chart: Victims by Incident Type")
        fig = px.pie(
            filtered_data,
            names="Incident Type",
            values="Number of Victims",
            title="Victims by Incident Type",
        )
        st.plotly_chart(fig)

        # Line Chart
        st.subheader("Line Chart: Victims Over Time")
        if "Date" in filtered_data.columns:
            line_data = filtered_data.groupby("Date")["Number of Victims"].sum()
            st.line_chart(line_data)

        # Heatmap
        st.subheader("Heatmap: Victims by Type and Responsible Party")
        if not filtered_data.empty:
            pivot = filtered_data.pivot_table(
                index="Incident Type", columns="Responsible Party", values="Number of Victims", aggfunc="sum", fill_value=0
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(pivot, cmap="Blues", annot=True, fmt="g", ax=ax)
            st.pyplot(fig)

        # Map Visualization
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
                mapbox_style="carto-positron"
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
else:
    st.error("No data available. Please upload a file or check your default data source.")
