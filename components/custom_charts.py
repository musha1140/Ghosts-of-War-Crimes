import plotly.express as px

def create_parallel_categories(data):
    return px.parallel_categories(
        data,
        dimensions=["Incident Type", "Responsible Party", "Location"],
        color="Number of Victims",
        color_continuous_scale=px.colors.sequential.Inferno
    )
