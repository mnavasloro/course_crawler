import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.parse import urlparse
import csv


dictionary = {'certificate': "https://www.coursera.org/sitemap~www~professional-certificate.xml", 
              'specialization': "https://www.coursera.org/sitemap~www~onDemandSpecializations.xml", 
              'course': "https://www.coursera.org/sitemap~www~courses.xml",
              'mastertrack': "https://www.coursera.org/sitemap~www~mastertrack.xml", 
              'project': "https://www.coursera.org/sitemap~www~guided-projects.xml"}
# url = 

for key in dictionary.keys():
    
  print(key + ' started!')
  url = dictionary.get(key)

  response = urllib.request.urlopen(url)
  xml = BeautifulSoup(response, 
                          'lxml-xml', 
                          from_encoding=response.info().get_param('charset'))
  urls = xml.find_all("loc")
  
  f = open(key + 's.csv', 'w', encoding='UTF8', newline='')
  w = csv.DictWriter(f, fieldnames=['url', 'name', 'topics', 'skills', 'type', 'description'], quoting=csv.QUOTE_ALL)
  w.writeheader()
  print(key + 's.csv created')
  x = len(urls)
  print(str(x) + ' items to parse:')
  i=0

  for url_tag in urls:
    i = i + 1
    url = url_tag.text

    url_response = requests.get(url)
    url_soup = BeautifulSoup(url_response.text, 'html.parser')

    try:      
      name = url_soup.title.string
      skills_tag = url_soup.find_all('span', {'class': '_ontdeqt'})
      skills = []
      for s in skills_tag:
          skills.append(s.string)

      description_tag = url_soup.find('div', {'class': 'description'})
      description = description_tag.text
      description = description.replace('\n', '\\n').replace('\r', '\\r').encode('utf-8')

      topics_tag = url_soup.find_all('a', {'data-track-component': 'breadcrumb_link'})
      topics = []
      for t in topics_tag:
          topics.append(t.string)
      if 'Browse' in topics:
        topics.remove('Browse')

      row = {
                  'url': url,
                  'name': name,
                  'topics' : topics,
                  'skills': skills,
                  'type': key,
                  'description': description,
              }

      w.writerow(row)
      print(str(i) + '/' + str(x) + ': ' + url)

    except:
      print('Problem while parsing ' + url)
       
  print(key + ' ended!')
  f.close()
  print('------------')

print('Scrapping finished')