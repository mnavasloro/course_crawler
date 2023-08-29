import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from urllib.parse import urlparse
import csv
import json
#import multiprocessing
from tqdm import tqdm
'''
Scrapper for Coursera
'''

# For each url, we get the information
def process_url(url_tag, filename):
  #for url_tag in urls[:100]:
  #  i = i + 1
    url = url_tag.text

    url_response = requests.get(url)
    url_soup = BeautifulSoup(url_response.text, 'html.parser')


    try:      
      
      language = "UNK"
      target_svg = url_soup.find('path', {'d': 'M5.818 2.499a3.13 3.13 0 00-3.32 3.346l.002.017V20.53l-.003.029a.84.84 0 001.447.671l3.987-4.309H18.18a3.14 3.14 0 003.32-3.32V5.862l.001-.017a3.13 3.13 0 00-3.32-3.346l-.015.001H5.834l-.016-.001zm.047-.999A4.13 4.13 0 001.5 5.897v14.576a1.84 1.84 0 003.175 1.438l.002-.001 3.692-3.99h9.767a4.14 4.14 0 004.364-4.364V5.897A4.13 4.13 0 0018.135 1.5H5.865z'})
      if target_svg:
        containing_div = target_svg.find_parent('div')
        language_tag = containing_div.find('div', {'class': 'cds-119 css-xv7mc6 cds-121'})
        if language_tag:
          language = language_tag.text
        else:
          pass
      else:
        pass
      
      name = url_soup.title.string
      skills_tag = url_soup.find_all('span', {'class': 'cds-119 css-18p0rob cds-121'})
      skills = []
      for s in skills_tag:
          skills.append(s.string)

      description = ""
      description_tagup = url_soup.find('div', {'class': 'about-section'})
      if description_tagup:
        description_tag = description_tagup.find('div', {'class': 'content-inner'})
        if description_tag:
            description = description_tag.text
            #description = description.replace('\n', '\\n').replace('\r', '\\r')

      topics_tag = url_soup.find_all('a', {'class': 'cds-119 cds-113 cds-115 cds-breadcrumbs-link css-1e18p6c cds-142'})
      topics = []
      for t in topics_tag:
          topics.append(t.string)
      if 'Browse' in topics:
        topics.remove('Browse')

      
      outcomes_tag = url_soup.find_all('div', {'class': 'css-88ryvb'})
      outcomes = []
      for o in outcomes_tag:
          p = o.find('div', {'class': 'css-1kgqbsw'})
          outcomes.append(p.string)
      
      
      row = {
                  'url': url,
                  'name': name,
                  'topics' : topics,
                  'skills': skills,
                  #'type': key,
                  'description': description,
                  'language': language,
                  'outcomes': outcomes,
              }
      
      json_string = json.dumps(row, indent=4)
      
      # We write a new json file with the information scrapped
      with open(filename, 'w') as f:
        f.write(json_string)
      
  #    print(str(i) + '/' + str(x) + ': ' + url)

   # If there is any problem, we catch the exception and ignore that url and go for the next one
    except Exception as e:
      print('Problem while parsing ' + url)
      print('An exception occurred: ' + str(e))


if __name__ == '__main__':
  
  # Different sitemaps with the urls to scrap
  dictionary = {'course': "https://www.coursera.org/sitemap~www~courses.xml",
                'certificate': "https://www.coursera.org/sitemap~www~professional-certificate.xml", 
                'specialization': "https://www.coursera.org/sitemap~www~onDemandSpecializations.xml", 
                'mastertrack': "https://www.coursera.org/sitemap~www~mastertrack.xml", 
                'project': "https://www.coursera.org/sitemap~www~guided-projects.xml"}
  
  # For each type of course
  for key in dictionary.keys():
      
    print(key + 's started!')
    url = dictionary.get(key)

    # We get the list of urls
    response = urllib.request.urlopen(url)
    xml = BeautifulSoup(response, 
                            'lxml-xml', 
                            from_encoding=response.info().get_param('charset'))
    urls = xml.find_all("loc")

    x = len(urls)
    print(str(x) + ' items to parse:')
    
    filenames = [f"coursera/{key}/{i}.json" for i in range(x)]    
    # with multiprocessing.Pool() as pool:
    #   pool.starmap(process_url, zip(urls, filenames))
    
    # with multiprocessing.Pool() as pool:
    #   for _ in tqdm(pool.imap_unordered(process_url, zip(urls, filenames), chunksize=1), total=len(filenames), desc=key):
    #     pass
      
    for url_tag, filename in tqdm(zip(urls, filenames), total=len(urls), desc=key):
      process_url(url_tag, filename)
        
    print(key + ' ended!')

    json_objects = []
    for filename in filenames:
      try:
        with open(filename, 'r') as file:
            data = json.load(file)
            json_objects.append(data)
      except:
        print("Error in file: ", filename)
    
    # We open the json file to write
    fjson = open('coursera/' + key + 's.json', 'w', encoding='UTF8', newline='')
    json_string = json.dumps(json_objects, indent=4)
    fjson.write(json_string)
    fjson.close()
    print('------------')

  # Scrapping finished
  print('Scrapping finished') 