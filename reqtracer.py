import re
from time import time
from pathlib import Path
from functools import partial, reduce
import pandas as pd
from tqdm import tqdm
from spire.doc import *
from spire.doc.common import *
from generate_html import df_to_html
from utils import get_ai_response, send_prompt, replace_tokens, recast_str, write_frame, load_single_file, find_LCS, write_string

class RequirementPromptBuilder:
    system_message = "I want you to act as a software quality assurance engineer. Your job is to review Requirements to ensure they meet system engineering best practices such as those described in the INCOSE Guide to Writing Requirements. You will need to approve detailed reports on software verification testing and provide recommendations for improvement. Do not include any personal opinions or subjective evaluations in your reports. "
    model = 'gpt-4o-mini'
    post_process_tokens = ['\n','\t','    ', '```python', '```']
    data_directory = Path.cwd() / 'data'
    input_directory = data_directory / 'input'
    output_directory = data_directory / 'output'
    logs_directory = data_directory / 'logs'
    
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
        try:
            for f in self.review_fps:
                    self.prompts.append(self.prompt_template(context=load_single_file(f)))
        except AttributeError:
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
        write_frame(self.df, f"{str(__class__.output_directory)}/{str(tag)}_{self.run_ids[0]}.csv", filetype='csv')

class RequirementReviewBuilder(RequirementPromptBuilder):
    
    def __init__(self, client, reqs, attrs, prompt_func):
        super().__init__(client, reqs, prompt_func)
        self.attrs = attrs
        self.attr_list = self.attrs.split('|')
        self.regex_pat = f'^({self.attrs})_Section'
        self.review_fps = []
        
        for x in __class__.input_directory.iterdir():
            match = re.search(self.regex_pat, str(x.name))
            if match is not None:
                self.review_fps.append(x)
    
    def run(self):
        super().build_prompts()
        super().fetch_responses()
        super().clean_responses()
        self.create_frame()
        super().output_frame(tag='_'.join([x[0:3] for x in self.attr_list])+'_review')
        self.output_reviews()
        return self

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
        self.df['prompt_description'] = self.prompt_func.__doc__.strip()

    def output_reviews(self):
        review_column = next((s for s in self.df.columns if 'complete_review' in s), None)
        requirement_reviews = str(list(self.df[review_column].values))
        write_string(requirement_reviews, f"{str(__class__.output_directory)}/reviews_{self.run_ids[-1]}.txt")

class RevisionBuilder(RequirementPromptBuilder):

    def __init__(self, client, reqs, attrs, prompt_func):
        super().__init__(client, reqs, prompt_func)
        self.attrs = attrs
        self.regex_pat = '(reviews_[0-9]+)'
        self.review_fps = []
        self.df2html = None

        file_times = []
        for x in __class__.output_directory.iterdir():
            match = re.search(self.regex_pat, str(x.name))
            if match is not None:
                print(match.group(0))
                file_times.append(int(match.group(0).split('_')[1]))
        most_recent_file = f"{str(__class__.output_directory)}/reviews_{sorted(file_times)[-1]}.txt"
        print(f'The most recent file found is: {most_recent_file}')
        self.review_fps = [most_recent_file]
    
    def run(self):
        super().build_prompts()
        super().fetch_responses()
        super().clean_responses()
        self.create_frame()
        super().output_frame(tag=self.attrs)
        self.generate_feedback_file()
        return self
    
    def create_frame(self):
        for sub_resp in self.responses:
            self.df_list.append(pd.DataFrame(recast_str(sub_resp), columns=['requirements','revision']))
        self.df = self.df_list[0]
        
        try:
            self.df['reviews'] = recast_str(load_single_file(self.review_fps[0]))
        except ValueError:
            print("The number of reviews doesn't match the number of revisions")
            print("\n")
            print("Try re-running the prompt")
            #super().build_prompts()
            #super().fetch_responses()
            #super().clean_responses()

        
        self.df['run_ids'] = str(self.run_ids)
        self.df['prompt_template'] = self.prompt_func.__name__
        self.df['prompt_description'] = self.prompt_func.__doc__

    def generate_feedback_file(self):
        self.df2html = df_to_html(self.df)
        write_string(self.df2html, f"{str(__class__.output_directory)}/revise_{self.run_ids[-1]}.html")
        document = Document()
        section = document.AddSection()
        section.PageSetup.Margins.All = 72
        paragraph = section.AddParagraph()
        paragraph.AppendHTML(self.df2html)
        document.SaveToFile(f"{str(__class__.output_directory)}/revise_{self.run_ids[-1]}.docx", FileFormat.Docx2019)
        document.Close()