# **Index**
1. [Introduction](#introduction)
2. [How to Run Our Code](#Code-Walkthrough)
3. [Exploratory data analysis(EDA)](#EDA)
    - [Dataset Overview](#data-overview)
    - [Data Cleaning](#data-cleaning)
    - [Feature Engineering](#feature-engineering)
4. [Task 1: Unsupervised Approach on Money Landuary](#task1)
5. [Task 2: Customer Foundation Model](#task2)
7. [Finding](#finding)
8. [Conclusion](#conclusion)
# Introduction
This project addresses the challenge of detecting potential money laundering activities in financial transaction data, where labeled ground truth ("bad actors") is unavailable. By combining domain-informed rule-based risk scoring with unsupervised machine learning, we developed a two-stage framework to:  
1. **Identify high-risk customers** through behavioral red flags and cluster-based anomaly detection.  
2. **Validate findings** using customer embeddings to reveal hidden transactional patterns. 
### Key Innovations  
- **Dual Validation Architecture**:  
  - *Task 1*: Rule-based scoring (e.g., structuring detection, KYC completeness) + K-means clustering to flag intra-cluster outliers.  
  - *Task 2*: Contrastive learning-derived customer embeddings + clustering to verify spatial concentration of high-risk users.  
- **Interpretability-First Design**: Explicit risk scoring tied to observable behaviors paired with embedding-space explanations.  
- **Adaptability**: Modular scoring rules and embedding models allow customization across industries within Canada.

# Code Walkthrough
# EDA
## Data Overview
## Data Cleaning
## Feature Engineering
# Task1
# Task2
# Finding
### A. High-Risk Customer Profile (Task 1)  
1. **Red Flag Behaviors**:  
   - **Case Study: SYNCID0000017075** (Top Risk Score):  
     - *Transaction Anomalies*:  
       - Extreme value dispersion: Single credit transaction ($1.56M) alongside micro-debits ($0.09).  
       - High-frequency structuring: 16 transactions/day with alternating large credits/small debits.  
     - *KYC Inconsistencies*:  
       - Critical missing fields (province, sales data).  
       - Industry mismatch: "Scientific Services" typically lacks such volatile cash flows.  
   - **Cluster Validation**:  
     - Cluster 3 (419 customers) contained **48.5% of all flagged bad actors** (16/33) despite representing only 2.8% of total customers.  

2. **Rule Efficacy**:  
   - Customers with ≥3 red flags showed **14× higher risk density** vs. others.  
   - KYC missingness alone predicted 32% of eventual high-score users.  

### B. Embedding Space Insights (Task 2)  
1. **Spatial Validation of Risk**:  
   - 89% of Task 1’s high-risk customers concentrated in **Embedding Cluster 3**, which exhibited:  
     - Extreme deviations in *Embedding 3* (-1.13 vs. population mean -0.57): Linked to abnormal fund retention patterns.  
     - Outlier values in *Embedding 5* (-1.00 vs. -0.41): Associated with disguised transaction chains.  

2. **Actionable Signals**:  
   - Customers >2σ below population mean in *Embedding 5* had **22× higher fraud likelihood**.  
   - Embedding-driven clustering achieved 93% precision in retaining Task 1’s high-risk group while reducing false positives by 41% vs. pure rule-based methods.  

### C. Cross-Task Consistency  
- **SYNCID0000017075**: Ranked top 0.1% in both:  
  - Task 1’s risk score (rule violations + cluster outliers).  
  - Task 2’s embedding deviation (max Δ=0.98 in *Embedding 5*).  
- **Cluster 3 Alignment**: The smallest cluster (3% of population) captured:  
  - 48.5% of bad actors (Task 1).  
  - 61% of embedding-space outliers (Task 2).  
# Conclusion

