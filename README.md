# 🚩 **Smart Flag**
**AI-Driven Freight Cost Prediction & Invoice Risk Flagging**

## 📌 Table of Contents
- [Project Overview](#-project-overview)
- [Business Objectives](#-business-objectives)
- [Data Sources](#-data-sources)
- [Exploratory Data Analysis (EDA)](#-exploratory-data-analysis-eda)
- [Models Used](#-models-used)
- [Evaluation Metrics](#-evaluation-metrics)
- [End-to-End Application](#-end-to-end-application)
- [Project Structure](#-project-structure)
- [How to Run This Project](#-how-to-run-this-project)
- [Author & Contact](#-author--contact)

---

## 📌 Project Overview

**Smart Flag** is an end-to-end machine learning system designed to automate and secure finance operations. 
This application analyzes vendor invoices to:
1. **Predict expected freight costs** accurately to prevent overpayments.
2. **Flag high-risk invoices** that require manual review due to abnormal cost discrepancies or delivery delays.

---

## 🎯 Business Objectives

### 1. Freight Cost Prediction (Regression)
**Objective:** Predict the freight cost for a vendor invoice using Invoice Dollars.
**Why it matters:**
- Freight is a critical component of landed costs.
- Poor freight estimation impacts margin analysis and budgeting.
- Accurate forecasting improves budgeting, procurement planning, and vendor negotiations.

### 2. Invoice Risk Flagging (Classification)
**Objective:** Predict whether an invoice should be flagged for **manual approval**.
**Why it matters:**
- Manual review of every invoice does not scale.
- Financial leakage often occurs in complex invoices.
- Automating safe approvals allows the finance team to focus only on flagged anomalies.

---

## 📂 Data Sources

Data is stored in a relational SQLite database (`inventory.db`).

**Tables Used:**
- `vendor_invoice` – Invoice-level financial and timing data  
- `purchases` – Item-level purchase details  
- `purchase_prices` – Reference purchase prices  
- `begin_inventory`, `end_inventory` – Inventory snapshots  

**Feature Engineering:** Advanced SQL aggregation (CTEs) was used to extract invoice-level features such as total brands, total item quantities, system-calculated item dollars, and average receiving delays.

---

## 📊 Exploratory Data Analysis (EDA)

Comprehensive EDA was performed to validate business hypotheses:
- Analyzed the correlation between `Quantity`, `Dollars`, and `Freight`.
- Used **Statistical Testing (SciPy t-tests)** to confirm that metrics like receiving delays and cost mismatches significantly differentiate "Flagged" invoices from "Normal" invoices (p-value < 0.05).
- Visualized data relationships using Seaborn heatmaps and Matplotlib.

---

## 🤖 Models Used

### Regression (Freight Prediction)
- Linear Regression
- Decision Tree Regressor
- **Random Forest Regressor (Final Selected Model)**

### Classification (Invoice Flagging)
- Logistic Regression
- Decision Tree Classifier
- **Random Forest Classifier (Final Model)**
  - *Optimized using **GridSearchCV**.* - *Hyperparameter tuning for `n_estimators`, `max_depth`, `min_samples_split` optimizing for the F1-Score.*

---

## 📈 Evaluation Metrics

### Regression Metrics
- MAE
- RMSE
- R² Score

### Classification Metrics
- Accuracy
- Precision, Recall, F1-score
- Classification report
- Feature importance analysis

---

## 🖥 End-to-End Application

The project features a **Premium Streamlit Dashboard** with custom CSS styling that provides:
- Real-time Freight Cost Estimation with interactive Plotly Gauge charts.
- AI-driven risk evaluation for incoming invoices.
- Automated mismatch discrepancy checks (Vendor Claimed $vs. System Calculated$).

---

## 📁 Project Structure

```text
smart-flag/
│
├── data/
│   └── inventory.db
│
├── freight_cost_prediction/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── invoice_flagging/
│   ├── data_preprocessing.py
│   ├── model_evaluation.py
│   └── train.py
│
├── inference/
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
├── models/                     # Auto-generated during training
│   ├── predict_freight_model.pkl
│   ├── predict_flag_invoice.pkl
│   └── scaler.pkl
│
├── notebooks/
│   ├── invoice flagging.ipynb
│   └── predicting freight cost.ipynb
│
├── app.py                      # Main Streamlit Frontend
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🚀 How to Run This Project

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/smart-flag-app.git
```

2. **Train and Save Best Fit Models:**
```bash
python freight_cost_prediction/train.py
python invoice_flagging/train.py
```

3. **Test Models:**
```bash
python inference/predict_freight.py
python inference/predict_invoice_flag.py
``` 

4. **Open Application:**
```bash
streamlit run app.py
```

---

## 👩‍💻 Author & Contact

**Riya Parekh** *MCA (AI/ML)* 📧 Email: [parekhriyasanjaykumar@amityonline.com](mailto:parekhriyasanjaykumar@amityonline.com)
```