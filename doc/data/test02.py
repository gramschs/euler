import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Assuming your dataframe is called 'df' and loaded from the Excel file
df = pd.read_excel('/Users/gramschs/Bewerbung/book_thma/doc/data/Beschleunigung_V01.xls')

# Method 1: Using plotly.graph_objects for step plot (most control)
def create_step_plot_go(df):
    fig = go.Figure()
    
    # Add step plot
    fig.add_trace(go.Scatter(
        x=df['Time (s)'],
        y=df['Linear Acceleration x (m/s^2)'],
        mode='lines+markers',
        line=dict(shape='hv', color='blue', width=2),  # 'hv' creates horizontal then vertical steps
        marker=dict(size=8, color='red', symbol='circle'),
        name='Linear Acceleration X'
    ))
    
    fig.update_layout(
        title='Linear Acceleration X vs Time (Step Plot)',
        xaxis_title='Time (s)',
        yaxis_title='Linear Acceleration X (m/s²)',
        template='plotly_white',
        showlegend=False
    )
    
    return fig

# Method 2: Creating step data manually for plotly express
def create_step_data(df):
    """Transform regular time series data into step plot data"""
    times = df['Time (s)'].values
    accel = df['Linear Acceleration x (m/s^2)'].values
    
    # Create step data
    step_times = []
    step_accel = []
    
    for i in range(len(times)):
        if i == 0:
            # First point starts from time 0
            step_times.extend([times[i]])
            step_accel.extend([accel[i]])
        else:
            # Add horizontal line from previous time to current time
            step_times.extend([times[i-1], times[i]])
            step_accel.extend([accel[i-1], accel[i-1]])
        
        # Add the marker point
        if i < len(times) - 1:  # Don't add final vertical line
            step_times.append(times[i])
            step_accel.append(accel[i])
    
    return pd.DataFrame({
        'Time (s)': step_times,
        'Linear Acceleration x (m/s^2)': step_accel
    })

# Method 3: Using the step data with plotly express
def create_step_plot_px(df):
    step_df = create_step_data(df)
    
    fig = px.line(step_df, 
                  x='Time (s)', 
                  y='Linear Acceleration x (m/s^2)',
                  title='Linear Acceleration X vs Time (Step Plot with PX)')
    
    # Add markers for original data points
    fig.add_scatter(x=df['Time (s)'], 
                   y=df['Linear Acceleration x (m/s^2)'],
                   mode='markers',
                   marker=dict(size=8, color='red'),
                   name='Measurements',
                   showlegend=False)
    
    fig.update_layout(
        xaxis_title='Time (s)',
        yaxis_title='Linear Acceleration X (m/s²)'
    )
    
    return fig

# Usage with your actual data:
#fig = create_step_plot_go(df)
#fig.show()

# Or with plotly express approach:
fig = create_step_plot_px(df)
fig.show()



print("Use create_step_plot_go(df) for the cleanest step plot with your data!")