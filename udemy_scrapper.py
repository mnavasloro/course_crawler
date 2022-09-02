import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import csv
'''
Scrapper for Udemy
'''

# Different sitemaps with the urls to scrap
dictionary = {'courses': "https://www.udemy.com/sitemap/courses.xml"}

domains = {'category': "https://www.udemy.com/sitemap/category.xml", 
              'subcategory': "https://www.udemy.com/sitemap/subcategory.xml", 
              'topics': "https://www.udemy.com/sitemap/topic.xml", 
              'ptopics': "https://www.udemy.com/sitemap/preset_topics.xml"}

url = "https://www.udemy.com/sitemap.xml"

# We get the list of urls
url_response1 = requests.get(url)
url_soup1 = BeautifulSoup(url_response1.text, 'html.parser')

# For each type of course
for key in dictionary.keys():  

  print(key + ' started!')

  # We get the list of urls
  response = urllib.request.urlopen(url)
  xml = BeautifulSoup(response, 
                          'lxml-xml', 
                          from_encoding=response.info().get_param('charset'))
  urls = xml.find_all("loc")

  urls = [u.text for u in urls if dictionary.get(key) in u.text]
      
  # We open the csv file to write
  f = open('udemy/' + key + '.csv', 'w', encoding='UTF8', newline='')
  w = csv.DictWriter(f, fieldnames=['url', 'name', 'topics', 'skills', 'type', 'description'], quoting=csv.QUOTE_ALL)
  w.writeheader()
  print(key + '.csv created')

  x = len(urls)
  print(str(x) + ' items to parse:')
  i=0

  # For each url, we get the information
  for url_tag2 in urls:
    i = i + 1
    response2 = urllib.request.urlopen(url_tag2)
    xml2 = BeautifulSoup(response2, 
                          'lxml-xml', 
                          from_encoding=response2.info().get_param('charset'))
    courses_urls = xml2.find_all("loc")
    j=0
    y=len(courses_urls)
    for url_tag in courses_urls:
      j = j + 1
      url = url_tag.text
      url_response = requests.get(url)
      url_soup = BeautifulSoup(url_response.text, 'html.parser')

      try:      
        name = url_soup.title.string
        skills_tag = url_soup.find_all('span', {'class': 'what-you-will-learn--objective-item--ECarc'})
        skills = []
        for s in skills_tag:
            skills.append(s.string)

        description_sec = url_soup.find('div', {'data-purpose':"course-description"})
        learnings = description_sec.find_all('p')
        description = ''
        for l in learnings:
          description = description + l.text + '\\n'
        description = description.replace('\n', '\\n').replace('\r', '\\r').encode('utf-8')
        
        topics_tag = url_soup.find_all('a', {'class': 'udlite-heading-sm'})
        topics = []
        for t in topics_tag:
            topics.append(t.string)

        row = {
                    'url': url,
                    'name': name,
                    'topics' : topics,
                    'skills': skills,
                    'type': key,
                    'description': description,
                }
        # We write a new row to the csv file with the information scrapped
        w.writerow(row)
        print(str(j) + '/' + str(y) + '| ' + str(i) + '/' + str(x) + ': ' + url)

      # If there is any problem, we catch the exception and ignore that url and go for the next one
      except:
        print(str(j) + '/' + str(y) + '| ' + str(i) + '/' + str(x) + ': ' + 'Problem while parsing ' + url)
          
  print(key + ' ended!')
  # We close the file
  f.close()
  print('------------')

# Scrapping finished
print('Scrapping finished')