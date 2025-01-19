from pathlib import Path
from airium import Airium
import pandas as pd
from utils import write_string, recast_str, get_diff

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
                    with a.th():
                        a("Feedback")


                # Table rows
                for row, data in df.iterrows():
                    with a.tr():
                        # Reviews column
                        with a.td():
                            a.span(_t=data['reviews'], style='font-size:12px')

                        # Requirement Column column
                        with a.td():
                            a.span(_t=data['requirements'], style='font-size:18px')

                        all_requirements = data['requirements'].split()
                        all_revision = data["revision"].split()
                        revision_tokens = get_diff(list1=all_revision, list2=all_requirements)

                        # Revisions column (with revision words bolded)
                        # Tokenizing the revision to apply bold
                        with a.td():
                            with a.span(style='font-size:18px'):
                                for tok in all_revision:
                                    # Check if the word needs to be bold
                                    if any(tok == bold_tok for bold_tok in revision_tokens):
                                        with a.b(style='color:red'):
                                            a(tok)
                                    else:
                                        a(tok)
                        break
    html = str(a)
    return html