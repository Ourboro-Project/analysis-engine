# Analysis-Ready Dataset Specification

## Purpose
This dataset is designed for both one-way ANOVA analysis and longitudinal descriptive reporting (cluster × time trends).


---


## Required Columns

### Cluster Variables (Independent Variable)
- cluster_id: Numeric or coded cluster assignment
- cluster_name: Human-readable cluster label (e.g., Active Buyers, Planning Buyers, etc.)

### Time Variables
- time: survey wave indicator (e.g., Y0, Y1, Y2)

### Dependent Variables
- DV: numeric outcome variable selected at runtime (e.g., happiness, down_payment, economic_resilience, etc.)
The DV is selected dynamically depending on the analysis being run.

### Controls
- age
- gender
- income
- education


---

## Data Shape Requirement

- Long format preferred:
  cluster_id | cluster_name | time (Y0, Y1, Y2) | DV | controls...

---

## Analysis Modules

### One-way ANOVA Module (Main Analysis)
- Input variables: cluster, DV

### Longitudinal Descriptive Module (Reporting)
- Input variables: cluster, DV, time


---


## Note

- cluster is pre-computed during the data pipeline stage
- time is optional for ANOVA but required for descriptive reporting
- DV is flexible and selected at runtime depending on analysis needs
