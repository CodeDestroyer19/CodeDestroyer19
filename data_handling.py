import re
import openai
from bs4 import BeautifulSoup

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
YYou are a helpful data quality assistant that is tasked with extracting contact 
information from unstructured data provided from an email in our database. 
From the string below, please extract any of the following fields that you find.

Desired Fields:
- Client email as client_email
- First Name as client_first_name
- Last Name as client_last_name
- Client phone number as client_phone_number
- Full Address as address
- Client ID (is between 7 and 9 digits usually at the bottom) as client_id
- If products are detected, organize them in an array where only the first product is displayed and it's values are stored. disregard the rest.

Save it in json format.

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


# # Print the JSON data
print(string_data)
