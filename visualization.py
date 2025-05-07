import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# def plot_signals(data, signals, title="Trading Signals"):
#     plt.figure(figsize=(12, 6))
#     plt.plot(data['Close'], label='Close Price', alpha=0.7)
#     plt.scatter(signals[signals['Signal'] == 1].index, 
#                 data['Close'][signals['Signal'] == 1], 
#                 color='green', label='Buy Signal', marker='^', alpha=1)
#     plt.scatter(signals[signals['Signal'] == -1].index, 
#                 data['Close'][signals['Signal'] == -1], 
#                 color='red', label='Sell Signal', marker='v', alpha=1)
#     plt.title(title)
#     plt.legend()
# st.pyplot(plt)

def plot_metrics(metrics):
    if isinstance(metrics, dict):
        metrics_df = pd.DataFrame([metrics])
    elif isinstance(metrics, list):
        metrics_df = pd.DataFrame(metrics)
    else:
        raise ValueError("Metrics should be a dictionary or a list of dictionaries")
    
    # Select only the metrics we want to plot
    metrics_to_plot = ['CAGR', 'Sharpe Ratio', 'Max Drawdown', 'Win Rate']
    metrics_df = metrics_df[metrics_to_plot]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    bars = plt.bar(metrics_df.columns, metrics_df.iloc[0], color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Customize the plot
    plt.title('Performance Metrics', pad=20, fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return plt

def plot_signals(data, signals, title="Trading Signals"):
    fig = go.Figure()

    # Add the Close price line
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'], 
        mode='lines', 
        name='Close Price',
        line=dict(color='blue'),
        hovertemplate='Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
    ))

    # Add Buy signals
    buy_signals = signals[signals['Signal'] == 1]
    fig.add_trace(go.Scatter(
        x=buy_signals.index, 
        y=data.loc[buy_signals.index, 'Close'], 
        mode='markers', 
        name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=10),
        hovertemplate='Buy Signal<br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
    ))

    # Add Sell signals
    sell_signals = signals[signals['Signal'] == -1]
    fig.add_trace(go.Scatter(
        x=sell_signals.index, 
        y=data.loc[sell_signals.index, 'Close'], 
        mode='markers', 
        name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=10),
        hovertemplate='Sell Signal<br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
    ))

    # Customize layout
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        template='plotly_white',
        height=600
    )

    return fig
