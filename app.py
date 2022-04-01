# from google_key import *
from pyexpat import model
import streamlit as st 
import ebay_api
import reddit_api

#insert household item name here


#pipeline


def main():
    st.header("Search Household Appliance")
    input = st.text_input('Search Term')
    if input != '':
        results = ebay_api.get_search_term(input)
        st.write(results)
    st.markdown('---')
    st.header('Reddit Search')
    model =st.text_input('search model')
    reddit_api.app(model)

if __name__ == "__main__":
    main()
    