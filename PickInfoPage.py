from tkinter import ttk
import ResultsPage
import tkinter

class PickInfoPage(ttk.Frame):
    
    def __init__(self, parent, controller, style_manager):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.s = style_manager
        self.initialize_widgets()
        self.display_widgets()

    def initialize_widgets(self):
        # Labels
        self.name_label = ttk.Label(self, font=('Monaco', 20))
        # Entries and Listboxes
        self.list_box = tkinter.Listbox(self, width=25, height=8, background='#484848', foreground='white', border=5, font=('Monaco', 15))
        # Buttons
        self.back_button = ttk.Button(self, text='Back', style='back.TButton', command=self.back_button_pressed)

    def display_widgets(self):
        # Labels
        self.name_label.grid(row=0, sticky='n', pady=10)
        # Entries and Listboxes
        self.list_box.grid(row=25)
        # Buttons
        self.back_button.grid(columnspan=2, row=50, pady=20, padx=50, ipady=10)

    def back_button_pressed(self):
        self.list_box.delete(0, tkinter.END)
        self.controller.show_frame(ResultsPage.ResultsPage)

class PickFiller:

    def __init__(self, controller, bet_manager):
        self.controller = controller
        self.bet_manager = bet_manager

    def load_pick_info(self, name):
        picks = self.bet_manager.bets[name].picks
        self.controller.frames[PickInfoPage].name_label.configure(text=f'{name}\'s picks')
        for key in picks.keys():
            if picks[key][1] == 'Submission':
                picks[key][1] = 'Sub'
            pts_line = f'+{picks[key][3]}'
            name_line = f'{picks[key][0].split()[1]} R{picks[key][2]} {picks[key][1]}'
            if picks[key][1] == 'Decision':
                name_line = f'{picks[key][0].split()[1]} {picks[key][1]}'
            self.controller.frames[PickInfoPage].list_box.insert(0, f'{pts_line} {name_line}')

