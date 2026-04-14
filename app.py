import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Smart Flag - AI Invoice Intelligence",
    page_icon="🚩",
    layout="wide"
)


st.markdown("""
<style>
    
    .stApp {
        background-color: #F0F4F8; 
    }
    
    
    h1 {
        color: #1E293B;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        border-left: 6px solid #FF4B4B; 
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
    }

    div[data-testid="stForm"] button {
        background-color: #ffffff !important; 
        border: 2px solid #10B981 !important; 
        color: #10B981 !important;            
        border-radius: 8px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        box-shadow: 0px 4px 6px rgba(16, 185, 129, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    div[data-testid="stForm"] button:hover {
        background-color: #10B981 !important; 
        color: white !important;              
        transform: translateY(-3px);
        box-shadow: 0px 8px 15px rgba(16, 185, 129, 0.3) !important;
    }

    .stNumberInput input {
        border-radius: 6px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #F8FAFC !important;
        transition: all 0.2s;
    }
    .stNumberInput input:focus {
        border-color: #3B82F6 !important; /* Blue focus outline */
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    .streamlit-expanderHeader {
        background-color: #F1F5F9;
        border-radius: 6px;
        color: #475569;
    }

    .impact-item {
        background-color: #ffffff;
        border: 1px solid #E2E8F0;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #334155;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0px 2px 4px rgba(0,0,0,0.02);
        cursor: default;
    }
    
    .impact-item:hover {
        transform: translateX(8px); 
        border-color: #FF4B4B;      
        box-shadow: 0px 6px 12px rgba(255, 75, 75, 0.1);
        background-color: #FFF5F5;  /* Very soft red tint */
        color: #B91C1C;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header Section
# -------------------------------------------------------
st.markdown("""
# 📦 Vendor Invoice Intelligence Portal  
### AI-Driven Freight Cost Prediction & Invoice Risk Flagging

This internal analytics portal leverages machine learning to  
- **Forecast freight costs accurately**
- **Detect risky or abnormal vendor invoices**
- **Reduce financial leakage and manual workload**
""")

st.divider()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
st.sidebar.markdown("""
    <div style="text-align: left; margin-top: -30px; padding-left: 5px;">
        <h1 style="font-family: 'Trebuchet MS', sans-serif; font-weight: 800; color: #FF4B4B; margin-bottom: 0; font-size: 2.2rem;">
            🚩 Smart Flag
        </h1>
        
    </div>
    <hr style="margin-top: 15px; margin-bottom: 25px; border-color: #E2E8F0;">
""", unsafe_allow_html=True)

st.sidebar.title("🔍 Model Selection")
selected_model = st.sidebar.radio(
    "Choose Prediction Module",
    [
        "Freight Cost Prediction",
        "Invoice Manual Approval Flag"
    ]
)

st.sidebar.markdown("""
---
<p style="font-size: 15px; font-weight: 700; color: #475569; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;">Business Impact</p>
<div class="impact-item">📉 Improved cost forecasting</div>
<div class="impact-item">🧾 Reduced invoice fraud & anomalies</div>
<div class="impact-item">⚙️ Faster finance operations</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Freight Cost Prediction
# -------------------------------------------------------
if selected_model == "Freight Cost Prediction":
    st.subheader("🚚 Freight Cost Prediction")

    st.markdown("""
    **Objective:** Predict freight cost for a vendor invoice using **Invoice Dollars** to support budgeting, forecasting, and vendor negotiations.
    """)

    with st.container():
        with st.form("freight_form"):
            col1, col2 = st.columns(2)

            with col1:
                dollars = st.number_input(
                    "**💰 Invoice Dollars**",
                    min_value=1.0,
                    value=18500.0
                )

            submit_freight = st.form_submit_button("🔮 Predict Freight Cost")

    if submit_freight:
        try:
            input_data = {
                "Dollars": [dollars]
            }

            prediction = predict_freight_cost(input_data)['Predicted_Freight']

            st.success("✅ Prediction completed successfully.")

            st.metric(
                label="📊 Estimated Freight Cost",
                value=f"${prediction[0]:,.2f}"
            )
            st.markdown("---")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prediction[0],
                title = {'text': "Estimated Freight Meter ($)", 'font': {'size': 20, 'color': '#334155'}},
                gauge = {
                    'axis': {'range': [None, max(500, prediction[0] * 1.5)], 'tickwidth': 2, 'tickcolor': "#475569"},
                    'bar': {'color': "#3B82F6"},
                    'bgcolor': "#F1F5F9",
                    'steps': [
                        {'range': [0, prediction[0]*0.7], 'color': "#DBEAFE"}, 
                        {'range': [prediction[0]*0.7, prediction[0]*1.2], 'color': "#93C5FD"} 
                    ]
                }
            ))
            fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "#1E293B"})
            st.plotly_chart(fig_gauge, use_container_width=True)

        except Exception as e:
            st.error("⚠️ Oops! Something went wrong while calculating the freight cost. Please check the inputs or try again later.")
            with st.expander("Show technical details"):
                st.write(f"Error: {e}")

# -------------------------------------------------------
# Invoice Flag Prediction
# -------------------------------------------------------
else:
    st.subheader("🚨 Invoice Manual Approval Prediction")

    st.markdown("""
    **Objective:** Predict whether a vendor invoice should be **flagged for manual approval** based on abnormal cost, freight, or delivery patterns.
    """)

    with st.container():
        with st.form("invoice_flag_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                invoice_quantity = st.number_input(
                    "**Invoice Quantity**",
                    min_value=1,
                    value=50
                )
                freight = st.number_input(
                    "**Freight Cost**",
                    min_value=0.0,
                    value=1.73
                )

            with col2:
                invoice_dollars = st.number_input(
                    "**Invoice Dollars**",
                    min_value=1.0,
                    value=352.95
                )
                total_item_quantity = st.number_input(
                    "**Total Item Quantity**",
                    min_value=1,
                    value=162
                )

            with col3:
                total_item_dollars = st.number_input(
                    "**Total Item Dollars**",
                    min_value=1.0,
                    value=2476.0
                )

            submit_flag = st.form_submit_button("🧠 Evaluate Invoice Risk")

    if submit_flag:
        try:
            input_data = {
                "invoice_quantity": [invoice_quantity],
                "invoice_dollars": [invoice_dollars],
                "Freight": [freight],
                "total_item_quantity": [total_item_quantity],
                "total_item_dollars": [total_item_dollars]
            }

            flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']

            is_flagged = bool(flag_prediction[0])

            if is_flagged:
                st.error("🚨 Invoice requires **MANUAL APPROVAL**")
            else:
                st.success("✅ Invoice is **SAFE for Auto-Approval**")
            
            st.markdown("### 📊 Cost Discrepancy Analysis")
            
            chart_data = pd.DataFrame({
                "Category": ["Vendor Claimed (Invoice $)", "System Calculated (Item $)"],
                "Amount": [invoice_dollars, total_item_dollars]
            })
            
            fig_bar = px.bar(
                chart_data, 
                x="Category", 
                y="Amount",
                text="Amount",
                color="Category",
                color_discrete_map={
                    "Vendor Claimed (Invoice $)": "#EF4444", 
                    "System Calculated (Item $)": "#10B981"  
                },
                title="Mismatch Check (Difference > $5 flags the invoice)"
            )
            fig_bar.update_traces(texttemplate='$%{text:,.2f}', textposition='outside', marker_line_width=0)
            fig_bar.update_layout(
                height=400, 
                showlegend=False, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=18, color="#1E293B"),
                xaxis=dict(title="", tickfont=dict(size=14)),
                yaxis=dict(title="Amount ($)", gridcolor="#E2E8F0")
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)   
            
        except Exception as e:
            st.error("⚠️ Oops! Our AI model encountered an issue processing this invoice. Please verify the numbers.")
            with st.expander("Show technical details"):
                st.write(f"Error: {e}")