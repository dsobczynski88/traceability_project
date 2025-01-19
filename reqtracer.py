import re
import pandas as pd
from pathlib import Path
from functools import partial, reduce
from utils import get_ai_response, send_prompt, replace_tokens, recast_str, write_frame, load_single_file, find_LCS, get_diff
from tqdm import tqdm
from time import time

class RequirementPromptBuilder:
    system_message = "I want you to act as a software quality assurance engineer. Your job is to review Requirements to ensure they meet system engineering best practices such as those described in the INCOSE Guide to Writing Requirements. You will need to approve detailed reports on software verification testing and provide recommendations for improvement. Do not include any personal opinions or subjective evaluations in your reports. "
    model = 'gpt-4o-mini'
    post_process_tokens = ['\n','\t','    ', '```python', '```']
    data_directory = Path.cwd() / 'data'
    
    def __init__(self, client, reqs, prompt_func):
        self.client = client
        self.reqs = reqs
        self.prompt_func=prompt_func
        self.prompt_template = partial(prompt_func, requirements=self.reqs)
        self.prompts = []
        self.responses = []
        self.df_list = []
        self.df = []
        self.run_ids = [] 
            
    def run(self):
        self.build_prompts()
        self.fetch_responses()
        self.clean_responses()
        self.create_frame()
        self.output_frame(tag='tag')
        return self
    
    def build_prompts(self):
        self.prompts.append(self.prompt_template())
    
    def fetch_responses(self):
        for prompt in tqdm(self.prompts):
            self.run_ids.append(str(round(time())))
            self.responses.append(get_ai_response(send_prompt(self.client, __class__.model, __class__.system_message, prompt)))

    def clean_responses(self):
        for idx, _ in enumerate(self.responses):
            self.responses[idx] = replace_tokens(self.responses[idx], __class__.post_process_tokens, '')

    def create_frame(self):
        for idx, sub_resp in enumerate(self.responses):
            self.df_list.append(pd.DataFrame(recast_str(sub_resp), columns=['requirements',f'response_{[idx]}']))
        if len(self.df_list) > 1:
            self.df = reduce(lambda l,r: pd.merge(l,r, on='requirements',how='inner'), self.df_list)
            self.df['all_responses'] = self.df[[c for c in self.df.columns if 'requirements' not in c]].apply(lambda r: ' '.join(r.values.astype(str)), axis=1)
        else:
            self.df = self.df_list[0]
            self.df.columns = ['requirements', 'all_responses']
        
        self.df['run_ids'] = str(self.run_ids)
        self.df['prompt_template'] = self.prompt_func.__name__
        self.df['prompt_description'] = self.prompt_func.__doc__

    def output_frame(self, tag):
        write_frame(self.df, f"{str(__class__.data_directory)}/{str(tag)}_{self.run_ids[0]}.csv", filetype='csv')

class RequirementReviewBuilder(RequirementPromptBuilder):
    
    def __init__(self, client, reqs, attrs, prompt_func):
        super().__init__(client, reqs, prompt_func)
        self.attrs = attrs
        self.attr_list = self.attrs.split('|')
        self.regex_pat = f'^({self.attrs})_Section'
        self.review_fps = []
        
        for x in __class__.data_directory.iterdir():
            match = re.search(self.regex_pat, str(x.name))
            if match is not None:
                self.review_fps.append(x)
    
    def run(self):
        self.build_prompts()
        super().fetch_responses()
        super().clean_responses()
        self.create_frame()
        super().output_frame(tag='_'.join([x[0:3] for x in self.attr_list])+'_review')
        return self

    def build_prompts(self):
        if self.review_fps is not None:
            for f in self.review_fps:
                self.prompts.append(self.prompt_template(context=load_single_file(f)))
        else:
            self.prompts.append(self.prompt_template())
    
    def create_frame(self):
        for idx, sub_resp in enumerate(self.responses):
            matched_attr = find_LCS(self.review_fps[idx].name, self.attrs)
            self.df_list.append(pd.DataFrame(recast_str(sub_resp), columns=['requirements',f'{matched_attr}_review_{idx}']))
        if len(self.df_list) > 1:
            self.df = reduce(lambda l,r: pd.merge(l,r, on='requirements',how='inner'), self.df_list)
            self.df[f'{self.attrs}_complete_review'] = self.df[[c for c in self.df.columns if 'requirements' not in c]].apply(lambda r: ' '.join(r.values.astype(str)), axis=1)
        else:
            self.df = self.df_list[0]
            self.df.columns = ['requirements', f'{self.attrs}_complete_review']

        self.df['prompts'] = str(self.prompts)
        self.df['run_ids'] = str(self.run_ids)
        self.df['prompt_template'] = self.prompt_func.__name__
        self.df['prompt_description'] = self.prompt_func.__doc__

class RevisionBuilder(RequirementPromptBuilder):

    def __init__(self, client, reqs, attrs, prompt_func):
        super().__init__(client, reqs, prompt_func)
        self.attrs = attrs
        self.regex_pat = 'review_[0-9]+'
        self.review_fps = []

        for x in __class__.data_directory.iterdir():
            match = re.search(self.regex_pat, str(x.name))
            if match is not None:
                self.review_fps.append(x)
        
        self.last_updated_file = str(max([int(x.stem.split('_')[-1]) for x in self.review_fps])) 
        self.review_fps = list(__class__.data_directory.rglob(f'*_{self.last_updated_file}.csv')) # get latest file
        print(self.review_fps)
        review_df = pd.read_csv(self.review_fps[0])
        review_column = next((s for s in review_df.columns if 'complete_review' in s), None)
        self.requirement_reviews = list(review_df[review_column].values)
    
    def run(self):
        self.build_prompts()
        super().fetch_responses()
        super().clean_responses()
        self.create_frame()
        super().output_frame(tag=self.attrs)
        return self
        
    def build_prompts(self):
        if self.review_fps is not None:
            self.prompts.append(self.prompt_template(reviews=self.requirement_reviews))
        else:
            self.prompts.append(self.prompt_template())
    
    def create_frame(self):
        for sub_resp in self.responses:
            self.df_list.append(pd.DataFrame(recast_str(sub_resp), columns=['requirements','revision']))
        self.df = self.df_list[0]
        self.df['reviews'] = self.requirement_reviews
        self.df['run_ids'] = str(self.run_ids)
        self.df['prompt_template'] = self.prompt_func.__name__
        self.df['prompt_description'] = self.prompt_func.__doc__