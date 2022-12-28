import virginia_cities
import pandas as pd
import numpy as np
import csv
import requests
from bs4 import BeautifulSoup


#import craigslist Virginia pages based on city/region
cities = virginia_cities.get_city_urls()

list_of_cities = []

for city in cities:
    # each city has approxiamtely 1800 pages for the "cars for sale by owner" category
    page_number = 1
    # this while loop cycles through all 1800 pages
    while(page_number <= 1800):
        # city_link variable takes a a different city name from the cities every time through the loop
        city_link = str(city) +"/search/cta?s=" + str(page_number)                  
        list_of_cities.append(city_link)
        page_number +=120
        
print(list_of_cities)
city_links = []

car_urls = 1 
     
for each_city_page in list_of_cities:  
      
    links_in_each_city_page = requests.get(each_city_page)
    
    if(links_in_each_city_page):
        soup = BeautifulSoup(links_in_each_city_page.content, 'html.parser')

        try:
            #get the macro-container for the car posts for that page
            posts = soup.find_all('a', class_= 'result-image gallery')

            # get all the html links in the page and append them to a list
            for link in posts:
                l = link.get('href')
                print(l)
                city_links.append(l)                                
        except:
            pass                            
        
print(len(city_links))
df = pd.DataFrame(city_links)
df.to_csv("./links.csv", sep=',',index=False)