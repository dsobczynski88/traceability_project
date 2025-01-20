from pathlib import Path
from dotenv import dotenv_values
import pandas as pd
from openai import OpenAI
from utils import load_requirements
from utils import write_string
from prompts.promptlib import single_attribute_review
from prompts.promptlib import revise
from reqtracer import RequirementReviewBuilder
from reqtracer import RevisionBuilder
from generate_html import df_to_html

config = dotenv_values(".env")
secret_key = config['OPENAI_API_KEY']
client = OpenAI(api_key=secret_key)
datapath = Path.cwd() / 'data'
filepath= datapath / 'input' / 'requirements.csv'
reqs = load_requirements(filepath)

# Run the review
reviewer = RequirementReviewBuilder(
    client=client,
    reqs=reqs,
    attrs='ambiguity|validity',
    prompt_func=single_attribute_review
).run()

# Run the revision
reviser = RevisionBuilder(
    client=client,
    reqs=reqs,
    attrs='revise',
    prompt_func=revise
).run()