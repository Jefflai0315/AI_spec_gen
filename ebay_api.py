
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from collections import deque


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
        
        print_single_df(specs)


        specs_dict = {}

        for i in specs:
            specs_dict[i[0]] = i[1]
        print(specs_dict)
    
    return [title, price,sold,specs_dict]

# to see the specs of an individual product
def print_single_df(specs):
    df = pd.DataFrame(specs, columns = ['Specs title','Specs value'])
    print(df)

def get_search_term(search_term, page_num=3):
    print('--------------')
    st_list = search_term.split(' ')
    links_list = deque([])
    for i in range(page_num):
        soup= get_page("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499337.m570.l1311&_nkw="+'+'.join(st_list) +"&_sacat="+str(i))
        
        # get all listings 
        listings = soup.find_all('li', attrs={'class': 's-item'})
        links = soup.find_all('a', class_ ='s-item__link')
        links_list.extend([item.get('href') for item in links]) # store the link to each product 
    
    links_list.popleft() # first link in list is not useful
    print('number of links:' ,len(links_list))

    array =[]
    # for link in links_list:
    for i in range(5):
        soup = get_page(links_list[i])   #(link)
        results = get_detail_data(soup) 
        array.append(results)  #store all the details of a product

    print(array)

    df = pd.DataFrame(array,columns=['Title','Price','Sold','Specs'])
    #extract model name
    df['Model Name'] = df['Specs'].apply(lambda x : x['Brand:'] +' ' + x['Model:'])
    print(df)
    return array
    

links_list =get_search_term('coffee maker')  








#/////////////////////////////// start of the code /////////////////////////////////////////////

# search_term = []
# # pass in search url of the search product page
# search_term.append('oven')
# ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=oven&_sacat="+str(0)
# r= requests.get(ebayUrl)
# data=r.text
# soup=BeautifulSoup(data,"html.parser")

# # get all listings 
# listings = soup.find_all('li', attrs={'class': 's-item'})
# links = soup.find_all('a', class_ ='s-item__link')
# items = [item.get('href') for item in links] # store the link to each product 

# array = []
# array_array = []
# for i in range(5):
#     soup =  get_page(items[i+1])   #open each product's url
#     results = get_detail_data(soup) 
#     array.append(results)  #store all the details of a product
# array_array.append(array)

# # return results = ['Object's title', 'Price', 'Sold', [['Specs title', 'Specs value']]]
# # return array  = [--list of results--]


# ##-----------------------------second serach----------------------------------------------##

# search_term.append('smart oven')
# ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=smart+oven&_sacat=0"
# r= requests.get(ebayUrl)
# data=r.text
# soup=BeautifulSoup(data,"html.parser")

# # get all listings 
# listings = soup.find_all('li', attrs={'class': 's-item'})
# links = soup.find_all('a', class_ ='s-item__link')
# items = [item.get('href') for item in links] # store the link to each product 

# array1 = []
# for i in range(5):
#     soup =  get_page(items[i+1])   #open each product's url
#     results = get_detail_data(soup) 
#     array1.append(results)  #store all the details of a product
# array_array.append(array1)

# # print(array1)

# ##-----------------------------third serach----------------------------------------------##
# search_term.append('power oven')
# ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=power+oven&_sacat=0&LH_TitleDesc=0&_odkw=save+oven&_osacat=0"
# r= requests.get(ebayUrl)
# data=r.text
# soup=BeautifulSoup(data,"html.parser")

# # get all listings 
# listings = soup.find_all('li', attrs={'class': 's-item'})
# links = soup.find_all('a', class_ ='s-item__link')
# items = [item.get('href') for item in links] # store the link to each product 

# array2 = []
# for i in range(5):
#     soup =  get_page(items[i+1])   #open each product's url
#     results = get_detail_data(soup) 
#     array2.append(results)  #store all the details of a product
# array_array.append(array2)

# ##-----------------------------next step : clean data------------------------------------------##


# import pickle
# import pandas as pd
# import re
# import nltk
# nltk.download('omw-1.4')
# nltk.download('stopwords')
# nltk.download('wordnet')
# from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import CountVectorizer

# def clean_text(text):                               # user defined function for cleaning text
#     text = text.lower()                             # all lower case
#     text = re.sub(r'\[.*?\]', ' ', text)            # remove text within [ ] (' ' instead of '')
#     text = re.sub(r'\<.*?\>', ' ', text)            # remove text within < > (' ' instead of '')
#     text = re.sub(r'http\S+', ' ', text)            # remove website ref http
#     text = re.sub(r'www\S+', ' ', text)             # remove website ref www
#     # text = re.sub('[F#f_7[0]','',text)

#     text = text.replace('€', 'euros')               # replace special character with words
#     text = text.replace('£', 'gbp')                 # replace special character with words
#     text = text.replace('$', 'dollar')              # replace special character with words
#     text = text.replace('%', 'percent')             # replace special character with words
#     text = text.replace('\n', ' ')                  # remove \n in text that has it
#     text = text.replace('\'', '’')                  # standardise apostrophe
#     text = text.replace('&#39;', '’')               # standardise apostrophe

#     text = text.replace('’d', ' would')             # remove ’ (for would, should? could? had + PP?)
#     text = text.replace('’s', ' is')                # remove ’ (for is, John's + N?)
#     text = text.replace('’re', ' are')              # remove ’ (for are)
#     text = text.replace('’ll', ' will')             # remove ’ (for will)
#     text = text.replace('’ve', ' have')             # remove ’ (for have)
#     text = text.replace('’m', ' am')                # remove ’ (for am)
#     text = text.replace('can’t', 'can not')         # remove ’ (for can't)
#     text = text.replace('won’t', 'will not')        # remove ’ (for won't)
#     text = text.replace('n’t', ' not')              # remove ’ (for don't, doesn't)

#     text = text.replace('’', ' ')                   # remove apostrophe (in general)
#     text = text.replace('&quot;', ' ')              # remove quotation sign (in general)

#     text = text.replace('cant', 'can not')          # typo 'can't' (note that cant is a proper word)
#     text = text.replace('dont', 'do not')           # typo 'don't'

#     text = re.sub(r'[^a-zA-Z0-9]', r' ', text)      # only alphanumeric left
#     text = text.replace("   ", ' ')                 # remove triple empty space
#     text = text.replace("  ", ' ')                  # remove double empty space
#     return text



# '''user inputs'''
# stop = ["wa", "doe", "ha", "video", "one",
#         "subscribe", "channel", "watch",
#         "watching", "thanks", "thank","N/A"]      # Add stopwords (lower case)

# '''initialise'''
# all_stopwords = stopwords.words('english')  # set english
# all_stopwords.extend(stop)                  # and extend with 'stop' above



# def create_specs_dic(array):
#     specs_dic = {}
#     for results in array:
#         specs = results[3]
#         for spec in specs:
#             if spec[0][:-1] not in specs_dic:
#                 specs_dic[spec[0][:-1]] = [spec[1]]
#             else:
#                 specs_dic[spec[0][:-1]].append(spec[1])

#     # conditions and features need to be tokenize as they are long strings

#     specs_dic['Condition'] = clean_text(''.join(specs_dic['Condition']))
#     specs_dic['Condition'] = nltk.tokenize.TreebankWordTokenizer().tokenize(specs_dic['Condition'])
#     specs_dic['Features'] = clean_text(''.join(specs_dic['Features']))
#     specs_dic['Features'] = nltk.tokenize.TreebankWordTokenizer().tokenize(specs_dic['Features'])
#     for k in range(len(specs_dic['Features'])):
#         specs_dic['Features'][k] = nltk.stem.WordNetLemmatizer().lemmatize(specs_dic['Features'][k])   
#     #     print("token k :" ,specs_dic['Features'][k])    # stem each token
#     # print('------------------')
#     for k in range(len(specs_dic['Condition'])):
#         specs_dic['Condition'][k] = nltk.stem.WordNetLemmatizer().lemmatize(specs_dic['Condition'][k])   
#         # print("token k :" ,specs_dic['Condition'][k])   # stem each token

#     for k,v in specs_dic.items():
#         specs_dic[k] = ' '.join(v)

#     return specs_dic



# specs_dic_array = []

# for array in array_array:
#     specs_dic_array.append(create_specs_dic(array))

# print(specs_dic_array)

# # specs_dic_array is a list of specification dictionary of different search term


# single_spec_dic = {}
# count= 0
# for specs_dic in specs_dic_array:
#     for k,v in specs_dic.items():
#         if k not in single_spec_dic:
#             single_spec_dic[k]= [[f'{search_term[count]}', v]]
#         else:
#             single_spec_dic[k].append([f'{search_term[count]}', v])
#     count +=1
     

# print(single_spec_dic)

# # single_spec_dic is a dictionary of specification with a list as a value, list is a 

# for k,v in single_spec_dic.items():
#     print(k)
#     df_clean = pd.DataFrame(v,columns=['Search term', 'Spec value'])
#     print(df_clean)
#     '''create dtm'''
#     cv = CountVectorizer(stop_words=all_stopwords)                       # initialise cv w/o stopwords
#     data_cv = cv.fit_transform(df_clean['Spec value'])                      # apply cv
#     dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names_out(), index=search_term)
#     print(dtm)

# # '''user inputs'''
# # stop = ["wa", "doe", "ha", "video", "one",
# #         "subscribe", "channel", "watch",
# #         "watching", "thanks", "thank","N/A"]      # Add stopwords (lower case)

# # '''initialise'''
# # all_stopwords = stopwords.words('english')  # set english
# # all_stopwords.extend(stop)                  # and extend with 'stop' above
# # '''create dtm'''
# # cv = CountVectorizer(stop_words=all_stopwords)                       # initialise cv w/o stopwords
# # data_cv = cv.fit_transform(data_clean['Spec value'])                      # apply cv
# # dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names(), index=specs_dic.keys())
# # print(dtm)




















