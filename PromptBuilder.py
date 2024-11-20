import pandas as pd
from time import localtime, strftime
from pathlib import Path
import tiktoken

# Below function from OpenAI cookbook
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

class PromptBuilder:

    def __init__(self, client, model, prompt, system=None):
        self.client = client
        self.model = model
        self.prompt = prompt
        self.system = system
        self.response_object = None
        self.response_result = None
        self.messages_list = []
        self.output = []
        
    def build_prompt(self):
        
        self.messages_list.append(
            {'role':'user',
             'content':self.prompt}
        )
        if self.system is not None:
            self.messages_list.append(
                {'role':'system',
                 'content':self.system}
            )
        return self.messages_list
    
    def show_prompt(self):
        print(self.messages_list)
    
    def create_response_object(self):
        self.response_object = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages_list
        )
    
    def get_response(self):
        self.build_prompt()
        self.show_prompt()
        self.create_response_object()
        self.response_result = self.response_object.choices[0].message.content
    
    def show_response(self):
        print(self.response_result)

    def run(self):
        self.show_prompt()
        self.get_response()
        self.show_response()
        self.output = [
            {
            'prompt':self.prompt,
            'system':self.system,
            'response': self.response_result,
            'timestamp': str(strftime("%Y_%m_%d_%H_%M", localtime())),
            'num_tokens_prompt':num_tokens_from_string(self.prompt,'o200k_base'),
            'num_tokens_response':num_tokens_from_string(self.response_result,'o200k_base'),
            'cost_per_token':0.03/1000,
            'human_review_of_response':'',
            'score':'',
            'tags':'',
            'id':'',
            'description':''
            }
        ]
        return self.output
    
    def run_attribute_review(self, requirements, attr_name):
        self.show_prompt()
        self.get_response()
        self.show_response()
        self.output = [
            {
                'requirements':requirements,
                'reviewed_attribute':attr_name,
                'prompt':self.prompt,
                'system':self.system,
                'response': self.response_result,
                'timestamp': str(strftime("%Y_%m_%d_%H_%M", localtime()))
            }
        ]
        return self.output