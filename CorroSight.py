import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# ---- Industrial Theme CSS Injection ----
industrial_css = """
<style>
:root {
    --industrial-dark: #2c3e50;       /* Deep steel blue */
    --industrial-medium: #7f8c8d;     /* Metallic gray */
    --industrial-light: #ecf0f1;      /* Light concrete */
    --industrial-accent: #e74c3c;     /* Rust red accents */
}

/* Base app styling */
.stApp {
    background: linear-gradient(135deg, var(--industrial-medium) 0%, var(--industrial-dark) 100%) !important;
    background-attachment: fixed !important;
}

/* All text elements - pure black */
h1, h2, h3, h4, h5, h6, p, div, span, .stMarkdown, .stAlert, .stText, .stCodeBlock {
    color: #000000 !important;
    text-shadow: 0px 0px 1px rgba(255,255,255,0.3) !important;
}

/* Widget containers */
.stTextInput, .stNumberInput, .stSelectbox, .stTextArea, 
.stDateInput, .stTimeInput, .stSlider, .stFileUploader {
    background-color: var(--industrial-light) !important;
    border: 1px solid var(--industrial-dark) !important;
    border-radius: 4px !important;
    padding: 8px !important;
}

/* Input elements */
.stTextInput>div>div>input, .stNumberInput>div>div>input, 
.stSelectbox>div>div>select, .stTextArea>div>div>textarea {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* Buttons */
.stButton>button {
    background: var(--industrial-dark) !important;
    color: var(--industrial-light) !important;
    border: 2px solid var(--industrial-accent) !important;
    border-radius: 4px !important;
    font-weight: bold !important;
    transition: all 0.3s !important;
}

.stButton>button:hover {
    background: var(--industrial-accent) !important;
    color: #ffffff !important;
    border-color: var(--industrial-dark) !important;
}

/* Containers & Cards */
.stAlert, .stExpander, .stDataFrame, .card {
    background-color: var(--industrial-light) !important;
    border: 2px solid var(--industrial-medium) !important;
    border-radius: 6px !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}

/* Expander header */
.stExpander > label {
    background-color: var(--industrial-dark) !important;
    color: var(--industrial-light) !important;
    padding: 8px 12px !important;
}

/* Tabs */
.stTabs [role="tab"] {
    background-color: var(--industrial-medium) !important;
    color: #ffffff !important;
    border-radius: 4px 4px 0 0 !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--industrial-light) !important;
    color: #000000 !important;
    font-weight: bold !important;
}

/* Charts container */
.element-container .stPlotlyChart, .element-container .stPyplot {
    background-color: var(--industrial-light) !important;
    padding: 15px !important;
    border-radius: 8px !important;
    border: 1px solid var(--industrial-dark) !important;
}

/* Tables */
table {
    background-color: #ffffff !important;
    color: #000000 !important;
}
</style>
"""

st.markdown(industrial_css, unsafe_allow_html=True)

# ---- Industrial Theme Configuration ----
st.set_page_config(
    page_title="Industrial Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# ---- Chart Styling Setup ----
# Matplotlib industrial style
plt.style.use('ggplot')
plt.rcParams['axes.facecolor'] = '#ecf0f1'
plt.rcParams['axes.edgecolor'] = '#2c3e50'
plt.rcParams['axes.labelcolor'] = '#000000'
plt.rcParams['xtick.color'] = '#000000'
plt.rcParams['ytick.color'] = '#000000'
plt.rcParams['text.color'] = '#000000'

# Plotly industrial template
import plotly.io as pio
industrial_template = {
    "layout": {
        "paper_bgcolor": "#ecf0f1",
        "plot_bgcolor": "#ecf0f1",
        "font": {"color": "#000000", "family": "Arial"},
        "title": {"font": {"size": 24, "color": "#000000"}},
        "xaxis": {
            "gridcolor": "#bdc3c7",
            "linecolor": "#2c3e50",
            "zerolinecolor": "#2c3e50"
        },
        "yaxis": {
            "gridcolor": "#bdc3c7",
            "linecolor": "#2c3e50",
            "zerolinecolor": "#2c3e50"
        },
        "colorway": ["#e74c3c", "#2c3e50", "#7f8c8d", "#3498db", "#f39c12"]
    }
}
pio.templates["industrial"] = industrial_template
pio.templates.default = "industrial"

# ---- Sample App Content ----
st.title("⚙️ Industrial Operations Dashboard")
st.subheader("Production Monitoring & Analytics")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Performance Metrics", "Data Explorer"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Factory Status")
        status_data = {
            "Production Line": ["Assembly", "Packaging", "Quality Control"],
            "Status": ["Running", "Stopped", "Running"],
            "Output (units/hr)": [120, 0, 95]
        }
        st.dataframe(pd.DataFrame(status_data), height=200)
        
        st.header("Equipment Health")
        equipment_health = {
            "Machine": ["Press #5", "Conveyor B", "Mixer X", "Cutter Z"],
            "Temp (°C)": [72, 45, 68, 82],
            "Vibration": [2.1, 1.4, 4.2, 3.8],
            "Status": ["Normal", "Normal", "Warning", "Alert"]
        }
        st.dataframe(pd.DataFrame(equipment_health))
    
    with col2:
        st.header("Production Trend")
        # Generate sample data
        days = pd.date_range(start="2023-06-01", periods=30, freq="D")
        production = np.random.normal(1000, 200, 30).cumsum()
        
        # Matplotlib chart
        fig1, ax = plt.subplots(figsize=(10, 4))
        ax.plot(days, production, color="#e74c3c", linewidth=2.5)
        ax.fill_between(days, production, alpha=0.2, color="#e74c3c")
        ax.set_title("Monthly Production Output", fontsize=16)
        ax.grid(True, linestyle="--", alpha=0.7)
        st.pyplot(fig1)
        
        # Plotly gauge
        efficiency = 87.4
        fig2 = px.indicator(
            value=efficiency,
            title="Overall Equipment Efficiency",
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#2c3e50"},
                'steps': [
                    {'range': [0, 70], 'color': "#e74c3c"},
                    {'range': [70, 90], 'color': "#f39c12"},
                    {'range': [90, 100], 'color': "#2ecc71"}
                ]
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Performance Analysis")
    
    # Create sample data
    categories = ["Welding", "Assembly", "Painting", "Testing", "Packaging"]
    values = [92, 88, 95, 90, 85]
    
    # Create columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Plotly bar chart
        fig = px.bar(
            x=categories,
            y=values,
            color=categories,
            color_discrete_sequence=["#e74c3c", "#2c3e50", "#7f8c8d", "#3498db", "#f39c12"],
            labels={"x": "Department", "y": "Efficiency (%)"},
            title="Department Efficiency"
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Total Output", "24,582 units", "+3.2% vs last month")
        st.metric("Defect Rate", "1.8%", "-0.4% improvement")
        st.metric("Energy Consumption", "42.8 MW", "+2.1% increase")
        st.metric("Downtime", "2.4%", "Within target")

with tab3:
    st.header("Data Exploration")
    
    # Generate sample industrial data
    np.random.seed(42)
    data = pd.DataFrame({
        "Timestamp": pd.date_range("2023-06-01", periods=500, freq="H"),
        "Temperature": np.random.normal(75, 5, 500),
        "Pressure": np.random.normal(120, 10, 500),
        "Flow_Rate": np.random.normal(45, 3, 500),
        "Vibration": np.random.normal(3.5, 1, 500),
        "Quality_Score": np.random.uniform(85, 99, 500)
    })
    
    # Widgets
    col1, col2, col3 = st.columns(3)
    with col1:
        metric = st.selectbox("Select Metric", data.columns[1:])
    with col2:
        time_range = st.selectbox("Time Range", ["24h", "7d", "30d"])
    with col3:
        threshold = st.slider("Alert Threshold", 0, 100, 90)
    
    # Filter data based on selection
    if time_range == "24h":
        filtered = data.iloc[-24:]
    elif time_range == "7d":
        filtered = data.iloc[-168:]
    else:
        filtered = data.iloc[-720:]
    
    # Plot time series
    fig = px.line(
        filtered,
        x="Timestamp",
        y=metric,
        title=f"{metric.replace('_', ' ')} Trend",
        line_shape="linear",
        render_mode="svg"
    )
    fig.add_hline(y=threshold, line_dash="dash", line_color="red", annotation_text="Alert Threshold")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data
    with st.expander("View Raw Data"):
        st.dataframe(data)

# ---- Footer ----
st.divider()
st.caption("Industrial Operations Dashboard v1.0 | © 2023 Corrosight Analytics")
