# Ghosts of War Crimes
Visualizing the devastating impacts of war crimes and crimes against humanity using interactive data visualizations and advanced filtering.

## Project Overview
This project enables users to explore datasets on war crimes and crimes against humanity, including incident details, responsible parties, and geospatial data. It features:
- Interactive filtering
- Geospatial visualizations using OpenStreetMap
- Parallel plots to analyze relationships between dimensions

### Features
1. **Data Upload**: Users can upload multiple CSV files for analysis.
2. **Interactive Filtering**: Filter data by location, incident type, and responsible parties.
3. **Visualizations**:
   - Animated scatter plots for temporal trends.
   - Interactive maps showing geolocated incidents.
   - Parallel plots for multidimensional analysis.

## Folder Structure
```
Ghosts-of-War-Crimes/
├── data/
│   ├── metadata/               # Metadata about datasets
│   ├── processed_data/         # Cleaned datasets for analysis
│   └── raw_data/               # Original datasets
├── svgs/                       # Custom visual assets (e.g., logo, charts)
├── screenshots/                # UI screenshots
├── tests/                      # Automated tests for app components
├── notebooks/                  # Jupyter notebooks for exploratory analysis
├── components/                 # Reusable code for Streamlit components
├── streamlit_app.py            # Main Streamlit app
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── LICENSE                     # License information
└── .gitignore                  # Files to exclude from version control

```
## Requirements

```
pip install -r requirements.txt
```
## Clone
```git clone https://github.com/your-username/Ghosts-of-War-Crimes.git
cd Ghosts-of-War-Crimes
```
## Run
```
streamlit run streamlit_app.py
```