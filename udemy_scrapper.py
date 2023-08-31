import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import csv
from tqdm import tqdm
import json
'''
Scrapper for Udemy
'''

# Different sitemaps with the urls to scrap
dictionary = {'courses': "https://www.udemy.com/sitemap/courses.xml"}

# domains = {'category': "https://www.udemy.com/sitemap/category.xml", 
#               'subcategory': "https://www.udemy.com/sitemap/subcategory.xml", 
#               'topics': "https://www.udemy.com/sitemap/topic.xml", 
#               'ptopics': "https://www.udemy.com/sitemap/preset_topics.xml"}

url = "https://www.udemy.com/sitemap.xml"

# We get the list of urls
url_response1 = requests.get(url)
url_soup1 = BeautifulSoup(url_response1.text, 'html.parser')

j=34156

# For each type of course
for key in dictionary.keys():  

  print(key + ' started!')

  
  # We get the list of urls
  response = requests.get(url)#urllib.request.urlopen(url)
  xml = BeautifulSoup(response.text, 
                          'lxml-xml')
  urls = xml.find_all("loc")

  urls = [u.text for u in urls if dictionary.get(key) in u.text]
      
  # We open the csv file to write
  #f = open('udemy/' + key + '.csv', 'w', encoding='UTF8', newline='')
  #w = csv.DictWriter(f, fieldnames=['url', 'name', 'topics', 'skills', 'type', 'description'], quoting=csv.QUOTE_ALL)
  #w.writeheader()
  #print(key + '.csv created')

  x = len(urls)
  print(str(x) + ' items to parse:')
  i=0

  json_objects = []
  urls = urls[i:]
  # For each url, we get the information
  for url_tag2 in urls:
    i = i + 1
    response2 = requests.get(url_tag2)
    xml2 = BeautifulSoup(response2.text, 
                          'lxml-xml')
    courses_urls = xml2.find_all("loc")

    # if i<169:
    #   j = j + 100
    #   print(j)
    #   continue
      
    y=len(courses_urls)
    if y==0:
      print("0 from ", i)
      break
    for url_tag in tqdm(courses_urls, total=len(courses_urls), desc=str(i)+'/'+str(x)):
      j = j + 1
      
      # if j<33699:
      #   print(j)
      #   continue
      url = url_tag.text
      url_response = requests.get(url)
      url_soup = BeautifulSoup(url_response.text, 'html.parser')

      try:      
        name = url_soup.title.string
        skills_tag = url_soup.find_all(class_=lambda class_: class_ and class_.startswith("what-you-will-learn--objective-item"))
        
        skills = []
        for s in skills_tag:
            skills.append(s.string)

        description = ''
        try:
          description_sec = url_soup.find('div', {'data-purpose':"course-description"})
          l = description_sec.find('div', {'class':"show-more-module--container--2QPRN"})
          description = l.text
        except:
          description = ''
        
        topics_tag = url_soup.find_all('a', {'class': 'udlite-heading-sm'})
        topics = []
        for t in topics_tag:
            topics.append(t.string)
            
        language = url_soup.find('div', {'class': 'clp-lead__element-item clp-lead__locale'})
        language = language.text
        
        outcome_t = url_soup.find('div', {'data-purpose':"course-description"})
        learnings = outcome_t.find_all('p')
        outcomes = []
        for l in learnings:
          outcomes.append(l.text)
                
        # We write a new row to the csv file with the information scrapped
        #w.writerow(row)
        #print(str(j) + '/' + str(y) + '| ' + str(i) + '/' + str(x) + ': ' + url)
        
        row = {
                    'url': url,
                    'name': name,
                    'topics' : topics,
                    'skills': skills,
                    'type': key,
                    'description': description,
                    'language': language,
                    'outcomes': outcomes,
                }
        
        json_string = json.dumps(row, indent=4)
        json_objects.append(row)
        
        # We write a new json file with the information scrapped
        with open(f"udemy/courses/{j}.json", 'w') as f:
          f.write(json_string)

      # If there is any problem, we catch the exception and ignore that url and go for the next one
      except Exception as e:
        print(str(j) + '/' + str(y) + '| ' + str(i) + '/' + str(x) + ': ' + 'Problem while parsing ' + url)
        print('An exception occurred: ' + str(e))
          
  print(key + ' ended!')
  # We close the file
  #f.close()
  # fjson = open('udemy/' + key + 's.json', 'w', encoding='UTF8', newline='')
  # json_string = json.dumps(json_objects, indent=4)
  # fjson.write(json_string)
  # fjson.close()
  print('------------')

# Scrapping finished
print('Scrapping finished')