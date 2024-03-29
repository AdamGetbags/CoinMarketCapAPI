# -*- coding: utf-8 -*-
"""
Coinmarketcap API
@author: adam getbags
"""

# Import modules 
import os
import requests
import pandas as pd
from coinMarketCapKey import cmc_key

print(os.getcwd())

# Assign base URL 
base_url = 'https://pro-api.coinmarketcap.com'

# Set headers // including API key
headers = {
    'X-CMC_PRO_API_KEY': cmc_key,
    'Content-Type': 'application/json'
}

def get_cmc_data(endpoint, params=None):

    if params == None:
              params = {}

    endpoint_url = base_url + endpoint
    
    try:
        # Send the get request with headers
        response = requests.get(endpoint_url, 
                                params=params,
                                headers=headers)
        print('requesting ' + response.url)
        # Check if request success (status code 200)
        if response.status_code == 200:
            # Parse and format response
            res_data = response.json()
            
        else:
            # Handle errors or other status codes 
            print(f"Request failed with status code {response.status_code}")
            return
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    return res_data

# CMC ID map 
map_data = get_cmc_data('/v1/cryptocurrency/map')

map_df = pd.DataFrame(map_data['data']) 
print(len(map_df))
print(map_df)
print(map_df.iloc[0])
print(map_df.iloc[-1])
    
map_df.to_excel('map_data.xlsx',
                index=False)


# get info data
info_params = {'id': "1,1027"}
info_data = get_cmc_data('/v2/cryptocurrency/info', params=info_params)
print(pd.DataFrame(info_data))

# get latest listing data
listing_params = {'limit': "250", 
          'sort': 'market_cap'}
listing_data_res = get_cmc_data('/v1/cryptocurrency/listings/latest', 
                                params=listing_params)

listing_data_res['data'][0]
listing_data_df = pd.DataFrame(listing_data_res['data'])

listing_data = pd.concat([
    listing_data_df,
    listing_data_df.quote.apply(pd.Series).USD.apply(pd.Series)],
    axis=1)

listing_data = listing_data.drop('quote', axis = 1)

pd.DataFrame(listing_data).to_excel(
    'listing_data.xlsx',
    index=False)

# get categories data
categories_params = {'id': "1"}
categories_data = get_cmc_data('/v1/cryptocurrency/categories', 
                        params=categories_params)

pd.DataFrame(categories_data['data']).to_excel(
    'categories_data.xlsx',
    index=False)
    
# get category data 
category_params = {'id': categories_data['data'][0]['id']}
category_data = get_cmc_data('/v1/cryptocurrency/category', 
                        params=category_params)

category_data.keys()
category_data['data']

pd.DataFrame(category_data['data']).to_excel(
    'category_data.xlsx',
    index=False)
