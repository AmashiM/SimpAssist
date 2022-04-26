import pyttsx3
import speech_recognition as sr
import json
from roku import Roku, Application
from typing import Any
from samsungtv import SamsungTV
from pyjarowinkler.distance import get_jaro_distance
import re

num = re.compile(r"(?P<Num>\d+)")


class Henno:
    def __init__(self):
        self.closed = False
        self.config = {}

        with open("./config.json", 'r') as r:
            self.config = json.load(r)


        self.engine = pyttsx3.init("sapi5")
        voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", voices[1].id)
        self.roku: Roku = None
        self.selected_app: Application = None
        

        self.samsung = None
        
        self.volume_change_rate = 1


        self.init_roku()
        # self.init_samsung()

    def init_roku(self):
        self.roku = Roku(self.config['roku'])
        print(self.roku.apps)

    def init_samsung(self):
        self.samsung = SamsungTV(self.config['samsung'])

    def jaro(self, a, b):
        return get_jaro_distance(a, b, winkler_ajustment=False)

    def samsung_power(self):
        self.samsung.power()
        
    def samsung_mute(self):
        self.samsung.mute()
    
    def samsung_menu(self):
        self.samsung.menu()
        
    def samsung_vup(self):
        self.samsung.volume_up(self.volume_change_rate or 1)
    
    def samsung_vdwn(self):
        self.samsung.volume_down(self.volume_change_rate or 1)
    
    def samsung_up(self):
        self.samsung.up()

    def samsung_down(self):
        self.samsung.down()

    def samsung_left(self):
        self.samsung.left()


    def samsung_right(self):
        self.samsung.right()
    
    def samsung_back(self):
        self.samsung.back()

    def select_roku_app(self, app):
        self.selected_app = self.roku[app]

    def roku_launch(self):
        self.selected_app.launch()


    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 0.85
            audio = r.listen(source)
        
        try:
            print("Recognizing...")
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")

        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"

        return query

    def end(self):
        self.closed = True
        self.samsung.close()


if __name__ == '__main__':
    print("started")

    henno = Henno()

    while not henno.closed:

        query = henno.listen().lower()
        if not query:
            continue
        print(query)
        try:
            args = query.split(" ")
            name = args[0]
            if "hamachi" in query or query.startswith(tuple(['shiromachi', 'tamachi'])):
                if "hello" in query:
                    henno.speak("hello world")
                elif "samsung" in query:
                    if "start" in query:
                        henno.init_samsung()
                    elif "power" in query:
                        henno.samsung_power()
                    elif "up" in query:
                        henno.samsung_up()
                    elif "down" in query:
                        henno.samsung_down()
                    elif "right" in query:
                        henno.samsung_right()
                    elif "left" in query:
                        henno.samsung_left()
                    elif "mute" in query:
                        henno.samsung_mute()
                    elif "back" in query:
                        henno.samsung_back()
                    elif "menu" in query:
                        henno.samsung_menu()
                    elif "volume" in query:
                        amount = num.search(query)
                        amt = int(amount.group("Num"))
                        if "add" in query or "ad" in query:
                            henno.samsung.volume_up(amt)
                        elif "remove" in query:
                            henno.samsung.volume_down(amt)
                elif "roku" in query:
                    print("roku func")
                    if "start" in query:
                        henno.speak("initializing roku")
                        henno.init_roku()
                    elif "right" in query:
                        henno.roku.right()
                    elif "left" in query:
                        henno.roku.left()
                    elif "up" in query:
                        henno.roku.up()
                    elif "down" in query:
                        henno.roku.down()
                    elif "home" in query:
                        henno.roku.home()
                    elif "play" in query:
                        henno.roku.play()
                    elif "forward" in query:
                        henno.roku.forward()
                    elif "back" in query:
                        henno.roku.back()
                    elif "replay" in query:
                        henno.roku.replay()
                    elif "select" in query:
                        if "netflix" in query:
                            henno.select_roku_app("Netflix")
                        elif "hulu" in query:
                            henno.select_roku_app("Hulu")
                        elif "crunchyroll" in query:
                            henno.select_roku_app("Crunchyroll")
                    elif "launch" in query:
                        name = query.split("launch")[1]
                        print(name)
                        closest = (None, 0)
                        for i in henno.roku.apps:
                            dist = henno.jaro(name, i.name)
                            if dist > closest[1]:
                                closest = (i, dist)
                        if closest[0] == None:
                            henno.speak("No App Found")
                            continue
                        else:
                            closest[0].launch()

                elif "exit" in query:
                    print("hi")
                    henno.speak("alright")
                    henno.end()
                    exit()
        except Exception as err:
            print(err)




