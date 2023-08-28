import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

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

{
  "gift": False,
  "delivery_days": 5,
  "price_value": "pretty affordable!"
}

customer_review = "This leaf blower is pretty amazing.  It has four settings: candle blower, gentle breeze, windy city, and tornado. It arrived in two days, just in time for my wife's anniversary present. I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been using it every other morning to clear the leaves on our lawn. It's slightly more expensive than the other leaf blowers out there, but I think it's worth it for the extra features."

customer_review = st.text_area("Customer Review",customer_review)

review_template = """For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as json with the following keys:
gift
delivery_days
price_value

text: {text}
"""
st.info(review_template)

if st.button("Process Prompt Template & chat message"):
    prompt_template = ChatPromptTemplate.from_template(review_template)
    messages = prompt_template.format_messages(text=customer_review)
    st.info(prompt_template)
    st.info(messages)
    chat = ChatOpenAI(temperature=temp, model=llm_model)
    response = chat(messages)
    st.info(response.content)

    gift_schema = ResponseSchema(name="gift",
                                description="Was the item purchased\
                                as a gift for someone else? \
                                Answer True if yes,\
                                False if not or unknown.")
    delivery_days_schema = ResponseSchema(name="delivery_days",
                                        description="How many days\
                                        did it take for the product\
                                        to arrive? If this \
                                        information is not found,\
                                        output -1.")
    price_value_schema = ResponseSchema(name="price_value",
                                        description="Extract any\
                                        sentences about the value or \
                                        price, and output them as a \
                                        comma separated Python list.")

    response_schemas = [gift_schema, 
                        delivery_days_schema,
                        price_value_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    st.info(format_instructions)

    review_template_2 = """\
    For the following text, extract the following information:

    gift: Was the item purchased as a gift for someone else? \
    Answer True if yes, False if not or unknown.

    delivery_days: How many days did it take for the product\
    to arrive? If this information is not found, output -1.

    price_value: Extract any sentences about the value or price,\
    and output them as a comma separated Python list.

    text: {text}

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_template(template=review_template_2)

    messages = prompt.format_messages(text=customer_review, 
                                    format_instructions=format_instructions)

    st.write(messages[0].content)
    response = chat(messages)
    st.write(response.content)
    output_dict = output_parser.parse(response.content)
    st.info(output_dict.get('delivery_days'))