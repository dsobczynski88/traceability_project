from openai import OpenAI
import getpass
from pathlib import Path
import pandas as pd
from PromptBuilder import PromptBuilder
from prompts import templates, context
from prompts.helper_funcs import add_response, write_output

# Define requirements to be reviewed
REQUIREMENTS = """
    1. The application shall provide a user-friendly GUI so the user can browse the pizza menu with available categories such as pizzas, sides, and drinks.
    2. The application shall make it easy for the user to create a customized pizza by selecting crust type, toppings, and size.
    3. The application needs to have a drag-and-drop feature for the user to to add or remove items from the shopping cart.
    """

# Load output dataframe containing AI-powered review of requirements
filename = Path('./req_reviewer.xlsx')

if filename.is_file():
    prompt_df = pd.read_excel(filename)
else:
    # If not found, create a new df "prompt_df"
    prompt_df = pd.DataFrame(columns=['requirements','reviewed_attribute',
                                      'prompt','system','response','timestamp'])

secret_key = getpass.getpass("Please enter your OpenAI Key:")
openai_client = OpenAI(api_key=secret_key)

# Load prompt template function for analyzing requirement attributes
req_attr_template = templates.req_attr_template

# Load attribute names, definitions, rationales as described in INCOSE's Guide to
# Writing Requirements. These will be fed to the template to create a unique prompt 
# for each attribute to be reviewed
names = context.attr_list
defs = context.attr_def_list
rats = context.attr_rat_list

# Load AI-generated examples of REQUIREMENTS which meet/do not meet the attributes
examples = context.attr_exmp_list

prompt_texts = prompt_df['prompt'].values
for i in range(len(names)):
    prompt = req_attr_template(REQUIREMENTS, names[i], defs[i], rats[i], examples[i])
    if prompt in prompt_texts:
        print('The prompt was already found in the dataframe')
        continue
    else:
        print(f'Running {names[i]} prompt\n')
        new_prompt = PromptBuilder(openai_client, 'gpt-4',prompt)
        output = new_prompt.run_attribute_review(REQUIREMENTS, names[i])
        print('---------------------------------------')
        prompt_df = add_response(prompt_df, output[0])

write_output(prompt_df, filename)

pivoted_df = prompt_df[['requirements','reviewed_attribute','response']].pivot(
    index='requirements',
    columns='reviewed_attribute',
    values='response'
).reset_index()

write_output(pivoted_df, './req_reviewer_pivoted.xlsx')