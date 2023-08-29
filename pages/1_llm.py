import openai
import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

st.header('A Prompt Engineering Playground form :blue[Pratyush Ranjan Mishra] :sunglasses:')
with st.sidebar:
    st.title('🤖💬 Prompt Practice Bot :flag-in:')
    temp = st.slider('Acuracy temperature 0 being more acurate and 1 being more creative', 0.0, 1.0, 0.7)
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

st.header('A Prompt Engineering Playground form :blue[Pratyush Ranjan Mishra] :sunglasses:')
llm = OpenAI()
chat_model = ChatOpenAI()

llm_text=st.text_input("LLM","Hi")
if st.button("Process as LLM Prompt"):
    st.info(llm.predict(llm_text))
    messages = [HumanMessage(content=llm_text)]
    st.info(llm.predict_messages(messages))

chat_text=st.text_input("Chat Model","Hi")
if st.button("Process as chat model"):
    st.info(chat_model.predict(chat_text))
    messages = [HumanMessage(content=chat_text)]
    st.info(chat_model.predict_messages(messages))

