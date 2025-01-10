from typing import List, Union, Callable
from pathlib import Path
from dotenv import dotenv_values
from tqdm import tqdm
from functools import partial, reduce
from helper import *
from openai import OpenAI
from prompts.promptlib import single_attribute_review

#attribute_review_template(self.reqs, load_single_file(f, output_type='str')

class RequirementAttributeReviewer:
    
    post_process_tokens = ['\n','\t','    ', '```python', '```']
    
    def __init__(self, reqs_fp: Path, review_fps: Union[List[Path], None], output_fp: Path, prompt_func: Callable):
        
        try:
            config = dotenv_values(".env")
            secret_key = config['OPENAI_API_KEY']
            self.client = OpenAI(api_key=secret_key)
        except FileNotFoundError:
            print('Please create a ".env" file containing the OpenAI API key') 
        # client refers to OpenAI API
        # reqs_fps refers to the filepath containing requirements
        # review_fps refers to a list of filepaths containing review documents
        # output_fp refers to 
        self.reqs_fp = reqs_fp
        self.review_fps = review_fps # Create function to cast list will check the review_fps input, if str it will make a list, else will just return the input list
        self.output_fp = output_fp
        self.reqs = load_requirements(reqs_fp) # Create function to load file based on the data type and return a list of strings
        self.reqs_str = str(self.reqs)
        self.prompt_template = partial(prompt_func, requirements=self.reqs)
        self.prompts = []
        self.responses = []
        self._df_list = []
        self.df = None
  
    def run(self):
        self._build_prompts()
        self._fetch_responses()
        self._clean_responses()
        #self._output_responses()
        self._create_frame()
        self._output_frame()
        #self._to_html()

    def _build_prompts(self):
        if self.review_fps is not None:
            for f in self.review_fps:
                self.prompts.append(self.prompt_template(context=load_single_file(f)))
        else:
            self.prompts.append(self.prompt_template())
            
    def _fetch_responses(self):
        for prompt in tqdm(self.prompts):
            self.responses.append(get_ai_response(send_prompt(self.client, prompt)))
    
    def _clean_responses(self):
        for idx, _ in enumerate(self.responses):
            self.responses[idx] = replace_tokens(self.responses[idx], __class__.post_process_tokens, '')

    def _output_responses(self):
        write_string(str(self.responses), self.output_fp / 'responses.txt')

    def _output_frame(self):
        write_frame(self.df, self.output_fp / 'df.csv', filetype='csv')

    def _create_frame(self):
        self._df_list = []
        for idx, sub_resp in enumerate(self.responses):
            print(sub_resp)
            self._df_list.append(pd.DataFrame(recast_str(sub_resp), columns=['requirements',f'review_{idx}']))
        if len(self._df_list) > 1:
            self.df = reduce(lambda l,r: pd.merge(l,r, on='requirements',how='inner'), self._df_list)
            self.df['reviews'] = self.df[[c for c in self.df.columns if 'review_' in c]].agg(' '.join, axis=1)
        else:
            self.df = self._df_list[0]
            self.df['reviews'] = self.df['review_0']