import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from plotly import graph_objects as go
from preprocessing import DataPreprocessor
from strategies import MovingAverageCrossover, RSIStrategy, BollingerBands, MACD, Breakout
from backtest import backtest_strategy
from predictions import forecast_ets
from pandas.plotting import table
from visualization import plot_signals, plot_metrics
from fpdf import FPDF

st.title("Backtesting Engine v1.0")
st.caption("A simple backtesting engine for trading strategies")

st.sidebar.title("Backtesting Engine v1.0")

st.sidebar.markdown("""
Welcome to the Backtesting Engine, a simple yet powerful tool for backtesting trading strategies. This application provides a comprehensive set of features to help you analyze and visualize your trading strategies.

**Developer**:
Pranshu Singh
                    
**GitHub**:
[pranshu-5123](https://github.com/pranshu-5123)

**Linkedin**:
[pranshusingh5123](https://www.linkedin.com/in/pranshusingh5123/)   

**Email**:
pranshusingh5123@gmail.com                 
                    
**Features:**

1. **Data Upload**:
   - Upload your data in CSV or Excel format.
   - View the uploaded data in a tabular format.

2. **Data Preprocessing**:
   - Preprocess your data using the built-in DataPreprocessor.
   - View the preprocessed data.

3. **Strategy Selection**:
   - Choose from a variety of trading strategies:
     - Moving Average Crossover
     - RSI Strategy
     - Bollinger Bands
     - MACD
     - Breakout

4. **Generate Trading Signals**:
   - Generate buy, sell, and hold signals based on the selected strategy.
   - View the generated signals in a tabular format.

5. **Interactive Trading Signals Visualizer**:
   - Visualize trading signals interactively using Plotly.

6. **Performance Metrics**:
   - Calculate performance metrics for the generated signals.
   - View the calculated metrics in a tabular format.

7. **Price Forecasting**:
   - Forecast future prices using the ETS model.ac
   - Visualize the forecasted prices alongside historical prices.

8. **Export Options**:
   - Export the generated signals and performance metrics as a CSV file.
   - Export the report as a PDF file with a proper table.

9. **Download Reports**:
   - Download the CSV or PDF report directly from the web app.
"""                    

)

# Initialize session state
if 'signals' not in st.session_state:
    st.session_state.signals = None
if 'metrics' not in st.session_state:
    st.session_state.metrics = None

# ... (your previous imports and code remain unchanged)

# Sample OHLC File Download
st.subheader("📄 Download Sample OHLC Data")
st.caption("Don’t have data? Download this ready-to-use sample file to experience the backtesting engine.")

try:
    with open("Sample_OHLC.csv", "rb") as f:
        st.download_button(
            label="📥 Click here to download a sample OHLC CSV",
            data=f,
            file_name="Sample_OHLC.csv",
            mime="text/csv"
        )
except FileNotFoundError:
    st.warning("Sample_OHLC.csv not found. Please add the file to your project directory.")



# Upload data
st.subheader("Upload your data")
st.caption("CSV or Excel files are accepted")

uploaded_file = st.file_uploader("Select a CSV file", type=["csv","xlsx"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if st.button("Show Dataframe"):
        st.write(df)

    # Preprocessing
    st.subheader("Preprocessing")
    preprocess = st.checkbox("Run Preprocessing", value=False)
    if preprocess:
        preprocessor = DataPreprocessor(df)
        df = preprocessor.preprocess_data()
        st.write("Preprocessing completed")
        st.write(df)
    else:
        st.write("Your data is not preprocessed yet, please check the above checkbox to preprocess your data")

    # Strategy
    st.subheader("Strategy Selection")

    strategy_options = ["Moving Average Crossover", "RSI Strategy", "Bollinger Bands", "MACD", "Breakout"]

    selected_strategy = st.selectbox("Select a Strategy", strategy_options)
    if selected_strategy == "Moving Average Crossover":
        short_window = st.slider("Short Moving Average Window", 5, 50, 10)
        long_window = st.slider("Long Moving Average Window", 20, 200, 50)
        params = {'short_window': short_window, 'long_window': long_window}
        strategy = MovingAverageCrossover(df, params)

    elif selected_strategy == "RSI Strategy":
        rsi_period = st.slider("RSI Period", 5, 50, 14)
        overbought = st.slider("Overbought Threshold", 50, 90, 70)
        oversold = st.slider("Oversold Threshold", 10, 50, 30)
        params = {'rsi_period': rsi_period, 'overbought': overbought, 'oversold': oversold}
        strategy = RSIStrategy(df, params)

    elif selected_strategy == "Bollinger Bands":
        period = st.slider("Moving Average Window", 5, 50, 20)
        std_dev = st.slider("Standard Deviation", 1, 3, 2)
        params = {'period': period, 'std_dev': std_dev}
        strategy = BollingerBands(df, params)

    elif selected_strategy == "MACD":
        fast_period = st.slider("Fast Moving Average Window", 5, 50, 12)
        slow_period = st.slider("Slow Moving Average Window", 20, 200, 26)
        signal_period = st.slider("Signal Line Window", 9, 20, 9)
        params = {'fast_period': fast_period, 'slow_period': slow_period, 'signal_period': signal_period}
        strategy = MACD(df, params)

    elif selected_strategy == "Breakout":
        breakout_period = st.slider("Breakout Period", 5, 50, 20)
        params = {'breakout_period': breakout_period}
        strategy = Breakout(df, params)

    initial_balance = st.number_input("Enter Initial Balance", value=100000)

    # Generate signals
    if st.button("Generate Signals"):
        st.info("Signal: 1 = Buy, -1 = Sell, 0 = Hold")
        st.session_state.signals = strategy.generate_signals()
        col1, col2 = st.columns([2, 1])
        with col1:
            st.dataframe(st.session_state.signals, width=500, height=500)
        with col2:
            st.dataframe(st.session_state.signals['Signal'].value_counts(), width=300, height=140)

    # Visualize Signals
    st.subheader("Interactive Trading Signals Visualizer")
    if st.session_state.signals is not None:
        interactive_plot = plot_signals(df, st.session_state.signals)
        st.plotly_chart(interactive_plot, use_container_width=True)
    else:
        st.write("Please generate signals first.")

    # Backtesting
    st.subheader("Performance Metrics")
    calculate_metrics_checkbox = st.checkbox("Calculate Metrics", value=False)
    if calculate_metrics_checkbox:
        if st.session_state.signals is not None:
            st.session_state.metrics = backtest_strategy(df, st.session_state.signals)
            st.dataframe(st.session_state.metrics)
        else:
            st.write("Please generate signals first.")
    else:
        st.write("Please check the above checkbox to calculate metrics")

    # Predictions
    st.subheader("Price Forecast")
    forecast_ets_checkbox = st.checkbox("Forecast Prices using ETS", value=False)
    if forecast_ets_checkbox:
        steps = st.number_input("Enter Number of Steps to Forecast", value=10)
        forecast = forecast_ets(df, steps=steps)
        st.dataframe(forecast, width=1000, height=500)

        # Plotting Forecast
        plt.figure(figsize=(10, 6)) 
        plt.plot(df['Close'], label="Historical Prices")
        plt.plot(forecast, label="Forecast", linestyle='--')
        plt.legend()
        plt.title("Price Forecast")
        st.pyplot(plt)

    # Plot Performance Metrics
    st.subheader("Check Performance Metrics")
    plot_metrics_button = st.button("Plot Performance Metrics")
    if plot_metrics_button:
        if st.session_state.metrics is not None:
            plot_metrics(st.session_state.metrics)
            st.pyplot(plt)
        else:
            st.write("Please calculate metrics first.")
    else:
        st.write("Please check the above checkbox to plot performance metrics")

# Export PDF
    def export_pdf(signals, metrics, filename="report.pdf"):
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Backtesting Report", ln=True, align='C')

        # Signals
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Trading Signals", ln=True, align='L')
        pdf.ln(10)
        for index, row in signals.iterrows():
            pdf.cell(200, 10, txt=f"{index}: {row['Signal']}", ln=True, align='L')

        # Metrics
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Performance Metrics", ln=True, align='L')
        pdf.ln(10)
        for key, value in metrics.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True, align='L')

        pdf.output(filename)

    # Export CSV
    def export_csv(signals, metrics, filename="report.csv"):
        with io.StringIO() as buffer:
            signals.to_csv(buffer, index=True)
            buffer.write("\n\n")
            metrics_df = pd.DataFrame([metrics])
            metrics_df.to_csv(buffer, index=True)
            st.download_button(
                label="Download CSV",
                data=buffer.getvalue(),
                file_name=filename,
                mime="text/csv",
            )

    # Export Options
    st.subheader("Export Options")
    export_format = st.selectbox("Select Export Format", ["CSV", "PDF"])
    if st.button("Export Report"):
        if st.session_state.signals is not None and st.session_state.metrics is not None:
            if export_format == "CSV":
                export_csv(st.session_state.signals, st.session_state.metrics)
            elif export_format == "PDF":
                export_pdf(st.session_state.signals, st.session_state.metrics)
                with open("report.pdf", "rb") as file:
                    st.download_button(
                        label="Download PDF",
                        data=file,
                        file_name="report.pdf",
                        mime="application/pdf",
                    )
            st.success("Report ready for download!")
        else:
            st.write("Please generate signals and calculate metrics first.")







