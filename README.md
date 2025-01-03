# *reqtracer* 
**Applying Generative AI to enhance software quality processes** 

### Inspiration
My inspiration for this project began during a career change into software quality. My goal is to look for ways to improve software development documentation with the broader goal to improve product quality. I hope that others find this work to be useful in their personal or professional experience. 

### Project Description
This project applies NLP and data science tools with the goal to improve software quality artifact reviews -- specifically regarding traceability. This project currently contains the following feature:

- *Requirements Ambiguity Checker*
    - This feature leverages basic prompt engineering techniques $^1$ via OpenAI's API to refine requirements writing. Specifically, the goal is to improve the quality of written requirement statements. The prompts are built using the INCOSE Guide to Writing requirements $^2$ which reflects system engineering best practices.

### Getting started

1) To use the ambiguity checker, clone the repository, create a .env file as follows:

    `OPENAI_API_KEY = 'Your api key'`

2) Upload a csv file to the data folder titled 'requirements'. See the sample file provided in the data folder.

3) Open a new command prompt and navigate to the top-level directory where main.py is contained.

4) Install dependencies:

    `py -m pip install -r requirements.txt`

5) Run the program:

    `py -m main`

### Technologies used
This project is written in Python. The choice of Python is based on its broad-range support from the data science and AI community.

### Intended Use
This project is intended to be used during the software development process to create or review software artifacts such as those created in a requirements management tool (requirements, test cases, etc.). 

### Credits
Would like to thank all my colleagues I've gotten to work with over these initial 12 months in this software quality role.

### Future Work
- Leveraging OpenAI's API to explore prompt engineering techniques to streamline requirements development
- Analyze requirement-test case relationships to optimize test case coverage
- Analyze test cases for language consistency and redundancy
- Enhanced traceability matrix by incorporating design linkages within formal requirements to test case trace matrix
- Analyze design to test case relationships to identify potential gaps in test case design

### References
$1.$ The Complete Prompt Engineering for AI Bootcamp (2024)

$2.$ INCOSE Guide to Writing Requirements Revision 4 1 July 2023.