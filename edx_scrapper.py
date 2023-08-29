import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.request import Request, urlopen
from urllib.parse import urlparse
#import csv
import json
from tqdm import tqdm
'''
Scrapper for EdX
'''

# Different sitemaps with the urls to scrap
dictionary = {#'Bachelor': "Online Bachelors's Degrees",
              #'Doctorate': "Online Doctorate Degrees", 
              #'License': "Online License Degrees", 
              #'Master': "Online Master's Degrees", 

              'MicroBachelors': "/microbachelors", 
              'MicroMasters': "/micromasters", 
              'ProfessionalCert': "/professional-certificate", 
              'XSeries': "/xseries"}

domains = {'Subjects': "Courses by Subject", 
              'Topics': "By Topic"}

url = "https://www.edx.org/sitemap"

# We get the list of urls
url_response = requests.get(url)
url_soup1 = BeautifulSoup(url_response.text, 'html.parser')

# For each type of course
for key in dictionary.keys():  
  sec = url_soup1.find('a', href=dictionary.get(key))
  print(key + ' started!')
      
  # We open the csv file to write
  #f = open('edx/' + key + '.csv', 'w', encoding='UTF8', newline='')
  #w = csv.DictWriter(f, fieldnames=['url', 'name', 'topics', 'skills', 'type', 'description'], quoting=csv.QUOTE_ALL)
  #w.writeheader()
  print(key + '.csv created')

  ul = sec.find_next('ul')
  urls = ul.find_all('a')

  x = len(urls)
  print(str(x) + ' items to parse:')
  i=0

  filenames = [f"edx/{key}/{i}.json" for i in range(x)] 
  json_objects = []
  # For each url, we get the information
  for url_tag, filename in tqdm(zip(urls, filenames), total=len(urls), desc=key):
    i = i + 1
    url = 'https://www.edx.org' + url_tag['href']

    url_response = requests.get(url)
    url_soup = BeautifulSoup(url_response.text, 'html.parser')

    try:
      
      language = "English"
      target_svg = url_soup.find('div', {'class': 'at-a-glance'})
      if target_svg:
        containing_div = target_svg.find_parent('div')
        language_tag = containing_div.find('li', string='Associated skills:')
        if language_tag:
          language = language_tag.text
            
      name = url_soup.title.string
      skills_tag = url_soup.find_all('li', {'class': 'topic-item mr-4'})
      
      
      skills = []    
      skills_tag = url_soup.find('div', {'class': 'at-a-glance'})
      if skills_tag:
        skills = skills_tag.text.split(", ")
            
      description = ""
      try:
        description_sec = url_soup.find('h2', string='About this course')
        if description_sec:
          desctext = description_sec.find_next('mt-2 lead-sm html-data')  
          description = desctext.text 
        else:
          description_sec = url_soup.find('div', {'class': 'overview-info'})
          description = description_sec.text
      except:
        description = ""

      
      topics_tag = url_soup.find_all('li', {'class': 'breadcrumb-item'})
      topics = []
      for t in topics_tag:
          topics.append(t.string)
      if 'Catalog' in topics:
        topics.remove('Catalog')
        
      outcomes_tag = url_soup.find('h2', string='What you will learn')
      ul = outcomes_tag.find_next('ul')
      learnings = ul.find_all('li')
      outcomes = []
      for l in learnings:
       outcomes.append(l.text)
      
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
      
      #json_string = json.dumps(row, indent=4)
      
      # We write a new json file with the information scrapped
      with open(filename, 'w') as f:
        f.write(json.dumps(row, indent=4))
        json_objects.append(row)
      
  #    print(str(i) + '/' + str(x) + ': ' + url)

   # If there is any problem, we catch the exception and ignore that url and go for the next one
    except Exception as e:
      print('Problem while parsing ' + url)
      print('An exception occurred: ' + str(e))
      
      
      # We write a new row to the csv file with the information scrapped
      #w.writerow(row)
      print(str(i) + '/' + str(x) + ': ' + url)

    # If there is any problem, we catch the exception and ignore that url and go for the next one
    except:
      print(str(i) + '/' + str(x) + ': ' + 'Problem while parsing ' + url)
          
  print(key + ' ended!')
  
  fjson = open('edx/' + key + 's.json', 'w', encoding='UTF8', newline='')
  json_string = json.dumps(json_objects, indent=4)
  fjson.write(json_string)
  fjson.close()
  print('------------')
    
  # We close the file
  #f.close()
  print('------------')

# Scrapping finished
print('Scrapping finished')