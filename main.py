import requests
import pandas as pd
import json
import time
import numpy as np
from matplotlib import pyplot as plt


def ask_api_total_cards(query):
    """Do query, return number of cards returned"""
    time.sleep(0.1)
    request_result = requests.get('https://api.scryfall.com/cards/search?q=' + query)
    response_dict = json.loads(request_result.text)
    if response_dict['object'] == 'error':
        if response_dict['code'] == 'not_found':
            return 0  # 0 cards found
    total_cards = response_dict['total_cards']
    return total_cards


# Queries for Scryfall, e
query_strings = {
    'Expansions': '+-is%3Areprint+st%3Aexpansion+-is%3Afunny+game%3Apaper&unique=cards&as=grid&order=name',
    'Core Sets': '+-is%3Areprint+st%3Acore+-is%3Afunny+game%3Apaper&unique=cards&as=grid&order=name',
    'Draft Innovation sets':
        '+-is%3Areprint+st%3Adraft_innovation+-is%3Afunny+game%3Apaper&unique=cards&as=grid&order=name',
    'Commander preconstructed decks':
        '+-is%3Areprint+st%3Acommander+-is%3Afunny+game%3Apaper&unique=cards&as=grid&order=name',
    'Portal starter decks': '+-is%3Areprint+game%3Apaper+st%3Astarter&unique=cards&as=grid&order=released&dir=asc',
    'Unsets and non-serious promo cards': '+-is%3Areprint+is%3Afunny+game%3Apaper&unique=cards&as=grid&order=name',
    'Digital-only and rebalanced cards':
        '+-is%3Areprint+-game%3Apaper&unique=cards&as=grid&order=released&dir=asc'
}

# choose years for analysis
start_year = 1993
end_year = 2022

#
new_cards_numbers = []

for year in range(start_year, end_year + 1):
    data_row = [year]
    print("Processing year: " + str(year) + "...")
    for set_type, query_string in query_strings.items():
        response = ask_api_total_cards('year%3A' + str(year) + query_string)
        # print(set_type + ": " + str(response))
        data_row.append(response)
    new_cards_numbers.append(data_row)

new_cards_arr = np.array(new_cards_numbers)
new_cards_index = new_cards_arr[:, 0]
new_cards_arr = new_cards_arr[:, 1:]
print(new_cards_index)
print(new_cards_arr)

column_names = []
for set_type in query_strings:
    column_names.append(set_type)

new_cards_df = pd.DataFrame(data=new_cards_arr, index=new_cards_index, columns=column_names)
new_cards_df.index.name = 'Year'
with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_columns', 500,
                       'display.width', 250):
    print(new_cards_df)

new_cards_df.plot(kind='bar', stacked=True, title='Source of new Magic the Gathering cards by year', width=0.9,
                  color=['#0008ff', '#008cff', '#ff00aa', '#13d129', '#fc1500', '#b5b2b1', '#ffee00'])
plt.ylabel('Number of cards')
plt.grid(axis='y', color="black", linestyle='dotted')
plt.show()

