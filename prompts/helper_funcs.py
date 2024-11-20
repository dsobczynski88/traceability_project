import pandas as pd

def add_response(df, new_row):
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def write_output(df,filename):
    if 'Unnamed: 0' in df.columns:
        df.drop(columns='Unnamed: 0',inplace=True)
    df.to_excel(filename)