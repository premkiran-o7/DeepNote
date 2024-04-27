import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-pro")


topic = st.chat_input("Enter the Topic")
story_line = ''
prompt = ''
prompt_template = '''
Prompt1 

Prompt2

Prompt3

Prompt4

Prompt5'''

if topic:
    story_line = llm.invoke(f"Write a storyline for explaining the topic {topic} in the form of comics and include text description. Limit the story line to exactly five panels")
    st.write(f"{story_line.content}")

if story_line:
    prompt = llm.invoke(f"Write prompts for {story_line} for image generation. Generate a prompt for each panel. Return only the prompts and the prompts should be in the form {prompt_template}. Mention the text to be shown in the image according to the storyline in the prompt")
    st.write(f"{prompt.content}")

