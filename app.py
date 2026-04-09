import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Recruitment Dashboard", layout="wide")

#  LOAD DATA 
@st.cache_data
def load_data():
    df = pd.read_csv("final_cleaned_recruitment_data.csv")
    df['Submission_Date'] = pd.to_datetime(df['Submission_Date'])
    df['Interview_Date'] = pd.to_datetime(df['Interview_Date'])
    return df

df = load_data()

st.title("📊 Recruitment Analytics Dashboard")

# SIDEBAR FILTERS 
st.sidebar.header("🔍 Filters")

source = st.sidebar.multiselect("Source", df['Source'].unique(), default=df['Source'].unique())
department = st.sidebar.multiselect("Department", df['Department'].unique(), default=df['Department'].unique())
status = st.sidebar.multiselect("Offer Status", df['Offer_Status'].unique(), default=df['Offer_Status'].unique())

# Date filter
date_range = st.sidebar.date_input("Select Date Range",
                                  [df['Submission_Date'].min(), df['Submission_Date'].max()])

# Apply filters
filtered_df = df[
    (df['Source'].isin(source)) &
    (df['Department'].isin(department)) &
    (df['Offer_Status'].isin(status)) &
    (df['Submission_Date'] >= pd.to_datetime(date_range[0])) &
    (df['Submission_Date'] <= pd.to_datetime(date_range[1]))
]

# KPIs 
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Candidates", len(filtered_df))
col2.metric("Selection Rate", f"{round((filtered_df['Offer_Status']=='Offered').mean()*100,2)}%")
col3.metric("Avg Salary (LPA)", round(filtered_df['Salary_LPA'].mean(),2))
col4.metric("Avg Experience", round(filtered_df['Experience'].mean(),2))

# ROW 1
col1, col2 = st.columns(2)

# Hiring by Source
with col1:
    st.subheader("Hiring by Source")
    fig, ax = plt.subplots()
    sns.countplot(x='Source', hue='Offer_Status', data=filtered_df, ax=ax)
    plt.xticks(rotation=30)
    st.pyplot(fig)

# Department Hiring
with col2:
    st.subheader("Hiring by Department")
    st.bar_chart(filtered_df['Department'].value_counts())

# ROW 2 
col1, col2 = st.columns(2)

# Experience vs Selection
with col1:
    st.subheader("Experience vs Selection")
    fig, ax = plt.subplots()
    sns.boxplot(x='Offer_Status', y='Experience', data=filtered_df, ax=ax)
    st.pyplot(fig)

# Salary Distribution
with col2:
    st.subheader("Salary Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Salary_LPA'], kde=True, ax=ax)
    st.pyplot(fig)

# ROW 3 

col1, col2 = st.columns(2)

# Technical Score Impact
with col1:
    st.subheader("Technical Score vs Selection")
    fig, ax = plt.subplots()
    sns.boxplot(x='Offer_Status', y='Technical_Score', data=filtered_df, ax=ax)
    st.pyplot(fig)

# Hiring Trend
with col2:
    st.subheader("Hiring Trend Over Time")
    trend = filtered_df.groupby('Submission_Date').size()
    st.line_chart(trend)

# TOP CLIENTS 
st.subheader("🏢 Top Hiring Clients")
st.dataframe(filtered_df['Client'].value_counts().head(10))

# RAW DATA 
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)

# DOWNLOAD 
st.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name='filtered_recruitment_data.csv',
    mime='text/csv'
)
