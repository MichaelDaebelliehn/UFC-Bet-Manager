import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class FightCard:

    def __init__(self, event_num):
        self.event_num = event_num
        self.url = "https://www.ufc.com/event/ufc-" + str(self.event_num)
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, features="lxml")
        self.num_fights = 0
        self.key_names = []
        self.card_details = self.get_card_details()
        

    def get_card_details(self):
        card_info = self.soup.find_all(class_="c-listing-fight__content")
        fight_list = []
        for fight in card_info:
            fight_list.append(self.get_fight_details(fight))
        self.num_fights = len(fight_list)
        fight_list = fight_list[::-1] # reverses list
        return fight_list

    def get_fight_details(self, fight):
        details = []
        # get fighter names
        names = []
        name_soup = fight.find_all(class_="c-listing-fight__detail-corner-name")
        for line in name_soup:
            names.append(line.get_text().strip())
        self.key_names = names[0::2]
        
        # get fight results
        round = fight.find(class_="c-listing-fight__result-text round").get_text()
        method = fight.find(class_="c-listing-fight__result-text method").get_text().split(' ')[0]
        red_result = fight.find(class_="c-listing-fight__corner-body--red").get_text().replace("\n", " ").split()[0]
        blue_result = fight.find(class_="c-listing-fight__corner-body--blue").get_text().replace("\n", " ").split()[0]
        if red_result == "Win":
            winner = names[0]
        elif red_result == "Draw":
            winner = "Draw"
        elif blue_result == "Win":
            winner = names[1]
        else:
            winner = "N/A"
        # get fighter pics
        imgs = fight.find_all(class_='image-style-event-fight-card-upper-body-of-standing-athlete')
        if len(imgs) < 2:
            red_img_link = 'N/A'
            blue_img_link = 'N/A'
        else:
            try:
                red_img_link = imgs[0]['src'].split('?')[0]
            except:
                red_img_link = 'N/A'
            try:
                blue_img_link = imgs[1]['src'].split('?')[0]
            except:
                blue_img_link = 'N/A'



        title = fight.find(class_='c-listing-fight__class').get_text().split('Title') 
        if len(title) > 1: # this is such a ghetto solution but it works and im lazy
            title = True  
        else: 
            title = False
    
        details.append(names[0])
        details.append(names[1])
        details.append(round)
        details.append(method)
        details.append(winner)
        details.append(title)
        details.append(red_img_link)
        details.append(blue_img_link)
        return details

    def get_live_page(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path='drivers\\chromedriver.exe', options=options)
        browser.get(self.url)
        html = browser.page_source
        browser.close()
        self.soup = BeautifulSoup(html, features='lxml')
        return self.get_card_details()
