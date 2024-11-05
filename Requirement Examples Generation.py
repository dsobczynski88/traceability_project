from openai import OpenAI
import getpass
from prompts import prompt_R03

#import re
#import pandas as pd
#import csv

class Prompt:

    def __init__(self, client, model, prompt, system=None):
        self.client = client
        self.model = model
        self.prompt = prompt
        self.system = system
        self.response_object = None
        self.response_result = None
        self.messages_list = []
        
    def build_prompt(self):
        
        self.messages_list.append(
            {'role':'user',
             'content':self.prompt}
        )
        if self.system is not None:
            self.messages_list.append(
                {'role':'system',
                 'content':self.system}
            )
        return self.messages_list
    
    def show_prompt(self):
        print(self.messages_list)
    
    def create_response_object(self):
        self.response_object = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages_list
        )
    
    def get_response(self):
        self.build_prompt()
        self.show_prompt()
        self.create_response_object()
        self.response_result = self.response_object.choices[0].message.content
    
    def show_response(self):
        print(self.response_result)

    def run(self):
        self.show_prompt()
        self.get_response()
        self.show_response()
        return self.response_result

secret_key = getpass.getpass("Please enter your OpenAI Key:")
openai_client = OpenAI(api_key=secret_key)

print(f'Running prompt:\n {prompt_R03.__doc__}')
new_prompt = Prompt(openai_client, 'gpt-4',prompt_R03())
new_prompt.run()
print('---------------------------------------')


#output below
"""
Attribute: Necessary (C1)
Application Description: Building a new eCommerce website for an electronic store.
Requirements Meeting Attribute: The website shall support a customer login feature to track orders | The website shall provide a search function for customers to find products | The website shall be able to process online payments through Visa, Mastercard, and Paypal.
Requirements Not Meeting Attribute: The website shall have a function for customers to play games | The website shall include a virtual mascot that interacts with customers | The website shall have a feature for customers to view the business owner's blog posts.

Attribute: Appropriate (C2)
Application Description: Developing a mobile banking application.
Requirements Meeting Attribute: The application shall provide a function for customers to check their account balance | The application shall have an option for customers to transfer funds between accounts | The application shall include a feature for setting up recurring payments.
Requirements Not Meeting Attribute: The application shall use machine learning algorithms | The application’s user interface shall have blue and white color scheme | The application shall be developed using JavaScript.

Attribute: Unambiguous (C3)
Application Description: Creating a new software for inventory management.
Requirements Meeting Attribute: The software shall be able to track the stock level of each item | The software shall have a function for users to generate inventory reports | The software shall alert users when an item's stock level falls below a certain threshold.
Requirements Not Meeting Attribute: The software should be easy to use | The software has to be fast | The software ought to look attractive.

Attribute: Complete (C4)
Application Description: Designing a new security system for a building.
Requirements Meeting Attribute: The system shall require a unique access code for each user | The system shall feature an alarm that is triggered by unauthorized access | The system shall log all access attempts and times in a database.
Requirements Not Meeting Attribute: The system shall be modern | The system shall be installed in all entrances | The system should work all the time.

Attribute: Singular (C5)
Application Description: Manufacturing a new smartphone model.
Requirements Meeting Attribute: The smartphone shall have a battery life of at least 12 hours | The smartphone's camera resolution shall be 12 megapixels | The smartphone shall have an internal memory capacity of at least 64GB.
Requirements Not Meeting Attribute: The smartphone must be lightweight and have a long battery life | The smartphone should have a camera with high resolution and good zoom capabilities | The smartphone should have a good capacity for apps and a strong processor.

Attribute: Feasible (C6)
Application Description: Constructing a new hospital building.
Requirements Meeting Attribute: The hospital shall have at least 100 patient rooms | The hospital shall include a pharmacy on the ground floor | The hospital shall meet all city safety codes and regulations. 
Requirements Not Meeting Attribute: The hospital shall be built within a month | The hospital shall be powered solely by renewable energy | The hospital shall include a helipad on the roof.

Attribute: Verifiable/Validatable (C7)
Application Description: Developing a new project management software.
Requirements Meeting Attribute: The software shall allow users to track the status of each project | The software shall have an option for users to assign tasks to other team members | The software shall allow users to input deadlines and send reminders.
Requirements Not Meeting Attribute: The software should be efficient | The software should be reliable | The software should be enjoyable to use.

Attribute: Correct (C8)
Application Description: Building a website for a travel agency.
Requirements Meeting Attribute: The website shall feature a booking tool for users to reserve flights and hotels | The website shall display a list of top travel destinations sorted by popularity | The website's design shall be mobile-friendly.
Requirements Not Meeting Attribute: The website shall include a virtual flight simulator game | The website should have social media integration with platforms like Instagram and Twitter | The website shall publish original articles on travel news.

Attribute: Conforming (C9)
Application Description: Creating a new database software.
Requirements Meeting Attribute: The software shall support SQL queries | The software shall provide backup and restore features for each database | The software shall have an option for users to define custom data types.
Requirements Not Meeting Attribute: The software shall be affordable | The software should be the best in the market | The software should always work without any issue.
"""