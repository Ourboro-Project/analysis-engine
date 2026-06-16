# ANOVA Analysis Data Contract

## Overview

This dataset is designed for One-Way ANOVA analysis.

Each row represents one respondent at one survey wave (wide-format structure).

---

## Example Dataset Structure
| ResponseId | cluster   | wave | var_1 | var_2 | var_3 |
|------------|-----------|------|-------|-------|-------|
| R001       | cluster_A | Y0   | 34    | 55000 | 7.2   |
| R002       | cluster_B | Y1   | 41    | 72000 | 6.8   |

> `var_1`, `var_2`, `var_3` ... : numeric features (DV candidates)
---

## Column Roles

### ResponseId

* Unique identifier for each respondent
* Used for data integrity and record alignment
* Not used in any statistical analysis

### cluster

* Independent variable (IV) for One-Way ANOVA
* Represents group membership for comparison across clusters

### wave

* Survey wave / time indicator (e.g., Y0, Y1, Y2)
* Used only for descriptive mean trends over time 

### Numeric features

* All numeric columns are treated as potential dependent variables (DVs)
* DV selection is determined by user input at runtime

---

## Analysis Scope

* Current implementation: One-Way ANOVA only
* Group comparison is performed using `cluster` as the IV
* Wave is used only for descriptive summaries, not statistical modeling

---

## Data Rules

* Additional numeric features may be added without schema changes
* DV analysis is based on user-selected numeric features
