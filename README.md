هذا هو النص بالإنجليزية، مقاد، منظم، وبدون أي تداخل في الكود، ومصحح حسب المعلومات الجديدة (أنكم في السنة الأولى وماشي PFE):

🚀 Mourabaha Portfolio Optimization
A Strategic Data-Driven Approach
This repository hosts the implementation of the research article: "Managing Mourabaha Financing Risk via Quadratic Programming: A Strategic Asset Allocation Approach."

🎯 Project Overview
In the context of participatory finance, managing a Murabaha portfolio requires a delicate balance between maximizing returns and adhering to strict Sharia-compliant investment constraints. This project leverages Quadratic Programming (QP) to provide a robust, data-driven framework for optimal asset allocation.

🛠 Key Features
Mathematical Optimization: Implements the SLSQP algorithm to maximize the Sharpe Ratio under complex linear constraints.

Sharia-Compliant Strategy: Enforces "Long-Only" constraints and specific sectoral bounds to align with institutional mandates.

Financial Robustness: Includes Winsorization to neutralize the impact of market outliers and ensure stable portfolio performance.

Decision Support: Provides a comprehensive analytical suite, including Rolling Volatility analysis and Risk-Return profiling.

📊 Project Structure
```text
├── data/               # Historical Murabaha financing datasets
├── notebook/           # Complete analysis workflow (Google Colab ready)
├── src/                # Core optimization scripts (SLSQP engine)
└── requirements.txt    # Essential Python dependencies
```
🚀 Getting Started
1. Clone the repository:

git clone [https://github.com/your-username/murabaha-optimization.git](https://github.com/your-username/murabaha-optimization.git)

2. Install dependencies:

pip install -r requirements.txt

3. Run the model:

python src/app.py

👥 Authors
Soukaina Hlal

Asma Daaou

Abdlouadoud Elkhalfi

Mohammed Elgharb

Research conducted as part of the academic coursework for the first year of the Master's degree in Financial Engineering and Participatory Finance (IFPIA).
