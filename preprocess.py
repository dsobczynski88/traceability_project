"""This script preprocesses sections of the INCOSE guide to writing requirements"""
import re
from pathlib import Path

def get_parsed_text(pattern, text, flags):
    """Get results of applying above regex expression"""
    
    raw_output = re.findall(pattern, text, flags)
    # Extracting the capturing group if a match is found
    if raw_output:
        print(raw_output)  # Output the captured text
        print('---------------------')
        return raw_output
    else:
        print("No match found.")
        return None
    
def create_file(section, text, outdir):
    """Create a text file for a specific text section"""

    # Open a file in write mode
    with open(f"{outdir}/Section_{section}.txt", "w") as f:
        # Write the string to the file
        f.write(text)
    
# Define output directory as the working directory
WD = Path.cwd()
DATA_DIR = WD / 'data'

with open(f"{str(DATA_DIR)}/ambiguity_context_incose_gtwr_24.txt",'r', encoding='utf-8') as f:
    sec_24 = f.read()

with open(f"{str(DATA_DIR)}/ambiguity_context_incose_gtwr_43.txt",'r', encoding='utf-8') as f:
    sec_43 = f.read()

# Output Section 2.4 of the INCOSE guide to writing requirements
create_file(section='2_4', text=sec_24, outdir=str(DATA_DIR))

# Preprocess Sections 4.3.1 - 4.3.6
FLAGS_43 = re.DOTALL
sec_pat = r'(4\.3\.[1-6])\s+(.*?)((?=4\.3\.[1-6])|(?=$))'
sec_txt = get_parsed_text(sec_pat, sec_43, FLAGS_43)
for sec in sec_txt:
    # Output sections the INCOSE guide to writing requirements
    create_file(section=sec[0].replace('.','_'), text=sec[1], outdir=DATA_DIR)