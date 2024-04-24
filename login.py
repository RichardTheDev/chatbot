import streamlit as st
from streamlit_authenticator import Authenticate
import streamlit as st


def check_credentials():
    # Hardcoded credentials for demonstration purposes
    st.image("logo.png")
    PASSWORD = st.secrets["password"]
    credentials = {
        'usernames': {
            'admin': {
                'name': 'Admin User',
                'password': PASSWORD,  # Hashing 'admin' password
                'email': 'admin@example.com',
            }
        }
    }

    # Instantiate the Authenticate class
    auth = Authenticate(credentials, cookie_name='auth', key='secret_key')

    # Define a function to create the login form
    # Use the login method from the Authenticate class
    name, authentication_status, username = auth.login(location='main')

    # Check if login was successful
    if authentication_status:
        return True
        # Additional logic here for authenticated users
    elif authentication_status == False:
        st.error('Mot de passe incorrect')
        return False
    # For no input, do not display any message

    # Call the login form function to display the form
# import streamlit as st
# from streamlit_authenticator import Authenticate
#
# def check_credentials():
#     # Hardcoded credentials for demonstration purposes
#     # In a real app, ensure you have secure handling for passwords, possibly using hashing
#     st.image("logo.svg")  # Displaying an image
#
#     # Setting up users and hashed passwords
#     usernames = ["admin"]
#     names = ["Admin User"]
#     passwords = ["password"]  # This should be a hashed password in a real scenario
#
#     # Creating a dictionary for the authenticator
#     hashed_passwords  = st.secrets["password"]
#     authenticator = Authenticate(names, usernames, hashed_passwords, 'some_cookie_name', 'some_signature_key',30)
#
#     # Displaying the login form and handling authentication
#     name, authentication_status, username = authenticator.login('Login', 'main')
#
#     if authentication_status:
#         st.success(f'Welcome {name}!')
#         return True
#     elif authentication_status == False:
#         st.error('Username/password is incorrect')
#         return False
#     elif authentication_status == None:
#         st.warning('Please enter your username and password')
#
#     return False
#
# # Example usage
# if check_credentials():
#     st.write("Authenticated content here")
# else:
#     st.write("Please login to see the content")
