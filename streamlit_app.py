import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
import matplotlib.pyplot as plt

# App Configuration
st.set_page_config(
    page_title="Ghosts of War Crimes Dashboard",
    layout="wide",
)

# Custom CSS for Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        color: #333333;
    }
    .stApp {
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3 {
        color: #1976D2;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #2196F3;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stPlotlyChart, .stDataFrame {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
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
        data = pd.read_csv(file_path)
        st.success("Data loaded successfully!")
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# Create Network Graph using NetworkX
def create_network_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        responsible_party = row.get("Responsible Party", "Unknown")
        location = row.get("Location", "Unknown")
        G.add_node(responsible_party, type="Responsible Party")
        G.add_node(location, type="Location")
        G.add_edge(responsible_party, location, weight=row.get("Number of Victims", 0))
    return G

# Visualize Network Graph with Matplotlib
def visualize_graph_matplotlib(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G, pos, with_labels=True, node_size=500, node_color="#2196F3",
        edge_color="#BBDEFB", font_size=8, font_color="white", font_weight="bold"
    )
    plt.title("Network Graph Visualization", fontsize=16, fontweight="bold")
    st.pyplot(plt)

# Main App Logic
df = load_data()

if not df.empty:
    st.sidebar.header("Filters")
    incident_types = st.sidebar.multiselect("Incident Type", df["Incident Type"].unique() if "Incident Type" in df.columns else [])
    locations = st.sidebar.multiselect("Location", df["Location"].unique() if "Location" in df.columns else [])
    parties = st.sidebar.multiselect("Responsible Party", df["Responsible Party"].unique() if "Responsible Party" in df.columns else [])

    # Apply Filters
    filtered_df = df
    if incident_types:
        filtered_df = filtered_df[filtered_df["Incident Type"].isin(incident_types)]
    if locations:
        filtered_df = filtered_df[filtered_df["Location"].isin(locations)]
    if parties:
        filtered_df = filtered_df[filtered_df["Responsible Party"].isin(parties)]

    # Tabs for Data, Visualizations, and Graphs
    tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "🔗 Network Graphs"])

    with tab1:
        st.subheader("Filtered Data")
        st.dataframe(filtered_df)
        st.download_button("Download Filtered Data", filtered_df.to_csv(index=False), "filtered_data.csv")

    with tab2:
        st.subheader("Incident Map")
        if "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
            fig = px.scatter(
                filtered_df,
                x="Longitude",
                y="Latitude",
                size="Number of Victims",
                color="Incident Type",
                hover_name="Location",
                labels={"x": "Longitude", "y": "Latitude"},
                title="Incident Locations"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Victims by Incident Type")
        bar_data = filtered_df.groupby("Incident Type")["Number of Victims"].sum().sort_values(ascending=False)
        fig_bar = px.bar(
            x=bar_data.index,
            y=bar_data.values,
            labels={'x': 'Incident Type', 'y': 'Number of Victims'},
            title='Victims by Incident Type'
        )
        fig_bar.update_traces(marker_color='#2196F3')
        st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        st.subheader("Network Graph (Matplotlib)")
        graph = create_network_graph(filtered_df)
        visualize_graph_matplotlib(graph)

else:
    st.error("No data available. Please upload a valid CSV file.")

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #E3F2FD; padding: 1rem; border-radius: 4px;'>
    <h3>Documentation & Disclaimer</h3>
    <p>For details about this app, visit our <a href="https://github.com/musha1140/Ghosts-of-War-Crimes/README.md">documentation</a>.</p>
    <p><strong>Contact:</strong> <a href="mailto:musherz@gas-lighting.com">musherz@gas-lighting.com</a></p>
</div>
""", unsafe_allow_html=True)
