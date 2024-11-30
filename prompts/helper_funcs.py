import pandas as pd

def add_response(df, new_row):
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def write_output(df,filename):
    if 'Unnamed: 0' in df.columns:
        df.drop(columns='Unnamed: 0',inplace=True)
    df.to_excel(filename)

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