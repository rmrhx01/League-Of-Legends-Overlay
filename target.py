import requests
import json
import os
import warnings
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

import pygetwindow as gw
import tkinter as tk
import time

# Suppress only the InsecureRequestWarning
warnings.filterwarnings("ignore", category=InsecureRequestWarning)

load_dotenv()

DIRECTORY = os.getenv("DIRECTORY")
BASE_URL = "https://127.0.0.1:"
API_KEY = os.getenv("API_KEY")
PROGRAM_DIRECTORY = os.getenv('PROGRAM_DIRECTORY')

class Client:
    def __init__(self):
        self.port,self.password = self.findId()
        self.url = BASE_URL + self.port 
        self.authHeader = ('riot',self.password)
        self.waitStartup()
        self.getSummonerId()


    def findId(self):
        with open(DIRECTORY + r'\lockfile') as lockfile:
            file = lockfile.read()
            file = file.split(':')
            print(f'Found succesfully.\nPort:{file[2]}\nPassword:{file[3]}')
            return (file[2],file[3])


    def goInvisible(self):
        response = self.makeRequest("GET","/lol-chat/v1/session",printFile="chat.json")
        

    def resetChat(self):
        pass


    def makeRequest(self,type:str,link:str,params:str = None,printFile:str = None):
        response=None
        match type:
            case "GET":
                response = requests.get(self.url+link,auth=self.authHeader,verify=False)
            case "POST":
                response = requests.post(self.url+link,params,verify=False)
            
        if printFile:
            object = json.dumps(response.json(),indent=4)
            with open(printFile,"w") as file:
                file.write(object)
        return response

    def getSummonerId(self):
        response = self.makeRequest("GET","/lol-chat/v1/me")
        dictionaryResponse = response.json()
        self.summonerId = dictionaryResponse['summonerId']
        self.name = f'{dictionaryResponse['gameName']}#{dictionaryResponse['gameTag']}'

    def getSkins(self, openFile = False):
        response = self.makeRequest("GET",f"/lol-champions/v1/inventories/{self.summonerId}/skins-minimal",printFile='debug.json')
        dictionaryResponse = response.json()
        skinsDictionary = {}
        for skin in dictionaryResponse:
            if skin['ownership']['owned'] == True:
                if skin['championId'] in skinsDictionary:
                    skinsDictionary[skin['championId']].append(skin['name'])
                else:
                    skinsDictionary[skin['championId']] = [skin['name']]


        championsDictionary = {}
        response = self.makeRequest("GET",f"/lol-champions/v1/inventories/{self.summonerId}/champions-minimal")
        dictionaryResponse = response.json()
        for champion in dictionaryResponse[1:]:
            championsDictionary[champion['id']] = champion['alias']

        championsDictionary = dict(sorted(championsDictionary.items(), key=lambda item: item[1]))

        with open(f"{self.name}_skins.txt","w") as file:
            for champion in championsDictionary:
                file.write(f'{championsDictionary[champion]}\n')
                for index,skin in enumerate(skinsDictionary[champion]):
                    file.write(f'{index}.- {skin}\n')
        
        if openFile:
            os.startfile(f"{self.name}_skins.txt")
     
    def getBlueEssence(self):
        response = self.makeRequest("GET","/lol-loot/v1/player-loot")

        json_object = response.json()

        blue_essence = 0
        for object in json_object:
            if object['disenchantLootName'] == 'CURRENCY_champion':
                blue_essence += object['disenchantValue']
            elif object['asset'] == 'currency_champion':
                disenchanted = object['count']

        print(f'Blue Essence:{disenchanted}\nBlue Essence in Fragments:{blue_essence}\nTotal:{disenchanted+blue_essence}')
        return(blue_essence,disenchanted)

    def waitStartup(self):
        while True:
            try:
                self.makeRequest("GET","/lol-chat/v1/me",printFile="response.json")
                gw.getWindowsWithTitle("League Of Legends")[0]
                break
            except requests.exceptions.ConnectionError:
                time.sleep(5)
            except:
                time.sleep(5)
    
class Lobby:
    def __init__(self, client:Client = None):
        if client == None:
            client = Client()

    def detectLobby(self):
        pass

    def getSummoners(self):
        #/lol-champ-select/v1/session
        
        res = self.client.makeRequest("GET",f"/lol-champ-select/v1/session")
        responseJson = res.json()
        formatted = json.dumps(responseJson,indent=4)
        with open("lobby.json","w") as f:
            f.write(formatted)
        myTeam = responseJson['myTeam']
        for member in myTeam:
            print(member['summonerId'])
        
class Overlay:
    def __init__(self,client:Client = None):
        if client == None:
            client = Client()
        target_window = gw.getWindowsWithTitle("League Of Legends")[0]
        x, y, width, height = target_window.left, target_window.top, target_window.width, target_window.height
        
        # Create a transparent window
        root = tk.Tk()
        root.overrideredirect(True) 
        root.attributes('-topmost', True, '-transparentcolor', 'blue')
        # Reposition and resize the overlay
        root.geometry(f"{int(width)}x{int(height)}+{x}+{y}")
        root.config(bg='blue')  # 'blue' will be transparent

        actions = {
        "Blue Essence": client.getBlueEssence,
        "Skins": lambda:client.getSkins(openFile=True),
        "Exit": root.destroy
        }

        selected_option = tk.StringVar(root)
        selected_option.set("Options")

        def on_select(selection):
            if selection in actions:
                actions[selection]()

        dropdown = tk.OptionMenu(root, selected_option, *actions.keys(), command=on_select)
        dropdown.config(bg="white", fg="black", width=20)
        dropdown.pack(pady=5,side=tk.TOP, anchor=tk.NW)

        

        

        # Run the overlay
        root.mainloop()


if __name__ == "__main__":
    print("Starting Overlay...")
    client = Client()
    overlay = Overlay(client)
    
""""""