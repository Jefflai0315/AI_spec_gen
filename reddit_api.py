import praw
import pandas as pd
import streamlit as st
import os

#initiate an reddit instant 
def app(model):

    # secret = st.text_input('secret','ymsWksZHFucX9C5QcITUtq8P78fSvA')
    # id = st.text_input('client_id','4Tqp6GN2jiX07Aj4kdwryw')
    secret ='ymsWksZHFucX9C5QcITUtq8P78fSvA'
    id ='4Tqp6GN2jiX07Aj4kdwryw'

    if secret != '' and id !='':
        try:
            reddit = praw.Reddit(client_id='4Tqp6GN2jiX07Aj4kdwryw', client_secret='ymsWksZHFucX9C5QcITUtq8P78fSvA', user_agent='RedWebScraping')
            # get 10 hot posts from the MachineLearning subreddit
            posts = []
            search_term = model
            oven_subreddit = reddit.subreddit(search_term) 
            for post in oven_subreddit.hot(limit=50):
                posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
            posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
            print(posts)


            # get search tearm subreddit data and description
            print(oven_subreddit.description)


            # get comments including replies for every reddit submission
            Dic = []
            for  i in range(len(posts)):
                inp = posts['id'][i]
                submission = reddit.submission(id = f'{inp}')
                print('finding comments for: ', submission)
                submission.comments.replace_more(limit=None)
                dic = [[]]
                for comment in submission.comments.list():
                    dic[0].append(comment.body)
                Dic.append(dic)

            #concatenate the comments to the posts dataframe
            comments = pd.DataFrame(Dic,columns=['comments'])
            print(comments)
            
            posts_comments = pd.concat([posts,comments],axis =1)
            print(type(posts_comments))

            #export into a json file for cleaning
            posts_comments.to_json('Export_DataFrame.json',default_handler=str,orient="records")
            if not os.path.exists("./outputs/result"):
                os.makedirs("./outputs/result")

            posts_comments.to_csv(f"./outputs/result/{model}.csv", index=False)

        except Exception as e:
            print(e)
            print('huh')

app("washingmachine")