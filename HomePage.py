from tkinter import ttk
import tkinter
from PIL import ImageTk, Image
from ResultsPage import ResultsPage

class HomePage(ttk.Frame):
    
    def __init__(self, parent, controller, style_manager):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.s = style_manager
        self.initialize_styles()
        self.initialize_widgets()
        self.display_widgets()

    def initialize_styles(self):
        text_color = 'white'
        # Labels
        self.s.configure('homeHeader.TLabel', background='#1D1E1E', foreground=text_color)
        self.s.configure('TLabel', background='#1D1E1E')
        self.s.configure('homeEventNumber.TLabel', font=('Arial Bold', 15), foreground=text_color)

        # Buttons
        self.s.configure('homeView.TButton', background='blue')
        self.s.configure('homeAdd.TButton', background='red')

        # Frames
        self.s.configure('home.TFrame', background='#1D1E1E')
        self.configure(style='home.TFrame')


    def initialize_widgets(self):
        # Labels
        img = self.convert_resize_image('imgs\\ufc_logo.png', 300, 100)
        self.header = ttk.Label(self, style='homeHeader.TLabel', image=img)
        self.header.image = img
        self.event_number_header =  ttk.Label(self, text='Event #', style='homeEventNumber.TLabel')
        # Entries
        self.event_number_entry = ttk.Entry(self, width=3, font=('Arial', 25), justify='center')
        self.event_number_entry.focus()
        # Buttons
        self.view_bets_button = ttk.Button(self, style='homeView.TButton', text='VIEW BETS', command=self.results_button_pressed)
        self.add_bet_button = ttk.Button(self, style='homeAdd.TButton', text='ADD BET', command=self.next_button_pressed)

    def display_widgets(self):
        # # Labels
        self.header.grid(row=0, columnspan=2, pady=10, padx=10)
        self.event_number_header.grid(row=1, column=0, columnspan=2, pady=10, padx=10)
        # Entries
        self.event_number_entry.grid(row=2, column=0, columnspan=2, pady=(10, 20))
        # Buttons
        self.view_bets_button.grid(row=3, column=0, pady=10, padx=10, ipady=10)
        self.add_bet_button.grid(row=3, column=1, pady=10, padx=10, ipady=10)

    def next_button_pressed(self):
        entry_range = range(1, 1000)
        event_entry = self.event_number_entry.get()
        if event_entry == '': event_entry=0
        if int(event_entry) in entry_range:
            self.controller.set_event_number(event_entry)
            self.controller.fill_fight_frames(event_entry)
        else:
            tkinter.messagebox.showinfo("Bad Entry",  f"Please enter a UFC event number.")
            self.event_number_entry.delete(0, tkinter.END)

    def results_button_pressed(self):
        event_num = self.event_number_entry.get()
        self.controller.set_event_number(event_num)
        self.controller.fill_results_page(event_num)
        self.controller.show_frame(ResultsPage)

    def convert_resize_image(self, file, width, height):
        img = Image.open(file)
        img = img.resize((width, height))
        tk_img = ImageTk.PhotoImage(img)
        return tk_img