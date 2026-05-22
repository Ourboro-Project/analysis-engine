# ANOVA Research Analysis Project

## 1. Project Overview
This project analyzes survey/research data using ANOVA methods to evaluate differences across groups, time, and questions.

---

## 2. Environment Setup

We use **Miniconda** to manage the Python environment.

The project may later include:
- additional preprocessing pipelines
- feature/index generation
- expanded statistical analysis
- increased scientific Python dependencies

### Why Miniconda?
- Lightweight compared to full Anaconda
- Reliable dependency management for scientific libraries (numpy, scipy, statsmodels)
- Easy environment reproduction via environment.yml
- Commonly used in data science workflows (ex. Jupyter-based workflows)

---

## 3. Environment Setup Instructions

### Clone Repository

```bash
git clone .........*need to add url later*
cd anova-analysis
```

### Create conda environment (first time only)
```bash
conda env create -f environment.yml
```

### Activate environment (every session)
```bash
conda activate anova_env
```

### Update environment (when environment.yml changes)
```bash
conda env update -f environment.yml --prune
```

---

## 4. Run Analysis

This project uses Jupyter Notebook for analysis.


Open Jupyter Notebook:

### 1) VS Code (Recommended)

- Open project in VS Code

- Select kernel : `anova_env`

- Run cells : `Shift + Enter`


### 2) Terminal (Jupyter)

```bash
conda activate anova_env
jupyter notebook
```

Then open `notebooks/repeated_anova.ipynb`

- Kernel setup (if not available)
```bash
python -m ipykernel install --user --name anova_env
```

---

## 5. Key Libraries Used
- pandas
- numpy
- scipy
- statsmodels
- seaborn

---

## 6. Project Structure
- /datasets -> raw and processed data
- /notebooks -> Jupyter analysis (ANOVA implementation)
- /outputs -> results, figures, and exported outputs
- /src -> reusable Python scripts and functions (future use if needed)
- environment.yml → environment setup