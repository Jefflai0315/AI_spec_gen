from unittest import result
from attr import attr
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import math

item_name = []
prices = []

# open new soup with a new url
def get_page(url):
    response =  requests.get(url)
    if not response.ok:
        print('server responded: ', response.status_code)
    else:
        data=response.text
        soup=BeautifulSoup(data,"html.parser")
        return soup

# use in the individual product page to find details
def get_detail_data(soup):
    try:
        title = soup.find('h1', attrs = {'class':"x-item-title__mainTitle"}).find('span').text
    except:
        title =' '

    try:
        price = soup.find('div', attrs = {'class':"mainPrice"}).find('span')
        price = price.get('content')
    except:
        price =' '

    try: 
        sold = soup.find('div', attrs = {'id':"why2buy"}).find('span').text #.split(' ')[0]
    except:
        sold =' '

    try: 
        review = soup.find('div', attrs = {'class':"overlay-top"}).find('a') #.split(' ')[0]
        reviewURL = review.get("href") + '&pgn='
        review_num = int(re.search(r'\d+', review.text).group())
        page = int(math.ceil(review_num/10))
        print(reviewURL,page)
    
        review = get_review(reviewURL, page)
        
    except:
        review =' '

    try:
        descs = soup.find('div', attrs ={'data-testid':"ux-layout-section__item",'class':"ux-layout-section__item ux-layout-section__item--table-view"}).find_all('span', attrs={'class':"ux-textspans"})
    except:
        descs = [' ']
    finally:
        specs = []
        
        for i in range(len(descs)):
            descs = [i for i in descs if i.contents[1] !='Read more'] #remove read more expandable tag
        

        for i in range(len(descs)-1):
            if i % 2 ==0:
                
                specs.append([descs[i].contents[1],descs[i+1].contents[1]])

        if specs[0][1][:10] == specs[1][0][:10]:
            specs[0][1] = specs[1][0]
            del specs[1]
        
        print(review)
    
    return [title, price,sold,specs]


# to see the specs of an individual product
def get_single_df(specs):
    df = pd.DataFrame(specs, columns = ['Specs title','Specs value'])
    return df

def get_review(url,page):
    reviews = []
    url = url.split('urw')
    # url1 = 'urw/Samsung-TU7000-43-4K-LED-Smart-TV-Titan-Gray'.join(url)
    # print(url1)
    print("in get_review")
    for i in range(page):
        # url2 = url1 + str(0+i)
        url = url + str(0+i)
        soup = get_page(url)
        print(soup)
        

        try: 
            review= soup.find_all('p',attrs= {'class':"review-item-content rvw-wrap-spaces", 'itemprop':"reviewBody"})
        except:
            review = ''
        finally:
            if review !="":
                reviews.extend(review)
    
    for i in range(len(reviews)):
        reviews[i] = str(reviews[i]).replace('<p class="review-item-content rvw-wrap-spaces" itemprop="reviewBody">','')
        reviews[i] = str(reviews[i]).replace('<span class="show-full-review">','')
        reviews[i] = str(reviews[i]).replace('</span>','')
        reviews[i] = str(reviews[i]).replace('</br>','')
        reviews[i] = str(reviews[i]).replace('<br/>','')
        reviews[i] = str(reviews[i]).replace('<a class="show-full-review-link" href="javascript:;">Read full review...</a>','')

    print(reviews)
        
    # strings = ','.join(reviews)
    # print(strings)
    # string1 = strings.replace('<p class="review-item-content rvw-wrap-spaces" itemprop="reviewBody">','')
    
    # try:
    #     review_num = int(soupR.find('h2', attrs = {'class':"reviews-section-title"}).text.split(' ')[0])
    # except:
    #     review_num = 0
    # finally:
    #     page = math.ceil(review_num/10)


search_term = []
# pass in search url of the search product page
search_term.append('oven')
ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=smart+TV&_sacat=0&LH_All=1&rt=nc&LH_ItemCondition=1000&_pgn="+str(1)
r= requests.get(ebayUrl)
data=r.text
soup=BeautifulSoup(data,"html.parser")

# get all listings 
listings = soup.find_all('li', attrs={'class': 's-item'})
links = soup.find_all('a', class_ ='s-item__link')
items = [item.get('href') for item in links] # store the link to each product 

array = []
array_array = []
for i in range(5):
    soup =  get_page(items[i+1])   #open each product's url
    results = get_detail_data(soup) 
    array.append(results)  #store all the details of a product
array_array.append(array)

# print(array_array)

# return results = ['Object's title', 'Price', 'Sold', [['Specs title', 'Specs value']]]
# return array  = [--list of results--]



    

    
