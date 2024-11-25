import streamlit as st
import pandas as pd
import plotly.express as px

# App Title
st.title("Ghosts of War Crimes")
st.caption("Visualizing the devastating impacts of war crimes and crimes against humanity.")

# File Upload Section
st.header("Upload CSV Data")
uploaded_file = st.file_uploader("Upload a CSV file containing war crimes data", type=["csv"])

if uploaded_file:
    # Load Data
    df = pd.read_csv(uploaded_file)
    
    # Display Data
    st.header("Dataset Overview")
    st.dataframe(df)

    # Filters
    st.sidebar.header("Filters")
    filter_location = st.sidebar.multiselect(
        "Filter by Location", options=df["Location"].unique(), default=df["Location"].unique()
    )
    filter_responsible_party = st.sidebar.multiselect(
        "Filter by Responsible Party", options=df["Responsible Party"].unique(), default=df["Responsible Party"].unique()
    )
    filter_incident = st.sidebar.multiselect(
        "Filter by Incident Type", options=df["Incident Type"].unique(), default=df["Incident Type"].unique()
    )

    # Filter Data
    filtered_data = df[
        (df["Location"].isin(filter_location)) &
        (df["Responsible Party"].isin(filter_responsible_party)) &
        (df["Incident Type"].isin(filter_incident))
    ]

    # Display Filtered Data
    st.header("Filtered Data")
    st.dataframe(filtered_data)

    # OpenStreetMap Visualization
    st.header("Incident Map (OpenStreetMap)")
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
        )
        fig_map.update_layout(mapbox_style="open-street-map")  # Switch to OpenStreetMap
        st.plotly_chart(fig_map)

    # Bar Chart
    st.header("Victims by Incident Type")
    bar_data = filtered_data.groupby("Incident Type")["Number of Victims"].sum()
    st.bar_chart(bar_data, use_container_width=True)

else:
    st.write("Please upload a CSV file to proceed.")