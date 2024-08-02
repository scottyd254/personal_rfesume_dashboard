import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

csv_file = 'datasets\retail_sales_dataset.csv'
@st.cache_data()
def load_data(csv_file):
    df = pd.read_csv(csv_file, index_col= 0)
    return df

df = load_data(csv_file)
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

min_age_group = df['Age'].min()-1
max_age_group = df['Age'].max()

no_bins = 6
bins = np.linspace(min_age_group, max_age_group, no_bins + 1)
age_bins = [int(bin) for bin in bins]
labels = [f'{bin[0]}-{bin[1]}' for bin in zip(age_bins, age_bins[1:])]
df['Age Group'] = pd.cut(df['Age'], bins=age_bins, labels=labels)

df['Revenue Per Unit'] = df['Total Amount'] / df['Quantity']



st.title('📈Sales Dashboard')

## -- PAGE SETUP -- ##
## -- introduction --- ##
st.markdown('---')

section = st.sidebar.radio('Go To',["Introduction", "Metrics", "Customer Insights", "Time-based Trends"])



selected_categories = st.sidebar.multiselect(
    'Select Categories',
    df['Product Category'].unique(),
    default=df['Product Category'].unique()
)

selected_gender = st.sidebar.multiselect(
    'Select Gender',
    df['Gender'].unique(),
    default=df['Gender'].unique()
)

selected_age_group = st.sidebar.multiselect(
    'Select Age Group',
    df['Age Group'].to_list(), 
    default=df['Age Group'].cat.categories.tolist()
)

if selected_categories or selected_gender or selected_age_group:
    filtered_df = df.copy()
    
    if selected_categories:
        filtered_df = filtered_df[filtered_df['Product Category'].isin(selected_categories)]
    
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]
    
    if selected_age_group:
        filtered_df = filtered_df[filtered_df['Age Group'].isin(selected_age_group)]
else:
    filtered_df = df
    
total_sales = filtered_df['Total Amount'].sum()
total_quantity_sold = filtered_df['Quantity'].sum()
average_sales = filtered_df['Total Amount'].mean()
number_of_transactions = filtered_df.shape[0]
average_order_value = total_sales / filtered_df['Customer ID'].nunique()
total_avg_revenue_per_unit = filtered_df['Revenue Per Unit'].mean()
avg_cum_sales = filtered_df['Total Amount'].sum() / number_of_transactions
avg_monthly_sales = filtered_df['Total Amount'].sum() / 12

def col_dashboard():
    col1, col2, col3 = st.columns(3, gap='small', vertical_alignment='top')
    with col1: 
        st.metric(label="Total Sales", value=f'${total_sales:,}')
        st.metric(label="Total Quantity Sold", value=f'{total_quantity_sold:,} pcs')
        st.metric(label="Average Monthly Sales", value=f'${avg_monthly_sales:,.2f}')
        
    with col2:
        st.metric(label="Average Sales", value=f'${average_sales:,.2f}')
        st.metric(label="Average Order Value", value=f'${average_order_value:,.2f}')
        st.metric(label="Average Cumulative Sales", value=f'${avg_cum_sales:,.2f}')
    with col3:
        st.metric(label="Unique Customers", value=f"{filtered_df['Customer ID'].nunique():,}")
        st.metric(label="Avg Revenue Per Unit", value=f'${total_avg_revenue_per_unit:,.2f}')
        st.metric(label="Number of Transactions", value=f"{number_of_transactions:,}")

    
def bar_chart_by_category():
    fig = px.bar(filtered_df,title="Total Sales by Category" ,x='Product Category', y='Total Amount', color='Product Category')
    return fig

def pie_chart_by_gender():
    fig = px.pie(filtered_df,title="Total Sales by Gender" ,values='Total Amount', names='Gender')
    return fig
def subplots_chart():
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Gender Distribution", "Age Distribution", "Sales by Gender and Age Group", "Top Product Categories by Gender"))

# Gender Distribution
    fig_gender_dist = px.histogram(filtered_df, x='Gender', title="Gender Distribution")
    for trace in fig_gender_dist.data:
        fig.add_trace(trace, row=1, col=1)

    # Age Distribution
    fig_age_dist = px.histogram(filtered_df, x='Age', nbins=10, title="Age Distribution")
    for trace in fig_age_dist.data:
        fig.add_trace(trace, row=1, col=2)

    # Sales by Gender and Age Group
    sales_by_gender_age = filtered_df.groupby(['Gender', 'Age Group'])['Total Amount'].sum().reset_index()
    fig_sales_by_gender_age = px.bar(sales_by_gender_age, x='Gender', y='Total Amount', color='Age Group', title="Sales by Gender and Age Group")
    for trace in fig_sales_by_gender_age.data:
        fig.add_trace(trace, row=2, col=1)

    # Top Product Categories by Gender
    top_categories_by_gender = filtered_df.groupby(['Gender', 'Product Category'])['Total Amount'].sum().reset_index()
    fig_top_categories_by_gender = px.bar(top_categories_by_gender, x='Total Amount', y='Product Category', color='Gender', orientation='h', title="Top Product Categories by Gender")
    for trace in fig_top_categories_by_gender.data:
        fig.add_trace(trace, row=2, col=2)

    # Update layout
    fig.update_layout(height=800, width=800, title_text="Customer Insights")
    return fig

def sales_by_month():
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
    filtered_df['Month'] = filtered_df['Month'].astype(str)
    sales_by_month = filtered_df.groupby('Month')['Total Amount'].sum().reset_index()
    fig_sales_over_time = px.line(sales_by_month, x='Month', y='Total Amount', title='Sales Over Time')
    return fig_sales_over_time
def sales_by_day_of_the_week():
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Day of Week'] = filtered_df['Date'].dt.day_name().sort_values(ascending=False)
    sales_by_day_of_week = filtered_df.groupby('Day of Week')['Total Amount'].sum().reset_index()
    fig_sales_by_week = px.bar(sales_by_day_of_week, x='Day of Week', y='Total Amount', title='Sales by Day of the Week')
    
    return fig_sales_by_week
def cumsum_sales_over_month():
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date']).sort_values(ascending=False)
    filtered_df['Cumulative Sales'] = filtered_df['Total Amount'].cumsum()
    cum_sales_over_time = filtered_df.groupby('Month')['Cumulative Sales'].sum().reset_index()
    fig_cumulative_sales = px.line(cum_sales_over_time, x='Month', y='Cumulative Sales', title='Cumulative Sales Over Time')
    return fig_cumulative_sales


    pass
def load_section(section):
    if section == "Introduction":
        st.markdown(
                """
                    ## About the Data
                    The dataset used in this dashboard is a dummy sales dataset sourced from Kaggle. While the data is synthetic, it closely mirrors real-world retail scenarios, enabling you to perform meaningful exploratory data analysis (EDA) and derive actionable insights. The dataset encompasses various aspects of retail sales, including:

                    - **Transaction Details**: Unique transaction IDs, dates, and customer IDs.
                    - **Customer Demographics**: Information on customer gender and age.
                    - **Product Information**: Categories of products sold and the quantity of items per transaction.
                    - **Sales Metrics**: Price per unit and total amount spent per transaction.
                """
        )
    elif section == "Metrics":
        st.markdown(
                """
                    ## Metrics           
                """
        )
        col_dashboard()
        st.markdown('---')
        

    elif section == "Customer Insights":
        st.markdown(
                """
                    ## Customer Insights
                """
        )
        col_dashboard()
        st.markdown('---')
        # bar chart of sales
        col1, col2 = st.columns(2, gap='small', vertical_alignment='top')
        with col1:
            st.plotly_chart(bar_chart_by_category())
        with col2:
            st.plotly_chart(pie_chart_by_gender())
        
        st.plotly_chart(subplots_chart())

    elif section == "Time-based Trends":
        st.markdown(
                """
                    ## Time-based Trends
                """
        )
        col_dashboard()
        st.markdown('---')
        st.plotly_chart(sales_by_month())
        st.plotly_chart(sales_by_day_of_the_week())
        st.plotly_chart(cumsum_sales_over_month())

load_section(section)


## --- key metrics --- ##

## -- col1: total sales --- ## ## -- col2: quantity sold --- ## ## -- col3: sales by category--- ##
