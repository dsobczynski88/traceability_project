def single_attribute_review(requirements, context):
    """
    This prompt template takes in a list of requirements and an INOCSE description of a particular requirement attribute.
    """

    return f"""
    Instructions
    ---
    Step 1 - The user will hand over a python list of Requirements.
    Step 2 - The user will hand over Context which describes a specific feature of well-written requirements
    Step 3 - Analyze the requirement of the python list provided in Step 1 using the Context provided in Step 2. Specifically, the analysis should review the Requirement against the Context and look for opportunities for improvement to align with the Context.
    
    Rules
    ---
    Return a python list of lists which contains the results of Step 3 for each requirement. Specifically, each list element of the must be a list containing the results from the Step 3 analysis as described in Response Format.
    
    Response Format:
    [
        [Requirement A, Review of Requirement A using Context],
        [Requirement B, Review of Requirement B using Context],
        [Requirement C, Review of Requirement C using Context],
        [...]
    ]

    Requirements: 
    {requirements}

    Context:
    {context}
    """

def naive_ambiguity_review(requirements):

    return f"""
    Instructions
    ---
    Step 1 - The user will hand over a python list of Requirements.
    Step 2 - The user requests that each requirement be reviewed for ambiguity
    Step 3 - Analyze the requirement of the python list provided in Step 1 per the request in Step 2. Specifically, the analysis should review the Requirement for areas of ambiguity and look for opportunities for improvement.
    
    Rules
    ---
    Return a python list of lists which contains the results of Step 3 for each requirement. Specifically, each list element of the must be a list containing the results from the Step 3 analysis as described in Response Format.
    
    Response Format:
    [
        [Requirement A, Review of Requirement A],
        [Requirement B, Review of Requirement B],
        [Requirement C, Review of Requirement C],
        [...]
    ]

    Requirements: 
    {requirements}
    """

def summarize(review):

    return f"""
    Instructions
    ---
    Step 1 - The user will hand over a detailed requirement Review enclosed within triple $$$.
    Step 2 - Summarize the review.

    Rules
    ---
    Return only the summarized review

    Review:
    $$$
    {review}
    $$$
    """

def revise(requirements, context):

    return f"""
    Instructions
    ---
    Step 1 - The user will hand over a python list of Requirements.
    Step 2 - The user will hand over a python list of Reviews where each revire corresponds to each requirement in Requirements
    Step 3 - For each of the Requirements, use the corresponding review in Reviews to propose a revised requirement. 
    
    Rules
    ---
    Return a python list of lists which contains the results of Step 3 for each requirement. Specifically, each list element of the must be a list containing the results from the Step 3 analysis as described in Response Format.
    
    Response Format:
    [
        [Requirement A, Revised Requirement A],
        [Requirement B, Revised Requirement B],
        [Requirement C, Revised Requirement C],
        [...]
    ]

    Requirements: 
    {requirements}

    Reviews:
    {context}
    """