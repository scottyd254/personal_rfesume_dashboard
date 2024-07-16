import streamlit as st 
from forms.contact import contact_form
# HEADER SECTION 

col1, col2 = st.columns(2, gap='small', vertical_alignment='center')

@st.experimental_dialog('Contact Me', width="small")
def show_contact_form():
    contact_form()

with col1: 
    st.image('assets/profile_pic.png', width=200)

with col2: 
    st.title('About Me')
    st.write(
    "I'm a data analyst and Python developer. I'm passionate about data science and machine learning."
    )
    
    if st.button('Get In Touch'):
        show_contact_form()

st.write('\n')

st.subheader('👨‍💻 Skills', divider=True)

st.write(
    """
        - Programming Languages: Python, SQL, R, Excel, Excel VBA, PowerBI, Chartjs
        - Data Science: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
        - Web Development: HTML, CSS, JavaScript, Bootstrap, Streamlit
        - Git: Git, Github
        - Machine Learning: Scikit-learn, TensorFlow, Keras
        - Big Data: Hadoop, Hive, Spark, PySpark, Apache Airflow, Airflow DAG
        - Back-End: Flask, Django, FastAPI
    """
)

st.write('\n')

st.subheader('👨‍🎓 Business Knowledge', divider=True)

st.write(
    """
        - Accounting Programs: Office 365, Google Workspace, QuickBooks, Sage Accounting, Sage 50
        - Financial Statements: Accounts Payable, Accounts Receivable, Bank Reconciliation, Financial Statements
        - Tax Preparation: Tax Returns, Tax Preparation
        - Budgeting: Budgeting, Forecasting
    """
)