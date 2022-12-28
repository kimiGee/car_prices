import pandas as pd
import numpy as np
import csv

import requests
from bs4 import BeautifulSoup

import time
from random import randint


def build_car_list(links):
    count = 0

    # store vehicle details in this list
    cars = []

    #loop over all links in the list     
    for link in links:
        # make HTTP requests
        each_page = requests.get(link)
        # The sleep function can help you to avoid the server to be overloaded with too many requests in a very short period of time.
        time.sleep(randint(1,2))
        # store the BS object in a variable
        page_soup = BeautifulSoup(each_page.content, 'html.parser')

        # loop over each link and store car details
        car_details = []
        try:
            # find price attribute and store in car details
            car_details.append(page_soup.find('span', class_="price").text)

            # find date time and append to car details
            for span in page_soup.find_all('span', recursive=True):
                if not span.attrs.values():
                    car_details.append(span.text)
            car_details.append("date time: " + page_soup.find('time', class_="date timeago")\
                                            .text.strip().replace(':',';'))

            # find date city name and append to car details
            city = link.strip()
            start = city.find("//") + len("//")
            end = city.find(".")
            substring = city[start:end]
            car_details.append('city:' + substring)

            # find geo coordinates and append to car details
            geos = page_soup.findAll("div", {"class": "mapbox"})
            lat = geos[0].contents[1].get('data-latitude')
            car_details.append('lat:' + lat.strip())
            long = geos[0].contents[1].get('data-longitude')
            car_details.append('long:' + long.strip())

            # find post body and append to car details
            post_body = page_soup.find(attrs={'id' : 'postingbody'}).contents[2]
            # remove non ascii characters from post bosy
            car_details.append('post_body:' + re.sub("[^0-9a-zA-Z]+", " ", post_body))

            # find postID and append to car details / We'll use this to assign labels to images later
            car_details.append('pID:' + link.strip().replace('html','').replace('.','').split('/')[-1])
        except:
            pass    
        
        # perform some basic cleanup and store in clean
        clean = []
        for string in car_details:
            # this attribute came without a label. Assign one.
            if string == car_details[1]:
                clean.append('year make model: ' + string)
            # clean up price text from $9,999 --> 9999
            if string == car_details[0]:
                clean.append('price: ' + string.replace(',','').replace('$',''))
            else:
                clean.append(string)

                
        # some attributes came without labels. Drop those.
        car_final = []
        for s in clean:
            if ':' in s:
                car_final.append(s)
                
        # append clean attributes for each vehicle to car list
        print('adding ', car_final, 'to cars list: ', count)
        cars.append(car_final)
        count += 1

        # just a counter to keep track of the loop
        if count % 100 == 0:
            print('loop # -> ',count)
        
    return cars
    

# method to strip() the keys and values after splitting in order to trim white-space.
def list_to_dict(rlist):
    return dict(map(lambda s : map(str.strip, s.split(':')), rlist))
            
            
            
            

def main():
    
    # read links from csv
    links = pd.read_csv('./owner_links.csv', names=['https'])
    links = links['https'][1:]
    cars = build_car_list(links)

    #  ---------------redundant data storage----------------- 
    df = pd.DataFrame(cars)
    df.to_csv("./car_data_init.csv", sep=',',index=False)

    # create a dictionary for label:value for each car attribute
    car_dicts = []
    for car in cars:
        try:
            car_dict = list_to_dict(car)
            car_dicts.append(car_dict)
            
        except:
            pass
        

    dfs = pd.DataFrame()

    for item in car_dicts:
        df = pd.DataFrame.from_dict(item,orient='index').transpose()
        #concatenate each new df from the loop into the parent df
        dfs= pd.concat([dfs,df], axis=0, ignore_index=True, sort=True)
        #clean duplicate year in 'year make model'
        dfs['year_c make model'] = dfs['year make model'].str.replace(r'\b(\w+)(\s+\1)+\b', r'\1', regex=True)
        

    # save data frame to csv
    dfs.to_csv('car_data.csv', sep='\t', encoding='utf-8')
    
    

if __name__ == "__main__":
    main()