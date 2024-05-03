from settings import *
from character import *
def get_connections():
    return {"1":[GREEN,0,0,import_character(),"soldier",(0,0)],"2":[GREEN,2,2,import_character(),"soldier",(1,0)]}
def send_character():
    pass
def get_turn():
    return "1"