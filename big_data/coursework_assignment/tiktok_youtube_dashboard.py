
import requests
import io
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from scipy import stats

# Custom Color Palette (using provided hex values)
COLORS = {
    'primary': '#007bff',  # Blue
    'secondary': '#fd7e14',  # Orange
    'background': '#f8f9fa ',  # Dark Gray
    'card': '#ffffff',   # Light Gray
    'text': '#33333',   # Grayish Blue
    'accent': '#007bff'   # Blue
}

# Configure Streamlit layout
st.set_page_config(
    layout="wide",
    page_title="Social Media Analytics",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown(f"""
    <style>
        /* Main container */
        .main {{
            background-color: {COLORS['background']}; 
            padding: 2rem;
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: {COLORS['text']} !important;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 600;
        }}
        
        /* Sidebar */
        .css-1d391kg {{
            background-color: {COLORS['card']};
        }}
        
        /* Cards */
        div[data-testid="stMetricValue"] {{
            background-color: {COLORS['card']};
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        /* Widgets */
        .stSelectbox, .stRadio > label {{
            color: {COLORS['text']} !important;
        }}
        
        /* Sliders */
        .stSlider > div > div {{
            background-color: {COLORS['background']}; 
            border-radius: 10px;
        }}
        
        /* Custom container for graphs */
        .graph-container {{
            background-color: {COLORS['card']};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: {COLORS['text']};
            font-size: 0.9rem;
            margin-top: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
    </style>
""", unsafe_allow_html=True)

# Dashboard Header with Icon
st.markdown(f"""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h1 style='font-size: 2.5rem; font-weight: 600;'>
            <span style='color: {COLORS["secondary"]}'>📊</span> 
            Social Media Analytics Dashboard
        </h1>
        <p style='color: {COLORS["text"]}; font_size: 1.1rem;'>
            TikTok & YouTube Metric Performances Over Views
        </p>
    </div>
""", unsafe_allow_html=True)

def load_pickle_from_github(url):
    """
    Loads a pickle file from a given GitHub URL.

    Args:
        url: The URL of the pickle file on GitHub.

    Returns:
        A pandas DataFrame containing the data loaded from the pickle file.
    """

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    try:
        data = pd.read_pickle(io.BytesIO(response.content))
    except Exception as e:
        print(f"Error loading pickle from {url}: {e}")
        return None

    return data

# Load the pickle files from GitHub
tiktok_df = load_pickle_from_github("https://github.com/Takosaga/fall_24/blob/main/big_data/coursework_assignment/tiktok.pkl?raw=true")
youtube_df = load_pickle_from_github("https://github.com/Takosaga/fall_24/blob/main/big_data/coursework_assignment/youtube.pkl?raw=true")


# Standardize column names
tiktok_df.rename(columns={
    'tiktok_view_count': 'view_count',
    'tiktok_like_count': 'like_count',
    'tiktok_comment_count': 'comment_count'
}, inplace=True)
youtube_df.rename(columns={
    'youtube_view_count': 'view_count',
    'youtube_like_count': 'like_count',
    'youtube_comment_count': 'comment_count'
}, inplace=True)

# Sidebar controls
st.sidebar.header("Settings")
y_metric = st.sidebar.selectbox("Choose Y-axis Metric", ["like_count", "comment_count"])
standardize = st.sidebar.checkbox("Standardize Metrics (z-scores)", value=True)
remove_outliers = st.sidebar.checkbox("Remove Outliers", value=True)
show_points = st.sidebar.checkbox("Show Data Points", value=False)

# Create columns for side-by-side plots
col1, col2 = st.columns(2)

# Function to create a single scatter plot
def create_scatter_plot(platform_data, platform_name, y_metric):
    fig = go.Figure()

    # Remove outliers if selected
    if remove_outliers:
        q1 = platform_data['view_count'].quantile(0.25)
        q3 = platform_data['view_count'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        platform_data = platform_data[(platform_data[y_metric] >= lower_bound) & (platform_data[y_metric] <= upper_bound)]

    # Standardize data if selected
    if standardize:
        scaler = StandardScaler()
        platform_data[['view_count', y_metric]] = scaler.fit_transform(platform_data[['view_count', y_metric]])

    x = platform_data['view_count'].values.reshape(-1, 1)  # Reshape x for LinearRegression
    y = platform_data[y_metric].values
    reg = LinearRegression().fit(x, y)
    platform_data['regression_line'] = reg.predict(x)

    # Calculate and format regression equation
    slope = reg.coef_[0]
    intercept = reg.intercept_
    equation = f"y = {slope:.3f}x + {intercept:.3f}"

    fig.add_trace(go.Scatter(
        x=platform_data['view_count'],
        y=platform_data[y_metric],
        mode='markers' if show_points else 'none',  # Show/hide data points
        marker=dict(size=8, opacity=0.7),
        name=f'{platform_name} Data Points',
        marker_color=platform_colors[platform_name]
    ))

    fig.add_trace(go.Scatter(
        x=platform_data['view_count'],
        y=platform_data['regression_line'],
        mode='lines',
        name=f'{platform_name} Regression Line',
        line=dict(width=3, color=platform_colors[platform_name]),
        text=equation,  # Add equation to hovertext
    ))

    # Display equation directly on the plot
    fig.add_annotation(
        x=0.05,  # Adjust x position as needed
        y=0.9,  # Adjust y position as needed
        xref="paper",
        yref="paper",
        text=equation,
        showarrow=False,
        font=dict(size=14, color=platform_colors[platform_name])
    )

    fig.update_layout(
        title=f"{platform_name}: Views vs {y_metric.replace('_', ' ').title()}",
        xaxis_title='Views',
        yaxis_title=y_metric.replace('_', ' ').title(),
        showlegend=True,
        title_x=0.5,
        plot_bgcolor=COLORS['background']  # Set the plot background color
    )
    return fig

# Define colors for each platform
platform_colors = {
    'TikTok': COLORS['primary'],
    'YouTube': COLORS['secondary']
}

# Create plots for each platform
tiktok_fig = create_scatter_plot(tiktok_df, 'TikTok', y_metric)
youtube_fig = create_scatter_plot(youtube_df, 'YouTube', y_metric)

# Display plots in columns
with col1:
    st.plotly_chart(tiktok_fig, use_container_width=True)

with col2:
    st.plotly_chart(youtube_fig, use_container_width=True)

summary_text = st.empty()

summary_text.markdown(f"""
    <div style="background-color: {COLORS['background']}; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
    <h3>Summary</h3>
    <p>
        This dashboard analyzes the relationship between views and {y_metric.replace('_', ' ').title()} for TikTok and YouTube videos. 
        The regression lines show a positive correlation between views and {y_metric} for both platforms.
        More views bring in more likes at a greater rate for TikTok than Youtube.
        More views bring in more comments at a slighlty greater rate for YouTube than TikTok.
        Data has been standardized using z-scores. Outliers were removed using the IQR method. 
    </p>
    <h4>Technologies Used:</h4>
    <ul>
        <li><b>Streamlit:</b> For building the interactive web application.</li>
        <li><b>Pandas:</b> For data manipulation and cleaning.</li>
        <li><b>Plotly:</b> For creating interactive and visually appealing charts.</li>
        <li><b>Seaborn:</b> For statistical graphics and data visualization.</li>
        <li><b>NumPy:</b> For numerical computing and array operations.</li>
        <li><b>Matplotlib:</b> For creating static, animated, and interactive visualizations.</li>
        <li><b>Scikit-learn:</b> For machine learning algorithms, including linear regression.</li>
        <li><b>SciPy:</b> For scientific and technical computing.</li>
        <li><b>SQLite:</b> For relational database management.</li>
        <li><b>MongoDB:</b> For NoSQL document database management.</li>
    </ul>
    <p>
        19,383 rows of TikTok data gathered from <a href="https://www.kaggle.com/datasets/yakhyojon/tiktok">Kaggle</a>. <br>
        4,450 rows Youtube data gathered from <a href="https://developers.google.com/youtube/v3/docs/">Google YouTube API</a>. <br>
        More data for YouTube should be gathered for more robust analysis. <br>
        <a href="https://github.com/Takosaga/fall_24/tree/main/coursework_assignment">Full Project Repo</a> <br>
    </p>
</div>
""", unsafe_allow_html=True)

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
