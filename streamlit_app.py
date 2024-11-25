import streamlit as st
import pandas as pd
import dgl
import torch
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# App Configuration
st.set_page_config(
    page_title="Ghosts of War Crimes Dashboard",
    layout="wide",
)

# Custom CSS for clean styling and responsive design
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

# Graph Creation and Visualization Functions
def create_dgl_graph(df):
    src = df['Responsible Party']
    dst = df['Location']

    # Categorical encoding
    src_ids = pd.Categorical(src).codes
    dst_ids = pd.Categorical(dst).codes

    graph = dgl.graph((torch.tensor(src_ids), torch.tensor(dst_ids)))
    return graph, src, dst

def visualize_graph(graph, src, dst):
    nx_graph = graph.to_networkx()
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(nx_graph)
    nx.draw(
        nx_graph, pos, with_labels=True,
        node_color="#2196F3", edge_color="#BBDEFB", node_size=500, font_size=8,
        font_color="white", font_weight="bold"
    )
    labels = {i: label for i, label in enumerate(src.append(dst).unique())}
    nx.draw_networkx_labels(nx_graph, pos, labels=labels)
    st.pyplot(plt)

def graph_metrics(graph):
    st.write(f"**Nodes:** {graph.num_nodes()}")
    st.write(f"**Edges:** {graph.num_edges()}")
    degree = graph.in_degrees().float()
    st.write(f"**Average In-Degree:** {torch.mean(degree):.2f}")

def plotly_graph(graph, src, dst):
    edge_x, edge_y = [], []
    pos = nx.spring_layout(graph.to_networkx())
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#BBDEFB'), mode='lines')
    node_x, node_y = zip(*[pos[node] for node in graph.nodes()])
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(color='#2196F3', size=10),
                            text=list(src.append(dst).unique()), hoverinfo='text')
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title='Graph Visualization',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

# Main App Logic
df = load_data()
if not df.empty:
    st.sidebar.header("Filters")
    selected_party = st.sidebar.multiselect("Responsible Party", options=df["Responsible Party"].unique(), default=df["Responsible Party"].unique())
    selected_location = st.sidebar.multiselect("Location", options=df["Location"].unique(), default=df["Location"].unique())
    filtered_data = df[df["Responsible Party"].isin(selected_party) & df["Location"].isin(selected_location)]

    graph, src, dst = create_dgl_graph(filtered_data)

    st.subheader("Graph Visualization")
    visualize_graph(graph, src, dst)

    st.subheader("Graph Metrics")
    graph_metrics(graph)

    st.subheader("Interactive Visualization")
    plotly_graph(graph, src, dst)
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
