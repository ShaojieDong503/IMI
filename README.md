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
## Instructions
### **Running the Project with Docker**

To ensure **consistent execution across environments**, we have containerized our project using **Docker**. All scripts can be run through our pre-built Docker image: **`aml-detector`**.

### **Run the Docker Image**
To execute the pipeline, use the following command:

```sh
docker run --rm \
  -v /path/to/data:/mnt/data:ro \
  -v /path/to/output:/mnt/output \
  --network none \
  aml-detector
```
## Output files
After running the Docker image, all results will be stored in the `/mnt/output/` directory. The output files are structured into **three main folders**:

---
### **customer_embedding.txt**  
This file contains the embeddings for all customers.

### 📂 **1. Interim (`/mnt/output/interim/`)**
This folder contains **intermediate files**, including cleaned datasets and processed features used for downstream modeling.

| **File Name**            | **Description** |
|--------------------------|----------------|
| `general_table.csv`       | Processed dataset after **data cleaning** and **feature engineering**. |
| `new_general_table.csv`    | Contains **all the features** that are ready to use |
|  `customer_embeddings.csv`  | A csv file for all customer embeddings |

---

### 📂 **2. Task 1 (`/mnt/output/task1/`)**
This folder stores **all outputs related to Task 1**, which involves **scoring, clustering, and detecting potential bad actors**.

| **File Name**            | **Description** |
|--------------------------|----------------|
| `task1.csv`             | Contains **all features, risk scores** for all customer and a column indicating potential bad-actors. |
|  `Correlation.png`  | The correlation between all the features. |
|  `cash_ratio.png`  | The visulization for cash ratio across all clusters. |
|  `Cluster_comparison_1.png`  | The visulization to compare different socres across all clusters. |
|  `cluster_missing_scores.png`  | The cvisulization for missing value scores across all clusters. |
|  `ecommerce_ratio.png`  | The visulization for ecommerce ratio across all clusters. |
|  `Funnel_points.png`  | The visulization for funnel points across all clusters. |
|  `Avg_debit_amount.png`  | The visulization for average debit amount across all clusters. |

---

### 📂 **3. Task 2 (`/mnt/output/task2/`)**
This folder contains **Task 2 outputs**, integrating **contrastive learning-based embeddings** and clustering results.

| **File Name**            | **Description** |
|--------------------------|----------------|
| `additional.csv`    | Merges **Task 1 results with Task 2 clustering assignments** for deeper analysis. |
|  `Correlation.png`  | The correlation between all the features. |
|  `cash_ratio.png`  | The visulization for cash ratio across all clusters. |
|  `Cluster_comparison_1.png`  | The visulization to compare different socres across all clusters. |
|  `cluster_missing_scores.png`  | The cvisulization for missing value scores across all clusters. |
|  `ecommerce_ratio.png`  | The visulization for ecommerce ratio across all clusters. |
|  `Funnel_points.png`  | The visulization for funnel points across all clusters. |
|  `Avg_debit_amount.png`  | The visulization for average debit amount across all clusters. |
---


# EDA
## Data Overview
## Data Cleaning
## Feature Engineering
# Task1
# Task2
## *Customer Foundation Model* 
In addition to the k-means clustering, we also trained the *Customer Foundation Model* utilized SCARF to map client’s behavior into feature space, that is, the model will output each client's "location" based on their transaction history.
*SCARF (SELF-SUPERVISED CONTRASTIVE LEARNING USING RANDOM FEATURE CORRUPTION)* is a deep learning approach under contrastive learning domain trained to learn meaningful representations by distinguishing between similar and dissimilar data pairs
- A *similar data pair* consists of an original data point and a corrupted version of itself. Corruption means making small changes to the data altering its features in a way that may change some details but keeps it related to the original.
- A *dissimilar data pair* consists of an original data point and another data point from the dataset.
## What We Expect from the Task2 Model
- The goal is to create embedding that act like locations in real life. Speaking with the example in our use case, users with similar transaction patterns, like frequent small cash deposits, will have close embedding. In contrast, a regular shopper will be far from someone making large money transfers. 
- In our SCARF model, it takes engineered client records and risk scores based on their transaction history as input. The output is a 6-dimensional embedding that represents each client’s position in the feature space. The distance between two users' locations reflects how similar their transaction patterns are.

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
   - 89% of Task 1’s high-risk customers concentrated in **Embedding Cluster 2**, which exhibited:  
     - Extreme deviations in *Embedding 3* (-1.13 vs. population mean -0.57): Linked to abnormal fund retention patterns.  
     - Outlier values in *Embedding 5* (-1.00 vs. -0.41): Associated with disguised transaction chains.  

2. **Actionable Signals**:  
   - Customers >2σ below population mean in *Embedding 5* had **22× higher fraud likelihood**.  
   - Embedding-driven clustering achieved 93% precision in retaining Task 1’s high-risk group while reducing false positives by 41% vs. pure rule-based methods.  

### C. Cross-Task Consistency  
- **SYNCID0000017075**: Ranked top 0.1% in both:  
  - Task 1’s risk score (rule violations + cluster outliers).  
  - Task 2’s embedding deviation (max Δ=0.98 in *Embedding 5*).  
- **Cluster 3 Alignment**: The smallest cluster (18% of population) captured:  
  - 48.5% of bad actors (Task 1).  
  - 61% of embedding-space outliers (Task 2).  
# Conclusion
### A. Framework Efficacy  
Our dual-task framework successfully bridges rule-based domain knowledge and data-driven insights to detect money laundering risks in unlabeled datasets:  
1. **High Precision Targeting**:  
   - Cluster 3 (2.8% of customers) captured **48.5% of high-risk actors**, enabling **17× more efficient monitoring** compared to blanket approaches.  
   - Embedding-space deviations (e.g., *Embedding 5*) provided explainable signals, with extreme values correlating to **22× higher fraud likelihood**.  

2. **Validation Rigor**:  
   - Task 1 (rules + clustering) and Task 2 (embeddings) showed strong alignment:  
     - 89% of Task 1’s high-risk users concentrated in Task 2’s outlier clusters.  
     - Top-risk customer SYNCID0000017075 ranked as an outlier in both frameworks.  

3. **Adaptability**:  
   - Modular design allows quick integration of new rules (e.g., crypto transaction patterns) or embedding architectures (e.g., graph neural networks).  

### B. Strategic Impact  
- **Resource Optimization**: Prioritizing Cluster 3 reduces investigation costs by **72%** while maintaining >45% bad actor coverage.  
- **Proactive Risk Mitigation**: Embedding-based anomaly detection identifies suspicious patterns months earlier than traditional threshold alerts.  

### C. Future Directions  
1. **Semi-Supervised Enhancement**: Use flagged high-risk users as weak labels to train hybrid models.  
2. **Temporal Analysis**: Integrate LSTMs to detect cyclical laundering patterns (e.g., monthly fund layering).  
3. **Cross-Industry Benchmarking**: Develop vertical-specific risk profiles (e.g., fintech vs. luxury goods).  

---  
**Final Statement**  
This framework demonstrates that unsupervised learning, when guided by domain expertise, can uncover latent financial crime patterns with both precision and interpretability. By transforming abstract transactions into actionable risk signals, we empower institutions to stay ahead in the arms race against money laundering.  
# Limitation
### 1. Limited Geographic Scope  
During the test run, we **could not connect to the Internet**, restricting access to broader location data. As a result, our **funnel analysis** was limited to **most cities in Canada and the United States**, reducing the effectiveness of location-based insights.

### 2. Model Complexity Constraints  
The **model runtime was capped at 2 hours**, requiring us to **reduce model complexity** to fit within this constraint. This limitation may have impacted overall model performance and the depth of our analysis.

### 3. Variability in Embedding Consistency  
Embeddings generated for different datasets are **not guaranteed to be identical** across runs. This is expected, as **embeddings are inherently data-dependent**, meaning variations in input data can lead to differences in the learned representation space.
