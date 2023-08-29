import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import requests
#import csv
import json
from tqdm import tqdm
import re
'''
JSON for EdX
'''


url = "https://igsyv1z1xi-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.19.1)%3B%20Browser%20(lite)%3B%20JS%20Helper%20(3.14.0)&x-algolia-api-key=1f72394b5b49fc876026952685f5defe&x-algolia-application-id=IGSYV1Z1XI"

payload = "{\"requests\":[{\"indexName\":\"product\",\"params\":\"clickAnalytics=true&facetFilters=%5B%22product%3ACourse%22%5D&facets=%5B%22availability%22%2C%22language%22%2C%22learning_type%22%2C%22level%22%2C%22partner%22%2C%22product%22%2C%22program_type%22%2C%22skills.skill%22%2C%22subject%22%5D&filters=(product%3A%22Course%22%20OR%20product%3A%22Program%22%20OR%20product%3A%22Executive%20Education%22%20OR%20product%3A%22Boot%20Camp%22%20OR%20product%3A%222U%20Degree%22)%20AND%20NOT%20blocked_in%3A%22TR%22%20AND%20(allowed_in%3A%22null%22%20OR%20allowed_in%3A%22TR%22)&hitsPerPage=2400&query=&tagFilters=\"}]}"
headers = {
  'Content-Type': 'text/plain'
}

response = requests.request("POST", url, headers=headers, data=payload)


data = json.loads(response.text)

json_objects = []

# Accessing values in the parsed JSON
results = data['results']
hits = results[0]['hits']
for r in tqdm(hits):
  try:
    name = r['title']
    url = r['marketing_url']
    #partner = r['partner'][0]
    description = r['primary_description']
    if r['tertiary_description']:
      description = description + '\n' + r['tertiary_description']
    description = re.sub(r'<.*?>', '', description)
    
    outcomes_text = r['secondary_description']
    outcomes_text = re.sub(r'<.*?>', '', outcomes_text)
    outcomes = outcomes_text.split('\n')
    outcomes = [item for item in outcomes if item != ""]
    
    type = r['product']
    topics = []
    if r['subject']:
      for i in r['subject']:
        topics.append(i)
    language = r['language']
    skills = []
    if r['skills']:
      for i in r['skills']:
        skills.append(i['skill'])
      
      
    row = {
                    'url': url,
                    'name': name,
                    'topics' : topics,
                    'skills': skills,
                    'type': type,
                    'description': description,
                    'language': language,
                    'outcomes': outcomes,
                }
    
    json_objects.append(row)
  except Exception as e:
    print('Problem while parsing ' + url)
    print('An exception occurred: ' + str(e))

fjson = open('edx/courses.json', 'w', encoding='UTF8', newline='')
json_string = json.dumps(json_objects, indent=4)
fjson.write(json_string)
fjson.close()

# Scrapping finished
print('Scrapping finished')