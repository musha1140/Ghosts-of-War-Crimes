import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

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
    .stSelectbox {
        background-color: white;
        border-radius: 4px;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
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

# Create Network Graph using NetworkX
def create_networkx_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        responsible_party = row["Responsible Party"]
        location = row["Location"]
        G.add_node(responsible_party, type="Responsible Party")
        G.add_node(location, type="Location")
        G.add_edge(responsible_party, location, weight=row["Number of Victims"])
    return G

# Visualize Graph using Matplotlib
def visualize_network_graph(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=500,
        node_color="#2196F3",
        edge_color="#BBDEFB",
        font_size=8,
        font_color="white",
        font_weight="bold"
    )
    plt.title("Network Graph Visualization", fontsize=16, fontweight="bold")
    st.pyplot(plt)

# Visualize Graph using Plotly
def plotly_network_graph(G):
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#BBDEFB'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color="#2196F3",
            size=10,
            line_width=2
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="Interactive Network Graph",
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    ))
    st.plotly_chart(fig, use_container_width=True)

# Main App Logic
df = load_data()
if not df.empty:
    st.sidebar.header("Filters")
    incident_types = st.sidebar.multiselect("Incident Type", df["Incident Type"].unique())
    locations = st.sidebar.multiselect("Location", df["Location"].unique())
    parties = st.sidebar.multiselect("Responsible Party", df["Responsible Party"].unique())

    filtered_df = df[
        (df["Incident Type"].isin(incident_types) if incident_types else True) &
        (df["Location"].isin(locations) if locations else True) &
        (df["Responsible Party"].isin(parties) if parties else True)
    ]

    # Tabs for Data, Visualizations, and Graphs
    tab1, tab2, tab3 = st.tabs(["📊 Data Overview", "📈 Visualizations", "🔗 Network Graphs"])

    # Tab 1: Data Overview
    with tab1:
        st.subheader("Filtered Data")
        st.write(f"Total Records: {len(filtered_df)}")
        st.dataframe(filtered_df)

        st.subheader("Download Filtered Data")
        csv = filtered_df.to_csv(index=False)
        st.download_button("Download CSV", data=csv, file_name="filtered_data.csv", mime="text/csv")

    # Tab 2: Visualizations
    with tab2:
        st.subheader("Incident Map")
        if "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
            fig_map = px.scatter_mapbox(
                filtered_df,
                lat="Latitude",
                lon="Longitude",
                size="Number of Victims",
                color="Incident Type",
                hover_name="Location",
                zoom=1,
                mapbox_style="carto-positron"
            )
            st.plotly_chart(fig_map, use_container_width=True)

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

    # Tab 3: Network Graphs
    with tab3:
        st.subheader("Network Graph (Matplotlib)")
        graph = create_networkx_graph(filtered_df)
        visualize_network_graph(graph)

        st.subheader("Network Graph (Plotly)")
        plotly_network_graph(graph)

else:
    st.error("No data available. Please upload a valid CSV file.")

# Footer Disclaimer and README.md link
st.markdown("---")
st.markdown("""
    <div style='background-color: #E3F2FD; padding: 1rem; border-radius: 4px; margin: 1rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);'>
        <h3 style='margin-top: 0; color: #1976D2;'>Documentation & Disclaimer</h3>
        <p>For detailed information about this dashboard, data sources, and full disclaimer, please see our 
        <a href='https://github.com/musha1140/README.md' target='_blank'>documentation</a>.</p>
        
        <p><strong>Contact:</strong> <a href='mailto:musherz@gas-lighting.com'>musherz@gas-lighting.com</a></p>
    </div>
    """, unsafe_allow_html=True)
