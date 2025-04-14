# 📊 Mono-Binning

Monotonic binning with Information Value (IV) and Weight of Evidence (WOE) transformation — optimized for **scorecard development**, **feature selection**, and **model explainability**.

---

## 🔧 Installation

```bash
pip install mono-binning


## Usage
```
from mono_binning import calculate_iv
import pandas as pd

# Load your dataset
df = pd.read_csv('data.csv')

# Step 1: Calculate IV summary, WOE-transformed DataFrame, and WOE maps
iv_summary, df_woe, woe_maps = calculate_iv(df, target='default_flag', execution='sequential')  # or 'concurrent'

# Step 2: View ranked variable importance by IV
print(iv_summary.sort_values('IV', ascending=False))


```

## Features
✅ Monotonic & Categorical Binning
- mono_bin() for numerical variables:

- Smart binning via qcut/cut fallback.

- Supports monotonic trend enforcement via IsotonicRegression.

- Handles missing values with special WOE.

- Applies alpha smoothing for stable IV/WOE.

- char_bin() for categorical variables:

- Treats 'nan', '', None, etc. as 'MISSING'.

- Safe WOE calculation using smoothing.
(bin_stats: pd.DataFrame, woe_map: Dict)
```

## 📚 Features

| Feature | Description |
|--------|-------------|
| ✅ `mono_bin` | Monotonic binning for numerical features using quantile-based cutoffs, with smoothing and trend enforcement |
| ✅ `char_bin` | Binning for categorical variables, treating missing or malformed entries as a distinct `"MISSING"` class |
| ✅ IV/WOE Output | All bin functions return bin stats and WOE maps |
| ✅ Missing Value Handling | Graceful support with separate WOE values for NaNs |
| ✅ Smoothing | Avoids instability with alpha smoothing |
| ✅ Trend Control | Use `force_trend='i'` for increasing or `'d'` for decreasing trend via isotonic regression |
| ✅ Parallel Execution | Use `calculate_iv_parallel()` for multi-threaded performance |
| ✅ Random Forest | Built-in `calculate_rf_importance()` and its parallel counterpart help compare model-based vs IV-driven variable importance |


## 🚀 Quick Start & API Reference

### 🧪 1. `calculate_iv()` – Main IV/WOE Calculation

```python
from mono_binning import calculate_iv
iv_summary, df_woe, woe_maps = calculate_iv(df, target='default_flag', execution='sequential')  # or 'concurrent'
```
### 🐢 2. calculate_iv_sequential() – Sequential IV Calculation

```python
from mono_binning import calculate_iv_sequential
iv_summary, df_woe, woe_maps = calculate_iv_sequential(df, target='default_flag')

```
### ⚡ 3. calculate_iv_parallel() – Parallel IV Calculation

```python
from mono_binning import calculate_iv_parallel
iv_summary, df_woe, woe_maps = calculate_iv_parallel(df, target='default_flag', max_workers=4)


```
### 🧱 4. mono_bin() – Numeric Monotonic Binning

```python
from mono_binning import mono_bin
bin_stats, woe_map = mono_bin(df['default_flag'], df['loan_amt'], var_name='loan_amt')


```
### 🧵 6. _iv_worker() – Internal Helper for IV Processing (Used in Threading)

```python
from mono_binning import _iv_worker

feature, bin_stats, woe_map = _iv_worker((df, 'default_flag', 'loan_amt', 0.5))
```
### 🌲 7. calculate_rf_importance() – Random Forest Feature Importance

```python
from mono_binning import calculate_rf_importance

importance_df = calculate_rf_importance(
    df, 
    target='default_flag', 
    features=['loan_amt', 'income', 'education'])
```

⚙️ IV & WOE Calculation
🐢 calculate_iv_sequential()
Processes one feature at a time.

Applies binning, returns IV summary, WOE-transformed DataFrame, and WOE maps.

⚡ calculate_iv_parallel()
Uses ThreadPoolExecutor for concurrency.

Parallelizes feature processing and WOE mapping.

🎯 calculate_iv()
Wrapper to switch between sequential and concurrent modes:
```
calculate_iv(df, target='target', execution='concurrent', max_workers=4)
```

### **. `Random Forest Feature Importance**
```
🌲 Random Forest Feature Importance
🔍 calculate_rf_importance()
Uses a full-feature pipeline (numerical + categorical preprocessing).

Computes feature importances using RandomForestClassifier.

🧵 calculate_rf_importance_concurrent()
Trains one RandomForest per feature in parallel.

Uses shared preprocessing pipeline.
```
---

### **. `LICENSE** (MIT Example)**
```text
MIT License
Copyright (c) 2023  Anvesh Reddy minukuri
... (add full license text from https://choosealicense.com/licenses/mit/)
```

---

## **🚀 Deployment Steps**

### **1. Build the Package**
```bash
# Navigate to package root
cd mono-binning

# Install build tools
pip install build

# Create distribution
python -m build
```
This generates a `dist/` folder with `.whl` and `.tar.gz` files.

---

### **2. Install Locally (Development)**
```bash
pip install -e .
```

---

### **3. Run Tests**
```bash
pip install pytest
pytest -v
```

---

### **4. Publish to PyPI**
```bash
pip install twine

# TestPyPI (optional)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

---

## **🔧  Highlights**
Feature	What You Did	Why It’s Smart
✅ ThreadPoolExecutor	Parallel binning + RF importance	Speeds up large datasets
✅ Alpha smoothing	Prevents divide-by-zero / log(0) issues	More robust WOE/IV calculations
✅ NaN handling	Assigns special WOE bin to missing vals	Keeps mappings consistent and crash-free
✅ Isotonic regression	Optional trend enforcement	Great for scorecard modeling
✅ Execution toggle	Switch between concurrent & sequential	Flexible for local vs. production runs

This structure follows **Python Packaging Authority (PyPA)** standards and includes best practices for maintainability. The package is now ready for production use!
