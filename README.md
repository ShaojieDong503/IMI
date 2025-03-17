# **Index**
1. [Introduction](#introduction)
2. [How to Run Our Code](#Code-Walkthrough)
3. [Exploratory data analysis(EDA)](#EDA)
    - [Dataset Overview](#data-overview)
    - [Data Cleaning](#data-cleaning)
    - [Feature Engineering](#feature-engineering)
4. [Task 1: Unsupervised Approach on Money Landuary](#task1)
5. [Task 2: Customer Foundation Model](#task2)
7. [Conclusion](#conclusion)
8. [Limitation](#limitation)
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
# Project Workflow  
**A Dual-Phase Unsupervised Framework for AML Detection**  

## 1. Data Integration & Preprocessing  
### Inputs:  
- Transaction data (CSVs: Card, ABM, ETF, Wire, EMT, Cheque)  
- KYC data (industry code, employee count, sales, etc.)  

### Process:  
1. **Exploratory Data Analysis (EDA)**  
   - Merge transaction data into a unified **General Aggregate Table** (features: avg. transaction frequency, cash transaction ratio, etc.).  


2. **Feature Engineering**  
   - Calculate **Red Flag Scores** after EDA.  
   - Check correlation between features.  


## 2. Task 1: Rule-Guided Clustering  
### Input:  
- General Aggregate Table + Red Flag Scores.  

### Process:  
1. **K-means Clustering**
   - Remove highly correlated features.   
   - Optimize cluster count using **Inertia and Silhouette scores** (final k=4).  

2. **Intra-Cluster Anomaly Scoring**  
   - For each customer in a cluster:  
     - Compare against cluster peers on 5 metrics:  
       `(Transaction frequency, Total deposits, Total spending, Cash ratio, Ecommerce ratio)` 
     - Detailed scoring system introduction are under [Task 1](#task1).

3. **Final Risk Ranking**  
   - Total Score = Red Flag Score + Intra-Cluster Outlier Score.  
   - Flag customers in **Top 0.5%** as "High-Risk Candidates".  (0.5% can help us focus on exterme scores and have more flexibility compares to a fixed number)


## 3. Task 2: Embedding-Based Validation  
### Input:  
- Same as Task 1 

### Process:  
1. **Contrastive Learning for Embeddings**  
   - Train a contrastive learning model to generate 6D customer embeddings.  

2. **Secondary Clustering**  
   - Apply K-means clustering to embedding space.  
   - Identify **Target Clusters** where High-Risk Candidates concentrate.  

3. **Cross-Task Validation**  
   - Compute overlap: If most High-Risk Candidate(Customer has a high score) concentrate in certain clusters, we say they share more spending behaviors and characteristics, which makes they more suspecious.  Customer who has a high score but not concentrate with others in a cluster means it has slightly lower risk but still need to be monitored. 


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
|  `new_abm.csv`  | Cleaned ABM transaction data |
|  `new_card.csv`  | Cleaned Card transaction data |
|  `new_cheque.csv`  | Cleaned Cheque transaction data |
|  `new_eft.csv`  | Cleaned EFT transaction data |
|  `new_emt.csv`  | Cleaned EMT transaction data |
|  `new_wire.csv`  | Cleaned Wire transaction data |

---

### 📂 **2. Task 1 (`/mnt/output/task1/`)**
This folder stores **all outputs related to Task 1**, which involves **scoring, clustering, and detecting potential bad actors**.

| **File Name**            | **Description** |
|--------------------------|----------------|
| `task1.csv`             | Contains **all features, risk scores** for all customer and a column indicating potential bad-actors |
|  `Correlation.png`  | The correlation between all the features |
|  `cash_ratio.png`  | The visulization for cash ratio across all clusters |
|  `Cluster_comparison_1.png`  | The visulization to compare different socres across all clusters |
|  `cluster_missing_scores.png`  | The cvisulization for missing value scores across all clusters |
|  `ecommerce_ratio.png`  | The visulization for ecommerce ratio across all clusters |
|  `Funnel_points.png`  | The visulization for funnel points across all clusters |
|  `Avg_debit_amount.png`  | The visulization for average debit amount across all clusters |
|  `Elbow_and_Silhouette.png`  | The visulization for Silhouette and Inertia Scores for Kmeans |
---

### 📂 **3. Task 2 (`/mnt/output/task2/`)**
This folder contains **Task 2 outputs**, integrating **contrastive learning-based embeddings** and clustering results.

| **File Name**            | **Description** |
|--------------------------|----------------|
| `additional.csv`    | Merges **Task 1 results with Task 2 clustering assignments** for deeper analysis. |
|  `results_summary.txt`  | All cluster results and lists of potential bad actors that we identified from Task 1 and Task 2. |
|  `Correlation.png`  | The correlation between all the features. |
|  `cash_ratio.png`  | The visulization for cash ratio across all clusters. |
|  `comparison_points.png`  | The visulization to compare different socres across all clusters. |
|  `cluster_missing_scores.png`  | The cvisulization for missing value scores across all clusters. |
|  `ecommerce_ratio.png`  | The visulization for ecommerce ratio across all clusters. |
|  `Funnel_points.png`  | The visulization for funnel points across all clusters. |
|  `Avg_debit_amount.png`  | The visulization for average debit amount across all clusters. |
|  📂 `high_risk_customers`  | A folder contains transactions timeseries plots for all high-risk customers. |
---


# EDA
## Data Overview
### Business Information - KYC

| **Field Name**      | **Description**                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| `country`           | The country where the business is located.                                      |
| `province`          | The province or state where the business operates (if applicable).             |
| `city`              | The city where the business is registered or operates.                         |
| `industry_code`     | A standardized code representing the industry in which the business operates (e.g., NAICS, SIC). |
| `employee_count`    | The number of employees working in the business.                               |
| `sales`             | The total sales revenue of the business, likely in a specific currency.        |
| `established_date`  | The date when the business was officially founded or incorporated.             |
| `onboard_date`      | The date when the business was onboarded into the system (e.g., for banking, compliance, or KYC verification). |

### Transaction Information

| **Field Name**      | **Description**                                                                 |
|---------------------|---------------------------------------------------------------------------------|
| `customer_id`       | A unique identifier for each customer who made a transaction.                  |
| `amount_cad`        | The transaction amount in Canadian dollars (CAD).                              |
| `debit_credit`      | Indicates whether the transaction is a debit (money spent) or credit (money received). |
| `cash_indicator`    | Specifies whether the transaction was made using cash or another payment method (e.g., card, digital payment). |
| `country`           | The country where the transaction took place.                                  |
| `province`          | The province (if applicable) where the transaction occurred.                   |
| `city`              | The city where the transaction was made.                                       |
| `transaction_date`  | The date when the transaction occurred.                                        |
| `transaction_time`  | The time at which the transaction was processed.                               |
| `merchant_category` | The type of merchant or business where the transaction took place (e.g., groceries, restaurants, retail). |
| `ecommerce_ind`     | A binary indicator (likely yes/no or 1/0) specifying whether the transaction was an e-commerce purchase (online) or an in-person transaction. |
## Data Cleaning
We keep all the data points and make missing fields particularly geographical ones like city, province, and country *unknown* instead of NaN
## Feature Engineering
### Transaction Data Processing
### 1. **Convert `transaction_date` to `datetime` and Split into Year, Month, and Day**
   - `transaction_date` will be converted into a `datetime` object.
   - Extract `year`, `month`, and `day` from the `transaction_date` field to create separate columns for each.

### 2. **Calculate Transaction Intervals**
   - Calculate the time intervals between consecutive transactions for the same customer and the same transaction type.
   - Compute the overall transaction intervals (including all transaction types) for each customer.
   
### 3. **Standardize `debit_credit` Values**
   - Unify the `debit_credit` values by converting `C/D` to `credit/debit` for consistency.
   - Replace `true/false` values in relevant columns with `1/0` for binary representation.

### 4. **Find Maximum and Average Transaction Amounts**
   - **Maximum Credit Transaction Amount:** Find the maximum credit transaction amount for each customer across all transactions.
   - **Maximum Debit Transaction Amount:** Find the maximum debit transaction amount for each customer across all transactions.
   - **Average Credit Transaction Amount:** Calculate the average credit transaction amount for each customer across all transactions.
   - **Average Debit Transaction Amount:** Calculate the average debit transaction amount for each customer across all transactions.

### 5. **Calculate Total Credit and Debit Amounts**
   - **`total_credit_amount_cad`**: Sum of all credit transaction amounts (in CAD) for each customer.
   - **`total_debit_amount_cad`**: Sum of all debit transaction amounts (in CAD) for each customer.

### 6. **Transaction Frequency and Interval Analysis**
   - **Number of Credit Transactions (`#_credit`)**: Count of credit transactions for each customer.
   - **Number of Debit Transactions (`#_debit`)**: Count of debit transactions for each customer.
   - **Transaction Frequency (`transaction_freq`)**: Total number of transactions for each customer.
   - **Average Transaction Interval in Days (`avg_transaction_interval_day`)**: Calculate the average interval (in days) between each transaction for each customer.
   - **Mode Transaction Interval in Days (`mode_transaction_interval_day`)**: Identify the most common interval (in days) between transactions for each customer.
   - **Active Period of Time for a Customer (`date_range`)**: Calculate the active time period from the earliest to the latest transaction date for each customer.

### 7. **Mode of Transaction Type**
   - **Mode Transaction Type**: Identify the most frequent transaction type for each customer (e.g., debit or credit).
   - Use a **Label Encoder** to encode transaction types for numerical processing.

### 8. **Calculate the Ratios of E-commerce and Cash Transactions**
   - **E-commerce Transaction Ratio**: Calculate the ratio of e-commerce transactions to the total number of transactions for each customer.
   - **Cash Transaction Ratio**: Calculate the ratio of cash transactions to the total number of transactions for each customer.
   - Fill missing values with `0` to handle missing data in these calculations.

### 9. **Calculate the Ratios of Online**
   - **Online Transaction Ratio**: Calculate the ratio of e-commerce, EFT, EMT, and Wire transactions to the total number of transactions         for each customer.
   - No missing values because we handled it before.

### 10. **Mode of Merchant Group*
   - **Mode of Merchant Group**: Find the most common merchant group other than 'others' of a customer based on card transaction data.
   - For customers without card transactions, the group will be "No certain group'.
   - Fill the rest of the blank value with 'Other' because the only merchant group they have is 'Other'.

### 10. **Handle Missing or Special Values**
   - Fill `n/a` values with `-1` because the first-day interval could be `-1`, and filling with the mean might result in `NaN`. Therefore, missing or special values will be replaced with `-1`.
# Task1
## The Scoring System
**Rule-Based Detection of Suspicious Transaction Patterns**  


### A. Structuring Detection  
#### **Definition**  
Structuring refers to the act of splitting large transactions into smaller amounts to evade regulatory reporting thresholds (e.g., $10,000 CAD under FINTRAC 24-hour rule, in this study, we believe 48-hour is a better threshold as the 'bad actors' are all trying to avoid the 24-hour rule).  

#### **Detection Logic**  
1. **Rolling Window Analysis**:  
   - For each customer, calculate:  
     - *Total debit/credit amounts* and *frequency* over a configurable window (default: 48 hours).  
     - *Average transaction amount* per window.  
   - **Flags**:  
     - `Credit/Debit structuring`: Total amount ≥ $10,000 with average transaction < $10,000.  
     - `Mixed structuring`: Both credit and debit structuring detected.  

2. **Scoring**:  
   | Scenario                     | Points |  
   |------------------------------|--------|  
   | Credit **OR** Debit Structuring | 1      |  
   | Credit **AND** Debit Structuring | 2      |  

---

### B. Funnel Behavior Detection  
#### **Definition**  
Funnel behavior involves rapid cross-location transactions within short timeframes, indicating potential money movement across jurisdictions.  

#### **Detection Logic**  
1. **Key Metrics**:  
   - **Geographic Dispersion** (Haversine distance between consecutive transactions).  
   - **Time Compression** (Days between transactions in different locations).  
   - **Transaction Frequency** (Unique locations per time window).  

2. **Composite Index**:  

- Scores normalized to [0,1] range using percentile ranks.  

3. **Thresholds**:  

| Percentile Range | Points |  
|-------------------|--------|  
| ≥99th             | 3      |  
| 95th–99th         | 2      |  
| 90th–95th         | 1      |  

---

### C. KYC Completeness Scoring
#### **Definition** 
Missing infomation in KYC table can indicate the customer is trying to hide it's true identity.  
#### **Rules**  
| Missing Field Type          | Points per Missing Field |  
|-----------------------------|--------------------------|  
| **Every missing Information** (Industry code, location,sales, etc.) | 1                       |  
| **Max Possible**            | 5                        |  

---

### D. Outlier Scoring (Intra-Cluster)  
For each cluster, evaluate 5 metrics:  
1. Total deposits  
2. Total withdrawals  
3. Cash transaction ratio  
4. Transaction frequency  
5. Ecommerce ratio

**Thresholds**:  
- >95th percentile of cluster: +1 point  
- >99th percentile of cluster: +2 points  

---
Customer has a high score usually has the following characteristics:

1. May have many high risk transactions that need to be reported.
2. We (as bank) may not know the customer well enough.
3. May be an critical customer as they are interact with our bank more than others.

Either situation reqires more attention on the customer, we need to keep monitoring the customer or verify the customer identity.



## K-means Clutering Model

After the feature engineering process and data analysis, we carefully selected the following features for clustering:

'total_debit_amount_cad', 'transaction_frequency','avg_transaction_interval_day', 'mode_transaction_interval_day', 'avg_credit_transaction_amount', avg_debit_transaction_amount', 'structuring_points_x', 'funnel_points', 'score_missing_kyc','ecommerce_ratio', 'cash_ratio'

Using the **K-Means algorithm** with **Inertia elbow method** and **Silhouette Scores**, we can determined that the optimal number of clusters for the data sets.(Optimal number of clusters may differ with different samples as the distribution will change)

This segmentation allows us to analyze behavioral patterns within each group and derive actionable insights.
## Summary
Task 1 is providing a business view of the data. We can find the potential bad actors using the **'bad_actor'** column in the outputfile **Task1.csv**. We can also look at why each customer is a 'bad actor' using the scoring columns in the same csv file. 

# Task2
## *Customer Foundation Model* 
In addition to the k-means clustering, we also trained the *Customer Foundation Model* utilized SCARF to map client’s behavior into feature space, that is, the model will output each client's "location" based on their transaction history.

*SCARF (SELF-SUPERVISED CONTRASTIVE LEARNING USING RANDOM FEATURE CORRUPTION)* is a deep learning approach under contrastive learning domain trained to learn meaningful representations by distinguishing between similar and dissimilar data pairs
- A *similar data pair* consists of an original data point and a corrupted version of itself. Corruption means making small changes to the data altering its features in a way that may change some details but keeps it related to the original.
- A *dissimilar data pair* consists of an original data point and another data point from the dataset.

During training, the SCARF model learns to pull similar data pairs closer while pushing dissimilar pairs further apart.

## Goal
The goal is to create embedding that act like locations in real life. Speaking with the example in our use case, users with similar transaction patterns, like frequent small cash deposits, will have close embedding. In contrast, a regular shopper will be far from someone making large money transfers.
### Specific Input/Output Format
In our SCARF model, it takes engineered client records and risk scores based on their transaction history as input. The output is a 6-dimensional embedding that represents each client’s position in the feature space. The distance between two users' locations reflects how similar their transaction patterns are.
## Summary
We use Kmeans clustering to visulize the embedding locations for every customer. Then we look back to Task 1 to see where the high-scoring customers are distributed among new clusters.

If high-scoring are concentrated within certain cluster, they are the high-risk customers we need to pay more attention to. We still need to keep monitoring other high-scoring customers as well.

To understand Task 2 outputs, please refer to the **additional.csv** where it's containing the output from Task1 and the clustering results from Task 2. Then you can refer to **reults_summary.txt** to find the customer and bad actors distribution for both task. 
- *Task 1 Clusters*: Look under `Task 1 Cluster Distribution for Bad Actors`.
- *Task 2 Clusters*: See `Clutser Distribution for Bad Actors (Task 2)`.  

**Visual Analysis**: Use radar charts (e.g., `embedding_radar.png`) to compare embedding distributions of high-risk clusters.

We identify the top **two** clusters that contain the highest concentration of high-scoring customers as our target clusters. Customers within these clusters are more likely to be actual bad actors compared to both other high-scoring customers and the rest of the customer base.

# Conclusion

### Core Validation Logic
1. **Dual-Layer Consistency**  
   - **Rule-Based Filtering (Task 1)** identified high-risk customers through explicit behavioral anomalies (e.g., structuring, geographic dispersion).  
   - **Embedding Clustering (Task 2)** independently revealed spatial aggregation of these flagged users, with large proportion concentrating in **1-2 target clusters**.  
   - *Why It Matters*: This alignment proves that both explicit rules *and* latent transactional patterns contribute to risk detection.  

2. **Complementary Signal Discovery**  
   - High-risk customers exhibited **deviations in some embedding dimensions** (e.g., funds retention, transaction chain opacity) not captured by rule-based scores.  
   - Conversely, embedding clusters with concentrated high-risk users showed **3-5× higher rule violation rates** than others.  
   - *Implication*: Rules and embeddings are mutually reinforcing – one detects "known" risks, the other uncovers "hidden" patterns. 


### Methodological Advantages  

1. **Adaptive Thresholds**  
   - Rule scoring uses **percentile-based cutoffs** (e.g., top 5% of transaction frequency) instead of fixed values, ensuring relevance across datasets.  
   - Embedding analysis focuses on **relative spatial density** (e.g., cluster risk ratios) rather than absolute coordinates.  

2. **Data-Agnostic Design**  
   - Works with any transactional schema containing:  
     - Customer IDs, timestamps, amounts, and location metadata (coordinates or administrative divisions).  
     - No dependency on pre-labeled fraud data.  

### How to Interpret Results  

- If `results_summary.txt` indicates a **large proportion of high-risk users** in specific clusters from **Task 2**, follow these steps:  

  - **All High-Scoring Customers**:  
    - Refer to **`Task 1: All Mid to High Risk Customers`**.  
    - These customers require **closer attention**, as they have been flagged as **potential bad actors** based on their transaction patterns.  

  - **Customers Identified by Both Tasks**:  
    - Look under **`Task 2: High-Risk Customers`**.  
    - **Top 2 clusters** are the two clusters which contains most high-scoring customers.
    - These customers are **concentrated in the key clusters from Task 2**, meaning they exhibit **similar transaction patterns and characteristics**.  
    - They have a **higher likelihood** of being **actual bad actors** compared to other customers.  

  - **Investigation Priorities**:  
    - **Prioritize** analyzing clusters identified in **Task 2** to uncover risk patterns.  
    - Review the **embedding radar charts** to identify **dominant anomaly dimensions** and gain deeper insights from embeddings.  



### Why This Works for the Data  
1. **Defense in Depth**  
   Combines hard rules (for regulatory compliance) with latent pattern detection (for evolving threats).  

2. **Actionable Granularity**  
   - Answers *"Who is risky and why?"* in one workflow.  
   - Example: A user scoring high on structuring *and* showing embedding deviations linked to layering schemes.  

3. **Future-Proofing**  
   - Modular architecture allows seamless integration of:  
     - New rules (e.g., NFT transaction thresholds).  
     - Advanced embeddings (e.g., temporal graph networks). 



# Limitation
### 1. Limited Geographic Scope  
During the test run, we **could not connect to the Internet**, restricting access to broader location data. As a result, our **funnel analysis** was limited to **most cities in Canada and the United States**, reducing the effectiveness of location-based insights.

### 2. Model Complexity Constraints  
The **model runtime was capped at 2 hours**, requiring us to **reduce model complexity** to fit within this constraint. This limitation may have impacted overall model performance and the depth of our analysis.

### 3. Variability in Embedding Consistency  
Embeddings generated for different datasets are **not guaranteed to be identical** across runs. This is expected, as **embeddings are inherently data-dependent**, meaning variations in input data can lead to differences in the learned representation space.

### 4. Limited Data
The model is trained using unlabeled data; model performance will be more accurately accessed once we have the true label of the data.


# Next Steps(In-prograss)
## Enhance Scoring Systems
We are currently developing **Time series prediction scoring**, where we are predicting customer transaction behavior using ARIMA mdoel and compares the true behaviour with our model prediction.

| Scoring Rules | Points |  
|-------------------|--------|  
| Way Beyond CI (10 standard errors away from prediction)            | 2      |  
| Beyond 95% CI     | 1      |  
| Within 95% CI     | 0      |  

## Interactive Dashboard
We also build a dashboard using Tableau that visuallized bad actors, see link below:
 https://public.tableau.com/views/BadActor_visualization/1?:language=zhCN&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

