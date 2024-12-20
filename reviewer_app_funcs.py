from pathlib import Path
import pandas as pd
from prompts import promptlib
from functools import partial, reduce
import re
import itertools

def send_prompt(client, prompt: str) -> dict:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "I want you to act as a software quality assurance engineer. Your job is to review Requirements to ensure they meet system engineering best practices such as those described in the INCOSE Guide to Writing Requirements. You will need to approve detailed reports on software verification testing and provide recommendations for improvement. Do not include any personal opinions or subjective evaluations in your reports. "},
            {"role": "user", "content": prompt},
        ],
    )

def get_ai_response(response) -> str:
    return response.choices[0].message.content

def get_requirements_review(client, requirements: str) -> list:
    prompts = promptlib.review_requirements(requirements)
    resp_list=[]
    for prompt in prompts:
        resp_list.append(get_ai_response(send_prompt(client, prompt)))
    return resp_list

def get_responses(client, prompts: list) -> list:
    resp_list=[]
    for prompt in prompts:
        resp_list.append(get_ai_response(send_prompt(client, prompt)))
    return resp_list

def get_review_summary(client) -> str:
    pass