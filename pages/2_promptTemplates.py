import openai
import streamlit as st
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
from langchain.schema import BaseOutputParser
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
    
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


with st.expander("Format Prompt"):
    prompt=st.text_input("Prompt","What is a good name for a company that makes {variable}?")
    variable=st.text_input("variable","colorful socks")
    final_prompt=prompt.format(variable=variable)
    st.write(final_prompt)

with st.expander("Prompt Templates"):
    st.code("""from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
template = "You are a helpful assistant that translates {input_language} to {output_language}."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chat_prompt.format_messages(input_language="English", output_language="French", text="I love programming.")""",language="python")
    template="You are a helpful assistant that translates {input_language} to {output_language}."
    st.info(template)
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    c1,c2,c3 = st.columns([1,1,1])
    from_lang=c1.text_input("Input Language","English")
    to_lang=c2.text_input("Output Language","French")
    text=c3.text_input("Text to Translate","I Love Programming.")
    chat_response=chat_prompt.format_messages(input_language=from_lang, output_language=to_lang, text=text)
    st.info(chat_response)

with st.expander("Output Parsers"):
    st.code('''from langchain.schema import BaseOutputParser
class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")
    CommaSeparatedListOutputParser().parse("hi, bye")''')
            
    text=st.text_input("Comma separated Input Text to parse:","He is a good man, but, he is getting in to, bad, hands.")
    parsed_text=CommaSeparatedListOutputParser().parse(text)
    st.code(parsed_text)

with st.expander("LLM Chain"):
    template = st.text_area("System Message Template","""You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more.""")
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(
        llm=ChatOpenAI(),
        prompt=chat_prompt,
        output_parser=CommaSeparatedListOutputParser()
    )
    st.info(template)
    input_prompt=st.text_input("Series Data like colors","Months")
    response=chain.run(input_prompt)
    st.write(response)
    