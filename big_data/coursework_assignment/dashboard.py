
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
            TikTok & YouTube Metric Performances Over Video duration
        </p>
    </div>
""", unsafe_allow_html=True)

# Load Data
tiktok_df = pd.read_pickle('tiktok.pkl')
youtube_df = pd.read_pickle('youtube.pkl')

# Data preprocessing
youtube_df = youtube_df[youtube_df['youtube_duration_sec'] < 1200]

# Calculate total engagement
tiktok_df['tiktok_total_engagement'] = tiktok_df[['tiktok_view_count', 'tiktok_like_count', 'tiktok_comment_count']].sum(axis=1)
youtube_df['youtube_total_engagement'] = youtube_df[['youtube_view_count', 'youtube_like_count', 'youtube_comment_count']].sum(axis=1)

# Sidebar with modern styling
with st.sidebar:
    st.markdown(f"""
        <div style='padding: 1rem 0; text-align: center;'>
            <h2 style='color: {COLORS["accent"]}; font-size: 1.5rem;'>Dashboard Controls</h2>
        </div>
    """, unsafe_allow_html=True)
    
    metric = st.selectbox(
        "📈 Select Metric",
        ["view_count", "like_count", "comment_count", "total_engagement"],
        help="Choose which metric to analyze"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    aggregation = st.radio(
        "📊 Aggregation Method",
        ["Mean", "Median", "Sum"],
        help="Select how to aggregate the data"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bin size controls with labels
    st.markdown(f"<p style='color: {COLORS['text']}'>🎯 Adjust Time Intervals</p>", unsafe_allow_html=True)
    
    tiktok_bins = st.slider(
        "TikTok Bin Size (seconds)",
        5, 60, step=5, value=5,
        help="Adjust the granularity of TikTok duration analysis"
    )
    
    youtube_bins = st.slider(
        "YouTube Bin Size (seconds)",
        10, 120, step=10, value=30,
        help="Adjust the granularity of YouTube duration analysis"
    )

# Convert metrics to thousands
for platform, prefix in zip([tiktok_df, youtube_df], ['tiktok', 'youtube']):
    for col in ['view_count', 'like_count', 'comment_count', 'total_engagement']:
        platform[f"{prefix}_{col}"] /= 1_000

# Enhanced histogram plotting function
def create_modern_histogram(df, duration_col, metric_col, bin_size, agg_func, title):
    df['duration_bin'] = pd.cut(df[duration_col], 
                               bins=range(0, int(df[duration_col].max() + bin_size), bin_size))
    aggregated = df.groupby('duration_bin')[metric_col].agg(agg_func).reset_index()
    aggregated['bin_center'] = aggregated['duration_bin'].apply(lambda x: x.mid)

    fig, ax1 = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor(COLORS['background'])
    ax1.set_facecolor(COLORS['background'])

    # Enhanced histogram
    sns.histplot(
        df[duration_col],
        bins=range(0, int(df[duration_col].max() + bin_size), bin_size),
        kde=False,
        ax=ax1,
        color=COLORS['primary'],
        alpha=0.7
    )

    # Styling for primary axis
    ax1.set_xlabel(f"Duration (Seconds)", fontsize=24, color=COLORS['text'])
    ax1.set_ylabel("Frequency", color=COLORS['primary'], fontsize=24)
    ax1.tick_params(axis='both', which='major', labelsize=16, colors=COLORS['text'])
    ax1.grid(True, alpha=0.2, color=COLORS['text'])

    # Enhanced overlay
    ax2 = ax1.twinx()
    ax2.plot(
        aggregated['bin_center'],
        aggregated[metric_col],
        marker='o',
        color=COLORS['secondary'],
        linewidth=2,
        label=f"{agg_func.capitalize()} {metric_col.split('_')[1]} (per 1,000)"
    )
    
    # Styling for secondary axis
    ax2.set_ylabel(
        f"{metric_col.split('_')[1].title()} ({agg_func.capitalize()}, per 1,000)",
        color=COLORS['secondary'],
        fontsize=24
    )
    ax2.tick_params(axis='y', which='major', labelsize=16, labelcolor=COLORS['secondary'])
    ax2.grid(False)

    # Title and legend
    plt.title(title, pad=20, color=COLORS['text'], fontsize=30)
    ax2.legend(loc="upper right", facecolor=COLORS['background'], 
              labelcolor=COLORS['text'], framealpha=0.9)

    # Adjust layout
    plt.tight_layout()
    return fig

# Create two columns for the graphs
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class='metric-card' style='background-color: {COLORS['card']}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {COLORS['primary']}; text-align: center;'>
                <h3 style='color: {COLORS["accent"]}; margin-bottom: 1rem;'>TikTok Data</h3>
        """, unsafe_allow_html=True)
    
    fig1 = create_modern_histogram(
        tiktok_df,
        "tiktok_duration_sec",
        f"tiktok_{metric}",
        tiktok_bins,
        aggregation.lower(),
        f"TikTok {metric} over Duration by Bin Size {tiktok_bins}"
    )
    st.pyplot(fig1)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='metric-card' style='background-color: {COLORS['card']}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {COLORS['primary']}; text-align: center;'>
                <h3 style='color: {COLORS["accent"]}; margin-bottom: 1rem;'>Youtube Data</h3>
        """, unsafe_allow_html=True)
    
    fig2 = create_modern_histogram(
        youtube_df,
        "youtube_duration_sec",
        f"youtube_{metric}",
        youtube_bins,
        aggregation.lower(),
        f"YouTube {metric} over Duration by Bin Size {youtube_bins}"
    )
    st.pyplot(fig2)
    st.markdown("</div>", unsafe_allow_html=True)

# Modern footer
st.markdown(f"""
    <div class='footer'>
        <p>
            <span style='color: {COLORS["accent"]}'>⚡</span> 
            Powered by Streamlit | 
            <span style='color: {COLORS["secondary"]}'>❤️</span> 
            Analytics Dashboard v1.0
        </p>
    </div>
""", unsafe_allow_html=True)
