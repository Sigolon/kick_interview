import requests
from bs4 import BeautifulSoup
import time
import os, json, pandas
import hashlib
import time 

def parser_url_index() : 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }

    cookies = {
        'isEU': 'false',
        'AMCVS_06AB2C1653DB07AD0A490D4B%40AdobeOrg': '1',
        'custProIn': '',
        's_cc': 'true',
        'HKJCSSOGP': '1713595766167',
        's_visit': '1',
        'TakeOverMessage': 'COM-7%7CCOM-7%7CCOM-7%7CCOM-7',
        'AMCV_06AB2C1653DB07AD0A490D4B%40AdobeOrg': '-330454231%7CMCIDTS%7C19834%7CMCMID%7C45565919299848919410590974230794634296%7CMCAAMLH-1714200656%7C11%7CMCAAMB-1714200656%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1713603056s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19841%7CvVersion%7C3.1.2',
        'ADRUM': 's=1713595864624&r=https%3A%2F%2Fwww.hkjc.com%2Fhome%2Fchinese%2Findex.aspx',
        'ASPSESSIONIDCCCQARAD': 'BOFHJIFBLCBFFIPCBHOLNHIF',
        'gpv_p5': 'https%3A%2F%2Fracing.hkjc.com%2Fracing%2Finformation%2Fchinese%2FRacing%2FLocalResults.aspx%3FRaceDate%3D2024%2F04%2F20%26Racecourse%3DST%26RaceNo%3D4',
        's_sq': '%5B%5BB%5D%5D'
    }

    url = f"https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?RaceDate=2024/04/20"
    response = requests.get(url, headers=headers, cookies=cookies)
    bs4_html = BeautifulSoup(response.text, "html.parser")
    date_html_list = bs4_html.find("select", {"id" : "selectId", "class" : "f_fs11"}).find_all("option")

    def date_translate(date_html_text) : 
        date_translate_text = '/'.join([date for date in date_html_text.split("/")][::-1])
        return date_translate_text
    
    def date_list_translate_dict(date) : 
        date_dict = {"date" : date}
        return date_dict

    date_list = [date_translate(date_html.text) for date_html in date_html_list]
    date_list = [date_list_translate_dict(date) for date in date_list]
    date_index_df = pandas.DataFrame(date_list)
    return date_index_df


def bs4_html_parser(date, page) : 
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }

    cookies = {
        'isEU': 'false',
        'AMCVS_06AB2C1653DB07AD0A490D4B%40AdobeOrg': '1',
        'custProIn': '',
        's_cc': 'true',
        'HKJCSSOGP': '1713595766167',
        's_visit': '1',
        'TakeOverMessage': 'COM-7%7CCOM-7%7CCOM-7%7CCOM-7',
        'AMCV_06AB2C1653DB07AD0A490D4B%40AdobeOrg': '-330454231%7CMCIDTS%7C19834%7CMCMID%7C45565919299848919410590974230794634296%7CMCAAMLH-1714200656%7C11%7CMCAAMB-1714200656%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1713603056s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19841%7CvVersion%7C3.1.2',
        'ADRUM': 's=1713595864624&r=https%3A%2F%2Fwww.hkjc.com%2Fhome%2Fchinese%2Findex.aspx',
        'ASPSESSIONIDCCCQARAD': 'BOFHJIFBLCBFFIPCBHOLNHIF',
        'gpv_p5': 'https%3A%2F%2Fracing.hkjc.com%2Fracing%2Finformation%2Fchinese%2FRacing%2FLocalResults.aspx%3FRaceDate%3D2024%2F04%2F20%26Racecourse%3DST%26RaceNo%3D4',
        's_sq': '%5B%5BB%5D%5D'
    }

    url = f"https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate={date}&RaceNo={page}"

    response = requests.get(url, headers=headers, cookies=cookies)
    bs4_html = BeautifulSoup(response.text, "html.parser")
    return bs4_html


def player_info_parser(player_info_origin_df, bs4_html) : 
    player_info_html_list = bs4_html.find("tbody", {"class" : "f_fs12 fontFam"}).find_all("tr")
    def player_data_parser(player_info_html) : 
        player_info_dict = {'名次': None, '馬號': None, '馬名': None, '騎師': None, '練馬師': None, '排位體重': None, '實際負磅': None, 
                            '檔位': None, '頭馬距離': None, '沿途走位': None,  '完成時間': None, '獨嬴賠率': None}
        
        fields = [
            ("馬名", {"class": "f_fs13 f_tal", "style": "white-space: nowrap;"}, 0, "model_1"),
            ("horse_info_url", {"class": "f_fs13 f_tal", "style": "white-space: nowrap;"}, "href", "model_1"),
            ("騎師", {"class": "f_fs13 f_tal"}, 1, "model_1"),
            ("練馬師", {"class": "f_fs13 f_tal"}, 2, "model_1"),
            ("馬號", {}, 1, "model_1"),
            ("實際負磅", {}, 5, "model_1"),
            ("排位體重", {}, 6, "model_1"),
            ("檔位", {}, 7, "model_1"),
            ("頭馬距離", {}, 8, "model_1"),
            ("完成時間", {}, 10, "model_1"),
            ("獨嬴賠率", {}, 11, "model_1"),
            ("沿途走位", {"style": "white-space: nowrap; text-align: center;"}, 0, "model_2"),
            ("名次", {"style": "white-space: nowrap;"}, 0, "model_2")
        ]

        def fields_parser(player_info_dict, field, attributes, index, model) : 
            if model == "model_1" : 
                    try:
                        if index == "href" : 
                            player_info_dict[field] = player_info_html.find_all("td", attributes)[0].find("a")["href"]
                        else  : 
                            player_info_dict[field] = player_info_html.find_all("td", attributes)[index].text
                    except:
                        player_info_dict[field] = None
            elif model == "model_2" : 
                try:
                    player_info_dict[field] = player_info_html.find_all("td", attributes)[index].text
                except:
                    player_info_dict[field] = None
            return player_info_dict

        if len(player_info_html.find_all("td")) == 12 : 
            for field, attributes, index, model in fields:
                player_info_dict = fields_parser(player_info_dict, field, attributes, index, model)

        else : 
            for field, attributes, index, model in fields:
                if field not in ["馬名", "horse_info_url", "沿途走位", "名次"] : 
                    continue
                player_info_dict = fields_parser(player_info_dict, field, attributes, index, model)
        return player_info_dict
    
    def player_meta_parser(player_info_dict) : 
        player_info_dict["日期"] = bs4_html.find("option", {"selected" : "selected"}).text
        player_info_dict["場次"] = bs4_html.find("td", {"colspan" : "16"}).text
        return player_info_dict

    player_info_list = [player_data_parser(player_info_html) for player_info_html in player_info_html_list]
    player_info_list = [player_meta_parser(player_info) for player_info in player_info_list]
    player_info_update_df = pandas.DataFrame(player_info_list)
    player_info_origin_df = pandas.concat([player_info_origin_df, player_info_update_df], ignore_index= True)
    return player_info_origin_df

def parser_horse_image(horse_info_url) : 
    horse_id = horse_info_url.split("_")[-1]
    image_url = f"https://racing.hkjc.com/racing/content/Images/horse/{horse_id}_s.jpg"
    
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    }

    cookies = {
    'AMCVS_06AB2C1653DB07AD0A490D4B@AdobeOrg': '1',
    'custProIn': '',
    's_cc': 'true',
    'TakeOverMessage': 'COM-7%7CCOM-7%7CCOM-7%7CCOM-7',
    'ADRUM': 's=1713595864624&r=https%3A%2F%2Fwww.hkjc.com%2Fhome%2Fchinese%2Findex.aspx',
    'ASPSESSIONIDCCCQARAD': 'BOFHJIFBLCBFFIPCBHOLNHIF',
    'LocalResultDragTable': '0%2F4%2C10%2F8%2C8%2F10%2C10%2F9',
    'ASPSESSIONIDCABSCSDB': 'GAFFKPFBCAMKGCBJPBBDJCBD',
    'ASPSESSIONIDCACTATDB': 'BGCPKNGBNAIGOAGFCFPGBJOH',
    'isEU': 'false',
    'HKJCSSOGP': '1713694019708',
    's_visit': '1',
    'ASPSESSIONIDCCDTDSCB': 'HHLOHPACEOEFNCHFDDJBBJMA',
    'ASPSESSIONIDAQQCDTAC': 'GDCBNNPBBOOADGLONPADDAPH',
    'ASPSESSIONIDACBTBSCA': 'HFNGFBACJKGMOEIPKMOJKKNG',
    's_sq': '%5B%5BB%5D%5D',
    'AMCV_06AB2C1653DB07AD0A490D4B@AdobeOrg': '1585540135|MCIDTS|19834|MCMID|45565919299848919410590974230794634296|MCAAMLH-1714299201|11|MCAAMB-1714299201|6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y|MCOPTOUT-1713701601s|NONE|MCAID|NONE|MCSYNCSOP|411-19841|vVersion|4.4.0',
    'gpv_p5': 'https%3A%2F%2Fracing.hkjc.com%2Fracing%2Fcontent%2FImages%2Fhorse%2FHK_2020_E494_s.jpg'
    }

    response = requests.get(image_url, headers=headers, cookies=cookies)
    with open(os.path.join("house_image", f"{horse_id}.jpg"), "wb") as file:
        file.write(response.content)
