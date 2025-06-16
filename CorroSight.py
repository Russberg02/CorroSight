import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend before importing plt
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

# Color palette with high-contrast grayscale for diagrams
COLORS = {
    'Goodman': '#d62728',     # Red
    'Soderberg': '#1f77b4',   # Blue
    'Gerber': '#ff7f0e',      # Orange
    'Morrow': '#2ca02c',      # Green
    'ASME-Elliptic': '#9467bd', # Purple
    'OperatingPoint': '#FF0000', # Red (for visibility)
    'KeyPoints': '#000000'    # Black
}

# Dataset colors for the three operating points
DATASET_COLORS = ['#FF0000', '#00FF00', '#0000FF']  # Red, Green, Blue

# High-contrast color palette
BLACK = "#000000"
DARK_GRAY = "#333333"
MEDIUM_GRAY = "#666666"
LIGHT_GRAY = "#DDDDDD"
WHITE = "#FFFFFF"
ACCENT = "#444444"  # Dark gray for visual hierarchy
RED = "#FF0000"     # For critical indicators

# Custom CSS for high-contrast black and white styling
st.markdown(f"""
<style>
    /* Main styling */
    .stApp {{
        background-color: {WHITE};
        color: {BLACK};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Titles and headers */
    h1, h2, h3, h4, h5, h6 {{
        color: {BLACK} !important;
        border-bottom: 2px solid {BLACK};
        padding-bottom: 0.3rem;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {WHITE};
        color: {BLACK};
        border-right: 1px solid {MEDIUM_GRAY};
    }}
    
    .sidebar .sidebar-content {{
        background-color: {WHITE};
        color: {BLACK};
    }}
    
    /* Button styling */
    .stButton>button {{
        background-color: {MEDIUM_GRAY};
        color: {WHITE};
        border-radius: 4px;
        border: 1px solid {BLACK};
        font-weight: bold;
        padding: 0.5rem 1rem;
    }}
    
    .stButton>button:hover {{
        background-color: {DARK_GRAY};
        color: {WHITE};
    }}
    
    /* Card styling */
    .card {{
        background: {WHITE};
        border-radius: 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid {BLACK};
        border: 1px solid {BLACK};
    }}
    
    /* Status indicators */
    .safe {{
        color: {MEDIUM_GRAY};
        font-weight: bold;
    }}
    
    .unsafe {{
        color: {RED};
        font-weight: bold;
    }}
    
    /* Value display */
    .value-display {{
        font-size: 1.6rem;
        font-weight: bold;
        color: {BLACK};
    }}
    
    /* Section headers */
    .section-header {{
        background-color: {LIGHT_GRAY};
        color: {BLACK};
        padding: 10px 15px;
        border-radius: 4px;
        margin-top: 20px;
        border-left: 4px solid {BLACK};
    }}
    
    /* Material design elements */
    .material-card {{
        background: {WHITE};
        border: 1px solid {BLACK};
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }}
    
    /* Progress bars */
    .progress-container {{
        height: 8px;
        background-color: {LIGHT_GRAY};
        border-radius: 4px;
        margin: 10px 0;
        overflow: hidden;
    }}
    
    .progress-bar {{
        height: 100%;
        background-color: {BLACK};
    }}
    
    /* Table styling */
    table {{
        border: 1px solid {BLACK} !important;
    }}
    
    tr {{
        border-bottom: 1px solid {BLACK} !important;
    }}
    
    th, td {{
        color: {BLACK} !important;
        background-color: {WHITE} !important;
        border: 1px solid {BLACK} !important;
    }}
    
    /* Expander styling */
    .stExpander {{
        border: 1px solid {BLACK} !important;
        border-radius: 4px;
        margin-bottom: 10px;
    }}
    
    .st-emotion-cache-1c7k2aw {{
        border-color: {BLACK} !important;
    }}
    
    /* Plot styling */
    .st-emotion-cache-1v0mbdj {{
        border: 1px solid {BLACK} !important;
        border-radius: 4px;
        padding: 10px;
        background-color: {WHITE} !important;
    }}
    
    /* Input fields */
    .stNumberInput, .stSlider {{
        color: {BLACK} !important;
        background-color: {WHITE} !important;
    }}
    
    /* Sidebar headers */
    .sidebar .stExpander > label {{
        color: {BLACK} !important;
        font-weight: bold !important;
    }}

    /* Add this new section for input fields */
    .stNumberInput, .stSlider {{
        color: var(--text) !important;
    }}
    
    .stNumberInput input, .stSlider input {{
        color: var(--text) !important;
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
    }}
    
    .stNumberInput label, .stSlider label {{
        color: var(--text) !important;
    }}
    
    /* Slider track styling */
    .stSlider div[data-baseweb="slider"] > div:first-child {{
        background-color: var(--light-gray) !important;
    }}
    
    /* Slider thumb styling */
    .stSlider div[role="slider"] {{
        background-color: var(--border) !important;
        border: 1px solid var(--border) !important;
    }}
    
    /* Focus state styling */
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 0.2rem rgba(100, 100, 100, 0.25) !important;
    }}
    
    /* Dataset tabs */
    .dataset-tab {{
        padding: 8px 12px;
        margin-right: 5px;
        border: 1px solid {BLACK};
        border-radius: 4px;
        cursor: pointer;
        display: inline-block;
    }}
    
    .dataset-tab.active {{
        background-color: {BLACK};
        color: {WHITE};
    }}
    
    .dataset-tab.inactive {{
        background-color: {LIGHT_GRAY};
        color: {BLACK};
    }}
    
    /* Fix for radio buttons in dark mode */
    .stRadio > div[role="radiogroup"] > label {{
        color: {BLACK} !important;
    }}
    
    /* Custom styling for radio buttons */
    .stRadio > div {{
        flex-direction: row !important;
        gap: 15px !important;
    }}
    
    .stRadio > div > label {{
        background-color: #f0f0f0;
        padding: 8px 15px;
        border-radius: 4px;
        border: 1px solid #ccc;
        transition: all 0.3s ease;
    }}
    
    .stRadio > div > label:hover {{
        background-color: #e0e0e0;
    }}
    
    .stRadio > div > [data-baseweb="radio"]:checked + label {{
        background-color: {DARK_GRAY} !important;
        color: {WHITE} !important;
        border-color: {DARK_GRAY};
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

# App header with high contrast theme
st.markdown(f"""
<div style="background-color:{WHITE}; padding:20px; border-radius:5px; margin-bottom:20px; border-bottom: 3px solid {BLACK}">
    <h1 style="color:{BLACK}; margin:0;">🔍 CorroSight: Advanced Pipeline Integrity Platform</h1>
    <p style="color:{DARK_GRAY};">Predictive Corrosion Management • Fitness-for-Service Assessment • Lifecycle Optimization</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with improved contrast headers
with st.sidebar:
    # Dataset selection moved to sidebar
    st.markdown(f"""
    <div style="background-color:{WHITE}; padding:10px; border-radius:4px; margin-bottom:15px; border: 1px solid {BLACK}">
        <h3 style="color:{BLACK}; margin:0;">Dataset Selection</h3>
    </div>
    """, unsafe_allow_html=True)
    
    current_dataset = st.radio(
        "Select dataset:",
        options=["Dataset 1", "Dataset 2", "Dataset 3"],
        index=["Dataset 1", "Dataset 2", "Dataset 3"].index(st.session_state.current_dataset),
        label_visibility="collapsed"
    )
    st.session_state.current_dataset = current_dataset
    
    st.markdown(f"""
    <div style="background-color:{WHITE}; padding:10px; border-radius:4px; margin-bottom:15px; border: 1px solid {BLACK}">
        <h3 style="color:{BLACK}; margin:0;">Pipeline Parameters</h3>
        <p style="color:{BLACK}; margin:0;">Current: <strong>{st.session_state.current_dataset}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📏 Dimensional Parameters", expanded=True):
        inputs = {
            'pipe_thickness': st.number_input('Pipe Thickness, t (mm)', min_value=0.1, value=9.5),
            'pipe_diameter': st.number_input('Pipe Diameter, D (mm)', min_value=0.1, value=168.275),
            'pipe_length': st.number_input('Pipe Length, L (mm)', min_value=0.1, value=2400000.0),
            'corrosion_length': st.number_input('Corrosion Length, Lc (mm)', min_value=0.0, value=23.0),
            'corrosion_depth': st.number_input('Corrosion Depth, Dc (mm)', min_value=0.0, max_value=10.0, value=3.9)
        }
    
    with st.expander("🧱 Material Properties", expanded=True):
        inputs['yield_stress'] = st.number_input('Yield Stress, Sy (MPa)', min_value=0.1, value=290.0)
        inputs['uts'] = st.number_input('Ultimate Tensile Strength, UTS (MPa)', min_value=0.1, value=495.0)
    
    with st.expander("📊 Operating Conditions", expanded=True):
        inputs['max_pressure'] = st.slider('Max Operating Pressure (MAOP) (MPa)', 0, 50, 13)
        inputs['min_pressure'] = st.slider('Min Operating Pressure (MPa)', 0, 50, 5)
    
    with st.expander("📈 Corrosion Growth", expanded=True):
        inputs['inspection_year'] = st.number_input('Inspection Year', min_value=1900, max_value=2100, value=2023)
        inputs['radial_corrosion_rate'] = st.number_input('Radial Corrosion Rate (mm/year)', min_value=0.01, value=0.1, step=0.01)
        inputs['axial_corrosion_rate'] = st.number_input('Axial Corrosion Rate (mm/year)', min_value=0.01, value=0.1, step=0.01)
        inputs['projection_years'] = st.slider('Projection Period (years)', 1, 50, 20)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="background-color:{WHITE}; padding:10px; border-radius:4px; margin-top:15px; border: 1px solid {BLACK}">
        <h4 style="color:{BLACK}; margin:0;">Safety Indicators</h4>
        <p style="color:{MEDIUM_GRAY}; margin:0;">✅ Safe: ERF ≤ 1<br>❌ Unsafe: ERF > 1</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Run Analysis', use_container_width=True, type="primary"):
            st.session_state.run_analysis = True
            # Store inputs for current dataset
            st.session_state.datasets[st.session_state.current_dataset]['inputs'] = inputs
            # Clear results to force recalculation
            st.session_state.datasets[st.session_state.current_dataset]['results'] = None
    
    with col2:
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
        <h4 style="border-bottom: 1px solid {BLACK}; padding-bottom: 5px;">Assessment Protocol</h4>
        <ol>
            <li>Select dataset to configure</li>
            <li>Enter pipeline dimensions and material properties</li>
            <li>Specify operating pressure range</li>
            <li>Set corrosion growth parameters</li>
            <li>Click "Run Analysis" to perform assessment</li>
            <li>Review burst pressure calculations</li>
            <li>Analyze remaining life predictions</li>
        </ol>
        <div class="progress-container">
            <div class="progress-bar" style="width: {'50%' if st.session_state.get('run_analysis', False) else '10%'};"></div>
        </div>
        <p style="text-align: right; margin:0; color:{BLACK};">Status: {'Analysis Complete' if st.session_state.get('run_analysis', False) else 'Ready for Input'}</p>
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
                ("Von Mises", pressures['P_vm'], BLACK, current_data['inputs']['max_pressure']/pressures['P_vm']),
                ("Tresca", pressures['P_tresca'], MEDIUM_GRAY, current_data['inputs']['max_pressure']/pressures['P_tresca']),
                ("ASME B31G", pressures['P_asme'], DARK_GRAY, current_data['inputs']['max_pressure']/pressures['P_asme']),
                ("DNV", pressures['P_dnv'], ACCENT, current_data['inputs']['max_pressure']/pressures['P_dnv']),
                ("PCORRC", pressures['P_pcorrc'], BLACK, current_data['inputs']['max_pressure']/pressures['P_pcorrc'])
            ]
            
            for i, (name, value, color, erf) in enumerate(burst_data):
                safe = erf <= 1
                status = "✅ Safe" if safe else "❌ Unsafe"
                status_class = "safe" if safe else "unsafe"
                
                with burst_cols[i]:
                    st.markdown(f"""
                    <div class="card" style="border-left: 4px solid {color};">
                        <h4 style="margin-top: 0;">{name}</h4>
                        <div class="value-display">{value:.2f} MPa</div>
                        <div style="font-size: 0.9rem; margin-top: 5px;">
                            ERF: <span class="{status_class}">{erf:.3f}</span> • {status}
                        </div>
                        <div style="height: 4px; background: {LIGHT_GRAY}; margin: 10px 0;">
                            <div style="height: 4px; background: {color}; width: {min(100, value/10*100)}%;"></div>
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
            
            # Display failure predictions
            cols = st.columns(4)
            with cols[0]:
                st.metric("Current Year", current_data['inputs']['inspection_year'])
            with cols[1]:
                st.metric("Critical ERF Now", f"{df.iloc[0]['critical_erf']:.3f}", 
                         delta_color="inverse")
            with cols[2]:
                asme_fail = failure_years.get('ASME', "Beyond projection")
                st.metric("ASME Failure Year", asme_fail)
            with cols[3]:
                dnv_fail = failure_years.get('DNV', "Beyond projection")
                st.metric("DNV Failure Year", dnv_fail)
            
            # Plot burst pressure over time
            fig, ax1 = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(WHITE)
            
            # Burst Pressure Plot
            ax1.plot(df['year'], df['P_asme'], label='ASME B31G', color=COLORS['Goodman'], linestyle='-')
            ax1.plot(df['year'], df['P_dnv'], label='DNV-RP-F101', color=COLORS['Soderberg'], linestyle='--')
            ax1.plot(df['year'], df['P_pcorrc'], label='PCORRC', color=COLORS['Gerber'], linestyle='-.')
            ax1.axhline(y=current_data['inputs']['max_pressure'], color=RED, linestyle=':', label='MAOP')
            ax1.set_xlabel('Year', fontsize=10, color=BLACK)
            ax1.set_ylabel('Burst Pressure (MPa)', fontsize=10, color=BLACK)
            ax1.tick_params(axis='y', colors=BLACK)
            ax1.grid(True, linestyle='--', alpha=0.7, color=MEDIUM_GRAY)
            
            # ERF Plot (secondary axis)
            ax2 = ax1.twinx()
            ax2.plot(df['year'], df['critical_erf'], label='Critical ERF', color=BLACK, linewidth=2.5)
            ax2.axhline(y=1.0, color=RED, linestyle='-', label='Failure Threshold')
            ax2.set_ylabel('ERF (MAOP/Burst Pressure)', fontsize=10, color=BLACK)
            ax2.tick_params(axis='y', colors=BLACK)
            
            # Formatting
            ax1.set_title('Burst Pressure Projection and ERF', fontsize=12, fontweight='bold', color=BLACK)
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', facecolor=WHITE, edgecolor=BLACK)
            
            # Set axis colors
            for ax in [ax1, ax2]:
                ax.spines['bottom'].set_color(BLACK)
                ax.spines['top'].set_color(BLACK)
                ax.spines['right'].set_color(BLACK)
                ax.spines['left'].set_color(BLACK)
            
            st.pyplot(fig)
            
            # Display detailed table
            with st.expander("Detailed Projection Data"):
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
                    color = RED if erf >= 1.0 else MEDIUM_GRAY
                    return f'color: {color}; font-weight: bold;'
                
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
                    <table style="width:100%; border-collapse: collapse; font-size: 0.95rem;">
                        <tr style="border-bottom: 1px solid {BLACK};">
                            <td style="padding: 8px;">Max VM Stress</td>
                            <td style="text-align: right; padding: 8px; font-weight: bold;">{stresses['sigma_vm_max']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid {BLACK};">
                            <td style="padding: 8px;">Min VM Stress</td>
                            <td style="text-align: right; padding: 8px; font-weight: bold;">{stresses['sigma_vm_min']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid {BLACK};">
                            <td style="padding: 8px;">Alternating Stress</td>
                            <td style="text-align: right; padding: 8px; font-weight: bold;">{stresses['sigma_a']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom: 1px solid {BLACK};">
                            <td style="padding: 8px;">Mean Stress</td>
                            <td style="text-align: right; padding: 8px; font-weight: bold;">{stresses['sigma_m']:.2f} MPa</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">Endurance Limit</td>
                            <td style="text-align: right; padding: 8px; font-weight: bold;">{stresses['Se']:.2f} MPa</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            
            with stress_col2:
                # Simple stress visualization with high contrast
                fig, ax = plt.subplots(figsize=(6, 4))
                categories = ['Max Stress', 'Min Stress', 'Amplitude']
                values = [
                    stresses['sigma_vm_max'],
                    stresses['sigma_vm_min'],
                    stresses['sigma_a']
                ]
                # Grayscale colors for bars
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
                bars = ax.bar(categories, values, color=colors, edgecolor=BLACK)
                
                # Add value labels
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f} MPa',
                            ha='center', va='bottom', fontsize=9, color=BLACK)
                
                ax.set_ylim(0, max(values) * 1.2)
                ax.set_title('Stress Distribution', fontsize=10, color=BLACK)
                ax.grid(axis='y', linestyle='--', alpha=0.7, color=MEDIUM_GRAY)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color(BLACK)
                ax.spines['bottom'].set_color(BLACK)
                ax.tick_params(axis='x', colors=BLACK)
                ax.tick_params(axis='y', colors=BLACK)
                ax.set_facecolor(WHITE)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Enhanced Plotting with Matplotlib with high contrast
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📉 Fatigue Analysis Diagram (All Datasets)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(WHITE)
            
            # Generate x-axis values
            x = np.linspace(0, inputs['uts']*1.1, 100)
            
            # Plot all criteria with distinct grayscale and line styles
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
                              color=DATASET_COLORS[i], s=150, edgecolor='black', zorder=10,
                              marker=markers[i], label=f'{dataset_name} (σm={ds["sigma_m"]:.1f}, σa={ds["sigma_a"]:.1f})')
            
            # Mark key points with consistent style
            ax.scatter(0, stresses['Se'], color=COLORS['KeyPoints'], s=100, marker='o', 
                      label=f'Se = {stresses["Se"]:.1f} MPa')
            ax.scatter(inputs['uts'], 0, color=COLORS['KeyPoints'], s=100, marker='s', 
                      label=f'UTS = {inputs["uts"]:.1f} MPa')
            ax.scatter(inputs['yield_stress'], 0, color=COLORS['KeyPoints'], s=100, marker='^', 
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
            ax.set_xlabel('Mean Stress (σm) [MPa]', fontsize=10, color=BLACK)
            ax.set_ylabel('Alternating Stress (σa) [MPa]', fontsize=10, color=BLACK)
            ax.set_title('Fatigue Analysis Diagram', fontsize=12, fontweight='bold', color=BLACK)
            ax.grid(True, linestyle='--', alpha=0.7, color=MEDIUM_GRAY)
            ax.set_facecolor(WHITE)
            
            # Set axis and tick colors to black
            ax.spines['bottom'].set_color(BLACK)
            ax.spines['top'].set_color(BLACK) 
            ax.spines['right'].set_color(BLACK)
            ax.spines['left'].set_color(BLACK)
            ax.tick_params(axis='x', colors=BLACK)
            ax.tick_params(axis='y', colors=BLACK)
            
            # Create custom legend
            ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1), fontsize=9, facecolor=WHITE, edgecolor=BLACK)
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
    <div class="material-card">
        <h4 style="text-align: center; color:{BLACK};">⏳ Ready for Analysis</h4>
        <p style="text-align: center; color:{BLACK};">
            Select a dataset, enter parameters in the sidebar, and click 'Run Analysis'
        </p>
        <div class="progress-container">
            <div class="progress-bar" style="width: 30%;"></div>
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
        <div style="color:{BLACK};">
        - **Mohd et al. (2014)**  
          *Journal of Offshore Mechanics and Arctic Engineering*  
          On the Burst Strength Capacity of an Aging Subsea Gas Pipeline  
          [DOI:10.1115/1.4028041](https://doi.org/10.1115/1.4028041)
        
        - **ASME B31G-2012**  
          Manual for Determining the Remaining Strength of Corroded Pipelines
        
        - **DNV-RP-F101**  
          Corroded Pipelines Standard
        </div>
        """, unsafe_allow_html=True)

with ref_col2:
    with st.expander("Additional Resources", expanded=False):
        st.markdown(f"""
        <div style="color:{BLACK};">
        - [Pipeline Corrosion Assessment Guide](https://www.asme.org/codes-standards/find-codes-standards/b31g-manual-determining-remaining-strength-corroded-pipelines)
        
        - [Corrosion Rate Calculator](https://www.nace.org/resources/corrosion-basics/calculators)
        
        - [Pipeline Integrity Management Standards](https://www.api.org/products-and-services/standards)
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="background-color:{LIGHT_GRAY}; padding:20px; border-radius:5px; margin-top:20px; border-top: 2px solid {BLACK}">
    <div style="display: flex; justify-content: space-between; align-items: center; color:{BLACK};">
        <div>
            <h4 style="margin:0;">CorroSight v1.0 | Advanced Pipeline Integrity Platform</h4>
            <p style="margin:0;">© 2023 CorroSight Solutions</p>
        </div>
        <div style="text-align: right;">
            <p style="margin:0;">Technical Support: support@corrosight.io</p>
            <p style="margin:0;">Phone: +1 (800) COR-ROSI</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
