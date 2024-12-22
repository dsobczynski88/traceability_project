from pathlib import Path
from openai import OpenAI
from dotenv import dotenv_values
from functools import reduce
from prompts.promptlib import single_attribute_review, revise
from helper import *


# Define input data (requirements) filename with extension
WD = Path.cwd()
DATA_DIR = WD / 'data'

input_data = DATA_DIR / 'software_requirements_extended.csv'

# Load input data (csv file)
data = pd.read_csv(input_data)

# Filter functional requirements only and get a sample of 30 functional requirements
mask = data['Type'].isin(['F','FR']) & data['Requirement'].str.contains('shall')
data = list(data[mask].sample(5)['Requirement'].values)

print(data)

# Load preprocessed text files
files = list(DATA_DIR.rglob('Section_2_4.txt'))
names = [x.name for x in files]

# Build prompt list using the preprocessed text files
prompt_list=[]
for f in files:
    context = load_file(str(f))
    prompt_list.append(single_attribute_review(data, context))

# Call OpenAI API using prompts defined in the prompt_list 
config = dotenv_values(".env")
secret_key = config['OPENAI_API_KEY']
client = OpenAI(api_key=secret_key) 
responses = get_responses(client, prompts=prompt_list)

# Output each response to a text file
outdir=str(Path.cwd())
for i in range(len(responses)):
    write_string(responses[i], f"{str(DATA_DIR)}/response_{names[i]}")

# Post process the AI responses and cast each response to a dataframe
replacements = ['\n','\t','    ', '```python', '```'] 
df_list = []
for i in range(len(responses)):
    responses[i] = eval(replace_tokens(responses[i], replace_tokens=replacements, replace_with=''))
    temp_df = pd.DataFrame(responses[i], columns=['requirements']+names)
    temp_df['reviews'] = temp_df.iloc[:,1:].agg(' '.join, axis=1) 
    df_list.append(temp_df)
review_df = reduce(lambda l,r: pd.merge(l,r, on='requirements',how='inner'), df_list)
write_output(review_df,f"{str(DATA_DIR)}/output_df.xlsx")

# Run the revision prompt which proposes a requirement revision based on AI-generated review
# using the output from above
requirements = list(review_df['requirements'].values)
reviews = list(review_df['reviews'].values)
revisions = get_responses(client, prompts=[revise(requirements, reviews)])

# Since a single prompt is being run, the output list has only 1 element
# To simplify further processing, we assign revisions to revisions[0]
revisions = revisions[0]

# Output revisions to a text file
outdir=str(Path.cwd())
write_string(revisions, f"{str(DATA_DIR)}/revisions.txt")

# Post process the revisions and cast to a dataframe
replacements = ['\n','\t','    ', '```python', '```']
revisions = eval(replace_tokens(revisions, replace_tokens=replacements, replace_with=''))
revision_df = pd.DataFrame(revisions, columns=['requirements','revision'])
write_output(revision_df,f"{str(DATA_DIR)}/revisions_df.xlsx")

# Combine revision_df with review_df
comb_df = pd.merge(left=review_df,right=revision_df, on='requirements',how='inner')
write_output(comb_df,f"{str(DATA_DIR)}/combined_output.xlsx")