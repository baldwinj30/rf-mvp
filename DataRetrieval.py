#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 20:41:43 2019

@author: jacob
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time

stat_type = "totals" # advanced, totals
    
base = ("https://www.basketball-reference.com/play-index/psl_finder.cgi?"
        "request=1&match=single&type=" + stat_type + "&per_minute_base=36&per_poss_base="
        "100&lg_id=NBA&is_playoffs=N&year_min=1980&year_max=&franch_id=&"
        "season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&"
        "height_min=0&height_max=99&birth_country_is=Y&birth_country=&"
        "birth_state=&college_id=&draft_year=&is_active=&debut_yr_nba_start=&"
        "debut_yr_nba_end=&is_hof=&is_as=Y&as_comp=gt&as_val=0&award=&"
        "pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&"
        "pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&"
        "c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&"
        "c5comp=&c6mult=&c6stat=&order_by=ws&order_by_asc=&offset=%s"
)

counter = 0
interval = 100
status = True

df_list = []
while status:
    html = urlopen(base % counter)
    soup = BeautifulSoup(html)    
    # use getText()to extract the text we need into a list 
    # (th are table headers, there are 2 and we want the second one)
    # (tr are table rows)
    try:
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    except IndexError as e:
        print("Index error, means we don't have a header anymore.  Results complete")
        break
    
    # this does not grab the rank, so we need to leave that off the header
    rows = soup.findAll('tr')[2:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    
    # dataframe setup
    df = pd.DataFrame(data=player_stats, columns=headers[1:])
    df_list.append(df)
    counter+=interval
    time.sleep(1)

df = pd.concat(df_list, ignore_index=True)
print(df)
df.to_pickle("all_star_" + stat_type + "_df.pkl")
