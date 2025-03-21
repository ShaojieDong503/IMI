# -*- coding: utf-8 -*-
"""Advance_Clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1yICmOiUjH0tF_AZ6OLsKscSUTueNHUXr
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import plotly.express as px

import os
from pathlib import Path

input_dir = os.getenv('INPUT_DIR', '/mnt/data') 
output_dir = os.getenv('OUTPUT_DIR', '/mnt/output') 
output_image = os.getenv('OUTPUT_DIR', '/mnt/output/task2')
output_cus_image = os.getenv('OUTPUT_DIR', '/mnt/output/task2/high_risk_customers')
task1_output_dir = os.getenv(output_dir, '/mnt/output/task1')
interim_dir = os.path.join(output_dir, 'interim')
task2_output_path = os.path.join(interim_dir, 'customer_embeddings.csv')
task1_output_path= os.path.join(task1_output_dir, 'task1.csv')


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
ensure_dir(output_image)
ensure_dir(output_cus_image)

df = pd.read_csv(task2_output_path)
df.head()

# Check correlation for all the

X = df.drop(columns=['customer_id'])
correlation_matrix = X.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Correlation Matrix Heatmap', fontsize=16)

plt.show()

# Drop features with high correlation
def remove_high_correlation(df, threshold=0.85):
    corr_matrix = df.corr().abs()
    drop_cols = set()

    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if corr_matrix.iloc[i, j] > threshold:
                col_i = corr_matrix.columns[i]
                col_j = corr_matrix.columns[j]
                
                if corr_matrix[col_i].mean() < corr_matrix[col_j].mean():
                    drop_cols.add(col_j)
                else:
                    drop_cols.add(col_i)

    return df.drop(columns=drop_cols), drop_cols

X_filtered, dropped_cols = remove_high_correlation(X, threshold=0.6)

correlation_matrix = X_filtered.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Correlation Matrix Heatmap', fontsize=16)

# Use all feature after remove high-correlated ones
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_filtered)
df_scaled = pd.DataFrame(X_scaled, columns=X_filtered.columns)

# Build K-means Clustering using Elbow Method and Silhouette Method
silhouette_scores = []
k_range = range(2, 6)


inertia = []
silhouette_scores = []

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(df_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(df_scaled, clusters))


plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(k_range, inertia, marker='o', linestyle='--', color='blue')
plt.xticks(k_range)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal Clusters')


plt.subplot(1, 2, 2)
plt.plot(k_range, silhouette_scores, marker='o', linestyle='--', color='green')
plt.xticks(k_range)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Method for Optimal Clusters')

plt.tight_layout()
output_path = os.path.join(output_image, 'Elbow_and_Silhouette.png')  
plt.savefig(output_path, dpi=300, bbox_inches='tight')  
plt.close()


# Use the Best K for the model
chosen_k = k_range[np.argmax(silhouette_scores)]
print(chosen_k)

kmeans = KMeans(n_clusters=chosen_k , random_state=71)
clusters = kmeans.fit_predict(df_scaled)
X['cluster'] = clusters
df['cluster'] = clusters

def plot_radar_chart(cluster_means, features):
    n_features = len(features)
    angles = np.linspace(0, 2 * np.pi, n_features, endpoint=False).tolist()
    angles += angles[:1] 

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})

    for idx, (cluster, row) in enumerate(cluster_means.iterrows()):
        values = row[features].tolist()
        values += values[:1]  
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=f'Cluster {cluster}')
        ax.fill(angles, values, alpha=0.1)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), features)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.show()
    img1_output_path = os.path.join(output_image, 'Embedding_radar.png')
    plt.savefig(img1_output_path, dpi=300, bbox_inches='tight')



cluster_means = X.groupby('cluster').mean()
key_features = list(X.columns)[:-1]
plot_radar_chart(cluster_means, key_features)


task2_output_path_2 = os.path.join(output_image, 'embedding_clustering.csv')
df.to_csv(task2_output_path_2,index=False)


# Compare the clusters with task 1 results
df_task1 = pd.read_csv(task1_output_path)
df_task1['Cluster_2'] = clusters

# Create an interactive scatter plot for avg_debit_transaction_amount
fig = px.scatter(
    df_task1,
    x='Cluster_2',
    y='avg_debit_transaction_amount',
    color='Cluster_2',  # Color points by their cluster,
    title='Interactive K-Means Clustering Visualization',
)
fig.update_xaxes(
    tickmode='array',
    tickvals=sorted(df['cluster'].unique()),  
    ticktext=sorted(df['cluster'].unique())   
)
# Save the plot
img2_output_path = os.path.join(output_image, 'Avg_debit_amount.png')
fig.write_image(img2_output_path) 
fig.show()

# Create a stacked bar plot for the funnel points by cluster
fig = px.histogram(
    df_task1,
    x='Cluster_2',
    y='funnel_points',
    color='Cluster_2'  # Color bars by their cluster
)

# Show the plot
fig.show()
img2_output_path = os.path.join(output_image, 'Funnel_points.png')
fig.write_image(img2_output_path) 

# Create a grouped bar plot for the average funnel and structuring points by cluster
df_agg = df_task1.groupby('Cluster_2')[['funnel_points', 'structuring_points_x']].mean().reset_index()

# Long Format
df_long = df_agg.melt(
    id_vars='Cluster_2',
    value_vars=['funnel_points', 'structuring_points_x'],
    var_name='metric',
    value_name='score'
)

# create a grouped bar plot
fig = px.bar(
    df_long,
    x='Cluster_2',
    y='score',
    color='metric',          # color using metric
    barmode='group',         # group bars
    title='Cluster Metrics Comparison',
    labels={'score': 'Average Score', 'cluster': 'Cluster'},
    color_discrete_map={
        'funnel_points': 'red',      # color for funnel_points
        'structuring_points_x': 'blue'
    }
)

# optimize the layout
fig.update_layout(
    xaxis={'type': 'category'},          
    legend_title='Metric Type',
    hovermode='x unified'
)

fig.show()
img2_output_path = os.path.join(output_image, 'comparison_points.png')
fig.write_image(img2_output_path) 


# Clutsers and cash ratio
fig = px.histogram(
    df_task1,
    x='Cluster_2',
    y='cash_ratio',
    color='Cluster_2'  # Color bars by their cluster
)
fig.show()
img2_output_path = os.path.join(output_image, 'cash_ratio.png')
fig.write_image(img2_output_path) 

# Cluster and Ecommerce ratio
fig = px.histogram(
    df_task1,
    x='Cluster_2',
    y='ecommerce_ratio',
    color='Cluster_2'  # Color bars by their cluster
)
fig.show()
img2_output_path = os.path.join(output_image, 'ecommerce_ratio.png')
fig.write_image(img2_output_path) 

# Create the output summary
task1_high_risk = df_task1[df_task1["bad_actor"]][["customer_id", "cluster"]]
task1_ids = task1_high_risk["customer_id"].tolist()
task2_cluster_counts = df_task1[df_task1["bad_actor"]]["Cluster_2"].value_counts()
top_clusters_task2 = task2_cluster_counts.head(2).index.tolist() 


task2_high_risk_ids = []
for cluster in top_clusters_task2:
    ids = df_task1[
        (df_task1["Cluster_2"] == cluster) & 
        (df_task1["bad_actor"])
    ]["customer_id"].tolist()
    task2_high_risk_ids.extend(ids)


output = [
    "=== Task 1: Total Bad Actor Distribution ===",
    str(df_task1['bad_actor'].value_counts()),
    "\n=== Task 1 Cluster Distribution for Bad Actors ===",
    str(df_task1.loc[df_task1["bad_actor"]]['cluster'].value_counts()),
    "\n=== Overall Cluster Distribution (Task 1) ===",
    str(df_task1['cluster'].value_counts()),
    "\n=== Cluster Distribution for Bad Actors (Task 2) ===",
    str(df_task1.loc[df_task1["bad_actor"]]['Cluster_2'].value_counts()),
    "\n=== Overall Cluster Distribution (Task2) ===",
    str(df_task1['Cluster_2'].value_counts()),
    "\n=== Task 1: All Mid to High Risk Customers ===",
    f"Total: {len(task1_ids)} customers",
    "\n".join(task1_ids),
    "\n\n=== Task 2: High-Risk Customers ===",
    f"Target Clusters: {top_clusters_task2}",
    f"Total: {len(task2_high_risk_ids)} customers",
    "\n".join(task2_high_risk_ids)
]

# save the path
task2_output_path_2 = os.path.join(output_image, 'reults_summary.txt')

# write the output to a file
with open(task2_output_path_2, 'w') as f:
    f.write("\n".join(output))


#Print out which cluster has the most bad actors
print(df_task1.loc[(df_task1["bad_actor"] == True)]['Cluster_2'].value_counts())
print(df_task1['Cluster_2'].value_counts())
print(df_task1.loc[(df_task1["bad_actor"] == True)]['cluster'].value_counts())
print(df_task1['cluster'].value_counts())
print(df_task1['bad_actor'].value_counts())


df_task1['high_risk_level'] = 0
df_task1['mid_risk_level'] = 0
df_task1['low_risk_level'] = 0

# mark high risk
assert all(cid in task1_ids for cid in task2_high_risk_ids), "ERROR: There is task1_ids not in task2_high_risk_ids"
df_task1.loc[df_task1['customer_id'].isin(task2_high_risk_ids), 'high_risk_level'] = 1

# mark mid risk
mid_risk_ids = list(set(task1_ids) - set(task2_high_risk_ids))
df_task1.loc[df_task1['customer_id'].isin(mid_risk_ids), 'mid_risk_level'] = 1

# mark low risk
df_task1['low_risk_level'] = (
    (df_task1['high_risk_level'] == 0) & 
    (df_task1['mid_risk_level'] == 0)
).astype(int)


#Save the additional output
task2_output_path_2 = os.path.join(output_image, 'addtional.csv')
df_task1.to_csv(task2_output_path_2,index=False)




# Save transaction timeseries plot for high risk customers
new_abm_table_path = os.path.join(interim_dir, 'new_abm.csv')
new_card_table_path = os.path.join(interim_dir, 'new_card.csv')
new_cheque_table_path = os.path.join(interim_dir, 'new_cheque.csv')
new_eft_table_path = os.path.join(interim_dir, 'new_eft.csv')
new_emt_table_path = os.path.join(interim_dir, 'new_emt.csv')
new_wire_table_path = os.path.join(interim_dir, 'new_wire.csv')
df_abm = pd.read_csv(new_abm_table_path)
df_card = pd.read_csv(new_card_table_path)
df_cheque = pd.read_csv(new_cheque_table_path)
df_eft = pd.read_csv(new_eft_table_path)
df_emt = pd.read_csv(new_emt_table_path)
df_wire = pd.read_csv(new_wire_table_path)

required_columns = [
    'customer_id',
    'amount_cad',
    'debit_credit',
    'transaction_date'
]
table_names = ['df_wire', 'df_emt', 'df_eft', 'df_cheque', 'df_card', 'df_abm']
for cust_id in task1_ids:
    all_transactions = []
    for table in table_names:
        df = globals().get(table,pd.DataFrame())
        if not df.empty:
            filtered = df.loc[df['customer_id']==cust_id,required_columns].copy()
            filtered['source_table'] = table
            all_transactions.append(filtered)
    combined = pd.concat(all_transactions,axis=0)
    combined['transaction_date'] = pd.to_datetime(combined['transaction_date'])
    combined = combined.sort_values('transaction_date').reset_index(drop=True)
    df_credit = combined[combined['debit_credit']=='credit']
    df_debit = combined[combined['debit_credit']=='debit']

    plt.figure(figsize=(10, 6))
    plt.plot(df_credit['transaction_date'], df_credit['amount_cad'], color='blue', label='Credit')
    plt.plot(df_debit['transaction_date'], df_debit['amount_cad'], color='red', label='Debit')
    plt.ticklabel_format(style='plain', axis='y')
    # Customize labels and title
    plt.xlabel('Date')
    plt.ylabel('Transaction Amount (CAD)')
    plt.title(f'Transaction Time Series for Customer {cust_id}')
    plt.legend()
    output_path = os.path.join(output_cus_image, f"{cust_id}.png")
    plt.savefig(output_path)
    plt.close()