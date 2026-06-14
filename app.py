import streamlit as st
import pandas as pd
from scipy.optimize import linprog
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Mourabaha Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #0066cc; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #0066cc; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Mourabaha Allocation Optimizer")
st.markdown("---")

# 2. Input Parameters
col1, col2 = st.columns(2)
budget = col1.number_input("Total Budget (MAD)", value=1000000)
g1 = col2.number_input("Growth Rate: Real Estate (g1)", value=0.0237)
g2 = col1.number_input("Growth Rate: Automotive (g2)", value=0.0221)
g3 = col2.number_input("Growth Rate: Equipment (g3)", value=0.1498)
g4 = col1.number_input("Growth Rate: Raw Materials (g4)", value=-0.0026)

if st.button("🚀 Run Optimization Analysis"):
    # Objective: Maximize returns (minimize negative returns)
    c = [-g1, -g2, -g3, -g4]
    
    # Constraints: Sectoral allocation bounds
    bounds = [(0.3, 0.8), (0.05, 0.25), (0.05, 0.3), (0.0, 0.1)]
    
    # Solve
    res = linprog(c, A_eq=[[1, 1, 1, 1]], b_eq=[1], bounds=bounds, method='highs')
    
    if res.success:
        st.balloons()
        
        # Prepare Results Data
        df = pd.DataFrame({
            "Sector": ["Real Estate", "Automotive", "Equipment", "Raw Materials"],
            "Amount (MAD)": [x * budget for x in res.x],
            "Allocation (%)": [x * 100 for x in res.x]
        })
        
        st.success("Optimization completed successfully!")
        
        # Display Results
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.subheader("Optimized Allocation Table")
            st.table(df.style.format({"Amount (MAD)": "{:,.2f}", "Allocation (%)": "{:.1f}%"}))
            
        with col_res2:
            st.subheader("Visualization")
            fig = px.pie(df, values='Allocation (%)', names='Sector', hole=0.3)
            st.plotly_chart(fig)
        
        # Risk Metric
        risk_level = "Low" if res.x[0] > 0.5 else "High"
        st.metric("Diversification Risk Index", risk_level)
        
        st.info("💡 Note: Results are generated using quadratic programming constraints.")
    else:
        st.error("Optimization failed. Please check your constraints.")
