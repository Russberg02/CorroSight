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
    page_icon="🔧"
)

# Preserved original color palette
PRIMARY = "#2E86AB"   # Steel blue
SECONDARY = "#5C6B73"  # Metallic gray
ACCENT = "#F18F01"     # Safety orange
WARNING = "#C73E1D"    # Deep red
BACKGROUND = "#F5F5F5"  # Light gray background
CARD_BG = "#FFFFFF"    # White cards
DARK_TEXT = "#333333"  # Dark gray text
LIGHT_TEXT = "#FFFFFF" # White text
DATASET_COLORS = ["#2E86AB", "#5C6B73", "#F18F01"]

# Original color definitions for diagrams
COLORS = {
    'Goodman': '#2E86AB',
    'Soderberg': '#5C6B73',
    'Gerber': '#F18F01',
    'Morrow': '#C73E1D',
    'ASME-Elliptic': '#6A1B9A',
    'OperatingPoint': '#2E86AB',
    'KeyPoints': '#333333'
}

# Custom CSS with original colors
st.markdown(f"""
<style>
    .stApp {{
        background: {BACKGROUND} !important;
        color: {DARK_TEXT};
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {DARK_TEXT} !important;
        border-bottom: 2px solid {PRIMARY};
        padding-bottom: 0.3rem;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {CARD_BG};
        color: {DARK_TEXT};
        border-right: 2px solid {PRIMARY};
    }}
    
    .stButton>button {{
        background-color: {PRIMARY};
        color: {LIGHT_TEXT};
        border-radius: 4px;
        border: 2px solid {PRIMARY};
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
    
    .safe {{ color: #43A047; font-weight: bold; }}
    .unsafe {{ color: {WARNING}; font-weight: bold; }}
    
    .value-display {{
        font-size: 1.8rem;
        font-weight: bold;
        color: {PRIMARY};
        text-align: center;
        margin: 10px 0;
    }}
    
    .section-header {{
        background: linear-gradient(90deg, {PRIMARY}, #2E86AB);
        color: {LIGHT_TEXT};
        padding: 12px 20px;
        border-radius: 8px;
        margin: 25px 0 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .progress-container {{
        height: 10px;
        background-color: #E0E0E0;
        border-radius: 5px;
        margin: 15px 0;
        overflow: hidden;
    }}
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {PRIMARY}, #2E86AB);
    }}
    
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
    
    /* Additional styles */
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
    
    .footer {{
        background: linear-gradient(90deg, {PRIMARY}, #2E86AB);
        color: {LIGHT_TEXT};
        padding: 25px;
        border-radius: 8px;
        margin-top: 30px;
        box-shadow: 0 -4px 6px rgba(0,0,0,0.05);
    }}
    
    @keyframes pulse {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
        100% {{ transform: scale(1); }}
    }}
    .pulse {{
        animation: pulse 2s infinite;
    }}
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'datasets' not in st.session_state:
    st.session_state.datasets = {
        'Dataset 1': {
            'inputs': {
                'pipe_thickness': 5.0,
                'pipe_diameter': 100.0,
                'pipe_length': 10000.0,
                'corrosion_length': 50.0,
                'corrosion_depth': 1.0,
                'yield_stress': 250.0,
                'uts': 400.0,
                'max_pressure': 10.0,
                'min_pressure': 5.0,
                'inspection_year': 2023,
                'radial_corrosion_rate': 0.1,
                'axial_corrosion_rate': 0.1,
                'projection_years': 10
            },
            'results': None
        },
        'Dataset 2': {
            'inputs': {
                'pipe_thickness': 8.0,
                'pipe_diameter': 200.0,
                'pipe_length': 20000.0,
                'corrosion_length': 100.0,
                'corrosion_depth': 2.0,
                'yield_stress': 300.0,
                'uts': 500.0,
                'max_pressure': 15.0,
                'min_pressure': 7.0,
                'inspection_year': 2023,
                'radial_corrosion_rate': 0.2,
                'axial_corrosion_rate': 0.15,
                'projection_years': 15
            },
            'results': None
        },
        'Dataset 3': {
            'inputs': {
                'pipe_thickness': 12.0,
                'pipe_diameter': 300.0,
                'pipe_length': 30000.0,
                'corrosion_length': 150.0,
                'corrosion_depth': 3.0,
                'yield_stress': 350.0,
                'uts': 550.0,
                'max_pressure': 20.0,
                'min_pressure': 10.0,
                'inspection_year': 2023,
                'radial_corrosion_rate': 0.3,
                'axial_corrosion_rate': 0.2,
                'projection_years': 20
            },
            'results': None
        }
    }

if 'current_dataset' not in st.session_state:
    st.session_state.current_dataset = 'Dataset 1'
if 'run_analysis' not in st.session_state:
    st.session_state.run_analysis = False

# Engineering Calculations
def modified_asme_b31g(D, t, d, L, Sy):
    """ASME B31G burst pressure calculation"""
    if t <= 0 or D <= 0:
        return 0
    flow_stress = Sy + 68.95
    limit = math.sqrt(50 * D * t)
    if L <= limit:
        M = math.sqrt(1 + 0.6275 * (L**2) / (D * t) - 0.003375 * (L**4) / ((D * t)**2))
    else:
        M = 3.3 + 0.032 * (L**2) / (D * t)
    return (2 * t * flow_stress / D) * ((1 - 0.85 * d/t) / (1 - 0.85 * (d/t) / M))

def dnv_rp_f101(D, t, d, L, UTS):
    """DNV-RP-F101 burst pressure calculation"""
    if t <= 0 or D <= 0:
        return 0
    Q = math.sqrt(1 + 0.31 * (L**2) / (D * t))
    return 0.9 * UTS * (2 * t / (D - t)) * ((1 - d/t) / (1 - (d/t) / Q))

def pcorrc(D, t, d, L, UTS):
    """PCORRC burst pressure calculation"""
    if t <= 0 or D <= 0:
        return 0
    exponent = -0.224 * L / math.sqrt(D * (t - d))
    return 0.95 * UTS * (2 * t / D) * (1 - d/t) * (1 - math.exp(exponent))

def calculate_pressures(inputs):
    """Calculate all burst pressures"""
    t = inputs['pipe_thickness']
    D = inputs['pipe_diameter']
    Lc = inputs['corrosion_length']
    Dc = inputs['corrosion_depth']
    UTS = inputs['uts']
    Sy = inputs['yield_stress']
    
    # Theoretical models
    P_vm = (4 * t * UTS) / (math.sqrt(3) * D) if D > 0 else 0
    P_tresca = (2 * t * UTS) / D if D > 0 else 0
    
    # Industry models
    P_asme = modified_asme_b31g(D, t, Dc, Lc, Sy)
    P_dnv = dnv_rp_f101(D, t, Dc, Lc, UTS)
    P_pcorrc = pcorrc(D, t, Dc, Lc, UTS)
    
    return {
        'P_vm': P_vm,
        'P_tresca': P_tresca,
        'P_asme': P_asme,
        'P_dnv': P_dnv,
        'P_pcorrc': P_pcorrc
    }

def calculate_stresses(inputs):
    """Calculate stress parameters"""
    t = inputs['pipe_thickness']
    D = inputs['pipe_diameter']
    Pop_max = inputs['max_pressure']
    Pop_min = inputs['min_pressure']
    
    if t <= 0:
        return {
            'sigma_vm_max': 0, 'sigma_vm_min': 0,
            'sigma_a': 0, 'sigma_m': 0,
            'Se': 0, 'sigma_f': 0
        }
    
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
    Se = 0.5 * inputs['uts']
    sigma_f = inputs['uts'] + 345
    
    return {
        'sigma_vm_max': sigma_vm_max,
        'sigma_vm_min': sigma_vm_min,
        'sigma_a': sigma_a,
        'sigma_m': sigma_m,
        'Se': Se,
        'sigma_f': sigma_f
    }

def calculate_fatigue_criteria(sigma_a, sigma_m, Se, UTS, Sy, sigma_f):
    """Calculate fatigue failure criteria"""
    return {
        'Goodman': (sigma_a / Se) + (sigma_m / UTS) if Se > 0 else 0,
        'Soderberg': (sigma_a / Se) + (sigma_m / Sy) if Se > 0 else 0,
        'Gerber': (sigma_a / Se) + (sigma_m / UTS)**2 if Se > 0 else 0,
        'Morrow': (sigma_a / Se) + (sigma_m / sigma_f) if Se > 0 else 0,
        'ASME-Elliptic': np.sqrt((sigma_a / Se)**2 + (sigma_m / Sy)**2) if Se > 0 else 0
    }

def calculate_ffs_assessment(inputs, current_depth, current_length):
    """Fitness-for-Service assessment over time"""
    results = []
    failure_years = {}
    
    for year in range(inputs['inspection_year'], 
                     inputs['inspection_year'] + inputs['projection_years'] + 1):
        years_elapsed = year - inputs['inspection_year']
        d = current_depth + inputs['radial_corrosion_rate'] * years_elapsed
        L = current_length + inputs['axial_corrosion_rate'] * years_elapsed
        
        # Cap depth at 80% wall thickness
        d = min(d, inputs['pipe_thickness'] * 0.8)
        
        # Calculate burst pressures
        P_asme = modified_asme_b31g(
            inputs['pipe_diameter'], inputs['pipe_thickness'], d, L, inputs['yield_stress'])
        P_dnv = dnv_rp_f101(
            inputs['pipe_diameter'], inputs['pipe_thickness'], d, L, inputs['uts'])
        P_pcorrc = pcorrc(
            inputs['pipe_diameter'], inputs['pipe_thickness'], d, L, inputs['uts'])
        
        # Calculate ERF
        erf_asme = inputs['max_pressure'] / P_asme if P_asme > 0 else 0
        erf_dnv = inputs['max_pressure'] / P_dnv if P_dnv > 0 else 0
        erf_pcorrc = inputs['max_pressure'] / P_pcorrc if P_pcorrc > 0 else 0
        
        critical_erf = max(erf_asme, erf_dnv, erf_pcorrc)
        
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
        
        # Track failures
        if erf_asme >= 1.0 and 'ASME' not in failure_years:
            failure_years['ASME'] = year
        if erf_dnv >= 1.0 and 'DNV' not in failure_years:
            failure_years['DNV'] = year
        if erf_pcorrc >= 1.0 and 'PCORRC' not in failure_years:
            failure_years['PCORRC'] = year
            
    return results, failure_years

# UI Components
def create_header():
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {PRIMARY}, #2c3e50); 
                padding:30px; border-radius:8px; margin-bottom:30px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <h1 style="color:{LIGHT_TEXT}; margin:0;">🔧 Pipeline Integrity Management System</h1>
        <p style="color:#E3F2FD; font-size:1.2rem;">Corrosion Assessment & Fitness-for-Service Analysis</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar():
    with st.sidebar:
        # Dataset selection
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {PRIMARY}, #2c3e50); 
                    padding:15px; border-radius:8px; margin-bottom:20px; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color:{LIGHT_TEXT}; margin:0; text-align:center;">Dataset Selection</h3>
        </div>
        """, unsafe_allow_html=True)
        
        dataset = st.radio(
            "Choose dataset:",
            ['Dataset 1', 'Dataset 2', 'Dataset 3'],
            index=['Dataset 1', 'Dataset 2', 'Dataset 3'].index(st.session_state.current_dataset))
        
        if st.session_state.current_dataset != dataset:
            st.session_state.current_dataset = dataset
            st.rerun()
            
        st.markdown("---")
        
        # Pipeline parameters
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {PRIMARY}, #2c3e50); 
                    padding:15px; border-radius:8px; margin-bottom:20px; 
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color:{LIGHT_TEXT}; margin:0; text-align:center;">Pipeline Parameters</h3>
            <p style="color:#E3F2FD; margin:0; text-align:center;">Current: 
                <strong>{st.session_state.current_dataset}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        current_data = st.session_state.datasets[st.session_state.current_dataset]
        inputs = current_data['inputs']
        
        with st.expander("◻ Dimensional Parameters", expanded=True):
            inputs['pipe_thickness'] = st.number_input(
                'Pipe Thickness, t (mm)',
                min_value=0.1, max_value=30.0, value=inputs['pipe_thickness'], step=0.1)
            inputs['pipe_diameter'] = st.number_input(
                'Pipe Diameter, D (mm)',
                min_value=1.0, max_value=5000.0, value=inputs['pipe_diameter'], step=1.0)
            inputs['pipe_length'] = st.number_input(
                'Pipe Length, L (mm)',
                min_value=0.0, max_value=10000000.0, value=inputs['pipe_length'], step=1000.0)
            inputs['corrosion_length'] = st.number_input(
                'Corrosion Length, Lc (mm)',
                min_value=0.0, max_value=1000.0, value=inputs['corrosion_length'], step=1.0)
            inputs['corrosion_depth'] = st.number_input(
                'Corrosion Depth, Dc (mm)',
                min_value=0.0, max_value=100.0, value=inputs['corrosion_depth'], step=0.1)
            
            # Validation
            if inputs['corrosion_depth'] > 0 and inputs['pipe_thickness'] > 0:
                if inputs['corrosion_depth'] > (0.8 * inputs['pipe_thickness']):
                    st.error("✗ Corrosion depth exceeds 80% of wall thickness - critical defect!")
        
        with st.expander("🟢 Material Properties", expanded=True):
            inputs['yield_stress'] = st.number_input(
                'Yield Stress, Sy (MPa)',
                min_value=0.0, max_value=2000.0, value=inputs['yield_stress'], step=10.0)
            inputs['uts'] = st.number_input(
                'Ultimate Tensile Strength, UTS (MPa)',
                min_value=0.0, max_value=3000.0, value=inputs['uts'], step=10.0)
            
            if inputs['yield_stress'] > 0 and inputs['uts'] > 0:
                if inputs['yield_stress'] > inputs['uts']:
                    st.error("✕ Yield stress cannot exceed ultimate tensile strength")
        
        with st.expander("⚡ Operating Conditions", expanded=True):
            inputs['max_pressure'] = st.number_input(
                'Max Operating Pressure (MAOP) (MPa)',
                min_value=0.0, max_value=100.0, value=inputs['max_pressure'], step=0.1)
            inputs['min_pressure'] = st.number_input(
                'Min Operating Pressure (MPa)',
                min_value=0.0, max_value=100.0, value=inputs['min_pressure'], step=0.1)
            
            if inputs['min_pressure'] > inputs['max_pressure']:
                st.error("✕ Minimum pressure cannot exceed maximum pressure")
        
        with st.expander("📈 Corrosion Growth", expanded=True):
            inputs['inspection_year'] = st.number_input(
                'Inspection Year',
                min_value=1900, max_value=2100, value=inputs['inspection_year'], step=1)
            inputs['radial_corrosion_rate'] = st.number_input(
                'Radial Corrosion Rate (mm/year)',
                min_value=0.0, max_value=10.0, value=inputs['radial_corrosion_rate'], step=0.01)
            inputs['axial_corrosion_rate'] = st.number_input(
                'Axial Corrosion Rate (mm/year)',
                min_value=0.0, max_value=10.0, value=inputs['axial_corrosion_rate'], step=0.01)
            inputs['projection_years'] = st.number_input(
                'Projection Period (years)',
                min_value=0, max_value=50, value=inputs['projection_years'], step=1)
        
        st.markdown("---")
        
        # Action buttons
        if st.button('Run Analysis', use_container_width=True, type="primary"):
            st.session_state.run_analysis = True
            st.session_state.datasets[st.session_state.current_dataset]['results'] = None
            st.rerun()
            
        if st.button('Reset All', use_container_width=True):
            st.session_state.run_analysis = False
            # Reset to initial state
            st.session_state.datasets = {
                'Dataset 1': {
                    'inputs': {
                        'pipe_thickness': 5.0,
                        'pipe_diameter': 100.0,
                        'pipe_length': 10000.0,
                        'corrosion_length': 50.0,
                        'corrosion_depth': 1.0,
                        'yield_stress': 250.0,
                        'uts': 400.0,
                        'max_pressure': 10.0,
                        'min_pressure': 5.0,
                        'inspection_year': 2023,
                        'radial_corrosion_rate': 0.1,
                        'axial_corrosion_rate': 0.1,
                        'projection_years': 10
                    },
                    'results': None
                },
                'Dataset 2': {
                    'inputs': {
                        'pipe_thickness': 8.0,
                        'pipe_diameter': 200.0,
                        'pipe_length': 20000.0,
                        'corrosion_length': 100.0,
                        'corrosion_depth': 2.0,
                        'yield_stress': 300.0,
                        'uts': 500.0,
                        'max_pressure': 15.0,
                        'min_pressure': 7.0,
                        'inspection_year': 2023,
                        'radial_corrosion_rate': 0.2,
                        'axial_corrosion_rate': 0.15,
                        'projection_years': 15
                    },
                    'results': None
                },
                'Dataset 3': {
                    'inputs': {
                        'pipe_thickness': 12.0,
                        'pipe_diameter': 300.0,
                        'pipe_length': 30000.0,
                        'corrosion_length': 150.0,
                        'corrosion_depth': 3.0,
                        'yield_stress': 350.0,
                        'uts': 550.0,
                        'max_pressure': 20.0,
                        'min_pressure': 10.0,
                        'inspection_year': 2023,
                        'radial_corrosion_rate': 0.3,
                        'axial_corrosion_rate': 0.2,
                        'projection_years': 20
                    },
                    'results': None
                }
            }
            st.rerun()
        
        st.markdown("---")
        
        # Safety indicators
        st.markdown(f"""
        <div style="background: {CARD_BG}; padding:15px; border-radius:8px; 
                    margin-top:15px; box-shadow: 0 4px 8px rgba(0,0,0,0.08); 
                    border-left: 4px solid #43A047;">
            <h4 style="color:{DARK_TEXT}; margin:0;">Safety Indicators</h4>
            <div style="display: flex; align-items: center; margin-top:10px;">
                <div style="background-color: #43A047; width:20px; height:20px; 
                            border-radius:50%; margin-right:10px;"></div>
                <span style="color:{DARK_TEXT};">Safe: ERF ≤ 1</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="background-color: {WARNING}; width:20px; height:20px; 
                            border-radius:50%; margin-right:10px;"></div>
                <span style="color:{DARK_TEXT};">Unsafe: ERF > 1</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_intro_section():
    st.subheader('Pipeline Configuration')
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png",
                 caption="Fig. 1: Corrosion defect geometry")
    
    with col2:
        st.markdown(f"""
        <div style="background: {CARD_BG}; border-radius:8px; padding:20px; box-shadow: 0 4px 8px rgba(0,0,0,0.08);">
            <h4 style="border-bottom: 2px solid {PRIMARY}; padding-bottom:8px; color:{DARK_TEXT};">Assessment Protocol</h4>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top:15px;">
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">1</div>
                    <span>Select dataset to configure</span>
                </div>
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">2</div>
                    <span>Enter pipeline parameters</span>
                </div>
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">3</div>
                    <span>Specify operating conditions</span>
                </div>
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">4</div>
                    <span>Set corrosion growth rates</span>
                </div>
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">5</div>
                    <span>Run analysis & review results</span>
                </div>
                <div style="display:flex; align-items:center;">
                    <div style="background:{PRIMARY}; color:white; width:30px; height:30px; 
                                border-radius:50%; display:flex; align-items:center; justify-content:center; margin-right:10px;">6</div>
                    <span>Analyze remaining life</span>
                </div>
            </div>
            <div class="progress-container" style="margin-top:20px;">
                <div class="progress-bar" style="width: {'50%' if st.session_state.run_analysis else '10%'};"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                <span style="color:{DARK_TEXT};">Status:</span>
                <span style="color:{PRIMARY}; font-weight:bold;">{"Analysis Complete" if st.session_state.run_analysis else "Ready for Input"}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_analysis_results():
    if st.session_state.run_analysis:
        current_data = st.session_state.datasets[st.session_state.current_dataset]
        inputs = current_data['inputs']
        
        try:
            # Calculate all parameters
            pressures = calculate_pressures(inputs)
            stresses = calculate_stresses(inputs)
            fatigue = calculate_fatigue_criteria(
                stresses['sigma_a'], stresses['sigma_m'],
                stresses['Se'], inputs['uts'],
                inputs['yield_stress'],
                stresses['sigma_f']
            )
            
            # Store results
            current_data['results'] = {
                'pressures': pressures,
                'stresses': stresses,
                'fatigue': fatigue
            }
            
            # Burst Pressure Results
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📊 Burst Pressure Assessment ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            burst_cols = st.columns(5)
            burst_data = [
                ("Von Mises", pressures['P_vm'], PRIMARY, inputs['max_pressure']/pressures['P_vm'] if pressures['P_vm'] > 0 else 0),
                ("Tresca", pressures['P_tresca'], SECONDARY, inputs['max_pressure']/pressures['P_tresca'] if pressures['P_tresca'] > 0 else 0),
                ("ASME B31G", pressures['P_asme'], ACCENT, inputs['max_pressure']/pressures['P_asme'] if pressures['P_asme'] > 0 else 0),
                ("DNV", pressures['P_dnv'], "#6A1B9A", inputs['max_pressure']/pressures['P_dnv'] if pressures['P_dnv'] > 0 else 0),
                ("PCORRC", pressures['P_pcorrc'], WARNING, inputs['max_pressure']/pressures['P_pcorrc'] if pressures['P_pcorrc'] > 0 else 0)
            ]
            
            for i, (name, value, color, erf) in enumerate(burst_data):
                safe = erf <= 1
                status = "✓ Safe" if safe else "✗ Unsafe"
                status_class = "safe" if safe else "unsafe"
                pulse_class = "pulse" if not safe else ""
                
                with burst_cols[i]:
                    st.markdown(f"""
                    <div class="card {pulse_class}" style="border-left:4px solid {color};">
                        <h4 style="color:{color}; margin-top:0;">{name}</h4>
                        <div class="value-display">{value:.2f} MPa</div>
                        <div style="font-size:1rem; text-align:center; margin:10px 0;">
                            ERF: <span class="{status_class}" style="font-size:1.2rem;">{erf:.3f}</span>
                        </div>
                        <div style="text-align:center; margin-bottom:10px;">
                            <strong>{status}</strong>
                        </div>
                        <div style="height:6px; background:#E0E0E0; border-radius:3px; margin:15px 0;">
                            <div style="height:6px; background:{color}; width:{min(100, value/10*100)}%; border-radius:3px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # FFS Assessment
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">✅ Fitness-for-Service Assessment ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            ffs_results, failure_years = calculate_ffs_assessment(
                inputs,
                inputs['corrosion_depth'],
                inputs['corrosion_length']
            )
            df = pd.DataFrame(ffs_results)
            
            # Failure predictions
            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:1.1rem; color:{DARK_TEXT};">Current Year</div>
                    <div style="font-size:2rem; font-weight:bold; color:{PRIMARY}; margin:10px 0;">
                        {inputs['inspection_year']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with metric_cols[1]:
                critical_erf = df.iloc[0]['critical_erf']
                status_color = "#43A047" if critical_erf <= 1 else WARNING
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:1.1rem; color:{DARK_TEXT};">Critical ERF Now</div>
                    <div style="font-size:2rem; font-weight:bold; color:{status_color}; margin:10px 0;">
                        {critical_erf:.3f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with metric_cols[2]:
                asme_fail = failure_years.get('ASME', "Beyond projection")
                color = WARNING if asme_fail != "Beyond projection" else DARK_TEXT
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:1.1rem; color:{DARK_TEXT};">ASME Failure Year</div>
                    <div style="font-size:2rem; font-weight:bold; color:{color}; margin:10px 0;">
                        {asme_fail}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with metric_cols[3]:
                dnv_fail = failure_years.get('DNV', "Beyond projection")
                color = WARNING if dnv_fail != "Beyond projection" else DARK_TEXT
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:1.1rem; color:{DARK_TEXT};">DNV Failure Year</div>
                    <div style="font-size:2rem; font-weight:bold; color:{color}; margin:10px 0;">
                        {dnv_fail}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Burst Pressure Projection
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📈 Burst Pressure Projection ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            fig1.patch.set_facecolor(CARD_BG)
            
            ax1.plot(df['year'], df['P_asme'], label='ASME B31G', color=COLORS['Goodman'], linewidth=2)
            ax1.plot(df['year'], df['P_dnv'], label='DNV-RP-F101', color=COLORS['Soderberg'], linewidth=2)
            ax1.plot(df['year'], df['P_pcorrc'], label='PCORRC', color=COLORS['Gerber'], linewidth=2)
            
            maop = inputs['max_pressure']
            ax1.axhline(y=maop, color=WARNING, linestyle='-', linewidth=2.5, label='MAOP')
            ax1.axhspan(ymin=0, ymax=maop, color=WARNING, alpha=0.1, label='Unsafe Zone')
            
            y_min = min(df[['P_asme','P_dnv','P_pcorrc']].min().min(), maop * 0.7)
            y_max = max(df[['P_asme','P_dnv','P_pcorrc']].max().max(), maop * 1.3)
            ax1.set_ylim(y_min, y_max)
            
            ax1.set_xlabel('Year', fontsize=10, color=DARK_TEXT)
            ax1.set_ylabel('Burst Pressure (MPa)', fontsize=10, color=DARK_TEXT)
            ax1.set_title('Burst Pressure Projection (Unsafe when Below MAOP)', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax1.grid(True, linestyle='-', alpha=0.7, color=PRIMARY)
            ax1.legend(loc='upper right', facecolor=CARD_BG, edgecolor=DARK_TEXT)
            st.pyplot(fig1)
            
            # ERF Projection
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📉 Estimated Repair Factor (ERF) Projection ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            fig2.patch.set_facecolor(CARD_BG)
            
            ax2.plot(df['year'], df['erf_asme'], label='ASME ERF', color=COLORS['Goodman'], linewidth=2)
            ax2.plot(df['year'], df['erf_dnv'], label='DNV ERF', color=COLORS['Soderberg'], linewidth=2)
            ax2.plot(df['year'], df['erf_pcorrc'], label='PCORRC ERF', color=COLORS['Gerber'], linewidth=2)
            
            ax2.axhline(y=1.0, color=WARNING, linestyle='-', linewidth=2.5, label='Safety Threshold (ERF=1)')
            erf_max = max(df[['erf_asme','erf_dnv','erf_pcorrc']].max().max(), 1.3)
            ax2.axhspan(ymin=1.0, ymax=erf_max, color=WARNING, alpha=0.1, label='Unsafe Zone')
            
            erf_min = min(df[['erf_asme','erf_dnv','erf_pcorrc']].min().min(), 0.7)
            ax2.set_ylim(erf_min, erf_max)
            
            ax2.set_xlabel('Year', fontsize=10, color=DARK_TEXT)
            ax2.set_ylabel('ERF (MAOP/Burst Pressure)', fontsize=10, color=DARK_TEXT)
            ax2.set_title('ERF Projection (Unsafe when Above 1.0)', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax2.grid(True, linestyle='-', alpha=0.7, color=PRIMARY)
            ax2.legend(loc='upper right', facecolor=CARD_BG, edgecolor=DARK_TEXT)
            st.pyplot(fig2)
            
            # Detailed table
            with st.expander("Detailed Projection Data", expanded=False):
                display_df = df.copy()
                display_df['Depth'] = display_df['depth'].apply(lambda x: f"{x:.2f} mm")
                display_df['Length'] = display_df['length'].apply(lambda x: f"{x:.2f} mm")
                display_df['ASME Burst'] = display_df['P_asme'].apply(lambda x: f"{x:.2f} MPa")
                display_df['DNV Burst'] = display_df['P_dnv'].apply(lambda x: f"{x:.2f} MPa")
                display_df['PCORRC Burst'] = display_df['P_pcorrc'].apply(lambda x: f"{x:.2f} MPa")
                display_df['Critical ERF'] = display_df['critical_erf'].apply(lambda x: f"{x:.3f}")
                
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
                <h3 style="margin:0;">⚙️ Stress Analysis ({st.session_state.current_dataset})</h3>
            </div>
            """, unsafe_allow_html=True)
            
            stress_col1, stress_col2 = st.columns([1, 1])
            
            with stress_col1:
                st.markdown(f"""
                <div style="background:{CARD_BG}; border-radius:8px; padding:20px; box-shadow:0 4px 8px rgba(0,0,0,0.08);">
                    <h4>Stress Parameters</h4>
                    <table style="width:100%; border-collapse:collapse; font-size:1rem;">
                        <tr style="border-bottom:1px solid #E0E0E0;">
                            <td style="padding:10px;">Max VM Stress</td>
                            <td style="text-align:right; padding:10px; font-weight:bold; color:{PRIMARY};">{stresses['sigma_vm_max']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom:1px solid #E0E0E0;">
                            <td style="padding:10px;">Min VM Stress</td>
                            <td style="text-align:right; padding:10px; font-weight:bold; color:{PRIMARY};">{stresses['sigma_vm_min']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom:1px solid #E0E0E0;">
                            <td style="padding:10px;">Alternating Stress</td>
                            <td style="text-align:right; padding:10px; font-weight:bold; color:{SECONDARY};">{stresses['sigma_a']:.2f} MPa</td>
                        </tr>
                        <tr style="border-bottom:1px solid #E0E0E0;">
                            <td style="padding:10px;">Mean Stress</td>
                            <td style="text-align:right; padding:10px; font-weight:bold; color:{SECONDARY};">{stresses['sigma_m']:.2f} MPa</td>
                        </tr>
                        <tr>
                            <td style="padding:10px;">Endurance Limit</td>
                            <td style="text-align:right; padding:10px; font-weight:bold; color:{ACCENT};">{stresses['Se']:.2f} MPa</td>
                        </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
                
            with stress_col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                categories = ['Max Stress', 'Min Stress', 'Amplitude']
                values = [stresses['sigma_vm_max'], stresses['sigma_vm_min'], stresses['sigma_a']]
                colors = [PRIMARY, SECONDARY, ACCENT]
                bars = ax.bar(categories, values, color=colors, edgecolor=DARK_TEXT)
                
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:.1f} MPa',
                            ha='center', va='bottom', fontsize=10, color=DARK_TEXT)
                
                ax.set_ylim(0, max(values) * 1.2)
                ax.set_title('Stress Distribution', fontsize=12, color=DARK_TEXT, fontweight='bold')
                ax.grid(axis='y', linestyle='-', alpha=0.7, color=PRIMARY)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color(DARK_TEXT)
                ax.spines['bottom'].set_color(DARK_TEXT)
                ax.tick_params(axis='x', colors=DARK_TEXT)
                ax.tick_params(axis='y', colors=DARK_TEXT)
                ax.set_facecolor(CARD_BG)
                plt.tight_layout()
                st.pyplot(fig)
            
            # Fatigue Analysis
            st.markdown(f"""
            <div class="section-header">
                <h3 style="margin:0;">📊 Fatigue Analysis Diagram (All Datasets)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor(CARD_BG)
            
            x = np.linspace(0, inputs['uts']*1.1, 100)
            
            ax.plot(x, stresses['Se']*(1 - x/inputs['uts']),
                     color=COLORS['Goodman'], linewidth=2.5, linestyle='-', label='Goodman')
            ax.plot(x, stresses['Se']*(1 - x/inputs['yield_stress']),
                     color=COLORS['Soderberg'], linewidth=2.5, linestyle='-', label='Soderberg')
            ax.plot(x, stresses['Se']*(1 - (x/inputs['uts'])**2),
                     color=COLORS['Gerber'], linestyle='-', linewidth=2.5, label='Gerber')
            ax.plot(x, stresses['Se']*(1 - x/stresses['sigma_f']),
                     color=COLORS['Morrow'], linestyle='-', linewidth=2.5, label='Morrow')
            ax.plot(x, stresses['Se']*np.sqrt(1 - (x/inputs['yield_stress'])**2),
                     color=COLORS['ASME-Elliptic'], linestyle=(0, (5, 1)), linewidth=2.5, label='ASME-Elliptic')
            
            markers = ['o', 's', 'D']
            for i, (dataset_name, dataset) in enumerate(st.session_state.datasets.items()):
                if dataset['results']:
                    ds = dataset['results']['stresses']
                    ax.scatter(ds['sigma_m'], ds['sigma_a'],
                                color=DATASET_COLORS[i], s=150, edgecolor=DARK_TEXT, zorder=10,
                                marker=markers[i], label=f'{dataset_name} (σm={ds["sigma_m"]:.1f}, σa={ds["sigma_a"]:.1f})')
            
            ax.scatter(0, stresses['Se'], color=DARK_TEXT, s=100, marker='o',
                        label=f'Se = {stresses["Se"]:.1f} MPa')
            ax.scatter(inputs['uts'], 0, color=DARK_TEXT, s=100, marker='s',
                        label=f'UTS = {inputs["uts"]:.1f} MPa')
            ax.scatter(inputs['yield_stress'], 0, color=DARK_TEXT, s=100, marker='^',
                        label=f'Sy = {inputs["yield_stress"]:.1f} MPa')
            
            all_points = []
            for dataset in st.session_state.datasets.values():
                if dataset['results']:
                    ds = dataset['results']['stresses']
                    all_points.append(ds['sigma_m'])
                    all_points.append(ds['sigma_a'])
            
            max_x = inputs['uts'] * 1.1
            max_y = stresses['Se'] * 1.5
            
            if all_points:
                max_x = max(max_x, max(all_points) * 1.2)
                max_y = max(max_y, max(all_points) * 1.5)
            
            ax.set_xlim(0, max_x)
            ax.set_ylim(0, max_y)
            ax.set_xlabel('Mean Stress (σm) [MPa]', fontsize=10, color=DARK_TEXT)
            ax.set_ylabel('Alternating Stress (σa) [MPa]', fontsize=10, color=DARK_TEXT)
            ax.set_title('Fatigue Analysis Diagram', fontsize=12, fontweight='bold', color=DARK_TEXT)
            ax.grid(True, linestyle='-', alpha=0.7, color=PRIMARY)
            ax.set_facecolor(CARD_BG)
            
            ax.spines['bottom'].set_color(DARK_TEXT)
            ax.spines['top'].set_color(DARK_TEXT)
            ax.spines['right'].set_color(DARK_TEXT)
            ax.spines['left'].set_color(DARK_TEXT)
            ax.tick_params(axis='x', colors=DARK_TEXT)
            ax.tick_params(axis='y', colors=DARK_TEXT)
            
            ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1), fontsize=9, 
                      facecolor=CARD_BG, edgecolor=DARK_TEXT)
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"❌ Error in calculations: {str(e)}")
    else:
        st.markdown(f"""
        <div style="background:{CARD_BG}; text-align:center; padding:40px 20px; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.08);">
            <h4 style="color:{DARK_TEXT}; margin-bottom:20px;">⏳ Ready for Analysis</h4>
            <p style="color:{DARK_TEXT}; font-size:1.1rem; max-width:600px; margin:0 auto;">
                Select a dataset, enter pipeline parameters in the sidebar, and click 'Run Analysis'
            </p>
            <div class="progress-container" style="max-width:400px; margin:30px auto;">
                <div class="progress-bar" style="width:30%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def create_references():
    st.markdown(f"""
    <div class="section-header">
        <h3 style="margin:0;">📚 References & Resources</h3>
    </div>
    """, unsafe_allow_html=True)
    
    ref_col1, ref_col2 = st.columns([1, 1])
    
    with ref_col1:
        with st.expander("Research References", expanded=False):
            st.markdown("""
            - **Mohd et al. (2014)**  
            Journal of Offshore Mechanics and Arctic Engineering  
            On the Burst Strength Capacity of an Aging Subsea Gas Pipeline  
            [DOI:10.1115/1.4028041](https://doi.org/10.1115/1.4028041)
            
            - **ASME B31G-2012**  
            Manual for Determining the Remaining Strength of Corroded Pipelines
            
            - **DNV-RP-F101**  
            Corroded Pipelines Standard
            """)
    
    with ref_col2:
        with st.expander("Additional Resources", expanded=False):
            st.markdown("""
            - Pipeline Corrosion Assessment Guide  
            [ASME Standards](https://www.asme.org/codes-standards)
            
            - Corrosion Rate Calculators  
            [NACE International](https://www.nace.org)
            
            - Pipeline Integrity Management Standards  
            [API Standards](https://www.api.org)
            """)

def create_footer():
    st.markdown(f"""
    <div class="footer">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <h4 style="margin:0; color:{LIGHT_TEXT};">Pipeline Integrity Manager v2.0</h4>
                <p style="margin:5px 0 0; color:#BBDEFB;">Fitness-for-Service Analysis</p>
            </div>
            <div style="text-align:right;">
                <p style="margin:0; color:#BBDEFB;">Technical Support: pipeline@engineering.com</p>
                <p style="margin:0; color:#BBDEFB;">Phone: +1 (555) 123-4567</p>
            </div>
        </div>
        <div style="text-align:center; margin-top:20px; color:#BBDEFB;">
            © 2023 Pipeline Engineering Solutions | All rights reserved
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Application
def main():
    create_header()
    create_sidebar()
    create_intro_section()
    display_analysis_results()
    create_references()
    create_footer()

if __name__ == "__main__":
    main()
