from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
import streamlit as st
from langchain_core.prompts import PromptTemplate
load_dotenv()

model= ChatMistralAI(model="mistral-medium-2508")

st.header("Langchain Prompt Template Example")

template= PromptTemplate(template="""
    Please summarize the research paper titled "{paper_title}" with the following specifications:
    Explanation Style: {output_style}
    Explanation Length: {output_length}
    1. Mathematical details:
    include relevant mathematical equations if present in the paper with proper markdown formatting like LaTeX. Explain mathematical concepts using simple, intuitive code snippets for detailed explanations.
    2" Analogies:
    Provide analogies to explain complex concepts in a simple way.
    
    If certain information is not provided in the paper, respond with "Insufficient information" instead of guessing. 
    Ensure the summary is clear, accurate, and aligned with the given style and length.""",
    input_variables=["paper_title", "output_style", "output_length"]
    )

paper_title = st.selectbox("Select a research paper", ["Select a paper", "Attention is all you need", "BERT", "GPT 2", "GPT 3"])
output_style = st.selectbox("Select an output style", ["Informative", "Code-oriented", "Mathematical", "Beginner-friendly"])
output_length = st.selectbox("Select an output length", ["Very short (3-4 sentences)", "Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed)"])


if st.button('Summarize'):
    chain= template | model
    result= chain.invoke({
    "paper_title": paper_title,
    "output_style": output_style,
    "output_length": output_length
    })
    st.write(result.content)