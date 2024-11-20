def req_attr_template(requirements, name, definition, rationale, examples):

    return f"""
    Instructions
    ---
    Step 1 - The user will hand over a numerical list of Requirements enclosed within triple $.
    Step 2 - The user will hand over an article which defines a specific requirement attribute, the rationale and examples of requirements which effectively meet and do not meet the attribute. The article will be provided in HTML div tags.
    Step 3 - Describe ways to improve the Step 1 requirements based on the provided article in div tags, highlighting how attributes were met or not met. 
    Step 4 - Return the Step 4 description for each requirement in a pipe-separated list.

    Example output
    ---
    Requirement|Analysis
    The application shall allow the user to browse the pizza menu with available categories such as pizzas, sides, and drinks. | This requirement is Specific, Measurable, Achievable, Relevant, and Time-bound (SMART). The goal, the user being able to browse the menu, is precise and measurable from development testing. It is technically feasible, directly related to user experience, and can be implemented within a given timeline.
    
    Rules
    ---
    For the Step 4 analysis of each requirement, be sure to elaborate on your reasoning.
    Return only the results of Step 4

    $$$
    {requirements}
    $$$

    <div>
    Attribute: {name}
    Definition: {definition}
    Rationale: {rationale}
    Examples: {examples}
    </div>       
    """