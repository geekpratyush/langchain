import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

get_completion("What is 1+1?")

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


chat = ChatOpenAI(temperature=0.0, model=llm_model)
template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""            
st.info(template_string)
prompt_template = ChatPromptTemplate.from_template(template_string)
st.info(prompt_template.messages[0].prompt)

st.code(prompt_template.messages[0].prompt.input_variables)

customer_style = """American English \
in a calm and respectful tone
"""
customer_style=st.text_area("Customer Style",customer_style)

customer_email = """Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!"""
customer_email=st.text_area("Customer Email",customer_email)
customer_messages = prompt_template.format_messages(
                    style=customer_style,
                    text=customer_email)

if st.button("Process"):
    with st.expander("Expand Customer Message Type"):
        st.write(type(customer_messages))
    with st.expander("Expand Customer Message content Type"):        
        st.write(type(customer_messages[0]))
    st.write(customer_messages[0])

if st.button("Process Customer message"):
        customer_response = chat(customer_messages)
        st.write(customer_response.content)

service_reply = """Hey there customer, \
the warranty does not cover \
cleaning expenses for your kitchen \
because it's your fault that \
you misused your blender \
by forgetting to put the lid on before \
starting the blender. \
Tough luck! See ya!
"""
service_reply=st.text_area("Service Reply",service_reply)
service_style_pirate = """\
a polite tone \
that speaks in English Pirate\
"""
service_style_pirate=st.text_area("Service style pirate",service_style_pirate)

if st.button("Process service messages"):
    service_messages = prompt_template.format_messages(
        style=service_style_pirate,
        text=service_reply)
    st.write(service_messages[0].content)
    service_response = chat(service_messages)
    st.write(service_response.content)
