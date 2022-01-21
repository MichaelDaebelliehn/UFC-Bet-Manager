import pickle
import tkinter
import HomePage
import NamePage
import random

class BetManager:

    def __init__(self, controller):
        self.total_pot = 0
        self.controller = controller
        self.bets = {}
    
    def add_player(self, frames, fights):
        event_num = frames[HomePage.HomePage].event_number_entry.get()
        player_name = frames[NamePage.NamePage].player_name_entry.get().strip()
        player_picks = {}
        for fight in fights:
            frame = frames[fight[0]]
            winner_pick = frame.winner_picked
            method_pick = frame.method_picked
            round_pick = frame.round_pick.get()
            player_picks[fight[0]] = [winner_pick, method_pick, round_pick]
        player = Player(player_name, player_picks)
        self.save_bet(player, event_num)
        self.controller.show_frame(HomePage.HomePage)

    def get_player_score(self, player, fights):
        results = {}
        for fight in fights:
            results[fight[0]] = [fight[4], fight[3], fight[2]]
        total_score = 0
        for key in player.picks.keys():
            correct = 0
            picks = player.picks
            # check for draw and correct fighter
            if results[key][0] != 'Draw':
                if picks[key][0] == results[key][0]:
                    total_score += 1
                    correct += 1
            # check if method is correct
            if results[key][1] == '':  # handles error incase of draw in a fight
                results[key][1] = 'DEC'
            if picks[key][1] == results[key][1]:
                if picks[key][1] == 'DEC':
                    total_score += 2
                    correct += 2
                else:
                    total_score += 1
                    correct += 1
            # check if round correct
            if picks[key][1] != 'DEC' != results[key][1]:
                if picks[key][2] == results[key][2]:
                    total_score += 1
                    correct += 1
            # bonus point for perfect pick
            if correct == 3:
                total_score += 1
        return total_score

    def save_bet(self, player, event_num):
        try:
            self.load_bets(event_num)
            self.bets[player.name] = player
            self.save_bets(event_num)
        except:
            self.bets[player.name] = player
            self.save_bets(event_num)


    def get_scores(self, event_num):
        try:
            self.load_bets(event_num)
            scores = {}
            for bet in self.bets.values():
                bet.score = self.get_player_score(self.bets[bet.name], self.controller.fights)
                scores[bet.name] = bet.score
            sorted_scores = sorted(scores.items(), key=lambda v: v[1])
            return sorted_scores
        except Exception as e:
            print(f'printing error in get_scores --> {e}')


    def delete_bet(self, event_num, name):
        if name == '': return
        print(name)
        self.load_bets(event_num)
        self.bets.pop(name, None)
        self.save_bets(event_num)

    def load_bets(self, event_num):
        filename = 'events\\ufc_' + str(event_num) + '.pkl'
        try:
            self.bets = pickle.load(open(filename, 'rb'))
        except Exception as e:
            print(f'printing error in load_bets --> {e}')

    def save_bets(self, event_num):
        filename = 'events\\ufc_' + str(event_num) + '.pkl'
        pickle.dump(self.bets, open(filename, 'wb'))


class Player:
    def __init__(self, name, picks):
        self.name = name
        self.picks = picks
        self.score = 0