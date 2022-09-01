import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.parse import urlparse

url = "https://www.coursera.org/sitemap~www~courses.xml"
response = urllib.request.urlopen(url)
xml = BeautifulSoup(response, 
                         'lxml-xml', 
                         from_encoding=response.info().get_param('charset'))
urls = xml.find_all("loc")

df = pd.DataFrame(columns=['url', 'name', 'topics', 'skills', 'description'])

x = len(urls)
print(x)
i=0

for url_tag in urls:
  i = i + 1
  url = url_tag.text

  url_response = requests.get(url)
  url_soup = BeautifulSoup(url_response.text, 'html.parser')
  name = url_soup.title.string

  try:
    skills_tag = url_soup.find_all('span', {'class': '_ontdeqt'})
    skills = []
    for s in skills_tag:
        skills.append(s.string)

    description_tag = url_soup.find('div', {'class': 'description'})
    description = description_tag.text

    topics_tag = url_soup.find_all('a', {'data-track-component': 'breadcrumb_link'})
    topics = []
    for t in topics_tag:
        topics.append(t.string)
    topics.remove('Browse')

    row = {
                'url': url,
                'name': name,
                'topics' : topics,
                'skills': skills,
                'description': description,
            }

    df = df.append(row, ignore_index=True)
    print(str(i) + '/' + str(x) + ': ' + url)

  except:
    print('Problem while parsing ' + url)

df.to_csv('output_coursera.csv')
print('Ended!')
