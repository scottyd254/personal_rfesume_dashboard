import streamlit as st 


# PAGE SETUP

def load_social_links(file_path):
    with open(file_path, 'r') as f:
        return f.read()
component = load_social_links('assets/socials.html')

about_me = st.Page(
    page='views/about_me.py',
    title='About Me',
    icon=':material/account_circle:',
    default=True
)

population_metrics_dashboard_page = st.Page(
    page='views/population_metrics_dashboard.py',
    title='Population Metrics Dashboard',
    icon=':material/insights:',
    default=False
)

sales_dashboard_page = st.Page(
    page='views/sales_dashboard.py',
    title='Sales Dashboard',
    icon=':material/monetization_on:',
    default=False
)

image_to_text = st.Page(
    page = 'views/image_to_txt.py',
    title = 'Text Extraction from Image File Using Tesseract OCR and Google Gemini AI',
    icon = ':material/monetization_on:',
    default = False
)
pg = st.navigation(
   {
       'About Me': [about_me],
       'Projects': [population_metrics_dashboard_page, sales_dashboard_page, image_to_text],
   }
        )
st.logo('assets/logo1.png', link='https://github.com/scotty_254')
st.sidebar.write('By scotty_254')
st.components.v1.html(component)

pg.run()