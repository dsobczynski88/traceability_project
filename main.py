from pathlib import Path
from openai import OpenAI
from dotenv import dotenv_values
from functools import reduce
from prompts.promptlib import single_attribute_review, revise
from helper import *
from tqdm import tqdm


#WD = Path.cwd()
#DATA_DIR = WD / 'data'
#input_data = DATA_DIR / 'requirements.csv'
#reviewer = RequirementAttributeReviewer(input_data, list(DATA_DIR.rglob('Section_2*.txt')), DATA_DIR, single_attribute_review)
#reviewer.run()


# Define input data (requirements) filename with extension
WD = Path.cwd()
DATA_DIR = WD / 'data'

input_data = DATA_DIR / 'requirements.csv'

# Load input data (csv file)
data = pd.read_csv(input_data)

try:
    data = list(data['Requirement'].values)
except KeyError:
    print('The input requirements.csv file must contain a column titled Requirement')
    quit()

# Load preprocessed text files
files = list(DATA_DIR.rglob('Section_*.txt'))
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
print('Running Ambiguity check for provided input...calling OpenAI API...') 
responses = get_responses(client, prompts=prompt_list)

# Load responses
response_files = list(DATA_DIR.rglob('response_*.txt'))
responses = [load_file(f) for f in response_files]

# Output each response to a text file
outdir=str(Path.cwd())
for i in range(len(responses)):
    write_string(responses[i], f"{str(DATA_DIR)}/response_{names[i]}")

# Post process the AI responses and cast each response to a dataframe
replacements = ['\n','\t','    ', '```python', '```'] 
df_list = []
print('Generating responses to prompts using OpenAI API...')
for i in range(len(responses)):
    responses[i] = eval(replace_tokens(responses[i], replace_tokens=replacements, replace_with=''))
    temp_df = pd.DataFrame(responses[i], columns=['requirements']+[names[i]]) 
    df_list.append(temp_df)
review_df = reduce(lambda l,r: pd.merge(l,r, on='requirements',how='inner'), df_list)

review_df['reviews'] = review_df.iloc[:,1:].agg(' '.join, axis=1)
write_output(review_df,f"{str(DATA_DIR)}/output_df.xlsx")

# Run the revision prompt which proposes a requirement revision based on AI-generated review
# using the output from above
requirements = list(review_df['requirements'].values)
reviews = list(review_df['reviews'].values)
print('Generating requirement revisions based on ambiguity checker reviews...')
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
comb_df['requirements_tok'] = comb_df['requirements'].apply(lambda s: s.split())
comb_df['revision_tok'] = comb_df['revision'].apply(lambda s: s.split())
comb_df['revision_tokens'] = comb_df[['revision_tok','requirements_tok']].apply(lambda l: get_diff(*l), axis=1)

write_output(comb_df,f"{str(DATA_DIR)}/combined_output.xlsx", filetype='excel')
write_output(comb_df,f"{str(DATA_DIR)}/combined_output.csv", filetype='csv')

# Convert review_df to HTML
# Initialize Airium and construct the HTML document