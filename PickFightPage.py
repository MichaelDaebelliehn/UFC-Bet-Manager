import tkinter
from tkinter import ttk
from tkinter import StringVar
from PIL import ImageTk

class PickFightPage(ttk.Frame):
    
    def __init__(self, parent, controller, style_manager):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.s = style_manager
        self.round_pick = StringVar()
        self.winner_picked = ''
        self.method_picked = ''
        self.round_options = ['1', '2', '3']
        self.title_round_options = ['1', '2', '3', '4', '5']
        self.round_override = False
        self.initialize_styles()
        self.initialize_widgets()
        self.display_widgets()

    def initialize_styles(self):
        # Labels
        self.s.configure('TLabel', foreground='white', font=('Helvetica', 10))
        self.s.configure('header.TLabel', foreground='yellow', font=('Helvetica', 15))
        self.s.configure('fighterName.TLabel', foreground='#0749D5', font=('Helvetica', 15))
        self.s.configure('red.fighterName.TLabel', foreground='#F02804', font=('Helvetica', 15))
        # Options & Checkboxes
        self.s.configure('TCheckbutton', background='#1D1E1E')
        # Buttons
        self.s.configure('back.TButton', background='red')
        self.s.configure('next.TButton', background='blue')

    def initialize_widgets(self):
        # Labels
        self.fighter_one_img = ttk.Label(self)
        self.fighter_two_img = ttk.Label(self)
        self.vs_label = ttk.Label(self, text='vs', font=('Helvetica', 15))
        self.fighter_one_name = ttk.Label(self, text='Conor Mcgregor', font=('Helvetica', 15), style='fighterName.TLabel')
        self.fighter_two_name = ttk.Label(self, text='Jon Jones', font=('Helvetica', 15), style='red.fighterName.TLabel')
        self.method_label = ttk.Label(self, text='METHOD:', style='header.TLabel')
        self.round_label = ttk.Label(self, text='ROUND')
        self.knockout_label = ttk.Label(self, text='KO/TKO')
        self.submission_label = ttk.Label(self, text='SUBMISSION')
        self.decision_label = ttk.Label(self, text='DECISION')
        # Options & Checkboxes
        self.round_option = ttk.OptionMenu(self, self.round_pick, '-', *self.round_options)
        self.fight_one_selected = tkinter.BooleanVar()
        self.fight_two_selected = tkinter.BooleanVar()
        self.ko_selected = tkinter.BooleanVar()
        self.override_selected = tkinter.BooleanVar()
        self.submission_selected = tkinter.BooleanVar()
        self.decision_selected = tkinter.BooleanVar()
        self.fighter_one_checkbox = ttk.Checkbutton(self, command=lambda:self.fight_selected(0), variable=self.fight_one_selected)
        self.fighter_two_checkbox = ttk.Checkbutton(self, command=lambda:self.fight_selected(1), variable=self.fight_two_selected)
        self.knockout_checkbox = ttk.Checkbutton(self, command=lambda:self.method_selected('KO'), variable=self.ko_selected)
        self.submission_checkbox = ttk.Checkbutton(self, command=lambda:self.method_selected('Submission'), variable=self.submission_selected)
        self.decision_checkbox = ttk.Checkbutton(self, command=lambda:self.method_selected('Decision'), variable=self.decision_selected)
        self.round_override_checkbox = ttk.Checkbutton(self, command=self.overrideRounds, variable=self.override_selected)
        # Buttons
        self.back_button = ttk.Button(self, text='Back', style='back.TButton', command=self.controller.show_prev_fight)
        self.next_button = ttk.Button(self, text="Next", style='next.TButton', command=self.next_button_pressed)

    def display_widgets(self):
        # Labels
        self.fighter_one_img.grid(row=0, column=0, padx=25)
        self.fighter_two_img.grid(row=0, column=1, padx=25)
        self.vs_label.grid(row=0, column=0, columnspan=2)
        self.fighter_one_name.grid(row=1, column=0)
        self.fighter_two_name.grid(row=1, column=1, columnspan=2)
        self.method_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        self.knockout_label.grid(row=4, column=0, sticky='w', padx=27)
        self.submission_label.grid(row=4, column=0, sticky='e', padx=5)
        self.decision_label.grid(row=4, column=1, sticky='w', padx=5)
        self.round_label.grid(row=4, column=1, sticky='e', padx=(0, 45))

        # Options & Checkboxes
        self.fighter_one_checkbox.grid(row=2, column=0)
        self.fighter_two_checkbox.grid(row=2, column=1)
        self.knockout_checkbox.grid(row=5, column=0, pady=10, padx=45, sticky='w')
        self.submission_checkbox.grid(row=5, column=0, pady=10, padx=30, sticky='e')
        self.decision_checkbox.grid(row=5, column=1, pady=10, padx=30, sticky='w')
        self.round_option.grid(row=5, column=1, pady=10, padx=(0, 50), sticky='e')
        self.round_override_checkbox.grid(row=5, column=1, sticky='e', padx=(0, 25))
        self.override_selected.set(False)
        
        # Buttons
        self.back_button.grid(row=6, column=0, pady=10, ipady=10)
        self.next_button.grid(row=6, column=1, pady=10, ipady=10)
    
    def overrideRounds(self):
        self.round_override = not self.round_override
        self.round_option.grid_forget()
        if self.round_override:
            self.round_option = ttk.OptionMenu(self, self.round_pick, '-', *self.title_round_options) # disgusting but it works
        else:
            self.round_option = ttk.OptionMenu(self, self.round_pick, '-', *self.round_options)
        self.round_option.grid(row=5, column=1, pady=10, padx=(0, 50), sticky='e')

    def next_button_pressed(self):
        if self.fight_one_selected.get() == False == self.fight_two_selected.get():
            tkinter.messagebox.showinfo("Error",  'Please select a fighter.')
            return
        if self.ko_selected.get() == False == self.submission_selected.get() and self.decision_selected.get() == False:
            tkinter.messagebox.showinfo("Error",  'Please select a method.')
            return('TODO: popup must select method')
        if self.round_pick.get() == '-' and self.decision_selected.get() == False:
            tkinter.messagebox.showinfo("Error",  'Please select a round.')
            return
        self.controller.show_next_fight()

    def fight_selected(self, fight_num):
        if fight_num == 0:
            self.fight_two_selected.set(False)
            self.winner_picked = self.fighter_one_name.cget('text')
        else:
            self.fight_one_selected.set(False)
            self.winner_picked = self.fighter_two_name.cget('text')

    def method_selected(self, method):
        if method == 'KO':
            self.submission_selected.set(False)
            self.decision_selected.set(False)
            self.method_picked = 'KO/TKO'
            self.round_option.configure(state='enabled')
        elif method == 'Submission':
            self.ko_selected.set(False)
            self.decision_selected.set(False)
            self.method_picked = 'Submission'
            self.round_option.configure(state='enabled')

        else:
            self.ko_selected.set(False)
            self.submission_selected.set(False)
            self.round_option.configure(state='disabled')
            self.method_picked = 'Decision'

    def fill_information(self, fight):
        self.fighter_one_name.configure(text=fight[0])
        self.fighter_two_name.configure(text=fight[1])
        if fight[-3]:
            self.round_option.grid_forget()
            self.round_option = ttk.OptionMenu(self, self.round_pick, '-', *self.title_round_options) # disgusting but it works
            self.round_option.grid(row=5, column=1, pady=10, padx=(0, 50), sticky='e')

    def fill_fighter_pics(self, img1, img2):
        # f1 = ImageTk.PhotoImage(img1.result())
        # f2 = ImageTk.PhotoImage(img2.result())
        f1 = ImageTk.PhotoImage(img1)
        f2 = ImageTk.PhotoImage(img2)
        self.fighter_one_img.configure(image=f1)
        self.fighter_two_img.configure(image=f2)
        self.fighter_one_img.image = f1
        self.fighter_two_img.image = f2

    def clear_information(self):
        self.fight_one_selected.set(False)
        self.fight_two_selected.set(False)
        self.ko_selected.set(False)
        self.submission_selected.set(False)
        self.decision_selected.set(False)
        self.round_option.selection_clear()
