from pathlib import Path
import pandas as pd
from prompts import promptlib
from functools import partial, reduce
import re
import itertools
from tqdm import tqdm

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
    for prompt in tqdm(prompts):
        resp_list.append(get_ai_response(send_prompt(client, prompt)))
    return resp_list

def get_review_summary(client) -> str:
    pass

def load_file(filepath):

    with open(filepath,'r', encoding='utf-8',errors='ignore') as f:
        return f.read()

def write_string(s, filepath):

    with open(filepath,'w', encoding='utf-8',errors='ignore') as f:
        f.write(s)

def add_line_breaks(s):
    if '\n' not in s[-2:]:
        return f'{s}\n'
    else:
        return s
    
def write_list(lst, filepath):
    
    with open(filepath,'w', encoding='utf-8',errors='ignore') as f:
        lst = [add_line_breaks(s) for s in lst]
        f.writelines(lst)

def add_response(df, new_row):
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def write_output(df,filename, filetype='excel'):
    if 'Unnamed: 0' in df.columns:
        df.drop(columns='Unnamed: 0',inplace=True)
    if filetype == 'excel':
        df.to_excel(filename)
    if filetype == 'csv':
        df.to_csv(filename)

def load_input(filename):
    return pd.read_excel(filename)
    
def get_type_name(var) -> str:
    """Get the string representation of the type of an input variable var

    Args:
        var: An input variable 
    """
    return type(var).__name__

def get_diff(list1,list2) -> list:
    """This functions takes in a 2-element list of lists
    and returns a list of different elements between the
    two lists of lists.

    Args:
        x (list): A 2-element list of lists
    """
    s1 = set(list1)
    s2 = set(list2)
    return list(s1.difference(s2))

def replace_tokens(_str:str,replace_tokens:list, replace_with:str) -> str:
    """Replace the list of tokens with the replace_with string for a given string

    Args:
        _str (str): the corpus (str) on which to apply the replacement
    Keyword Args:
        replace_tokens (list): the list of tokens to be replaced
        replace_with (str): the regex used to replace replace_tokens
    """
    for tok in replace_tokens:
        _str = _str.replace(tok, replace_with)
    return _str

def remove_whitespace(_str:str) -> str:
    """Replaces combinations of new line characters and tabs with a space

    Args:
        _str (str): the corpus (str) on which to apply the function
    """  
    _str = re.sub(r'[\n\t]+', ' ', _str)
    return _str

def recast_str(_str:str, na_value=[]):
    """This function takes in a str and default value for errors or NaNs. The built-in
    python function eval() is applied on the input string in effort to cast the string
    to some expected data type (e.g., list, dict). This is particularly useful as exporting
    pandas dataframes to excel may result in loss of data typing and this is a way to 
    recover this infomation. In the event there is a type or syntax error with the eval()
    function, the na_value is returned.

    """  
    if type(_str) == float:
        return na_value
    if str(_str) == 'nan':
        return na_value
    else:
        try:
            casted = eval(_str)
        except SyntaxError:
            print(f'The following string was unable to be casted using eval()')
            print(f'The value will be converted to data type: {type(na_value)}')
            return na_value
        except TypeError:
            print(f'The input data type: {get_type_name(_str)} cannot be evaluated')
            return na_value
        except NameError:
            return na_value
        else:
            return casted
        
def concat_list_of_str(_list:list, delim='\n') -> str:
    """Take an input list and return a concatenated string where
    a new line separates each list element 

    Args:
        _list (list): A list of strings
    """
    try:
        assert get_type_name(_list) == 'list'
    except AssertionError:
        print('The input is not a list')
        return str(_list)
    else:
        output = ''
        for e in _list:
            output = output + ' ' + e + ' ' + delim
        return output
    
def dict_list_to_df(list_of_dicts: list, ignore_index: bool) -> pd.DataFrame:
    """
    This function takes in a list of dictionaries and for each dictionary, creates a transposed
    dataframe, where the keys of each dictionary are the column names and values of the dictionary
    are the dataframe values. Each dataframe is appended to a list and then concatenated. Note that 
    the join used to concatenate each transposed dataframe is 'outer' such that in the case where one
    dictionary is missing certain keys (i.e., column values), these will be replaced with 'NaN' but
    the column value will still appear.
    
    Args:
        list_of_dicts (list): a dictionary of items which is converted to a dataframe.
        ignore_index (bool): a boolean value to specify whether desired to keep original index
    """
    df_list = []
    for r in list_of_dicts:
        df = pd.DataFrame(r.items()).transpose()
        df.columns = df.iloc[0]
        df = df[1:]
        df_list.append(df)
    return pd.concat(df_list, axis=0, join='outer', ignore_index=ignore_index)