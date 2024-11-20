from openai import OpenAI
import getpass
import pandas as pd
from pathlib import Path
from PromptBuilder import PromptBuilder
from prompts.helper_funcs import add_response, write_output

TEST_SYSTEM = """
Enter the system instructions here
"""

TEST_PROMPT = """
Enter your prompt (user message) here   
"""

TEST_MODEL = 'gpt-4'

secret_key = getpass.getpass("Please enter your OpenAI Key:")
openai_client = OpenAI(api_key=secret_key)

# Load prompt dataframe
filename = Path('./prompt_df_test.xlsx')

if filename.is_file():
    prompt_df = pd.read_excel(filename)
else:
    # If not found, create a new df "prompt_df"
    prompt_df = pd.DataFrame(columns=['prompt','system','response','timestamp','num_tokens_prompt','num_tokens_response','cost_per_token','review','score','tags','id','description'])

new_prompt = PromptBuilder(openai_client, TEST_MODEL,TEST_PROMPT,TEST_SYSTEM)
output = new_prompt.run()
print('---------------------------------------')
prompt_df = add_response(prompt_df, output[0])
write_output(prompt_df, filename)