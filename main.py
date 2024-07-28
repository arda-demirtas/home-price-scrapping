from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
#import requests
from seleniumbase import Driver
import time

class HomePrice:
    def __init__(self):
        self.__driver = Driver(uc=True)
        self.__driver.maximize_window()

    def get_url(self, province, page):
        data = f"https://www.realtor.com/realestateandhomes-search/{province}/type-single-family-home,condo,townhome,multi-family-home,mfd-mobile-home/pg-{page}"
        return data
    
    def parse(self, url, province):
        self.__driver.get(url)
        time.sleep(2)
        df = pd.DataFrame(columns=['kind','bed', 'bath', 'sqft', 'price', 'address', 'province'])
        cards = []
        for _ in range(8):      
            self.__driver.execute_script('window.scrollBy(0, 1600)')
            time.sleep(2)
            bs = BeautifulSoup(self.__driver.page_source, 'html.parser')
            cards = bs.find_all('div', {'class' : 'BasePropertyCard_propertyCardWrap__30VCU'})
            for cardd in cards:
                try:        
                    bed = cardd.find('li', {'data-testid' : 'property-meta-beds'}).text
                    bath = cardd.find('li', {'data-testid' : 'property-meta-baths'}).text
                    sqft = cardd.find('li', {'data-testid' : 'property-meta-sqft'})
                    sqft = sqft.find('span', {'class' : 'meta-value'}).text
                    price = cardd.find('div', {'data-testid' : 'card-price'}).text
                    address = cardd.find('div', {'class' : 'card-address truncate-line'}).text
                    bed = int(bed.replace("bed", ""))
                    bath = float(bath.replace("bath", ""))
                    sqft = float(sqft.replace(",", ""))
                    price = float(price.replace('$', '').replace(',', ''))
                    kind = cardd.find('div', {'class' : 'base__StyledType-rui__sc-108xfm0-0 hRTvWe message'}).text
                    df = df._append({'kind' : kind,'bed' : bed, 'bath' : bath, 'sqft' : sqft, 'price' : price, 'address' : address, 'province' : province}, ignore_index = True)
                except:
                    pass
        df = df.drop_duplicates()
        return df
    

#example
hp = HomePrice()
url = hp.get_url('Colorado', '1')#province = colorado, page = 1
df = hp.parse(url, 'Colorado')#parse the data and turn it to df
df.index = range(df.shape[0])
df.to_csv("homes.csv", index=False)

