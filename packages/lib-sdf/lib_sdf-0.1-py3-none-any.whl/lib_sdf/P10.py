#10 .Data Visualization and StoryTelling
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv('P10.csv')  # Change the path to your dataset

# Check column names to ensure the expected columns exist
print(df.columns)

# Ensure 'churn' is numeric and handle any missing values
df['churn'] = pd.to_numeric(df['churn'], errors='coerce')

# Churn rate by gender (using seaborn)
if 'gender' in df.columns and 'churn' in df.columns:
    sns.countplot(data=df, x='gender', hue='churn')
    plt.title('Churn Rate by Gender')
    plt.show()

# Churn rate by age group (using plotly)
if 'age' in df.columns and 'churn' in df.columns:
    fig = px.histogram(df, x='age', color='churn', nbins=20, histnorm='percent')
    fig.update_layout(title='Churn Rate by Age Group', xaxis_title='Age', yaxis_title='% of Customers')
    fig.show()

# Churn rate by service type (using matplotlib)
if 'service_type' in df.columns and 'churn' in df.columns:
    service_churn = df.groupby('service_type')['churn'].mean()
    plt.pie(service_churn, labels=service_churn.index, autopct='%1.1f%%')
    plt.title('Churn Rate by Service Type')
    plt.show()

# Correlation matrix (using seaborn) - Now we filter only numeric columns
numeric_columns = df.select_dtypes(include=['number']).columns  # Get only numeric columns
if len(numeric_columns) > 1:  # Ensure there's more than one numeric column
    correlation_matrix = df[numeric_columns].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()

# Customer tenure vs. churn (using plotly)
if 'tenure' in df.columns and 'churn' in df.columns:
    fig = px.scatter(df, x='tenure', y='churn', color='churn')
    fig.update_layout(title='Customer Tenure vs. Churn', xaxis_title="Tenure", yaxis_title='Churn (1=Yes, 0=No)')
    fig.show()

# Customer segmentation (using plotly)
if 'feature1' in df.columns and 'feature2' in df.columns and 'cluster' in df.columns:
    fig = px.scatter(df, x='feature1', y='feature2', color='cluster')
    fig.update_layout(title='Customer Segmentation')
    fig.show()
