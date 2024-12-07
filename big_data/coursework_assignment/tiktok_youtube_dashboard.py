
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Modern color palette
COLORS = {
    'primary': '#4361ee',      # Royal blue
    'secondary': '#ff6b6b',    # Coral red
    'background': '#1a1a2e',   # Dark navy
    'card': '#162447',         # Lighter navy
    'text': '#e6e6e6',         # Off-white
    'accent': '#4cc9f0'        # Light blue
}

# Configure Streamlit layout
st.set_page_config(
    layout="wide",
    page_title="Social Media Analytics",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
        /* Main container */
        .main {
            background-color: %s;
            padding: 2rem;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: %s !important;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: %s;
        }
        
        /* Cards */
        div[data-testid="stMetricValue"] {
            background-color: %s;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Widgets */
        .stSelectbox, .stRadio > label {
            color: %s !important;
        }
        
        /* Sliders */
        .stSlider > div > div {
            background-color: %s;
            border-radius: 10px;
        }
        
        /* Custom container for graphs */
        .graph-container {
            background-color: %s;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: %s;
            font-size: 0.9rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Custom metric styles */
        .metric-card {
            background-color: %s;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            border-left: 4px solid %s;
            border-right: 4px solid %s;
        }
    </style>
""" % (
    COLORS['background'], COLORS['text'], COLORS['card'],
    COLORS['card'], COLORS['text'], COLORS['background'],
    COLORS['card'], COLORS['text'], COLORS['card'],
    COLORS['primary'], COLORS['primary']
), unsafe_allow_html=True)

# Dashboard Header with Icon
st.markdown(f"""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='font-size: 2.5rem; font-weight: 600;'>
            <span style='color: {COLORS["secondary"]}'>📊</span> 
            Social Media Analytics Dashboard
        </h1>
        <p style='color: {COLORS["text"]}; font-size: 1.1rem;'>
            TikTok & YouTube Metric Performances Over Views
        </p>
    </div>
""", unsafe_allow_html=True)

# Load Data
tiktok_df = pd.read_pickle('tiktok.pkl')
youtube_df = pd.read_pickle('youtube.pkl')

# Scatterplot with Regression Line
def scatterplot_with_regression(df, x_col, y_col, title):
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor(COLORS['background'])
    ax.set_facecolor(COLORS['background'])
    
    # Scatterplot with regression line
    sns.regplot(
        data=df,
        x=x_col,
        y=y_col,
        scatter_kws={'color': COLORS['accent'], 's': 50, 'alpha': 0.7},
        line_kws={'color': COLORS['secondary'], 'linewidth': 2},
        ax=ax
    )
    
    # Styling
    ax.set_title(title, fontsize=24, color=COLORS['text'], pad=20)
    ax.set_xlabel(x_col.replace('_', ' ').title(), fontsize=18, color=COLORS['text'])
    ax.set_ylabel(y_col.replace('_', ' ').title(), fontsize=18, color=COLORS['text'])
    ax.tick_params(colors=COLORS['text'])
    ax.grid(True, color=COLORS['text'], alpha=0.2)
    
    return fig

# Sidebar for Scatterplot Controls
with st.sidebar:
    st.markdown(f"<h2 style='color: {COLORS['accent']}'>Scatterplot Settings</h2>", unsafe_allow_html=True)
    scatter_x = st.selectbox("X-axis Metric", tiktok_df.columns, index=0)
    scatter_y = st.selectbox("Y-axis Metric", tiktok_df.columns, index=1)
    scatter_data = st.radio("Choose Dataset", ["TikTok", "YouTube"])
    st.markdown("<br>", unsafe_allow_html=True)

# Scatterplot Section
selected_df = tiktok_df if scatter_data == "TikTok" else youtube_df
scatter_title = f"{scatter_data} Scatterplot: {scatter_x} vs {scatter_y}"

st.markdown(f"<h2 style='color: {COLORS['accent']}'>{scatter_title}</h2>", unsafe_allow_html=True)

scatter_fig = scatterplot_with_regression(
    selected_df, scatter_x, scatter_y, scatter_title
)
st.pyplot(scatter_fig)
