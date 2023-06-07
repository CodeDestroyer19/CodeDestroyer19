import re
import openai
from bs4 import BeautifulSoup
import json

openai.api_key = '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'


with open('newhtml.html', 'r') as f:
    dataSet = f.read()

# The HTML email content
html_content = dataSet

# Create BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Extract text from html file

def extract_text_from_html():
    text = soup.get_text()
    # Remove extra whitespaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Find the relevant elements and extract the data
data = {}
string_data = extract_text_from_html()
basic_prompt_discription = f'''
You are a data quality assistant tasked with extracting 
contact information and product details from an email in your database. 
Your goal is to extract the following fields:

-Client email as client_email
-First Name as client_first_name
-Last Name as client_last_name
-Client phone number as client_phone_number
-Full Address as address
-Client ID (a 7 to 9-digit number usually found at the bottom) as client_id
-If products are detected, organize them in an array where only the first product is displayed, and its values are stored. Disregard the rest, but refer to the "Code" field as product_id.

Using the provided unstructured data from an email in your database, extract the required fields and present the result in JSON format.
Ensure that you correctly identify the client details and avoid confusing them with the emailer's details.

Here is the string: {string_data}
'''


def process_natural_language(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=10000,
        n=1,
        stop=None,
        temperature=0.7
    )

    if 'choices' in response and len(response.choices) > 0:
        return response.choices[0].text.strip()

    return None

#Response JSON DATA from natural language processer
response_data = {
  "client_email": "c.goulon@ginge-kerr.lu",
  "client_first_name": "Christophe",
  "client_last_name": "GOULON",
  "client_phone_number": "",
  "address": "46 ZAE Le Triangle Vert, 5691 ELLANGE, Luxembourg",
  "client_id": "",
  "products": [
    {
      "product_id": "20000000100011160",
      "quantity": "1",
      "name": "Zoll AED Plus défibrillateur semi-automatique",
      "description": ""
    }
  ]
}

#Check if important values are present
def check_client_id(data):
    if 'client_id' in data and data['client_id']:
        return True
    else:
        return False

has_client_id = check_client_id(response_data)
print(has_client_id)  # Output: True

#Remove any empty fields not found in the email
def remove_empty_fields(data):

    def remove_empty(obj):
        if isinstance(obj, dict):
            return {key: remove_empty(value) for key, value in obj.items() if value != ''}
        elif isinstance(obj, list):
            return [remove_empty(item) for item in obj if item != '']
        else:
            return obj

    cleaned_data = remove_empty(data)

    return cleaned_data

cleaned_json_data = remove_empty_fields(response_data)

# # Print the JSON data
print(cleaned_json_data)
