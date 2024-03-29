# -*- coding: utf-8 -*-
"""
Coinmarketcap API Streamlit App
@author: adam getbags
"""

# Import modules 
import streamlit as st
import pandas as pd
import os

# Read listing data 
listing_data = pd.read_excel('listing_data.xlsx')

# Rename columns
listing_data = listing_data.rename(columns={
    "percent_change_7d": "pct_chg_7d",
    "percent_change_30d": "pct_chg_30d",
    "percent_change_60d": "pct_chg_60d",
    "percent_change_90d": "pct_chg_90d"})

# Remove stablecoins
listing_data = listing_data[
    listing_data['tags'].str.contains("stablecoin") == False]

# Sort by volume
listing_data = listing_data.sort_values('volume_24h', 
                                        ascending=False,
                                        ignore_index=True)

# top n return data
num_listings = 20
top_n_return_data = listing_data[listing_data.id != 1][[
                                 'name',
                                 'volume_24h',
                                 'pct_chg_7d', 
                                 'pct_chg_30d',
                                 'pct_chg_60d',
                                 'pct_chg_90d']].head(num_listings)

btc_data = listing_data.loc[listing_data['id'] == 1]

btc_return_data = btc_data[['pct_chg_7d', 
                            'pct_chg_30d',
                            'pct_chg_60d',
                            'pct_chg_90d']]

rel_rets = top_n_return_data[['name', 'volume_24h']]

format_to_percentage = lambda x: '{:.2f}%'.format(x)

btc_return_data = btc_return_data.applymap(format_to_percentage)
btc_return_data = btc_return_data.rename(index={0: 'BTC'})

# Relative returns 
rel_rets = top_n_return_data[['name', 'volume_24h']]

rel_rets['rel_ret_7d'] = top_n_return_data[
    'pct_chg_7d'] - btc_data['pct_chg_7d'][0]

rel_rets['rel_ret_30d'] = top_n_return_data[
    'pct_chg_30d'] - btc_data['pct_chg_30d'][0]

rel_rets['rel_ret_60d'] = top_n_return_data[
    'pct_chg_60d'] - btc_data['pct_chg_60d'][0]

rel_rets['rel_ret_90d'] = top_n_return_data[
    'pct_chg_90d'] - btc_data['pct_chg_90d'][0]

st.title(':green[Bitcoin]:red[ Returns]')

btc_return_data

st.divider()

st.title(':green[Other Coin]:red[ Returns]')

top_n_return_data

st.divider()

st.title(':green[Relative]:red[ Returns]')

rel_rets_sorted = rel_rets.sort_values('rel_ret_7d', 
                                      ascending=False, 
                                      ignore_index=True)

rel_rets_sorted