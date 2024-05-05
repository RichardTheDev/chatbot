# import os
# import time
# import base64
# import re
# import json
# from login import check_credentials
# import streamlit as st
# import openai
# from openai.types.beta.threads import MessageContentImageFile
# from tools import TOOL_MAP
#
#
#
# openai_api_key = st.secrets["openaikey"]
# client = None
# client = openai.OpenAI(api_key=openai_api_key)
# assistant_id = st.secrets["assistant_id"]
# instructions = ""
# assistant_title = "Lindsay Goldberg Chatbot DEMO"
# enabled_file_upload_message =""
#
#
# def create_thread(content, file):
#     messages = [
#         {
#             "role": "user",
#             "content": content,
#         }
#     ]
#     if file is not None:
#         messages[0].update({"file_ids": [file.id]})
#     thread = client.beta.threads.create(messages=messages)
#     return thread
#
#
# def create_message(thread, content, file):
#     file_ids = []
#     if file is not None:
#         file_ids.append(file.id)
#     client.beta.threads.messages.create(
#         thread_id=thread.id, role="user", content=content, file_ids=file_ids
#     )
#
#
# def create_run(thread):
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id, assistant_id=assistant_id, instructions=instructions
#     )
#     return run
#
#
# def create_file_link(file_name, file_id):
#     content = client.files.content(file_id)
#     content_type = content.response.headers["content-type"]
#     b64 = base64.b64encode(content.text.encode(content.encoding)).decode()
#     link_tag = f'<a href="data:{content_type};base64,{b64}" download="{file_name}">Download Link</a>'
#     return link_tag
#
#
# # def get_message_value_list(messages):
# #     messages_value_list = []
# #     for message in messages:
# #         message_content = ""
# #         print(message)
# #         if not isinstance(message, MessageContentImageFile):
# #             if message.content:
# #                 message_content = message.content[0].text
# #                 annotations = message_content.annotations
# #             else:
# #                 st.error("No value ", message)
# #         else:
# #             image_file = client.files.retrieve(message.file_id)
# #             messages_value_list.append(
# #                 f"Click <here> to download {image_file.filename}"
# #             )
# #         citations = []
# #         for index, annotation in enumerate(annotations):
# #             message_content.value = message_content.value.replace(
# #                 annotation.text, f" [{index}]"
# #             )
# #
# #             if file_citation := getattr(annotation, "file_citation", None):
# #                 cited_file = client.files.retrieve(file_citation.file_id)
# #                 citations.append(
# #                     f"[{index}] {file_citation.quote} from {cited_file.filename}"
# #                 )
# #             elif file_path := getattr(annotation, "file_path", None):
# #                 link_tag = create_file_link(
# #                     annotation.text.split("/")[-1], file_path.file_id
# #                 )
# #                 message_content.value = re.sub(
# #                     r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_content.value
# #                 )
# #
# #         message_content.value += "\n" + "\n".join(citations)
# #         messages_value_list.append(message_content.value)
# #         print(messages_value_list)
# #         return messages_value_list
# def get_message_value_list(messages):
#     messages_value_list = []
#     for message in messages:
#         message_content = ""
#         print(message)
#         if not isinstance(message, MessageContentImageFile):
#             if message.content:
#                 message_content = message.content[0].text
#                 annotations = message_content.annotations
#             else:
#                 # Corrected usage of st.error to properly format the message
#                 st.error(f"No value for message: {message}")
#         else:
#             image_file = client.files.retrieve(message.file_id)
#             messages_value_list.append(
#                 f"Click <here> to download {image_file.filename}"
#             )
#         citations = []
#         for index, annotation in enumerate(annotations):
#             message_content.value = message_content.value.replace(
#                 annotation.text, f" [{index}]"
#             )
#
#             if file_citation := getattr(annotation, "file_citation", None):
#                 cited_file = client.files.retrieve(file_citation.file_id)
#                 citations.append(
#                     f"[{index}] {file_citation.quote} from {cited_file.filename}"
#                 )
#             elif file_path := getattr(annotation, "file_path", None):
#                 link_tag = create_file_link(
#                     annotation.text.split("/")[-1], file_path.file_id
#                 )
#                 message_content.value = re.sub(
#                     r"\[(.*?)\]\s*\(\s*(.*?)\s*\)", link_tag, message_content.value
#                 )
#
#         message_content.value += "\n" + "\n".join(citations)
#         messages_value_list.append(message_content.value)
#     return messages_value_list[:1]
#
#
# def get_message_list(thread, run):
#     completed = False
#     while not completed:
#         run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#         print("run.status:", run.status)
#         messages = client.beta.threads.messages.list(thread_id=thread.id)
#         print("messages:", "\n".join(get_message_value_list(messages)))
#         if run.status == "completed":
#             completed = True
#         elif run.status == "failed":
#             break
#         else:
#             time.sleep(1)
#
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     return get_message_value_list(messages)
#
#
# def get_response(user_input, file):
#     if "thread" not in st.session_state:
#         st.session_state.thread = create_thread(user_input, file)
#     else:
#         create_message(st.session_state.thread, user_input, file)
#     run = create_run(st.session_state.thread)
#     run = client.beta.threads.runs.retrieve(
#         thread_id=st.session_state.thread.id, run_id=run.id
#     )
#
#     while run.status == "in_progress":
#         print("run.status:", run.status)
#
#         time.sleep(1)
#         run = client.beta.threads.runs.retrieve(
#             thread_id=st.session_state.thread.id, run_id=run.id
#         )
#         run_steps = client.beta.threads.runs.steps.list(
#             thread_id=st.session_state.thread.id, run_id=run.id
#         )
#         print("run_steps:", run_steps)
#         for step in run_steps.data:
#             if hasattr(step.step_details, "tool_calls"):
#                 for tool_call in step.step_details.tool_calls:
#                     if (
#                         hasattr(tool_call, "code_interpreter")
#                         and tool_call.code_interpreter.input != ""
#                     ):
#                         input_code = f"### code interpreter\ninput:\n```python\n{tool_call.code_interpreter.input}\n```"
#                         print(input_code)
#                         if (
#                             len(st.session_state.tool_calls) == 0
#                             or tool_call.id not in [x.id for x in st.session_state.tool_calls]
#                         ):
#                             st.session_state.tool_calls.append(tool_call)
#                             with st.chat_message("Assistant"):
#                                 st.markdown(
#                                     input_code,
#                                     True,
#                                 )
#                                 st.session_state.chat_log.append(
#                                     {
#                                         "name": "assistant",
#                                         "msg": input_code,
#                                     }
#                                 )
#
#     if run.status == "requires_action":
#         print("run.status:", run.status)
#         run = execute_action(run, st.session_state.thread)
#
#     return "\n".join(get_message_list(st.session_state.thread, run))
#
#
# def execute_action(run, thread):
#     tool_outputs = []
#     for tool_call in run.required_action.submit_tool_outputs.tool_calls:
#         tool_id = tool_call.id
#         tool_function_name = tool_call.function.name
#         print(tool_call.function.arguments)
#
#         tool_function_arguments = json.loads(tool_call.function.arguments)
#
#         print("id:", tool_id)
#         print("name:", tool_function_name)
#         print("arguments:", tool_function_arguments)
#
#         tool_function_output = TOOL_MAP[tool_function_name](**tool_function_arguments)
#         print("tool_function_output", tool_function_output)
#         tool_outputs.append({"tool_call_id": tool_id, "output": tool_function_output})
#
#     run = client.beta.threads.runs.submit_tool_outputs(
#         thread_id=thread.id,
#         run_id=run.id,
#         tool_outputs=tool_outputs,
#     )
#     return run
#
#
# def handle_uploaded_file(uploaded_file):
#     file = client.files.create(file=uploaded_file, purpose="assistants")
#     return file
#
#
# def render_chat():
#     for chat in st.session_state.chat_log:
#         with st.chat_message(chat["name"]):
#             st.markdown(chat["msg"], True)
#
#
# if "tool_call" not in st.session_state:
#     st.session_state.tool_calls = []
#
# if "chat_log" not in st.session_state:
#     st.session_state.chat_log = []
#
# if "in_progress" not in st.session_state:
#     st.session_state.in_progress = False
#
#
# def disable_form():
#     st.session_state.in_progress = True
#
#
# def main():
#     st.title(assistant_title)
#     st.markdown("[by Updev Solutions](https://updev-solutions.com)", unsafe_allow_html=True)
#     # st.info("This assistant is designed to help you provide accurate and diplomatic responses to misinformed comments on social media regarding the Israeli-Palestinian conflict. Simply paste the comment into the chatbot, and it will offer you an informed and measured reply, based on facts from the PDF documents provided, to enlighten the discussion.")
#     user_msg = st.chat_input(
#         "Message", on_submit=disable_form, disabled=st.session_state.in_progress
#     )
#     if True:
#         uploaded_file = st.sidebar.file_uploader(
#             enabled_file_upload_message,
#             type=[
#                 "txt",
#                 "pdf",
#                 "png",
#                 "jpg",
#                 "jpeg",
#                 "csv",
#                 "json",
#                 "geojson",
#                 "xlsx",
#                 "xls",
#             ],
#             disabled=st.session_state.in_progress,
#         )
#     else:
#         uploaded_file = None
#     if user_msg:
#         render_chat()
#         with st.chat_message("user"):
#             st.markdown(user_msg, True)
#         st.session_state.chat_log.append({"name": "user", "msg": user_msg})
#         file = None
#         if uploaded_file is not None:
#             file = handle_uploaded_file(uploaded_file)
#         with st.spinner("Wait for response..."):
#             response = get_response(user_msg, file)
#         with st.chat_message("Assistant"):
#             st.markdown(response, True)
#
#         st.session_state.chat_log.append({"name": "assistant", "msg": response})
#         st.session_state.in_progress = False
#         st.session_state.tool_call = None
#         st.rerun()
#     render_chat()
#
#
#
#
# if __name__ == '__main__':
#     st.markdown("""
#                 <style>
#                 .stActionButton {visibility: hidden;}
#                 /* Hide the Streamlit footer */
#                 .reportview-container .main footer {visibility: hidden;}
#                 /* Additionally, hide Streamlit's hamburger menu - optional */
#                 .sidebar .sidebar-content {visibility: hidden;}
#                 </style>
#                 """, unsafe_allow_html=True)
#     isAuth = check_credentials()
#     if isAuth:
#         main()
import streamlit as st
from assistantOpenAi import *
import time

def process_run(st, thread_id, assistant_id):
    # Run the Assistant
    run_id = runAssistant(thread_id, assistant_id)
    status = 'running'

    # Check Status Session
    while status != 'completed':
        with st.spinner('Waiting for assistant response . . .'):
            time.sleep(20)  # 20-second delay
            status = checkRunStatus(thread_id, run_id)

    # Retrieve the Thread Messages
    thread_messages = retrieveThread(thread_id)
    for message in thread_messages:
        if message['role'] == 'user':
            st.write('User Message:', message['content'])
        else:
            st.write('Assistant Response:', message['content'])

def main():
    st.title("Lindsay Goldberg Chatbot DEMO")
    st.markdown("[by Updev Solutions](https://updev-solutions.com)", unsafe_allow_html=True)
    """
    It's your personal AI Assistant. I create file_search assistants, just upload your knowledge base and start chatting to your documents.
    """

    if 'assistant_initialized' not in st.session_state:
        # Input field for the title
        title = "Finance Chatbot"

        # File uploader widget
        uploaded_files = st.file_uploader("Upload Files for the Assistant", accept_multiple_files=True, key="uploader")
        file_locations = []
        initiation = st.text_input("Enter the assistant's first question", key="initiation")

        if uploaded_files and title and initiation:
            for uploaded_file in uploaded_files:
                # Read file as bytes
                bytes_data = uploaded_file.getvalue()
                location = f"temp_file_{uploaded_file.name}"
                # Save each file with a unique name
                with open(location, "wb") as f:
                    f.write(bytes_data)
                file_locations.append(location)
                # st.success(f'File {uploaded_file.name} has been uploaded successfully.')

            # Upload file and create assistant
            with st.spinner('Processing your file and setting up the assistant...'):
                file_ids = [saveFileOpenAI(location) for location in file_locations]
                assistant_id, vector_id = createAssistant(file_ids, title)

            # Start the Thread
            thread_id = startAssistantThread(initiation, vector_id)

            # Save state
            st.session_state.thread_id = thread_id
            st.session_state.assistant_id = assistant_id
            st.session_state.last_message = initiation
            st.session_state.assistant_initialized = True

            st.write("Assistant ID:", assistant_id)
            st.write("Vector ID:", vector_id)
            st.write("Thread ID:", thread_id)

            process_run(st, thread_id, assistant_id)

    # Handling follow-up questions only if assistant is initialized
    if 'assistant_initialized' in st.session_state and st.session_state.assistant_initialized:
        follow_up = st.text_input("Enter your follow-up question", key="follow_up")
        submit_button = st.button("Submit Follow-up")

        if submit_button and follow_up and follow_up != st.session_state.last_message:
            st.session_state.last_message = follow_up
            addMessageToThread(st.session_state.thread_id, follow_up)
            process_run(st, st.session_state.thread_id, st.session_state.assistant_id)

if __name__ == "__main__":
    main()