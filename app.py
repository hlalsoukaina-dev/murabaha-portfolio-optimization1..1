import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize
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

st.title("🏦 Mourabaha Portfolio Optimizer (Quadratic)")
st.markdown("---")

# 2. Input Parameters (Sidebar)
st.sidebar.header("⚙️ Portfolio Parameters")
budget = st.sidebar.number_input("Total Budget (MAD)", value=1000000)
g1 = st.sidebar.number_input("Growth Rate: Real Estate (g1)", value=0.0237)
g2 = st.sidebar.number_input("Growth Rate: Automobile (g2)", value=0.0221)
g3 = st.sidebar.number_input("Growth Rate: Equipment (g3)", value=0.1498)
g4 = st.sidebar.number_input("Growth Rate: Raw Materials (g4)", value=-0.0026)

if st.sidebar.button("🚀 Run Optimization"):
    # Expected returns
    returns = np.array([g1, g2, g3, g4])
    
    # Objective function
    def objective(weights):
        return -np.sum(weights * returns)

    # Constraints
    constraints = (
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}, 
        {'type': 'ineq', 'fun': lambda x: x - np.array([0.3, 0.05, 0.05, 0.0])}, 
        {'type': 'ineq', 'fun': lambda x: np.array([0.8, 0.25, 0.3, 0.1]) - x}  
    )
    
    # Solver execution
    x0 = [0.25, 0.25, 0.25, 0.25]
    res = minimize(objective, x0, method='SLSQP', constraints=constraints)
    
    if res.success:
        st.balloons()
        amounts = res.x * budget
        profit = amounts * returns
        
        df = pd.DataFrame({
            "Sector": ["Real Estate", "Automobile", "Equipment", "Raw Materials"],
            "Invested Amount (MAD)": amounts,
            "Allocation (%)": res.x * 100,
            "Expected Profit (MAD)": profit
        })
        
        st.success("Analysis completed successfully (Quadratic Programming)!")
        
        col_res1, col_res2 = st.columns([1, 1])
        with col_res1:
            st.subheader("📊 Allocation Table")
            st.table(df.style.format({"Invested Amount (MAD)": "{:,.2f}", "Allocation (%)": "{:.1f}%", "Expected Profit (MAD)": "{:,.2f}"}))
            
            # Download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results (CSV)", data=csv, file_name='murabaha_allocation.csv', mime='text/csv')
            
        with col_res2:
            st.subheader("🍕 Portfolio Distribution")
            fig_pie = px.pie(df, values='Allocation (%)', names='Sector', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.subheader("📈 Expected Profit per Sector")
        fig_bar = px.bar(df, x='Sector', y='Expected Profit (MAD)', color='Sector')
        st.plotly_chart(fig_bar, use_container_width=True)
        
        risk = "Low" if res.x[0] > 0.5 else "High"
        st.metric("🛡️ Risk Index", risk)
        
        st.info("💡 Note: This analysis is based on Quadratic Programming (SLSQP) for robust strategic allocation.")
        st.warning("⚠️ Disclaimer: This tool is for academic purposes only.")
    else:
        st.error("Optimization failed. Please check your constraints.")
