import streamlit as st
import re
import requests 

WEB_HOOK_API_URL = st.secrets["WEB_HOOK_URL"]
def is_valid_email(email):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email) is not None

def contact_form():
    with st.form('contact_form'):
        name = st.text_input('Name')
        email = st.text_input('Email')
        message = st.text_area('Enter Your Message')
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if not WEB_HOOK_API_URL:
                st.error('WEB_HOOK_API_URL is not set.')
                st.stop()
            if not name: 
                st.error('Please enter your name.')
                st.stop()

            if not email:
                st.error('Please enter a valid email address.')
                st.stop()

            if not is_valid_email(email):
                st.error('Please enter a valid email address.')
                st.stop()

            if not message: 
                st.error('Please enter your message.')
                st.stop()

            data = {
                'name': name, 
                'email': email,
                'message': message
            }

            response = requests.post(WEB_HOOK_API_URL, json=data)

            if response.status_code == 200:
                st.success('Message sent successfully.')


