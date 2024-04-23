import re

def horse_info_url(horse_info_url) : 
    horse_info_url = "https://racing.hkjc.com/" + horse_info_url
    return horse_info_url


def running_position(running_position) :
    try : 
        pattern = r"\d"
        running_position = " ".join(re.findall(pattern, running_position))
        return running_position
    except : 
        return running_position

def race(race) : 
    try : 
        pattern = r"\d"
        race = re.search(pattern, race).group()
        return race
    except : 
        return race

def horse_number(horse_number) : 
    try : 
        pattern = r"\d+"
        horse_number = re.search(pattern, horse_number).group()
        return horse_number
    except : 
        return horse_number
    
def horse_name(horse_name) : 
    try : 
        horse_name = horse_name.split("(")[0].replace(" ", "")
        return horse_name
    except : 
        return horse_name

def trainer(trainer) : 
    try : 
        trainer = trainer.replace("\n", "")
        return trainer
    except : 
        return trainer

def jockey(jockey) : 
    try : 
        jockey = jockey.replace("\n", "")
        return jockey
    except : 
        return jockey

def horse_id(horse_info_url) :
    try : 
        horse_id = horse_info_url.split("_")[-1]
        return horse_id
    except : 
        return None