import tkinter
from tkinter import ttk
import HomePage
from PickInfoPage import PickInfoPage, PickFiller

class ResultsPage(ttk.Frame):
    
    def __init__(self, parent, controller, style_manager):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.s = style_manager
        self.pick_filler = PickFiller(controller, controller.bet_manager)
        self.initialize_styles()
        self.initialize_widgets()
        self.display_widgets()

    def initialize_styles(self):
        # Labels
        self.s.configure('ranks.TLabel', background='#1D1E1E')
        # Buttons
        self.s.configure('view.TButton', background='green')
        self.s.configure('delete.TButton', background='red')
        self.s.configure('home.TButton', background='blue')


    def initialize_widgets(self):
        # Labels
        headers = ['Rank', 'Name', 'Score']
        self.header_label = ttk.Label(self, text='{:7}{:10}{:6}'.format(headers[0], headers[1], headers[2]), style='ranks.TLabel', font=('Monaco', 15))
        # Entries and Scrollbars
        self.list_box = tkinter.Listbox(self, width=25, height=8, background='#484848', foreground='white', border=5, font=('Monaco', 15))
        # Buttons
        self.home_button = ttk.Button(self, text='Home', style='home.TButton', command=lambda:self.controller.show_frame(HomePage.HomePage))
        self.view_button = ttk.Button(self, text='View Bet', style='view.TButton', command=self.view_bet)
        self.delete_button = ttk.Button(self, text='Delete Bet', style='delete.TButton', command=self.delete_bet)

    def display_widgets(self):
        # Labels
        self.header_label.grid(row=0, column=0, columnspan=3, sticky='w')
        # Entries and Scrollbars
        self.list_box.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        # Buttons
        self.view_button.grid(row=2, column=1, pady=10, padx=10, ipady=10)
        self.delete_button.grid(row=2, column=0, pady=10, padx=10, ipady=10)
        self.home_button.grid(row=2, column=2, pady=10, padx=10, ipady=10)

    def fill_page(self, event_num):
        self.list_box.delete(0, tkinter.END)
        if event_num == 0: return
        scores = self.controller.bet_manager.get_scores(event_num)
        for x, score in enumerate(scores):
            line = '{:7}{:10}{:6}'.format(str(len(scores)-x), score[0], str(score[1]))
            self.list_box.insert(0, line)

    def view_bet(self):
        index = self.list_box.curselection()[0]
        name = self.list_box.get(index)[2:-6].strip()
        self.pick_filler.load_pick_info(name)
        self.controller.show_frame(PickInfoPage)

    def delete_bet(self):
        index = self.list_box.curselection()[0]
        name = self.list_box.get(index)[2:-6].strip()
        confirmed = tkinter.messagebox.askyesno("Delete bet?",  f"Are you sure you want to delete {name}?")
        if confirmed:
            self.controller.bet_manager.delete_bet(self.controller.event_num, name)
            self.list_box.delete(index)
        self.fill_page(self.controller.event_num)
