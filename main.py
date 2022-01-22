from PIL import Image
import requests
import tkinter as tk
from HomePage import HomePage
from NamePage import NamePage
from PickFightPage import PickFightPage
from ResultsPage import ResultsPage
from PickInfoPage import PickInfoPage
from BetManager import BetManager
from FightCard import FightCard
from tkinter import PhotoImage, ttk
from tkinter.ttk import Style
import concurrent.futures
from multiprocessing import freeze_support

class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('UFC Bet Manager vBeta 1.0')
        img = PhotoImage(file='imgs\\ufc_icon.png')
        self.iconphoto(False, img)
        self.s = Style()
        self.s.configure('TFrame', background='#1D1E1E')
        self.container = ttk.Frame(self)
        self.bet_manager = BetManager(self)
        self.event_num = 0
        self.total_fights = 0
        self.fight_index = 0
        self.frames = {}
        self.buffer_frame = ttk.Frame(self.container)
        self.buffer_frame.grid(row=0, column=0, sticky='nsew')
        self.buffer_frame.grid_columnconfigure(0, weight=1)
        self.buffer_frame.grid_rowconfigure(0, weight=1)
        for F in (HomePage, NamePage, PickFightPage, ResultsPage, PickInfoPage):
            frame = F(self.container, self, self.s)
            self.frames[F] = frame
        self.bind('<Escape>', self.close_window)
        self.current_frame = self.frames[HomePage]
        self.configure_container()
        self.show_frame(HomePage)
        freeze_support()


    def close_window(self, root):
        self.destroy()
            

    def set_event_number(self, event_num):
        self.event_num = event_num

    def configure_container(self):
        self.container.pack(side='top', fill='both', expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)


    def show_frame(self, container):
        self.current_frame.grid_forget()
        frame = self.frames[container]
        self.current_frame = frame
        frame.grid(row=0, column=0)

    def fill_fight_frames(self, event_num):
        card = FightCard(event_num)
        self.fights = card.card_details
        self.total_fights = len(self.fights)
        fighter_pics = {}
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for fight in self.fights:
                fighter_pics[fight[0]] = executor.submit(get_player_pic, fight[-2])
                fighter_pics[fight[1]] = executor.submit(get_player_pic, fight[-1])
        for fight in self.fights:
            frame = PickFightPage(self.container, self, self.s)
            self.frames[fight[0]] = frame
            frame.fill_information(fight)
            frame.fill_fighter_pics(fighter_pics[fight[0]], fighter_pics[fight[1]])
        self.show_frame(NamePage)

    def fill_results_page(self, event_num):
        card = FightCard(event_num)
        self.fights = card.card_details
        self.frames[ResultsPage].fill_page(event_num)

    def clear_frames(self):
        for fight in self.fights:
            self.frames[fight[0]].clear_information()
        self.frames[NamePage].clear_information()

    def show_next_fight(self):
        if self.fight_index < self.total_fights:
            self.show_frame(self.fights[self.fight_index][0])
        else:
            self.add_player()
            self.clear_frames()
            self.fight_index = 0
            return
        self.fight_index += 1
    

    def show_prev_fight(self):
        self.fight_index -= 1
        if self.fight_index > 0:
            self.show_frame(self.fights[self.fight_index-1][0])
        else:
            self.show_frame(NamePage)

    def add_player(self):
        self.bet_manager.add_player(self.frames, self.fights)


def convert_resize_image_web(file, width, height):
    if file == 'N/A':
        file = 'imgs\\standing-stance-right-silhouette.png'
        img = Image.open(file)
        img = img.crop((100, 0, 720, 500))
    else:
        img = Image.open(requests.get(file, stream=True).raw)
        img = img.crop((0, 0, 185, 150))
    img = img.resize((width, height))
    return img

def get_player_pic(fight):
    return convert_resize_image_web(fight, 125, 125)

if __name__ == "__main__":
    app = MainApplication()
    app.geometry('400x350')
    app.mainloop()