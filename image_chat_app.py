import streamlit as st
import tiktoken

from langchain_openai import ChatOpenAI

from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from typing import List

import os
import PyPDF2
from pdf2image import convert_from_bytes

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=st.secrets['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_PROJECT"]="KeyaSessions"
os.environ['LANGCHAIN_ENDPOINT']="https://api.smith.langchain.com"

def create_llm_message(prompt:str, messages:List):
  llm_msg=[]
  llm_msg.append(SystemMessage(content=prompt))

  for msg in messages:
    if msg["role"]=="user":
        llm_msg.append(HumanMessage(content=msg['content']))
    if msg["role"]=="assistant":
        llm_msg.append(AIMessage(content=msg['content']))
    if msg["role"]=="system":
        llm_msg.append(SystemMessage(content=msg['content']))
  return llm_msg

def pdf_text(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text_content = []

    # Extract text from each page
    for page in pdf_reader.pages:
        text_content.append(page.extract_text())

    # Join all the text content into a single string
    full_text = "\n\n".join(text_content)

    return full_text

from pdf2image import convert_from_bytes

def pdf_images(uploaded_file):
    images = convert_from_bytes(uploaded_file.read(), dpi=300)
    buffered = io.BytesIO()
    image=images[0]
    image.save(buffered, format="PNG")
    b64= base64.b64encode(buffered.getvalue()).decode()

    print(f"B^4 is: {b64=}")

    return full_text

SYSTEM_PROMPT=f"""
You are a helpful and thoughtful doctor and nutrition coach for patients with IBD.
Keep your responses concise - ideally one paragraph with two-three sentences.
"""

avatars={"system":"💻🧠","user":"🧑‍💼","assistant":"🎓"}
model = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key = st.secrets['OPENAI_API_KEY'])
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["visible"]:
        avatar=avatars[message["role"]]
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
        
prompt = st.chat_input("How can I help you?")
prompt_add=None
uploaded_file = st.file_uploader("Upload PDF", accept_multiple_files=False)
if uploaded_file:
    file_contents=pdf_images(uploaded_file)
    st.write(f"Uploaded file {uploaded_file.name}")
    file_content=pdf_images(uploaded_file)
    prompt_add=f"User uploaded the following PDF: {file_content}"
if prompt or prompt_add:
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt, "visible": True})
        with st.chat_message("user"):
            st.markdown(prompt)
    if prompt_add:
        st.session_state.messages.append({"role": "user", "content": prompt_add, "visible": False})
    llm_msg=create_llm_message(SYSTEM_PROMPT,st.session_state.messages)

    with st.chat_message("assistant", avatar=avatars["assistant"]):
        response=model.invoke(llm_msg)
        full_response=response.content
        st.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response, "visible": True})

