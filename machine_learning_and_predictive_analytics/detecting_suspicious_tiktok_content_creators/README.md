# Detecting Suspicious TikTok Content Creators

## 🚀 Project Overview
This repository contains the implementation of interpretable machine learning models for detecting suspicious users on TikTok. The study focuses on user behavior and content features to complement content-based moderation strategies. 

## 🎯 Objective
1. Identify suspicious users (under scrutiny or banned) based on their behavior and content.
2. Evaluate the performance of interpretable models, prioritizing trust and clarity in decision-making.
3. Optimize and interpret the best-performing model to provide actionable insights.

---

## 📊 Key Features
- **Dataset**: 19,383 TikTok user entries, with features like:
  - User attributes: ban and verification status.
  - Video attributes: views, likes, comments, shares, downloads, claim status, and transcription text.
- **Models**: 
  - Logistic Regression: Linear and interpretable.
  - Decision Tree: Non-linear, interpretable, and visualizable.
- **Analysis Goals**:
  - Address class imbalance using techniques like SMOTE and SMOTEENN.
  - Preprocess data with outlier removal and feature scaling.
  - Create interpretable models to ensure trust in decision-making.

---

## 🛠️ Methodology
1. **Data Preprocessing**:
   - Handled missing values and outliers.
   - Encoded categorical variables with `OneHotEncoder`.
   - Tokenized text features using Bag-of-Words with the top 20 most frequent terms.
   - Addressed class imbalance using SMOTE and SMOTEENN techniques.
2. **Model Training**:
   - Logistic Regression for baseline and feature coefficient analysis.
   - Decision Tree for detailed visualization and feature importance analysis.
   - Hyperparameter tuning to improve model performance.
3. **Evaluation Metrics**:
   - Precision, Recall, and F1 Score to prioritize balanced performance over raw accuracy.

---
![](https://github.com/Takosaga/fall_24/blob/main/machine_learning_and_predictive_analytics/detecting_suspicious_tiktok_content_creators/reports/figures/decision_tree.png)
## 🌟 Results
- **Best Model**: Decision Tree with a maximum depth of 3 and SMOTEENN resampling, achieving an F1 score of **0.47**.
- **Key Features**:
  - Video view count, video duration, and specific keywords (e.g., "friend," "media," "internet").
  - Model interpretability ensured through visual decision-making processes.
- **Recommendations**:
  - Future iterations should explore more complex models like neural networks combined with Explainable AI (XAI) techniques for enhanced interpretability.

---

## 🔗 Project Links
- **Project Repository**: [Source Code](https://github.com/Takosaga/fall_24/tree/main/machine_learning_and_predictive_analytics/detecting_suspicious_tiktok_content_creators)  


<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>


## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         detecting_suspecious_tiktok_content_creators and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── detecting_suspecious_tiktok_content_creators   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes detecting_suspecious_tiktok_content_creators a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

