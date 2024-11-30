import streamlit as st
from reviewer_app_funcs import get_requirements_review
from prompts.helper_funcs import concat_list_of_str, dict_list_to_df
from prompts.promptlib import requirement_attributes, requirement_review_delimiter
from dotenv import dotenv_values
from openai import OpenAI
import pandas as pd

config = dotenv_values(".env")
secret_key = config['OPENAI_API_KEY']
client = OpenAI(api_key=secret_key)

def display_header() -> None:
    st.title("Welcome to the Requirements Reviewer App!")

def display_widgets() -> str:
    requirements = st.text_area("Paste your requirements in the form below (press Ctrl + Enter to send)")
    #if not requirements:
    #    st.error("Please paste your requirements in the above form")
    return requirements

def get_delimiter() -> str:
    delim = st.text_area("Enter the delimiter for the pasted requirements (press Ctrl + Enter to send)")
    return delim or ""

def extract_requirements() -> str:
    requirements = display_widgets()
    return requirements or ""

def split_text(text, delim) -> list:
    return text.split(delim)

def display_review_complete() -> None:
    st.write("## Your requirement review is complete! ##")
    
def main() -> None:
    display_header()
    if requirements_to_review := extract_requirements():
        if requirements_delimiter := get_delimiter():
            if requirements_list := split_text(requirements_to_review, requirements_delimiter):
                with st.spinner(text="Reviewing the requirements..."):
                    reviews = []
                    for requirement in requirements_list:
                        review = get_requirements_review(client, requirements=requirement)
                        reviews.append(dict(zip(requirement_attributes,review)))
                display_review_complete()
                reviews_df = dict_list_to_df(reviews, ignore_index=True)
                reviews_df.index = requirements_list
                st.data_editor(
                    reviews_df,
                    column_config={
                        "widgets": st.column_config.TextColumn(
                            width="small"
                        )
                    }
                )

if __name__ == "__main__":
    main()