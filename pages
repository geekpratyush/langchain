import openai
import streamlit as st

def get_completion(prompt, model="gpt-3.5-turbo",temperature="0.7"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    print(prompt)
    return response.choices[0].message["content"]

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


with st.form("my_form"):
    if instruction := st.text_area("Instruction to Model","You are a language expert, please summarize the text written here.",height=100):
        text = st.text_area("Enter your text here","Provide your text that to be processed as per the instruction above.",height=100)
        prompt=instruction+" \""+text+"\""
        st.write(prompt)
        #prompt = st.text_area("Prompt",f"""Summarize the text delimited by triple backticks into a single sentence.```{text}```""")
        submitted = st.form_submit_button("Submit")
    if submitted:
       response = get_completion(prompt=prompt,temperature=temp)
       st.write(response)






