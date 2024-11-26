import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# App Configuration
st.set_page_config(page_title="Ghosts of War Crimes Dashboard", layout="wide")

# Dynamic CSS for Styling
st.markdown(
    """
    <style>
    .main { background-color: #f9f9f9; color: #333; }
    .stApp { font-family: 'Roboto', sans-serif; }
    h1, h2, h3 { color: #1976D2; font-weight: 500; }
    .stPlotlyChart { background-color: white; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True
)

st.title("Ghosts of War Crimes Dashboard")
st.caption("*Explore the impacts of war crimes and crimes against humanity.*")

# Data Loading Function
@st.cache_data
def load_data(file_path="./data/processed_data/processed_data.csv"):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.warning(f"Could not load data: {e}")
        return pd.DataFrame()

# Load data
df = load_data()

# Drizzle-Based Validation
if not df.empty:
    st.sidebar.header("Filters")
    incident_types = st.sidebar.multiselect("Incident Type", df.get("Incident Type", []).unique())
    locations = st.sidebar.multiselect("Location", df.get("Location", []).unique())
    parties = st.sidebar.multiselect("Responsible Party", df.get("Responsible Party", []).unique())

    # Filter the dataset dynamically
    filtered_df = df.copy()
    if "Incident Type" in df.columns and incident_types:
        filtered_df = filtered_df[filtered_df["Incident Type"].isin(incident_types)]
    if "Location" in df.columns and locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(locations)]
    if "Responsible Party" in df.columns and parties:
        filtered_df = filtered_df[filtered_df["Responsible Party"].isin(parties)]

    # Tabs for Layout
    tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "🗺️ Maps"])

    # Tab 1: Data Overview
    with tab1:
        st.subheader("Filtered Data")
        st.write(f"Total Records: {len(filtered_df)}")
        st.dataframe(filtered_df)

        # Download Button
        st.download_button(
            label="Download Filtered Data",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_data.csv",
            mime="text/csv",
        )

    # Tab 2: Visualizations
    with tab2:
        if "Incident Type" in filtered_df.columns and "Number of Victims" in filtered_df.columns:
            st.subheader("Victims by Incident Type")
            bar_data = filtered_df.groupby("Incident Type")["Number of Victims"].sum().sort_values(ascending=False)
            fig_bar = px.bar(
                x=bar_data.index,
                y=bar_data.values,
                labels={"x": "Incident Type", "y": "Number of Victims"},
                title="Victims by Incident Type",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Missing data for visualizations. Please check your dataset.")

    # Tab 3: Maps
    with tab3:
        if "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
            st.subheader("Incident Map")
            fig_map = px.scatter_mapbox(
                filtered_df,
                lat="Latitude",
                lon="Longitude",
                size="Number of Victims",
                size_max=50,
                color="Incident Type",
                hover_name="Location",
                mapbox_style="carto-positron",
                zoom=1,
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Missing latitude/longitude data for map rendering.")
else:
    st.error("No data available. Please upload a valid CSV file.")

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #E3F2FD; padding: 1rem; border-radius: 8px;'>
    <h3 style='margin-top: 0; color: #1976D2;'>Documentation & Disclaimer</h3>
    <p>For detailed information about this dashboard, data sources, and full disclaimer, please see our
    <a href='https://github.com/musha1140/README.md' target='_blank'>documentation</a>.</p>
    <p><strong>Contact:</strong> <a href='mailto:musherz@gas-lighting.com'>musherz@gas-lighting.com</a></p>
</div>
""", unsafe_allow_html=True)
