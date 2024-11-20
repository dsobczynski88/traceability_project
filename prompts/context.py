"""
The 
"""

DELIMITER_1 = "|"
DELIMITER_2 = "$"


attr_list = "Necessary (C1)|Appropriate (C2)|Unambiguous (C3)|Complete (C4)|Singular (C5)|Feasible (C6)|Verifiable/Validatable (C7)|Correct (C8)|Conforming (C9)".split(DELIMITER_1)

attr_def_list = "The need statement or requirement statement defines capability, characteristic, constraint, or quality factor needed or required to satisfy a lifecycle concept, need, source, or higher-level requirement.|The specific intent and amount of detail of the need or requirement statement is appropriate to the level (the level of abstraction, organization, or system architecture) of the entity to which it refers.|Need statements and requirement statements must be stated such that their intent is clear and can be interpreted in only one way by all the intended audiences.|The need statement sufficiently describes the necessary capability, characteristic, constraint, conditions, or quality factor to meet the lifecycle concept or source from which it was transformed. The requirement statement sufficiently describes the necessary capability, characteristic, constraint, conditions, or quality factor to meet the need, source, or higher-level requirement from which it was transformed.|The need statement or requirement statement should state a single capability, characteristic, constraint, or quality factor.|The need or requirement can be realized within entity constraints (for example: cost, schedule, technical, legal, ethical, safety) with acceptable risk.|The need statement is structured and worded such that its realization can be validated to the approving authority’s satisfaction. The requirement statement is structured and worded such that its realization can be verified to the approving authority’s satisfaction.|The need statement must be an accurate representation of the lifecycle concept or source from which it was transformed. The requirement statement must be an accurate representation of the need, source, or higher level requirement from which it was transformed.|Statements and expressions of individual needs and requirements should conform to an approved standard pattern and style guide or standard for writing and managing needs and requirements.".split(DELIMITER_1)

attr_rat_list = """
    If the statement under review is not included in the set of needs or set of requirements, a deficiency in capability or characteristic will exist which cannot be fulfilled by implementing other needs or requirements in the set. Realization of every need and requirement requires resources, effort, and cost in the form of development, review, management, implementation, design verification, design validation, system verification, system validation, maintenance, and disposal. Unnecessary needs and requirements can lead to non-value-added work, additional cost, and unnecessary risk. Unnecessary needs or requirements inappropriately constrain the available solution space and cause extra program expense for developing, managing, implementing, verifying the unnecessary requirements, and validating the unnecessary needs. In the worst case, unnecessary needs or requirements may over-constrain and compromise the overall SOI performance, leading to infeasible solutions which fail to satisfy necessary needs and resulting requirements. Including unnecessary needs and requirements may also result in a set of needs or set of requirements that is not Feasible (C12). A need or requirement is not necessary (not needed in the set of needs or set of requirements) if the: • need or requirement can be removed, and the remaining set will still result in the entity’s lifecycle concept or needs being satisfied; • intent of the need or requirement will be met by the implementation of other needs or requirements; • need or requirement cannot be traced back to a source, need, or higher-level requirement; or • author cannot communicate a valid reason (rationale) for the need or requirement.
    | The wording of needs is often stated at a higher level of abstraction than is appropriate for a requirement. See the example under R31. As shown in Figure 9, levels can also refer to levels within an organization or levels within an architecture—system, subsystems, or system elements. Needs and requirements may be defined at any level of the organization or system architecture; however, as a rule, a need or requirement should be expressed at the level of the entity to which it refers, and that entity must be able to be validated or verified to have met the need or requirement at that level. Requirements for lower-level entities stated within the requirements set for a higher-level entity may seem like implementation. When design details are stated as design inputs, there is often no definition of the “why” and what the parent requirement is that the design detail requirement is addressing. In this case, the real higher-level entity requirement may not be stated and thus not properly allocated to the next lower-level entities. When this is the case, the requirement should be moved down to the appropriate level entity set of requirements and the missing parent requirement added to the higher-level entity’s set of requirements. Conversely, higher level entity requirements stated improperly within a lower-level entity’s set of requirements may not have been allocated properly to the other entities at the next level of the architecture, resulting in missing child requirements for those entities. A need or requirement stated at the wrong level for an entity is either not Correct (C8) or may not be verifiable/ validatable (C7) at that level. Refer to the NRM for an in-depth discussion on levels.
    |A need statement and a requirement statement must lend itself to a single interpretation of intent. These statements are effectively an agreement between two parties communicating intent from one to the other and forming the basis of verification and validation that the intent was met. An agreement is difficult to enact unless both parties are clear on the exact obligation. Ambiguity leads to interpretations of a need or requirement not intended by the author leading to problems such schedule slips, budget overruns, or a failure of the SOI to pass system validation and not be accepted for its intended use; which could result in litigation and financial loss. An ambiguous need or requirement is neither Correct (C8) nor Verifiable/Validatable (C7).
    |An agreement is not useful unless the obligation is complete and does not need further 
    explanation. A well-formed need statement needs no further amplification to implement its intent and to define 
    system validation success criteria, method, and approach. A well-formed requirement statement needs no further amplification to implement its intent and to 
    define system verification success criteria, method, and approach.  Examples include: • Functional requirements must include a performance characteristic to be complete and 
    verifiable.  This can result in multiple requirements for a function, each with a different performance characteristic. 
    • Interface requirements should include a reference to the location of the agreement that 
    defines how the entity needs to interact with the entity to which it interfaces (for example, an 
    Interface Control Document (ICD).   
    • Terms used within a need statement or requirement statement must be defined uniquely and 
    unambiguously within the project glossary or Data Dictionary. 
    • Requirements based on a standard or regulation must clearly communicate what the system 
    must do to meet the intent of the standard or regulation requirement from which it was 
    derived.  
    An incomplete need statement or requirement statement is not Verifiable/Validatable (C7) nor 
    Correct (C8) due to missing information (the need or requirement fails to address either “what”, 
    “how well”, or “under what conditions”).
    
    |The formal transformation from a lifecycle concept into a need can be a many-to-one, one-to-one 
    or a one-to-many transformation, however, the resultant need statement(s) must each represent 
    a single thought, aspect, or expectation.  
    Similarly, the formal transformation of a need, source, or allocated parent requirement into a 
    requirement can be a many-to-one, one-to-one, or a one-to-many transformation so the resultant 
    requirement statement(s) must each represent a single thought, aspect, or expectation.  
    The effectiveness of several process activities associated with needs and requirements 
    definition—such as decomposition, derivation, allocation, traceability, verification, and 
    validation—depend on being able to identify singular statements.  For instance, the system 
    verification information defined for a requirement can be far more precise when that requirement 
    addresses a single capability, characteristic, constraint, or quality factor.   
    Additionally, when verifying/validating the SOI against a need or requirement with multiple 
    aspects, if one aspect passes, but others fail, it is difficult to assess the verification/validation 
    status of the SOI against that need or requirement as a whole. A need or requirement with 
    multiple thoughts is difficult to allocate and to trace to a higher-level requirement or source. 
    A nonsingular need or requirement is neither Verifiable/Validatable (C7) nor Correct (C8). 
    Requirements patterns are useful ways to ensure singularity since each need or requirement 
    should conform with one and only one pattern (see Appendix C).

    |There is little point in agreeing to an obligation for a need or requirement that is not feasible.  
    Agreeing to a need or requirement that cannot be realized with acceptable risk within constraints 
    often results in project cost overruns and schedule slips.  Inherently unachievable needs and 
    requirements, such as 100% reliability, are at best a waste of time, and at worst lead to 
    needlessly expensive solutions. 
    The need or requirement is considered feasible if, when considered along with other needs or 
    requirements for a single system element (that is, a set of entity needs or requirements), it does 
    not cause an unacceptable cost, schedule, or risk impact during the entity’s lifecycle. 
    An infeasible need or requirement cannot be satisfied because it: 
    a. breaks the laws of physics,  
    b. violates laws or regulations in an applicable jurisdiction,  
    c. conflicts with another requirement and cannot be concurrently satisfied, or 
    d. leads to excessive program risk because of technical immaturity or inadequate margin with 
    respect to program cost and schedule as a function of lifecycle phase. 
    An infeasible need or requirement is neither verifiable (C7) nor correct (C8).

    |Unless a need statement is written in a way that allows requirement validation, design validation, 
    and system validation, there is no way to tell whether it has been satisfied and that the 
    expectation has been met.  
    • Each need statement must include the necessary information such that validation success 
    criteria can be defined, and the SOI can be validated such that sufficient evidence can be 
    gathered to determine whether the success criteria have been met, that is, there is no 
    ambiguity regarding what the need statement communicates and there are no missing 
    characteristics within the need statement, that is, it has the characteristics for well-formed 
    need statements as defined in this Section.  
    • An unvalidatable need can result in multiple, objective observers (for example, requirement 
    writers, architects, designers, or testers) interpreting the need differently making it difficult to 
    validate that the requirement, design, and SOI meets the need.  
    Unless a requirement statement is written in a way that allows design verification and system 
    verification, there is no way to tell if it has been satisfied and that the obligation has been met.  
    • Each requirement statement must include the necessary information such that verification 
    success criteria can be defined, and the SOI can be verified such that sufficient evidence can 
    be gathered to assess whether the success criteria has been met, that is, there is no 
    ambiguity regarding what the requirement statement communicates and there are no missing 
    characteristics within the requirement statement, that is, it has the characteristics for well
    formed requirement statements as defined in this Section.  
    • An unverifiable requirement can result in multiple, objective observers (for example, designers 
    or testers) interpreting the requirement differently, making it difficult to verify the design and 
    SOI meets the requirement.  
    Verifiability and validatability is a necessary condition for establishing the other characteristics of 
    need and requirement statements defined in this Section.  Therefore, verifiability and validatability 
    should be addressed as the initial criterion and a basis for ensuring these other characteristics.

    |Correct implies “no errors” both from the perspective of the inclusion of incorrect information, the 
    omission of required information, and avoidance of ambiguous wording. These aspects are very 
    similar to those in other disciplines such as NLP with the classical human filters of generalization, 
    deletion, and distortion. 
    Incorrect information can mean having the wrong: 
    • values, 
    • functions, 
    • conditions, or  
    • other characteristics identified in the need or requirement. 
    An incorrect need can result in a need that does not reflect the intent of the lifecycle concept or 
    sources from which it was transformed.  An incorrect need can result in incorrect requirements 
    transformed from that need. An incorrect requirement can result in a requirement that does not 
    reflect the intent of the need, source, or higher-level requirement from which it was transformed.   
    The need or requirement cannot be correct if it does not have the characteristics: Necessary 
    (C1), Unambiguous (C3), Complete (C4), Feasible (C6), Verifiable/Validatable (C7), and 
    Conforming (C9).

    |When needs and requirements within the same organization have the same look and feel, each 
    need statement and requirement statement is easier to be written, understood, and reviewed.   
    Further, when conforming to an approved standard, the quality of the individual need statement 
    and requirement statement will improve, as will the quality of the need set, and the requirement 
    set. 
    For the derivation of a need from a lifecycle concept to be formal, the structure of the resultant 
    need statement must also be formal.   
    • For example, all needs may be required to be structured according to a specific pattern 
    defined by the organization for the type of need statement: “The <stakeholders> need the 
    <subject clause> to <action verb clause> <object clause>, <optional qualifying clause>.”   
    For the transformation from a need statement to a requirement statement to be formal, the 
    structure of the resultant requirement statement must also be formal.   
    • For example, all requirement statements may be required to be structured according to a 
    specific pattern defined by the organization for the type of requirement statement: “When 
    <condition clause>, the <subject clause> shall <action verb clause> <object clause>, 
    <optional qualifying clause>.”  
    Conforming to standards and templates for need statements and requirement statements: 
    • provides a template for wording associated with the different types of needs and 
    requirements; 
    • provides consistent wording prevents ambiguity for engineers being exposed to new types of 
    needs and requirements they are managing; and 
    • will help to identify missing information resulting in the characteristics of Complete (C10), 
    Unambiguous (C3) and Verifiable/Validatable (C7). 
    See R1 for more detail on need statements and requirement statements formats and Appendix C 
    for more detailed information on the use of templates and patterns.
    """.split(DELIMITER_1)

attr_exmp_list = """
    Application Description: Building a new eCommerce website for an electronic store.
    Requirements Meeting Attribute: The website shall support a customer login feature to track orders | The website shall provide a search function for customers to find products | The website shall be able to process online payments through Visa, Mastercard, and Paypal.
    Requirements Not Meeting Attribute: The website shall have a function for customers to play games | The website shall include a virtual mascot that interacts with customers | The website shall have a feature for customers to view the business owner's blog posts.$
    Application Description: Developing a mobile banking application.
    Requirements Meeting Attribute: The application shall provide a function for customers to check their account balance | The application shall have an option for customers to transfer funds between accounts | The application shall include a feature for setting up recurring payments.
    Requirements Not Meeting Attribute: The application shall use machine learning algorithms | The application’s user interface shall have blue and white color scheme | The application shall be developed using JavaScript.$
    Application Description: Creating a new software for inventory management.
    Requirements Meeting Attribute: The software shall be able to track the stock level of each item | The software shall have a function for users to generate inventory reports | The software shall alert users when an item's stock level falls below a certain threshold.
    Requirements Not Meeting Attribute: The software should be easy to use | The software has to be fast | The software ought to look attractive.$
    Application Description: Designing a new security system for a building.
    Requirements Meeting Attribute: The system shall require a unique access code for each user | The system shall feature an alarm that is triggered by unauthorized access | The system shall log all access attempts and times in a database.
    Requirements Not Meeting Attribute: The system shall be modern | The system shall be installed in all entrances | The system should work all the time.$
    Application Description: Manufacturing a new smartphone model.
    Requirements Meeting Attribute: The smartphone shall have a battery life of at least 12 hours | The smartphone's camera resolution shall be 12 megapixels | The smartphone shall have an internal memory capacity of at least 64GB.
    Requirements Not Meeting Attribute: The smartphone must be lightweight and have a long battery life | The smartphone should have a camera with high resolution and good zoom capabilities | The smartphone should have a good capacity for apps and a strong processor.$
    Application Description: Constructing a new hospital building.
    Requirements Meeting Attribute: The hospital shall have at least 100 patient rooms | The hospital shall include a pharmacy on the ground floor | The hospital shall meet all city safety codes and regulations. 
    Requirements Not Meeting Attribute: The hospital shall be built within a month | The hospital shall be powered solely by renewable energy | The hospital shall include a helipad on the roof.$
    Application Description: Developing a new project management software.
    Requirements Meeting Attribute: The software shall allow users to track the status of each project | The software shall have an option for users to assign tasks to other team members | The software shall allow users to input deadlines and send reminders.
    Requirements Not Meeting Attribute: The software should be efficient | The software should be reliable | The software should be enjoyable to use.$
    Application Description: Building a website for a travel agency.
    Requirements Meeting Attribute: The website shall feature a booking tool for users to reserve flights and hotels | The website shall display a list of top travel destinations sorted by popularity | The website's design shall be mobile-friendly.
    Requirements Not Meeting Attribute: The website shall include a virtual flight simulator game | The website should have social media integration with platforms like Instagram and Twitter | The website shall publish original articles on travel news.$
    Application Description: Creating a new database software.
    Requirements Meeting Attribute: The software shall support SQL queries | The software shall provide backup and restore features for each database | The software shall have an option for users to define custom data types.
    Requirements Not Meeting Attribute: The software shall be affordable | The software should be the best in the market | The software should always work without any issue.
    """.split(DELIMITER_2)