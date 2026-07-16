import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Stablecoin Anomaly Detection", layout="wide", page_icon="📊")

st.title("Distributed AWS Middleware: Stablecoin Run Detection")
st.caption("Real-Time Blockchain Anomaly Detection Engine | K-Nearest Neighbors & XGBoost Simulation")

st.sidebar.header("Pipeline Configuration")
selected_asset = st.sidebar.selectbox("Select Digital Asset Target", ["UST/LUNA Liquidity Pool (Simulated)", "USDC/USDT Curve Pool"])
anomaly_threshold = st.sidebar.slider("XGBoost Anomaly Threshold", 0.0, 1.0, 0.85)
run_simulation = st.sidebar.button("Initialize Ingestion Pipeline")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: AWS Lambda -> API Gateway -> XGBoost Inference")

if run_simulation:
    st.subheader(f"Monitoring: {selected_asset}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_peg = col1.empty()
    metric_volume = col2.empty()
    metric_outbound = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(42)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="S")
    
    peg_values = []
    outbound_velocity = []
    anomaly_scores = []
    
    base_peg = 1.000
    
    for i in range(100):
        if i < 40:
            current_peg = base_peg + np.random.uniform(-0.001, 0.001)
            current_velocity = np.random.uniform(10, 50)
            current_anomaly = np.random.uniform(0.1, 0.3)
        elif i >= 40 and i < 70:
            current_peg = base_peg - (i - 40) * 0.005 + np.random.uniform(-0.005, 0.005)
            current_velocity = np.random.uniform(200, 800)
            current_anomaly = np.random.uniform(0.7, 0.95)
        else:
            current_peg = base_peg - 0.15 + np.random.uniform(-0.02, 0.02)
            current_velocity = np.random.uniform(500, 1200)
            current_anomaly = np.random.uniform(0.85, 0.99)
            
        peg_values.append(current_peg)
        outbound_velocity.append(current_velocity)
        anomaly_scores.append(current_anomaly)
        
        metric_peg.metric("Current Peg (USD)", f"${current_peg:.3f}", f"{(current_peg - 1.0):.3f}")
        metric_volume.metric("24h Pool Volume", f"${np.random.uniform(400, 450):.1f}M")
        metric_outbound.metric("Outbound Velocity (Tx/s)", f"{int(current_velocity)}")
        
        if current_anomaly >= anomaly_threshold:
            metric_status.metric("Network Status", "FRAGILE - DE-PEG DETECTED", "High Risk")
        else:
            metric_status.metric("Network Status", "STABLE", "Normal")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=peg_values, mode='lines', name='Asset Price (USD)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=anomaly_scores, mode='lines', name='XGBoost Anomaly Score', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Real-Time Liquidity Depletion & Anomaly Score",
            xaxis=dict(title="Timestamp"),
            yaxis=dict(title="Price in USD", range=[0.8, 1.05]),
            yaxis2=dict(title="Anomaly Score", overlaying='y', side='right', range=[0, 1]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if current_anomaly >= anomaly_threshold:
            log_placeholder.error(f"SYSTEM ALERT: Anomalous transaction velocity detected at {time_steps[i].strftime('%H:%M:%S')}. Liquidity drain exceeding standard deviations. Initiating localized circuit breakers.")
        else:
            log_placeholder.success(f"Log: Transaction batch {i} processed successfully via AWS Lambda. No anomalies detected.")
            
        time.sleep(0.1)
        
    st.info("Simulation Complete. Distributed middleware successfully isolated the algorithmic bank run.")
else:
    st.info("Click 'Initialize Ingestion Pipeline' in the sidebar to simulate real-time blockchain data ingestion.")