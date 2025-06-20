import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.lines import Line2D

# Configuration
st.set_page_config(
    layout="wide",
    page_title="Pipeline Integrity Manager",
    page_icon="⚙️"
)

# Industrial color palette
PRIMARY = "#2c3e50"    # Steel blue
SECONDARY = "#7f8c8d"  # Metallic gray
ACCENT = "#e74c3c"     # Rust red
WARNING = "#d32f2f"    # Red
BACKGROUND = "#ecf0f1"  # Concrete light
CARD_BG = "#ffffff"    # White cards
DARK_TEXT = "#000000"  # Black text
LIGHT_TEXT = "#FFFFFF" # Light text
DATASET_COLORS = ["#2c3e50", "#7f8c8d", "#e74c3c"]  # Dataset colors

# Color palette for diagrams
COLORS = {
    'Goodman': '#d32f2f',     # Red
    'Soderberg': '#2c3e50',   # Steel blue
    'Gerber': '#7f8c8d',      # Metallic gray
    'Morrow': '#e74c3c',      # Rust red
    'ASME-Elliptic': '#6A1B9A', # Purple
    'OperatingPoint': '#d32f2f', # Red for visibility
    'KeyPoints': '#000000'    # Black
}

# Custom CSS for industrial theme with black text
st.markdown(f"""
<style>
    /* Main styling - industrial gradient background */
    .stApp {{
        background: linear-gradient(135deg, {SECONDARY} 0%, {PRIMARY} 100%) !important;
        background-attachment: fixed !important;
        color: {DARK_TEXT};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Titles and headers - black text */
    h1, h2, h3, h4, h5, h6 {{
        color: {DARK_TEXT} !important;
        border-bottom: 2px solid {PRIMARY};
        padding-bottom: 0.3rem;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {CARD_BG};
        color: {DARK_TEXT};
        border-right: 2px solid {PRIMARY};
    }}
    
    .sidebar .sidebar-content {{
        background-color: {CARD_BG};
        color: {DARK_TEXT};
    }}
    
    /* Button styling */
    .stButton>button {{
        background-color: {PRIMARY};
        color: {LIGHT_TEXT};
        border-radius: 4px;
        border: 2px solid {ACCENT};
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        background-color: {ACCENT};
        color: {LIGHT_TEXT};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    /* Card styling */
    .card {{
        background: {CARD_BG};
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        padding: 20px;
        margin-bottom: 20px;
        border-left: 4px solid {PRIMARY};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }}
    
    /* Status indicators */
    .safe {{
        color: #43A047;
        font-weight: bold;
    }}
    
    .unsafe {{
        color: {WARNING};
        font-weight: bold;
    }}
    
    /* Value display */
    .value-display {{
        font-size: 1.8rem;
        font-weight: bold;
        color: {PRIMARY};
        text-align: center;
        margin: 10px 0;
    }}
    
    /* Section headers */
    .section-header {{
        background: linear-gradient(90deg, {PRIMARY}, #2c3e50);
        color: {LIGHT_TEXT};
        padding: 12px 20px;
        border-radius: 8px;
        margin: 25px 0 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    /* Material design elements */
    .material-card {{
        background: {CARD_BG};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }}
    
    .material-card:hover {{
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }}
    
    /* Progress bars */
    .progress-container {{
        height: 10px;
        background-color: #E0E0E0;
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
    }}
    
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {PRIMARY}, #2c3e50);
    }}
    
    /* Table styling */
    table {{
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    th {{
        background-color: {PRIMARY} !important;
        color: {LIGHT_TEXT} !important;
    }}
    
    tr:nth-child(even) {{
        background-color: #F5F7FA !important;
    }}
    
    /* Expander styling */
    .stExpander {{
        border: 1px solid #E0E0E0 !important;
        border-radius: 8px;
        margin-bottom: 15px;
        overflow: hidden;
    }}
    
    .stExpander summary {{
        background-color: {PRIMARY} !important;
        color: {LIGHT_TEXT} !important;
        padding: 12px 15px;
        font-weight: bold;
    }}
    
    /* Plot styling */
    .st-emotion-cache-1v0mbdj {{
        border-radius: 8px;
        padding: 15px;
        background-color: {CARD_BG} !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }}
    
    /* Input fields */
    .stNumberInput, .stSlider {{
        color: {DARK_TEXT} !important;
    }}
    
    /* Slider styling */
    div[data-baseweb="slider"] > div:first-child {{
        background-color: #E0E0E0 !important;
    }}
    
    div[role="slider"] {{
        background-color: {PRIMARY} !important;
        border: none !important;
    }}
    
    /* Dataset tabs */
    .dataset-tab {{
        padding: 10px 20px;
        margin-right: 10px;
        border-radius: 30px;
        cursor: pointer;
        display: inline-block;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    .dataset-tab.active {{
        background-color: {PRIMARY};
        color: {LIGHT_TEXT};
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    .dataset-tab.inactive {{
        background-color: #E3F2FD;
        color: {PRIMARY};
    }}
    
    .dataset-tab.inactive:hover {{
        background-color: #BBDEFB;
        transform: translateY(-2px);
    }}
    
    /* Metric cards */
    .metric-card {{
        background: {CARD_BG};
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        border-top: 4px solid {PRIMARY};
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.12);
    }}
    
    /* Footer styling */
    .footer {{
        background: linear-gradient(90deg, {PRIMARY}, #2c3e50);
        color: {LIGHT_TEXT};
        padding: 25px;
        border-radius: 8px;
        margin-top: 30px;
        box-shadow: 0 -4px 6px rgba(0,0,0,0.05);
    }}
    
    /* Animation for important values */
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    /* Force all text to black */
    body, p, div, span, input, label, select, textarea, .stMarkdown, .stAlert, .stText, .stCodeBlock {{
        color: {DARK_TEXT} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state for datasets
if 'datasets' not in st.session_state:
    st.session_state.datasets = {
        'Dataset 1': {'inputs': None, 'results': None},
        'Dataset 2': {'inputs': None, 'results': None},
        'Dataset 3': {'inputs': None, 'results': None}
    }

if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = 'Dataset 1'

# App header with industrial theme
st.markdown(f"""
<div style="background: linear-gradient(90deg, {PRIMARY}, #2c3e50); padding:30px; border-radius:8px; margin-bottom:30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <h1 style="color:{LIGHT_TEXT}; margin:0;">⚙️ Pipeline Integrity Management System</h1>
    <p style="color:#E3F2FD; font-size:1.2rem;">Corrosion Assessment & Fitness-for-Service Analysis</p>
</div>
""", unsafe_allow_html=True)

# Dataset tabs with industrial design
st.markdown("""
<div style="display: flex; justify-content: center; margin-bottom: 30px;">
    <div style="background: white; padding: 10px; border-radius: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
""", unsafe_allow_html=True)

cols = st.columns(3)
for i, dataset in enumerate(['Dataset 1', 'Dataset 2', 'Dataset 3']):
    with cols[i]:
        is_active = st.session_state.current_dataset == dataset
        class_name = "active" if is_active else "inactive"
        st.markdown(f'<div class="dataset-tab {class_name}" onclick="setDataset(\'{dataset}\')">{dataset}</div>', 
                   unsafe_allow_html=True)

st.markdown("""
    </div>
</div>

<script>
function setDataset(dataset) {
    fetch('/set_dataset?dataset=' + dataset).then(() => window.location.reload());
}
</script>
""", unsafe_allow_html=True)

# Sidebar with industrial theme
with st.sidebar:
    # Dataset selection
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {PRIMARY}, #2c3e50); padding:15px; border-radius:8px; margin-bottom:20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h3 style="color:{LIGHT_TEXT}; margin:0; text-align:center;">Pipeline Parameters</h3>
        <p style="color:#E3F2FD; margin:0; text-align:center;">Current: <strong>{st.session_state.current_dataset}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input sections in expanders
    with st.expander("📏 Dimensional Parameters", expanded=True):
        inputs = {
            'pipe_thickness': st.number_input('Pipe Thickness, t (mm)', 
                                            min_value=1.0, max_value=30.0, 
                                            value=9.5, step=0.1,
                                            help="Wall thickness of the pipe"),
            'pipe_diameter': st.number_input('Pipe Diameter, D (mm)', 
                                           min_value=50.0, max_value=500.0, 
                                           value=168.275, step=0.1,
                                           help="Outside diameter of pipe"),
            'pipe_length': st.number_input('Pipe Length, L (mm)', 
                                         min_value=1000.0, max_value=5000000.0, 
                                         value=2400000.0, step=1000.0,
                                         help="Total length of pipeline section"),
            'corrosion_length': st.number_input('Corrosion Length, Lc (mm)', 
                                            min_value=0.0, max_value=500.0, 
                                            value=23.0, step=1.0,
                                            help="Axial length of corrosion defect"),
            'corrosion_depth': st.number_input('Corrosion Depth, Dc (mm)', 
                                           min_value=0.0, max_value=10.0, 
                                           value=3.9, step=0.1,
                                           help="Maximum depth of corrosion")
        }
    
    with st.expander("🧱 Material Properties", expanded=True):
        inputs['yield_stress'] = st.number_input('Yield Stress, Sy (MPa)', 
                                               min_value=100.0, max_value=1000.0, 
                                               value=290.0, step=10.0,
                                               help="Material yield strength")
        inputs['uts'] = st.number_input('Ultimate Tensile Strength, UTS (MPa)', 
                                      min_value=200.0, max_value=1500.0, 
                                      value=495.0, step=10.0,
                                      help="Material ultimate tensile strength")
    
    with st.expander("📊 Operating Conditions", expanded=True):
        inputs['max_pressure'] = st.number_input('Max Operating Pressure (MAOP) (MPa)', 
                                               min_value=0, max_value=50, 
                                               value=13, step=1,
                                               help="Maximum allowable operating pressure")
        inputs['min_pressure'] = st.number_input('Min Operating Pressure (MPa)', 
                                                min_value=0, max_value=50, 
                                                value=5, step=1,
                                                help="Minimum operating pressure")
    
    with st.expander("📈 Corrosion Growth", expanded=True):
        inputs['inspection_year'] = st.number_input('Inspection Year', 
                                                  min_value=1900, max_value=2100, 
                                                  value=2023, step=1,
                                                  help="Year of current inspection")
        inputs['radial_corrosion_rate'] = st.number_input('Radial Corrosion Rate (mm/year)', 
                                                        min_value=0.01, max_value=2.0, 
                                                        value=0.1, step=0.01,
                                                        help="Depth increase per year")
        inputs['axial_corrosion_rate'] = st.number_input('Axial Corrosion Rate (mm/year)', 
                                                       min_value=0.01, max_value=2.0, 
                                                       value=0.1, step=0.01,
                                                       help="Length increase per year")
        inputs['projection_years'] = st.number_input('Projection Period (years)', 
                                                   min_value=1, max_value=50, 
                                                   value=20, step=1,
                                                   help="Years to project into future")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background: {CARD_BG}; padding:15px; border-radius:8px; margin-top:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.08); border-left: 4px solid #43A047;">
        <h4 style="color:{DARK_TEXT}; margin:0;">Safety Indicators</h4>
        <div style="display: flex; align-items: center; margin-top:10px;">
            <div style="background-color: #43A047; width:20px; height:20px; border-radius:50%; margin-right:10px;"></div>
            <span style="color:{DARK_TEXT};">Safe: ERF ≤ 1</span>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="background-color: {WARNING}; width:20px; height:20px; border-radius:50%; margin-right:10px;"></div>
            <span style="color:{DARK_TEXT};">Unsafe: ERF > 1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button('Run Analysis', use_container_width=True, type="primary"):
        st.session_state.run_analysis = True
        # Store inputs for current dataset
        st.session_state.datasets[st.session_state.current_dataset]['inputs'] = inputs
        # Clear results to force recalculation
        st.session_state.datasets[st.session_state.current_dataset]['results'] = None
    
    if st.button('Reset All', use_container_width=True):
        st.session_state.run_analysis = False
        # Reset all datasets
        for key in st.session_state.datasets:
            st.session_state.datasets[key] = {'inputs': None, 'results': None}

# Image and intro section
st.subheader('Pipeline Configuration')
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png", 
             caption="Fig. 1: Corrosion defect geometry")
with col2:
    st.markdown(f"""
    <div class="material-card">
        <h4 style="border-bottom: 2px solid {PRIMARY}; padding-bottom: 8px; color:{DARK_TEXT};">Assessment Protocol</h4>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">1</div>
                <span>Select dataset to configure</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">2</div>
                <span>Enter pipeline parameters</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">3</div>
                <span>Specify operating conditions</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">4</div>
                <span>Set corrosion growth rates</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">5</div>
                <span>Run analysis & review results</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {PRIMARY}; color:white; width:30px; height:30px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">6</div>
                <span>Analyze remaining life</span>
            </div>
        </div>
        <div class="progress-container" style="margin-top:20px;">
            <div class="progress-bar" style="width: {'50%' if st.session_state.get('run_analysis', False) else '10%'};"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top:10px;">
            <span style="color:{DARK_TEXT};">Status:</span>
            <span style="color:{PRIMARY}; font-weight:bold;">{'Analysis Complete' if st.session_state.get('run_analysis', False) else 'Ready for Input'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Burst pressure models
def modified_asme_b31g(D, t, d, L, Sy):
    flow_stress = Sy + 68.95  # MPa (SMYS + 10 ksi)
    limit = math.sqrt(50 * D * t)
    
    if L <= limit:
        M = math.sqrt(1 + 0.6275 * (L**2) / (D * t) - 0.003375 * (L**4) / ((D * t)**2))
    else:
        M = 3.3 + 0.032 * (L**2) / (D * t)
    
    return (2 * t * flow_stress / D) * ((1 - 0.85 * d/t) / (1 - 0.85 * (d/t) / M))

def dnv_rp_f101(D, t, d, L, UTS):
    Q = math.sqrt(1 + 0.31 * (L**2) / (D * t))
    return 0.9 * UTS * (2 * t / (D - t)) * ((1 - d/t) / (1 - (d/t) / Q))

def pcorrc(D, t, d, L, UTS):
    return 0.95 * UTS * (2 * t / D) * (1 - d/t) * (1 - math.exp(-0.224 * L / math.sqrt(D * (t - d))))

# Calculations
def calculate_pressures(inputs):
    t = inputs['pipe_thickness']
    D = inputs['pipe_diameter']
    Lc = inputs['corrosion_length']
    Dc = inputs['corrosion_depth']
    UTS = inputs['uts']
    Sy = inputs['yield_stress']
    
    # Validate inputs to prevent division by zero
    if t <= 0 or D <= 0:
        raise ValueError("Pipe thickness and diameter must be positive values")
    
    # Use specialized models
    P_asme = modified_asme_b31g(D, t, Dc, Lc, Sy)
    P_dnv = dnv_rp_f101(D, t, Dc, Lc, UTS)
    P_pcorrc = pcorrc(D, t, Dc, Lc, UTS)
    
    # Keep existing models for comparison
    P_vm = (4 * t * UTS) / (math.sqrt(3) * D)
    P_tresca = (2 * t * UTS) / D
    
    return {
        'P_vm': P_vm,
        'P_tresca': P_tresca,
        'P_asme': P_asme,
        'P_dnv': P_dnv,
        'P_pcorrc': P_pcorrc
    }

def calculate_stresses(inputs):
    t = inputs['pipe_thickness']
    D = inputs['pipe_diameter']
    Pop_max = inputs['max_pressure']
    Pop_min = inputs['min_pressure']
    UTS = inputs['uts']
    Sy = inputs['yield_stress']
    
    # Principal stresses
    P1_max = Pop_max * D / (2 * t)
    P2_max = Pop_max * D / (4 * t)
    P3_max = 0
    
    P1_min = Pop_min * D / (2 * t)
    P2_min = Pop_min * D / (4 * t)
    P3_min = 0
    
    # Von Mises stresses
    def vm_stress(p1, p2, p3):
        return (1/math.sqrt(2)) * math.sqrt((p1-p2)**2 + (p2-p3)**2 + (p3-p1)**2)
    
    sigma_vm_max = vm_stress(P1_max, P2_max, P3_max)
    sigma_vm_min = vm_stress(P1_min, P2_min, P3_min)
    
    # Fatigue parameters
    sigma_a = (sigma_vm_max - sigma_vm_min) / 2
    sigma_m = (sigma_vm_max + sigma_vm_min) / 2
    Se = 0.5 * UTS
    sigma_f = UTS + 345  # Morrow's fatigue strength coefficient
    
    return {
        'sigma_vm_max': sigma_vm_max,
        'sigma_vm_min': sigma_vm_min,
        'sigma_a': sigma_a,
        'sigma_m': sigma_m,
        'Se': Se,
        'sigma_f': sigma_f
    }

def calculate_fatigue_criteria(sigma_a, sigma_m, Se, UTS, Sy, sigma_f):
    return {
        'Goodman': (sigma_a / Se) + (sigma_m / UTS),
        'Soderberg': (sigma_a / Se) + (sigma_m / Sy),
        'Gerber': (sigma_a / Se) + (sigma_m / UTS)**2,
        'Morrow': (sigma_a / Se) + (sigma_m / sigma_f),
        'ASME-Elliptic': np.sqrt((sigma_a / Se)**2 + (sigma_m / Sy)**2)
    }

# FFS Assessment
def calculate_ffs_assessment(inputs, current_depth, current_length):
    results = []
    failure_years = {}
    
    for year in range(inputs['inspection_year'], 
                     inputs['inspection_year'] + inputs['projection_years'] + 1):
        # Calculate corrosion growth
        years_elapsed = year - inputs['inspection_year']
        d = current_depth + inputs['radial_corrosion_rate'] * years_elapsed
        L = current_length + inputs['axial_corrosion_rate'] * years_elapsed
        
        # Cap depth at 80% wall thickness
        d = min(d, inputs['pipe_thickness'] * 0.8)
        
        # Calculate burst pressures
        P_asme = modified_asme_b31g(
            inputs['pipe_diameter'],
            inputs['pipe_thickness'],
            d,
            L,
            inputs['yield_stress']
        )
        
        P_dnv = dnv_rp_f101(
            inputs['pipe_diameter'],
            inputs['pipe_thickness'],
            d,
            L,
            inputs['uts']
        )
        
        P_pcorrc = pcorrc(
            inputs['pipe_diameter'],
            inputs['pipe_thickness'],
            d,
            L,
            inputs['uts']
        )
        
        # Calculate ERF (Estimated Repair Factor)
        erf_asme = inputs['max_pressure'] / P_asme
        erf_dnv = inputs['max_pressure'] / P_dnv
        erf_pcorrc = inputs['max_pressure'] / P_pcorrc
        
        # Determine critical ERF
        critical_erf = max(erf_asme, erf_dnv, erf_pcorrc)
        
        # Record results
        results.append({
            'year': year,
            'depth': d,
            'length': L,
            'P_asme': P_asme,
            'P_dnv': P_dnv,
            'P_pcorrc': P_pcorrc,
            'erf_asme': erf_asme,
            'erf_dnv': erf_dnv,
            'erf_pcorrc': erf_pcorrc,
            'critical_erf': critical_erf
        })
        
        # Track failure years
        if erf_asme >= 1.0 and 'ASME' not in failure_years:
            failure_years['ASME'] = year
        if erf_dnv >= 1.0 and 'DNV' not in failure_years:
            failure_years['DNV'] = year
        if erf_pcorrc >= 1.0 and 'PCORRC' not in failure_years:
            failure_years['PCORRC'] = year
    
    return results, failure_years

# Main analysis section
if st.session_state.get('run_analysis', False):
    # Calculate for current dataset
    current_data = st.session_state.datasets[st.session_state.current_dataset]
    
    if current_data['inputs'] is not None:
        try:
            # Calculate all parameters
            pressures = calculate_pressures(current_data['inputs'])
            stresses = calculate_stresses(current_data['inputs'])
            fatigue = calculate_fatigue_criteria(
                stresses['sigma_a'], stresses['sigma_m'],
                stresses['Se'], current_data['inputs']['uts'], 
                current_data['inputs']['yield_stress'],
                stresses['sigma_f']
            )
            
            # Store results
            current_data['results'] = {
                'pressures': pressures,
                'stresses': stresses,
                'fatigue': fatigue
            }
            
            # Burst Pressure Results in Card Layout
            st.markdown(f"""
<div class="section-header">
    <h3 style="margin:0;">📊 Burst Pressure Assessment ({st.session_state.current_dataset})</h3>
</div>
""", unsafe_allow_html=True)
            
            burst_cols = st.columns(5)
            burst_data = [
                ("Von Mises", pressures['P_vm'], PRIMARY, current_data['inputs']['max_pressure']/pressures['P_vm']),
                ("Tresca", pressures['P_tresca'], SECONDARY, current_data['inputs']['max_pressure']/pressures['P_tresca']),
                ("ASME B31G", pressures['P_asme'], ACCENT, current_data['inputs']['max_pressure']/pressures['P_asme']),
                ("DNV", pressures['P_dnv'], "#6A1B9A", current_data['inputs']['max_pressure']/pressures['P_dnv']),
                ("PCORRC", pressures['P_pcorrc'], WARNING, current_data['inputs']['max_pressure']/pressures['P_pcorrc'])
            ]
            
            for i, (name, value, color, erf) in enumerate(burst_data):
                safe = erf <= 1
                status = "✅ Safe" if safe else "❌ Unsafe"
                status_class = "safe" if safe else "unsafe"
                pulse_class = "pulse" if not safe else ""
                
                with burst_cols[i]:
                    st.markdown(f"""
                    <div class="card {pulse_class}" style="border-left: 4px solid {color};">
                        <h4 style="margin-top: 0; color:{color};">{name}</h4>
                        <div class="value-display">{value:.2f} MPa</div>
                        <div style="font-size: 1rem; text-align:center; margin: 10px 0;">
                            ERF: <span class="{status_class}" style="font-size:1.2rem;">{erf:.3f}</span>
                        </div>
                        <div style="text-align:center; margin-bottom:10px;">
                            <strong>{status}</strong>
                        </div>
                        <div style="height: 6px; background: #E0E0E0; border-radius:3px; margin: 15px 0;">
                            <div style="height: 6px; background: {color}; width: {min(100, value/10*100)}%; border-radius:3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # FFS Assessment Section
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">⏳ Fitness-for-Service Assessment ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Get current corrosion parameters
            current_depth = current_data['inputs']['corrosion_depth']
            current_length = current_data['inputs']['corrosion_length']
            
            # Calculate FFS assessment
            ffs_results, failure_years = calculate_ffs_assessment(
                current_data['inputs'], 
                current_depth, 
                current_length
            )
            
            # Create DataFrame for display
            df = pd.DataFrame(ffs_results)
            
            # Display failure predictions in metric cards
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 1.1rem; color:{DARK_TEXT};">Current Year</div>
                    <div style="font-size: 2rem; font-weight:bold; color:{PRIMARY}; margin:10px 0;">{current_data['inputs']['inspection_year']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[1]:
                critical_erf = df.iloc[0]['critical_erf']
                status_color = "#43A047" if critical_erf <= 1 else WARNING
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 1.1rem; color:{DARK_TEXT};">Critical ERF Now</div>
                    <div style="font-size: 2rem; font-weight:bold; color:{status_color}; margin:10px 0;">{critical_erf:.3f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[2]:
                asme_fail = failure_years.get('ASME', "Beyond projection")
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 1.1rem; color:{DARK_TEXT};">ASME Failure Year</div>
                    <div style="font-size: 2rem; font-weight:bold; color:{WARNING if asme_fail != "Beyond projection" else DARK_TEXT}; margin:10px 0;">{asme_fail}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with metric_cols[3]:
                dnv_fail = failure_years.get('DNV', "Beyond projection")
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size: 1.1rem; color:{DARK_TEXT};">DNV Failure Year</div>
                    <div style="font-size: 2rem; font-weight:bold; color:{WARNING if dnv_fail != "Beyond projection" else DARK_TEXT}; margin:10px 0;">{dnv_fail}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Plot 1: Burst Pressure over time
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📉 Burst Pressure Projection ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)

            fig1, ax1 = plt.subplots(figsize=(10, 5))
            fig1.patch.set_facecolor(CARD_BG)

            # Burst Pressure Plot
            ax1.plot(df['year'], df['P_asme'], label='ASME B31G', color=COLORS['Goodman'], linestyle='-', linewidth=2)
            ax1.plot(df['year'], df['P_dnv'], label='DNV-RP-F101', color=COLORS['Soderberg'], linestyle='--', linewidth=2)
            ax1.plot(df['year'], df['P_pcorrc'], label='PCORRC', color=COLORS['Gerber'], linestyle='-.', linewidth=2)
            ax1.axhline(y=current_data['inputs']['max_pressure'], color=WARNING, linestyle=':', linewidth=2.5, label='MAOP')

            # Formatting
            ax1.set_xlabel('Year', fontsize=10, color=DARK_TEXT)
            ax1.set_ylabel('Burst Pressure (MPa)', fontsize=10, color=DARK_TEXT)
            ax1.set_title('Burst Pressure Projection', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax1.grid(True, linestyle='--', alpha=0.7, color=PRIMARY)
            ax1.legend(loc='upper right', facecolor=CARD_BG, edgecolor=DARK_TEXT)

            # Set axis colors
            ax1.spines['bottom'].set_color(DARK_TEXT)
            ax1.spines['top'].set_color(DARK_TEXT) 
            ax1.spines['right'].set_color(DARK_TEXT)
            ax1.spines['left'].set_color(DARK_TEXT)
            ax1.tick_params(axis='x', colors=DARK_TEXT)
            ax1.tick_params(axis='y', colors=DARK_TEXT)

            st.pyplot(fig1)

            # Plot 2: ERF over time
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📈 Estimated Repair Factor (ERF) Projection ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)

            fig2, ax2 = plt.subplots(figsize=(10, 5))
            fig2.patch.set_facecolor(CARD_BG)

            # ERF Plot
            ax2.plot(df['year'], df['erf_asme'], label='ASME ERF', color=COLORS['Goodman'], linestyle='-', linewidth=2)
            ax2.plot(df['year'], df['erf_dnv'], label='DNV ERF', color=COLORS['Soderberg'], linestyle='--', linewidth=2)
            ax2.plot(df['year'], df['erf_pcorrc'], label='PCORRC ERF', color=COLORS['Gerber'], linestyle='-.', linewidth=2)
            ax2.plot(df['year'], df['critical_erf'], label='Critical ERF', color=DARK_TEXT, linewidth=3)
            ax2.axhline(y=1.0, color=WARNING, linestyle='-', linewidth=2, label='Failure Threshold')

            # Formatting
            ax2.set_xlabel('Year', fontsize=10, color=DARK_TEXT)
            ax2.set_ylabel('ERF (MAOP/Burst Pressure)', fontsize=10, color=DARK_TEXT)
            ax2.set_title('Estimated Repair Factor Projection', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax2.grid(True, linestyle='--', alpha=0.7, color=PRIMARY)
            ax2.legend(loc='upper right', facecolor=CARD_BG, edgecolor=DARK_TEXT)

            # Set axis colors
            ax2.spines['bottom'].set_color(DARK_TEXT)
            ax2.spines['top'].set_color(DARK_TEXT) 
            ax2.spines['right'].set_color(DARK_TEXT)
            ax2.spines['left'].set_color(DARK_TEXT)
            ax2.tick_params(axis='x', colors=DARK_TEXT)
            ax2.tick_params(axis='y', colors=DARK_TEXT)

            st.pyplot(fig2)

            # Display detailed table
            with st.expander("Detailed Projection Data", expanded=False):
                # Format columns
                display_df = df.copy()
                display_df['Depth'] = display_df['depth'].apply(lambda x: f"{x:.2f} mm")
                display_df['Length'] = display_df['length'].apply(lambda x: f"{x:.2f} mm")
                display_df['ASME Burst'] = display_df['P_asme'].apply(lambda x: f"{x:.2f} MPa")
                display_df['DNV Burst'] = display_df['P_dnv'].apply(lambda x: f"{x:.2f} MPa")
                display_df['PCORRC Burst'] = display_df['P_pcorrc'].apply(lambda x: f"{x:.2f} MPa")
                display_df['Critical ERF'] = display_df['critical_erf'].apply(lambda x: f"{x:.3f}")
                
                # Highlight failure years
                def highlight_erf(val):
                    erf = float(val)
                    color = WARNING if erf >= 1.0 else "#43A047"
                    weight = "bold" if erf >= 1.0 else "normal"
                    return f'color: {color}; font-weight: {weight};'
                
                st.dataframe(
                    display_df[['year', 'Depth', 'Length', 'ASME Burst', 'DNV Burst', 'PCORRC Burst', 'Critical ERF']]
                    .style.applymap(highlight_erf, subset=['Critical ERF']),
                    height=300
                )
            
            # Stress Analysis
            st.markdown(f"""
<div class="section-header">
    <h3 style="margin:0;">📈 Stress Analysis ({st.session_state.current_dataset})</h3>
</div>
""", unsafe_allow_html=True)
            
            stress_col1, stress_col2 = st.columns([1, 1])
            
            with stress_col1:
                st.markdown(f"""
                <div class="material-card">
                    <h4>Stress Parameters</h4>
                    <table style="width:100%; border-collapse: collapse; font-size: 1rem;">
                        <tr style="border-bottom: 1px solid #E0E0E0;">
                            <td style="padding: 10px;">Max VM Stress</td>
                            <td style="text-align: right; padding: 10px; font-weight: bold; color:{PRIMARY};">{stresses['sigma_vm_max']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E0E0E0;">
                            <td style="padding: 10px;">Min VM Stress</td>
                            <td style="text-align: right; padding: 10px; font-weight: bold; color:{PRIMARY};">{stresses['sigma_vm_min']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E0E0E0;">
                            <td style="padding: 10px;">Alternating Stress</td>
                            <td style="text-align: right; padding: 10px; font-weight: bold; color:{SECONDARY};">{stresses['sigma_a']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #E0E0E0;">
                            <td style="padding: 10px;">Mean Stress</td>
                            <td style="text-align: right; padding: 10px; font-weight: bold; color:{SECONDARY};">{stresses['sigma_m']:.2f} MPa</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px;">Endurance Limit</td>
                            <td style="text-align: right; padding: 10px; font-weight: bold; color:{ACCENT};">{stresses['Se']:.2f} MPa</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            with stress_col2:
                # Stress visualization with industrial colors
                fig, ax = plt.subplots(figsize=(6, 4))
                categories = ['Max Stress', 'Min Stress', 'Amplitude']
                values = [
                    stresses['sigma_vm_max'],
                    stresses['sigma_vm_min'],
                    stresses['sigma_a']
                ]
                colors = [PRIMARY, SECONDARY, ACCENT]
                bars = ax.bar(categories, values, color=colors, edgecolor=DARK_TEXT)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f} MPa',
                            ha='center', va='bottom', fontsize=10, color=DARK_TEXT)
                
                ax.set_ylim(0, max(values) * 1.2)
                ax.set_title('Stress Distribution', fontsize=12, color=DARK_TEXT, fontweight='bold')
                ax.grid(axis='y', linestyle='--', alpha=0.7, color=PRIMARY)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color(DARK_TEXT)
                ax.spines['bottom'].set_color(DARK_TEXT)
                ax.tick_params(axis='x', colors=DARK_TEXT)
                ax.tick_params(axis='y', colors=DARK_TEXT)
                ax.set_facecolor(CARD_BG)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Enhanced Plotting with Matplotlib
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📉 Fatigue Analysis Diagram (All Datasets)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(CARD_BG)
            
            # Generate x-axis values
            x = np.linspace(0, inputs['uts']*1.1, 100)
            
            # Plot all criteria with distinct colors and line styles
            ax.plot(x, stresses['Se']*(1 - x/inputs['uts']), 
                    color=COLORS['Goodman'], linewidth=2.5, linestyle='-', label='Goodman')
            ax.plot(x, stresses['Se']*(1 - x/inputs['yield_stress']), 
                    color=COLORS['Soderberg'], linewidth=2.5, linestyle='--', label='Soderberg')
            ax.plot(x, stresses['Se']*(1 - (x/inputs['uts'])**2), 
                    color=COLORS['Gerber'], linestyle=':', linewidth=2.5, label='Gerber')
            ax.plot(x, stresses['Se']*(1 - x/stresses['sigma_f']), 
                    color=COLORS['Morrow'], linestyle='-.', linewidth=2.5, label='Morrow')
            ax.plot(x, stresses['Se']*np.sqrt(1 - (x/inputs['yield_stress'])**2), 
                    color=COLORS['ASME-Elliptic'], linestyle=(0, (5, 1)), linewidth=2.5, label='ASME-Elliptic')
            
            # Plot operating points for all datasets
            markers = ['o', 's', 'D']  # Circle, Square, Diamond
            for i, (dataset_name, dataset) in enumerate(st.session_state.datasets.items()):
                if dataset['results']:
                    ds = dataset['results']['stresses']
                    ax.scatter(ds['sigma_m'], ds['sigma_a'], 
                              color=DATASET_COLORS[i], s=150, edgecolor=DARK_TEXT, zorder=10,
                              marker=markers[i], label=f'{dataset_name} (σm={ds["sigma_m"]:.1f}, σa={ds["sigma_a"]:.1f})')
            
            # Mark key points
            ax.scatter(0, stresses['Se'], color=DARK_TEXT, s=100, marker='o', 
                      label=f'Se = {stresses["Se"]:.1f} MPa')
            ax.scatter(inputs['uts'], 0, color=DARK_TEXT, s=100, marker='s', 
                      label=f'UTS = {inputs["uts"]:.1f} MPa')
            ax.scatter(inputs['yield_stress'], 0, color=DARK_TEXT, s=100, marker='^', 
                      label=f'Sy = {inputs["yield_stress"]:.1f} MPa')
            
            # Formatting with high contrast - handle incomplete datasets
            max_x = inputs['uts'] * 1.1
            max_y = stresses['Se'] * 1.5
            
            # Collect all operating points to determine axis limits
            all_points = []
            for dataset in st.session_state.datasets.values():
                if dataset['results']:
                    ds = dataset['results']['stresses']
                    all_points.append(ds['sigma_m'])
                    all_points.append(ds['sigma_a'])
            
            if all_points:
                max_x = max(max_x, max(all_points) * 1.2)
                max_y = max(max_y, max(all_points) * 1.5)
            
            ax.set_xlim(0, max_x)
            ax.set_ylim(0, max_y)
            ax.set_xlabel('Mean Stress (σm) [MPa]', fontsize=10, color=DARK_TEXT)
            ax.set_ylabel('Alternating Stress (σa) [MPa]', fontsize=10, color=DARK_TEXT)
            ax.set_title('Fatigue Analysis Diagram', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax.grid(True, linestyle='--', alpha=0.7, color=PRIMARY)
            ax.set_facecolor(CARD_BG)
            
            # Set axis and tick colors
            ax.spines['bottom'].set_color(DARK_TEXT)
            ax.spines['top'].set_color(DARK_TEXT) 
            ax.spines['right'].set_color(DARK_TEXT)
            ax.spines['left'].set_color(DARK_TEXT)
            ax.tick_params(axis='x', colors=DARK_TEXT)
            ax.tick_params(axis='y', colors=DARK_TEXT)
            
            # Create custom legend
            ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1), fontsize=9, facecolor=CARD_BG, edgecolor=DARK_TEXT)
            plt.tight_layout()
            
            st.pyplot(fig)

        except ValueError as e:
            st.error(f"🚨 Calculation error: {str(e)}")
        except Exception as e:
            st.error(f"🚨 An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please run analysis for this dataset first")
else:
    st.markdown(f"""
    <div class="material-card" style="text-align: center; padding: 40px 20px;">
        <h4 style="color:{DARK_TEXT}; margin-bottom:20px;">⏳ Ready for Analysis</h4>
        <p style="color:{DARK_TEXT}; font-size:1.1rem; max-width:600px; margin:0 auto;">
            Select a dataset, enter pipeline parameters in the sidebar, and click 'Run Analysis' to perform integrity assessment
        </p>
        <div class="progress-container" style="max-width:400px; margin:30px auto;">
            <div class="progress-bar" style="width: 30%;"></div>
        </div>
        <div style="margin-top:20px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="{PRIMARY}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

# References and links in expanders
st.markdown(f"""
<div class="section-header">
    <h3 style="margin:0;">📚 References & Resources</h3>
</div>
""", unsafe_allow_html=True)

ref_col1, ref_col2 = st.columns([1, 1])
with ref_col1:
    with st.expander("Research References", expanded=False):
        st.markdown(f"""
        <div style="color:{DARK_TEXT};">
        - **Mohd et al. (2014)**  
          <span style="color:{PRIMARY};">Journal of Offshore Mechanics and Arctic Engineering</span>  
          On the Burst Strength Capacity of an Aging Subsea Gas Pipeline  
          [DOI:10.1115/1.4028041](https://doi.org/10.1115/1.4028041)
        
        - **ASME B31G-2012**  
          <span style="color:{PRIMARY};">Manual for Determining the Remaining Strength of Corroded Pipelines</span>
        
        - **DNV-RP-F101**  
          <span style="color:{PRIMARY};">Corroded Pipelines Standard</span>
        </div>
        """, unsafe_allow_html=True)

with ref_col2:
    with st.expander("Additional Resources", expanded=False):
        st.markdown(f"""
        <div style="color:{DARK_TEXT};">
        - <span style="color:{PRIMARY};">Pipeline Corrosion Assessment Guide</span>  
          [ASME Standards](https://www.asme.org/codes-standards/find-codes-standards/b31g-manual-determining-remaining-strength-corroded-pipelines)
        
        - <span style="color:{PRIMARY};">Corrosion Rate Calculator</span>  
          [NACE International](https://www.nace.org/resources/corrosion-basics/calculators)
        
        - <span style="color:{PRIMARY};">Pipeline Integrity Management Standards</span>  
          [API Standards](https://www.api.org/products-and-services/standards)
        </div>
        """, unsafe_allow_html=True)

# Footer with industrial design
st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h4 style="margin:0; color:{LIGHT_TEXT};">Pipeline Integrity Manager v2.0</h4>
            <p style="margin:5px 0 0; color:#BBDEFB;">Fitness-for-Service Analysis</p>
        </div>
        <div style="text-align: right;">
            <p style="margin:0; color:#BBDEFB;">Technical Support: pipeline@engineering.com</p>
            <p style="margin:0; color:#BBDEFB;">Phone: +1 (555) 123-4567</p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 20px; color:#BBDEFB;">
        © 2023 Pipeline Engineering Solutions | All rights reserved
    </div>
</div>
""", unsafe_allow_html=True)
