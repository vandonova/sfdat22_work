import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random

def scrapePainting(url):
    r = requests.get(url)
    print r, url
    b = BeautifulSoup(r.text, 'html.parser')
    
    url_id = r.url.split('/')[-1]
    
    artist = b.find('a', {'id':'fine-ART-ProductLabelArtistNameLink'})
    if artist is not None:
        artist = b.find('a', {'id':'fine-ART-ProductLabelArtistNameLink'}).text
        
    title = b.find('span', {'id': 'fineArtTitle'})
    if title is not None:
        title = b.find('span', {'id': 'fineArtTitle'}).text
        
    image = re.findall('http://ecx.images-amazon.com/images/I/.*\.jpg', r.text)
    if image is not None:
        image = re.findall('http://ecx.images-amazon.com/images/I/.*\.jpg', r.text)
        
    price = b.find('span', {'id': 'priceblock_ourprice'})
    if price is not None:
        price = b.find('span', {'id': 'priceblock_ourprice'}).text.replace('$','').replace(',', '')
        if '.' in price:
            price = float(price.replace('.', ''))/100
        else:
            price = float(price)
            
    desc = b.find('div', {'id': 'productDescription_feature_div'})
    if desc is not None:
        desc = b.find('div', {'id': 'productDescription_feature_div'}).getText().replace('\n','')
        
    height = None
    width = None
    size = b.find('span', {'id': 'mnba_buybox_size'})
    if size is not None:
        size = [a.strip() for a in b.find('span', {'id': 'mnba_buybox_size'}).text.split('x')]
        if len(size) == 2:
            height = float(size[0].replace('in.','').strip())
            width = float(size[1].replace('in.','').strip())
            depth = 1.
        elif len(size) == 3:
            height = float(size[0].replace('in.','').strip())
            width = float(size[1].replace('in.','').strip())
            depth = float(size[2].replace('in.','').strip())

    return {'url_id': url_id, 'artist': artist, 'title':title, 'image': image, 'price': price, 
            'description':desc, 'height': height, 'width': width, 'size':size}


for page in range(1,4):
    
    page_url = "http://www.amazon.com/s/ref=sr_pg_3?rh=n%3A4991425011%2Cn%3A%214991426011%2Cn%3A6685269011%2Cn%3A6685289011&page="+str(page)+"&ie=UTF8&qid=1462467907"
    r = requests.get(page_url)
    r.text

    b = BeautifulSoup(r.text, 'html.parser')

    url_1 = []
    for link in b.findAll('a', {'class':"a-link-normal a-text-normal"}):
        url_1.append(link.get('href'))
    
    url_list = url_1[::2]
	url_list = random.shuffle(url_list)
	
    paintings = []
    for url in url_list:
        try:
            paintings.append(scrapePainting(url))
        except Exception as error:
            print error
        time.sleep(random.randint(5,20))

df = pd.DataFrame(paintings)
df.to_csv("paintings_first_df.csv", index=False)