import requests
from bs4 import BeautifulSoup 

'''
    Ultimately did not use the get_cities function since
    Craiglist ads are organized by greater regions, not cities
'''
def get_cities():    
    cities = []
    url = 'https://www.virginia-demographics.com/cities_by_population'
    result = requests.get(url)
    content = result.text

    soup = BeautifulSoup(content, 'lxml')
    
    box = soup.find('table', class_="ranklist")
    
    # loop through entries in the table for 'a' tags, which in this case
    # indicate one of the top hundred most populous cities in VA
    for row in box.find_all('td'):
        result = row.find_all('a')
        # append the text within the tag to the list of cities
        for a in result:
            cities.append(a.get_text())
    
    return cities



def get_city_urls():
    city_links = []
    
    # list of craigslist locality links within VA
    url = 'https://geo.craigslist.org/iso/us/VA'
    result = requests.get(url)
    content = result.text

    soup = BeautifulSoup(content, "lxml")
    
    box = soup.find('ul', class_='height3 geo-site-list')
    
    print("The href links are :")
    
    for link in box.find_all('a'):
        city = link.get('href')
        if (city.startswith("https")) == False:
                    city = "https://" + city
        city_links.append(city)
        
    return city_links

