import requests
import pandas
import random
from crawler_function import bs4_html_parser, player_info_parser, parser_url_index
date_index_df = parser_url_index()
target_index = date_index_df[date_index_df["date"] == "2022/09/11"].index[0]
date_index_df = date_index_df.drop(index=range(target_index+1, len(date_index_df)))
player_info_origin_df = pandas.DataFrame([])
not_have_data_date = []
for date in date_index_df["date"] : 
    print(date)
    bs4_html = bs4_html_parser(date, 1)
    if bs4_html.find("tbody", {"class" : "f_fs12 fontFam"}) == None :
        not_have_data_date.append({"date" : date, "html" : bs4_html})
        continue
    player_info_origin_df = player_info_parser(player_info_origin_df, bs4_html)

    for page in random.sample(range(2, 15), 13) : 
        bs4_html = bs4_html_parser(date, page)
        if bs4_html.find("tbody", {"class" : "f_fs12 fontFam"}) == None :
            continue
        player_info_origin_df = player_info_parser(player_info_origin_df, bs4_html)
player_info_origin_df.to_json("data_base.json")
not_have_data_date_df =  pandas.DataFrame(not_have_data_date)
not_have_data_date_df.to_json("date_check.json")

# ETL
from etl_function import horse_info_url, running_position, race, horse_number, horse_name, jockey, trainer, horse_id
df = pandas.read_json("data_base.json")
df["horse_info_url"] = df["horse_info_url"].map(horse_info_url)
df["沿途走位"] = df["沿途走位"].map(running_position)
df["場次"] = df["場次"].map(race)
df["馬號"] = df["馬號"].map(horse_number)
df["馬名"] = df["馬名"].map(horse_name)
df["騎師"] = df["騎師"].map(jockey)
df["練馬師"] = df["練馬師"].map(trainer)
df["horse_id"] = df["horse_info_url"].map(horse_id)
df.to_json("data_base.json")

# download house image
import os
from crawler_function import parser_horse_image
df = pandas.read_json("data_base.json")
for horse_info_url in  df["horse_info_url"].unique() : 
    parser_horse_image(horse_info_url)

# connect to sqlite db
import sqlite3
df = pandas.read_json('data_base.json')
conn = sqlite3.connect('data_base.db')
df.to_sql('player_info', conn, if_exists='replace', index=False, dtype={
    '日期': 'TEXT',
    '場次': 'TEXT',
    '名次': 'TEXT',
    '馬號': 'TEXT',
    '馬名': 'TEXT',
    '騎師': 'TEXT',
    '練馬師': 'TEXT',
    '排位體重': 'INTEGER',
    '實際負磅': 'INTEGER',
    '檔位': 'INTEGER',
    '頭馬距離': 'TEXT',
    '沿途走位': 'TEXT',
    '完成時間': 'TEXT',
    '獨嬴賠率': 'REAL'
})
conn.close()