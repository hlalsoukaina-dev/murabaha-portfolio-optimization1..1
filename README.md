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
* **Financial Robustness:** Includes **Winsorization** to neutralize the impact of market outliers and extreme volatility.

<br>

### 📊 Project Structure

```text
├── data/               # Historical Murabaha financing datasets
├── notebook/           # Complete analysis workflow (Google Colab ready)
├── src/                # Core optimization scripts (SLSQP engine)
└── requirements.txt    # Essential Python dependencies
```
🚀 Getting Started
1. Clone the repository:

git clone https://github.com/your-username/murabaha-optimization.git

2. Install dependencies:

pip install -r requirements.txt

3. Run the model:

python src/app.py

👥 Authors
Soukaina Hlal

Asma Daaou

Abdlouadoud Elkhalfi

Mohammed Elgharb

Project submitted in partial fulfillment of the requirements for the Master's degree in Financial Engineering and Participatory Finance (IFPIA).
