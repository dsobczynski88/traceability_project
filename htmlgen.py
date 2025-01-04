from pathlib import Path
from airium import Airium
import pandas as pd
from helper import write_string, recast_str

def df_to_html(df):

    a = Airium()

    # Begin HTML document
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="UTF-8")
            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            a.title(_t="Reviews and Revisions")

        with a.body():
            with a.table():
                # Table header
                with a.tr():
                    with a.th():
                        a("Reviews")
                    with a.th():
                        a("Requirement")
                    with a.th():
                        a("Revision")


                # Table rows
                for row, data in df.iterrows():
                    with a.tr():
                        # Reviews column
                        with a.td():
                            a.span(_t=data['reviews'], style='font-size:12px')

                        # Requirement Column column
                        with a.td():
                            a.span(_t=data['requirements'], style='font-size:18px')

                        all_tokens = data['revision'].split()
                        revision_tokens = recast_str(data["revision_tokens"])

                        # Revisions column (with revision words bolded)
                        # Tokenizing the revision to apply bold
                        with a.td():
                            with a.span(style='font-size:18px'):
                                for tok in all_tokens:
                                    # Check if the word needs to be bold
                                    if any(tok == bold_tok for bold_tok in revision_tokens):
                                        with a.b():
                                            a(tok)
                                    else:
                                        a(tok)
                        break
    html = str(a)
    return html

df = pd.read_excel('./data/combined_output.xlsx')

html_str = df_to_html(df)

fp = Path.cwd() / 'output.html'

write_string(html_str, fp)