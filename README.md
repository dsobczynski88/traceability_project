# *reqtracer* 
**Applying NLP and data science to software quality processes** 

### Inspiration
My inspiration for this project began during a career change into software quality. My goal is to look for ways to improve software development documentation with the broader goal to improve product quality. I hope that others find this work to be useful in their personal or professional experience. 

### Project Description
This project applies NLP and data science tools with the goal to improve software quality artifact reviews -- specifically regarding traceability. This project intends to perform the following functions:

1. Analyze requirement-test case relationships to optimize test case coverage
2. Analyze test cases for language consistency and redundancy
3. Enhanced traceability matrix by incorporating design linkages within formal requirements to test case trace matrix
4. Analyze design to test case relationships to identify potential gaps in test case design*
*Currently in progress

### Technologies used
This project is written in Python. The choice of Python is based on its broad-range support from the data science and AI community.

### Challenges faced and outlook ahead
TBD

### Getting Started
TBD

#### How to install the project (Windows)
TBD

### Intended Use
This project is intended to be used during the software development process to analyze relationships between requirements and test artifacts. The goal of this analysis is to assist software quality engineers in their review of test cases to identify inconsistent, absent, or incorrect relationships. In future development, this is desired to be expanded to tie design descriptions into the analysis to determine whether test cases fully test the requirement in a way which aligns with the specified design outputs.

### Credits
Would like to thank all my colleagues I've gotten to work with over these initial 12 months in this software quality role. 

### Future Work
- **Prompt Engineering for Identifying Inconsistencies or areas of improvement during documentation reviews**
    - Leverage LLMs to explore prompt engineering approaches to supplement test and requirement reviews
	- For highly similar test cases, apply Prompt Engineering with LLMs to create a “consolidated” test case
    - Use case for this could be regression testing for software post initial launch as there would be a baseline dataset to use for creating the model