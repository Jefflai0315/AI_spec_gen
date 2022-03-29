# from google_key import *
import streamlit as st 
import ebay_api

#insert household item name here


#pipeline


def main():
    input = st.text_input('Search Term')
    results = ebay_api.get_search_term(input)
    st.write(results)

if __name__ == "__main__":
    main()
    