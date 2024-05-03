import streamlit as st
from streamlit_authenticator import Authenticate
import streamlit as st


def check_credentials():
    # Hardcoded credentials for demonstration purposes
    # st.image("logo.png")
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
# def get_message_value_list(messages):
#     messages_value_list = []
#     for message in messages:
#         message_content = ""
#         print(message)
#         if not isinstance(message, MessageContentImageFile):
#             if message.content:  # Check if content is not empty
#                 message_content = message.content[0].text
#                 annotations = message_content.annotations
#                 citations = []
#                 for index, annotation in enumerate(annotations):
#                     message_content.value = message_content.value.replace(
#                         annotation.text, f" [{index}]"
#                     )
#
#                     if file_citation := getattr(annotation, "file_citation", None):
#                         cited_file = client.files.retrieve(file_citation.file_id)
#                         citations.append(
#                             f"[{index}] {file_citation.quote} from {cited_file.filename}"
#                         )
#                     elif file_path := getattr(annotation, "file_path", None):
#                         link_tag = create_file_link(
#                             annotation.text.split("/")[-1], file_path.file_id
#                         )
#                         message_content.value = re.sub(
#                             r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_content.value
#                         )
#
#                 message_content.value += "\n" + "\n".join(citations)
#                 messages_value_list.append(message_content.value)
#             else:
#                 messages_value_list.append("No content available.")
#         else:
#             image_file = client.files.retrieve(message.file_id)
#             messages_value_list.append(
#                 f"Click <here> to download {image_file.filename}"
#             )
#     return messages_value_list
