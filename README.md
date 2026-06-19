# 🚀 Mourabaha Portfolio Optimization

### A Strategic Data-Driven Approach

This repository hosts the implementation of the research project: **"Managing Mourabaha Financing Risk via Quadratic Programming: A Strategic Asset Allocation Approach."**

<br>

### 🎯 Project Overview

In the context of participatory finance, managing a **Murabaha** portfolio requires a delicate balance between maximizing returns and adhering to strict Sharia-compliant investment constraints. This project leverages **Quadratic Programming (QP)** to provide a robust, data-driven framework for optimal asset allocation.

<br>

### 🛠 Key Features

* **Mathematical Optimization:** Implements the **SLSQP algorithm** to maximize the **Sharpe Ratio** under complex linear constraints.
* **Sharia-Compliant Strategy:** Enforces "Long-Only" constraints and specific sectoral bounds (e.g., 40-60% Real Estate) to align with institutional mandates.
* **Financial Robustness:** Includes **Winsorization** to neutralize the impact of market outliers and extreme volatility, ensuring stable portfolio performance.
* **Decision Support:** Provides a comprehensive analytical suite, including **Rolling Volatility** analysis and **Risk-Return profiling**.

<br>

### 🏗 Methodology (CRISP-DM)

This project follows the industry-standard **CRISP-DM** lifecycle, ensuring a systematic approach from data ingestion to model deployment:

1. **Data Understanding & Prep:** Cleaning and normalizing heterogeneous financing datasets.
2. **Modelling:** Solving the portfolio optimization problem using `scipy.optimize`.
3. **Evaluation:** Visualizing results via correlation matrices, boxplots, and risk-return scatter plots.

<br>

### 📊 Project Structure

```text
├── data/               # Historical Murabaha financing datasets
├── notebook/           # Complete analysis workflow (Google Colab ready)
├── src/                # Core optimization scripts (SLSQP engine)
└── requirements.txt    # Essential Python dependencies

git clone [https://github.com/your-username/murabaha-optimization.git](https://github.com/your-username/murabaha-optimization.git)
pip install -r requirements.txt
python src/app.py


### 👥 Authors

* **Soukaina Hlal**  
* **Asma Daaou**  
* **Abdlouadoud Elkhalfi**  
* **Mohammed Elgharb**

