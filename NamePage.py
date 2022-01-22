import HomePage, tkinter
from tkinter import ttk
from tkinter import messagebox

class NamePage(ttk.Frame):
    
    def __init__(self, parent, controller, style_manager):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.s = style_manager
        self.initialize_styles()
        self.initialize_widgets()
        self.display_widgets()

    def initialize_styles(self):
        # Labels
        self.s.configure('newPlayer.TLabel', font=('Helvetica', 30, 'bold'), foreground='red')
        self.s.configure('name.TLabel', font=('Helvetica', 12), foreground='white')
        self.s.configure('bet.TLabel', font=('Helvetica', 12), foreground='white')
        # Buttons
        self.s.configure('back.TButton', background='red')
        self.s.configure('next.TButton', background='blue')

    def initialize_widgets(self):
        # Labels
        self.new_bet_header= ttk.Label(self, text='NEW BET', style='newPlayer.TLabel')
        self.name_label = ttk.Label(self, text='Name:', style='name.TLabel')
        self.bet_label = ttk.Label(self, text="Betting", style='bet.TLabel')
        # Entries and Checkboxes
        self.player_name_entry = ttk.Entry(self, width=10, justify='center', font=('Helvetica', 15, 'bold'))
        self.is_betting = tkinter.BooleanVar()
        self.bet_check_box =  ttk.Checkbutton(self, variable=self.is_betting)
        # Buttons
        self.back_button = ttk.Button(self, text='Back', style='back.TButton', command=self.back_button_pressed)
        self.next_button = ttk.Button(self, text="Next", style='next.TButton', command=self.next_button_pressed)

    def display_widgets(self):
        # # Labels
        self.new_bet_header.grid(column=0, row=0, columnspan=2, pady=10)
        self.name_label.grid(column=0, row=1, columnspan=2, pady=(25, 0))
        # self.bet_label.grid(column=0, row=3, pady=(20,0), columnspan=2)
        # Entries and Checkboxes
        self.player_name_entry.grid(column=0, row=2, pady=20, columnspan=2)
        # self.bet_check_box.grid(column=0, row=4, columnspan=2)
        self.is_betting.set(True)
        # Buttons
        self.back_button.grid(column=0, row=5, pady=20, padx=50, ipady=10)
        self.next_button.grid(column=1, row=5, pady=20, padx=50, ipady=10)
    
    def back_button_pressed(self):
        self.controller.clear_frames()
        self.controller.show_frame(HomePage.HomePage)
    
    def next_button_pressed(self):
        if self.player_name_entry.get().strip() != '':
            self.controller.show_next_fight()
        else:
            tkinter.messagebox.showinfo("Invalid entry", "Please enter a name.")

    def clear_information(self):
        self.player_name_entry.delete(0, 'end')