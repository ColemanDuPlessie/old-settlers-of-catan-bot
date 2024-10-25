"""
Created on Fri Oct  9 18:56:46 2020

Settlers of Catan
"""
import tkinter as tk
import random
import math
import time

board = None

def play(HEXSIZE, TRADELIMIT, bots_to_use, true_root, bal, epsilon, dup_care, force_bal, port_care):
    global board
    SIDESCALE = 0.5
    DICESCALE = 0.8
    PLAYERSPACING = 1.55
    HARBOREDGING = 4.25
    CARDSIZE = 1.5
    DEVCARDSIZE = 1.75
    
    SQRT3 = math.sqrt(3)
    CARDTOPCORNERS = ((int(1200/144*HEXSIZE), int(915/144*HEXSIZE)), (int(1600/144*HEXSIZE), int(915/144*HEXSIZE)))
    BUTTONZONECOORDS = (int(1200/144*HEXSIZE), int(50/144*HEXSIZE), int(1525/144*HEXSIZE), int(800/144*HEXSIZE))
    OPTIONZONECOORDS = (int(800/144*HEXSIZE), int(25/144*HEXSIZE), int(1100/144*HEXSIZE), int(300/144*HEXSIZE))
    CHECKBOXCOLORS = {True : "#00FF00", False : "#FF0000"}
    DEVCARDLEFTCORNERS = ((int(1800/144*HEXSIZE), int(200/144*HEXSIZE)), (int(1800/144*HEXSIZE), int(900/144*HEXSIZE)))
    DEVCARDFILL = "#FFFFBB"
    
    IMPORTANTSTATES = (2, 7, 9)
    DEVCARDDISTRIBUTION = {"Soldier" : 20, "Road Building" : 3, "Year of Plenty" : 3, "Monopoly" : 3, "Victory Point" : 5}
    
    prod_to_color = {0 : "#0000DD", -1 : "#997700", 1 : "#006600", 2 : "#AA1919", 3 : "#00DD00", 4 : "#DDDD22", 5 : "#888888", 6 : "#000000", 7 : "#FFFFFF", 8 : "#008800", 9 : "#881111", 10 : "#00FF00", 11 : "#FFFF44", 12 : "#888888"}
    owner_to_color = {-1 : "#FFFFFF", 1 : "#D4AA1C", 2 : "#D4441C", 3 : "#441C88", 4 : "#44881C"}
    owner_to_light_color = {-1 : "#FFFFFF", 1 : "#EAC28E", 2 : "#EAAA91", 3 : "#AA91BB", 4 : "#AABB91"}
    owner_to_dark_color = {-1 : "#888888", 1 : "#72550E", 2 : "#72220E", 3 : "#220E44", 4 : "#22440E"}
    
    roll_odds = {2 : 1, 3 : 2, 4 : 3, 5 : 4, 6 : 5, 7 : 6, 8 : 5, 9 : 4, 10 : 3, 11 : 2, 12 : 1}
    code_to_state_str = {0 : "You may trade.", 1 : "You must respond to an opponent's trade", 2 : "You must move the robber (Click a hex)", 3 : "You may build", 4 : "Build a settlement", 5 : "Build a city", 6 : "Build a road", 7 : "Lose 1/2 (rounded down) of your cards by clicking on them", 8 : "You may play a development card(s)", 9 : "You must steal with the robber (Click a player card on the left)", 10 : "Select an opponent (or not) to trade with", 11 : "Play Soldier Card?", 12 : "Choose a resource type (Click a hex)"}
    builds = {"Road" : 6, "Settlement" : 4, "City" : 5, "Development Card" : 8}
    
    HIDDEN = tk.HIDDEN
    NORMAL = tk.NORMAL
    
    def combs(a):
        if len(a) == 0:
            return [[]]
        cs = []
        for c in combs(a[1:]):
            cs += [c, c+[a[0]]]
        return cs
    
    def settlement_coords(x, y):
        y = y - HEXSIZE/32
        return (x-HEXSIZE/8, y+HEXSIZE/8, x+HEXSIZE/8, y+HEXSIZE/8, x+HEXSIZE/8, y-HEXSIZE/16, x, int(y-HEXSIZE/8*1.5), x-HEXSIZE/8, y-HEXSIZE/16)
    
    def city_coords(x, y):
        x = x + HEXSIZE/8
        y = y - HEXSIZE/32
        return (x-HEXSIZE/4, y+HEXSIZE/16*3, x+HEXSIZE/8, y+HEXSIZE/16*3, x+HEXSIZE/8, y-HEXSIZE/16, x, int(y-HEXSIZE/8*1.5), x-HEXSIZE/8, y-HEXSIZE/16, x-HEXSIZE/8, y, x-HEXSIZE/4, y)
    
    def robber_coords(x, y):
        y = y + HEXSIZE/24
        x = x + int(HEXSIZE / 4.2)
        top = (x-HEXSIZE/12*0.75, y-2.5*HEXSIZE/12, x+HEXSIZE/12*0.75, y-HEXSIZE/12)
        middle = (x-HEXSIZE/12, y-HEXSIZE/12, x+HEXSIZE/12, y+HEXSIZE/12)
        bottom = (x-HEXSIZE/12, y, x+HEXSIZE/12, y+HEXSIZE/6)
        return (top, middle, bottom)
    
    def die_coords(x, y, num):
        DIESIZE = HEXSIZE * DICESCALE
        ans = []
        if num % 2 == 1:
            ans.append((x-DIESIZE/16, y-DIESIZE/16, x+DIESIZE/16, y+DIESIZE/16))
        if num > 1:
            ans.append((x-DIESIZE/4, y-DIESIZE/4, x-DIESIZE/8, y-DIESIZE/8))
            ans.append((x+DIESIZE/8, y+DIESIZE/8, x+DIESIZE/4, y+DIESIZE/4))
        if num > 3:
            ans.append((x-DIESIZE/4, y+DIESIZE/4, x-DIESIZE/8, y+DIESIZE/8))
            ans.append((x+DIESIZE/4, y-DIESIZE/4, x+DIESIZE/8, y-DIESIZE/8))
        if num == 6:
            ans.append((x-DIESIZE/4, y-DIESIZE/16, x-DIESIZE/8, y+DIESIZE/16))
            ans.append((x+DIESIZE/8, y-DIESIZE/16, x+DIESIZE/4, y+DIESIZE/16))
        ans.append((x-1.5*DIESIZE/4, y-1.5*DIESIZE/4, x+1.5*DIESIZE/4, y+1.5*DIESIZE/4))
        return ans
    
    def card_coords(x, y):
        return rounded_rect_coords(x-HEXSIZE/8*2.5, y-HEXSIZE/8*3.5, x+HEXSIZE/8*2.5, y+HEXSIZE/8*3.5, HEXSIZE/16)
    
    def x_coords(x, y, size):
        return [x+size, y+size, x-size, y-size, x, y, x+size, y-size, x-size, y+size]
    
    def check_coords(x, y, size):
        return [x+size/2, y-size, x-size/2, y+size, x-size, y+size/2]
    
    def arrow_coords(x, y, down):
        ans = [x-HEXSIZE/12, y,
                x+HEXSIZE/12, y,
                x+HEXSIZE/12, y-HEXSIZE/8,
                x+HEXSIZE/8*1.5, y-HEXSIZE/8,
                x, y-HEXSIZE/4,
                x-HEXSIZE/8*1.5, y-HEXSIZE/8,
                x-HEXSIZE/12, y-HEXSIZE/8]
        if down:
            for idx in range(len(ans)):
                if idx % 2 == 1:
                    ans[idx] = 2*y-ans[idx]
        return ans
    
    def sword_coords(x, y):
        x = x-HEXSIZE/16
        y=y+HEXSIZE/16
        return [x+HEXSIZE/4, y-HEXSIZE/4,
                x+HEXSIZE/4, y-HEXSIZE/16*3,
                x+HEXSIZE/16, y,
                x-HEXSIZE/16, y-HEXSIZE/8,
                x-HEXSIZE/8, y-HEXSIZE/16,
                x-HEXSIZE/16, y,
                x-HEXSIZE/8, y+HEXSIZE/16,
                x-HEXSIZE/16, y+HEXSIZE/8,
                x, y+HEXSIZE/16,
                x+HEXSIZE/16, y+HEXSIZE/8,
                x+HEXSIZE/8, y+HEXSIZE/16,
                x, y-HEXSIZE/16,
                x+HEXSIZE/16*3, y-HEXSIZE/4]
    
    def harbor_line_coords(center, vert1, vert2, board):
        choices1 = [board.hex_locs[item] for item in vert1.get_locs()]
        vert1_pos = (choices1[0][0]+choices1[1][0]+choices1[2][0])/3, (choices1[0][1]+choices1[1][1]+choices1[2][1])/3
        choices2 = [board.hex_locs[item] for item in vert2.get_locs()]
        vert2_pos = (choices2[0][0]+choices2[1][0]+choices2[2][0])/3, (choices2[0][1]+choices2[1][1]+choices2[2][1])/3
        center_pos = board.hex_locs[center]
        return [(vert1_pos[0]*HARBOREDGING+center_pos[0])/(1+HARBOREDGING), (vert1_pos[1]*HARBOREDGING+center_pos[1])/(1+HARBOREDGING), center_pos[0], center_pos[1], (vert2_pos[0]*HARBOREDGING+center_pos[0])/(1+HARBOREDGING), (vert2_pos[1]*HARBOREDGING+center_pos[1])/(1+HARBOREDGING)]
    
    def rounded_rect_coords(x1, y1, x2, y2, radius = 25):
        return [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    
    class Bot:
        
        def __init__(self, board, people, me):
            self.board = board
            self.people = people
            self.me = me
            self.name = "Dead Bot"
            self.initialise()
        
        def initialise(self):
            return
        
        def get_name(self):
            return self.name
        
        def receive_prompt(self, prompt, info):
            ans = "ERROR!!!!"
            if prompt == 0:
                ans = self.trade()
            elif prompt == 1:
                ans = self.eval_trade(info)
            elif prompt == 2:
                ans = self.move_robber()
            elif prompt == 3:
                ans = self.build()
            elif prompt == 4:
                ans = self.build_settlement(info)
            elif prompt == 5:
                ans = self.build_city(info)
            elif prompt == 6:
                ans = self.build_road(info)
            elif prompt == 7:
                ans = self.get_robbed(info)
            elif prompt == 8:
                ans = self.play_dev_card()
            elif prompt == 9:
                ans = self.choose_steal(info)
            elif prompt == 10:
                ans = self.pick_traded(info)
            elif prompt == 11:
                ans = self.play_soldier()
            elif prompt == 12:
                ans = self.choose_resource(info)
            self.board.receive_response(ans, self.me.uid)
        
        def log_roll(self, roll):
            pass
        
        def build_settlement(self, legal_choices):
            return random.choice(legal_choices)
        
        def build_city(self, legal_choices):
            return random.choice(legal_choices)
        
        def build_road(self, legal_choices):
            return random.choice(legal_choices)
        
        def trade(self):
            return None
        
        def eval_trade(self, out_in_enemy):
            return False
        
        def pick_traded(self, uids):
            if len(uids) == 0:
                return None
            return random.choice(uids)
        
        def build(self):
            return None
        
        def move_robber(self):
            ans = random.choice([item for item in set(self.board.get_hexes().values())-set((self.board.get_hexes()[self.board.get_robber_loc()],)) if item.get_prod() > 0 and item.get_prod() < 7])
            return ans
        
        def get_robbed(self, cards):
            return random.sample(cards, len(cards)//2)
        
        def choose_steal(self, enemies):
            return random.choice(enemies)
        
        def play_dev_card(self):
            return None
        
        def play_soldier(self):
            return True
        
        def choose_resource(self, monopoly = False):
            return random.randrange(1, 6)
    
    class TakeMyStuff(Bot):
        
        def initialise(self):
            self.name = "Take my stuff!"
        
        def trade(self):
            return (tuple(self.me.cards), (random.randrange(1, 6),))
        
        def eval_trade(self, out_in_enemy):
            return all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)])
        
        def pick_traded(self, uids):
            if len(uids) == 0:
                return None
            return min(uids)
    
    class RandomBot(Bot):
        
        def initialise(self):
            self.name = "Mostly Random Bot"
        
        def eval_trade(self, out_in_enemy):
            return random.random() > 0.75 and all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)])
        
        def build(self):
            if set(self.me.cards) >= set((1, 2, 3, 4)) and len(self.me.settlements) < 5:
                legal_sets = self.board.get_legal_settlements()
                for road in self.me.roads:
                    for vertex in road.get_vertices():
                        if vertex in legal_sets:
                            break
                    else:
                        continue
                    break
                else:
                    if len(self.me.roads) < 15 and random.random() < 0.1:
                        return builds["Road"]
                return builds["Settlement"]
            elif set(self.me.cards) >= set((1, 2)) and len(self.me.roads) < 15 and random.random() < 0.3:
                return builds["Road"]
            elif self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2 and len(self.me.cities) < 4 and len(self.me.settlements) > 0:
                return builds["City"]
            return None
    
    class FoolBot(Bot):
        
        def initialise(self):
            self.name = "Foolish Bot"
            self.can_settle = False
        
        def build_road(self, legal_choices):
            top_tier = []
            mid_tier = []
            legal_sets = self.board.get_legal_settlements()
            for side in legal_choices:
                awesome = False
                for vertex in side.get_vertices():
                    problem = False
                    for other in vertex.get_sides():
                        if other.owner == self.me.uid:
                            break
                    else:
                        if vertex in legal_sets:
                            awesome = True
                    if problem:
                        break
                    else:
                        problem = True
                else:
                    mid_tier.append(side)
                if awesome:
                    top_tier.append(side)
            if len(top_tier) > 0:
                return random.choice(top_tier)
            if len(mid_tier) > 0:
                return random.choice(mid_tier)
            return random.choice(legal_choices)
        
        def build_settlement(self, legal_choices):
            weights = [sum([roll_odds[self.board.get_hex(space).get_num()] for space in choice.get_locs() if self.board.get_hex(space).get_num() in roll_odds]) for choice in legal_choices]
            best = max(weights)
            choices = [idx for idx, val in enumerate(weights) if val == best]
            return legal_choices[random.choice(choices)]
        
        def build_city(self, legal_choices): return self.build_settlement(legal_choices)
        
        def move_robber(self):
            choices = set([item for item in set(self.board.get_hexes().values())-set((self.board.get_hexes()[self.board.get_robber_loc()],)) if item.get_prod() > 0 and item.get_prod() < 7])
            bad_choices = set([item for item in self.board.hexes.values() if any([vertex.owner == self.me.uid for vertex in item.get_vertices()])])
            return random.choice(tuple(choices-bad_choices))
        
        def get_robbed(self, cards):
            to_steal = len(cards)//2
            ans = []
            unsafe = [item for item in cards]
            if self.can_settle:
                for removed in range(1, 5):
                    if removed in unsafe:
                        unsafe.remove(removed)
            else:
                while to_steal > 0 and 3 in unsafe:
                    new = 3
                    unsafe.remove(new)
                    ans.append(new)
                    to_steal -= 1
            while to_steal > 0:
                new = random.choice(unsafe)
                unsafe.remove(new)
                ans.append(new)
                to_steal -= 1
            return ans
        
        def build(self):
            if self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2 and len(self.me.cities) < 4 and len(self.me.settlements) > 0:
                return builds["City"]
            self.can_settle = True
            if len(self.me.settlements) < 5:
                legal_sets = self.board.get_legal_settlements()
                for road in self.me.roads:
                    for vertex in road.get_vertices():
                        if vertex in legal_sets:
                            break
                    else:
                        continue
                    break
                else:
                    self.can_settle = False
            if self.can_settle and set(self.me.cards) >= set((1, 2, 3, 4)) and len(self.me.settlements) < 5:
                return builds["Settlement"]
            elif not self.can_settle and set(self.me.cards) >= set((1, 2)) and len(self.me.roads) < 15:
                return builds["Road"]
            return None
    
    class BalanceBot(FoolBot):
        
        def initialise(self):
            self.name = "Balanced Fool"
            self.can_settle = False
            self.balances = [0, 0, 0, 0, 0]
        
        def build_settlement(self, legal_choices, log_build = True):
            weights = [sum([roll_odds[self.board.get_hex(space).get_num()] * (1+0.5*int(self.balances[self.board.get_hex(space).get_prod()-1] == min(self.balances))) for space in choice.get_locs() if self.board.get_hex(space).get_num() in roll_odds]) for choice in legal_choices]
            best = max(weights)
            choices = [idx for idx, val in enumerate(weights) if val == best]
            ans = legal_choices[random.choice(choices)]
            if log_build:
                for adj_loc in ans.get_locs():
                    adj = self.board.get_hex(adj_loc)
                    if adj.get_num() not in roll_odds:
                        continue
                    self.balances[adj.get_prod()-1] += roll_odds[adj.get_num()]
            return ans
        
    class BalanceRoad(BalanceBot):
        
        def initialise(self):
            self.name = "Balanced Roadbuilder"
            self.can_settle = False
            self.balances = [0, 0, 0, 0, 0]
    
        def build_road(self, legal_choices):
            top_tier = []
            mid_tier = []
            legal_sets = self.board.get_legal_settlements()
            for side in legal_choices:
                    awesome = False
                    for vertex in side.get_vertices():
                        if vertex in legal_sets:
                            awesome = True
                            break
                    if awesome:
                        top_tier.append(side)
            if len(top_tier) > 0:
                return random.choice(top_tier)
            if len(mid_tier) > 0:
                return random.choice(mid_tier)
            return random.choice(legal_choices)
        
        def build(self):
            if self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2 and len(self.me.cities) < 4 and len(self.me.settlements) > 0:
                return builds["City"]
            self.can_settle = True
            if len(self.me.settlements) < 5:
                legal_sets = self.board.get_legal_settlements()
                for road in self.me.roads:
                    for vertex in road.get_vertices():
                        if vertex in legal_sets:
                            break
                    else:
                        continue
                    break
                else:
                    self.can_settle = False
            if self.can_settle and set(self.me.cards) >= set((1, 2, 3, 4)) and len(self.me.settlements) < 5:
                return builds["Settlement"]
            elif self.me.cards.count(1) > int(self.can_settle) and self.me.cards.count(2) > int(self.can_settle) and len(self.me.roads) < 15:
                return builds["Road"]
            return None
    
    class RoadHarbourer(BalanceRoad):
        
        def initialise(self):
            self.name = "Roadbuilder 4:1 Fool"
            self.can_settle = False
            self.did_trade = False
            self.balances = [0, 0, 0, 0, 0]
    
        def build(self):
            self.did_trade = False
            if self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2 and len(self.me.cities) < 4 and len(self.me.settlements) > 0:
                return builds["City"]
            self.can_settle = True
            if len(self.me.settlements) < 5:
                legal_sets = self.board.get_legal_settlements()
                for road in self.me.roads:
                    for vertex in road.get_vertices():
                        if vertex in legal_sets:
                            break
                    else:
                        continue
                    break
                else:
                    self.can_settle = False
            if self.can_settle and set(self.me.cards) >= set((1, 2, 3, 4)) and len(self.me.settlements) < 5:
                return builds["Settlement"]
            elif self.me.cards.count(1) > int(self.can_settle) and self.me.cards.count(2) > int(self.can_settle) and len(self.me.roads) < 15:
                return builds["Road"]
            return None
    
        def trade(self):
            if self.did_trade: return None
            self.did_trade = True
            if self.can_settle:
                needed = [num for num in range(1, 5) if num not in self.me.cards]
                givable = []
                for num in range(1, 6):
                    if self.me.cards.count(num) > int(num < 5) + self.me.harbor_deals[num-1]:
                        givable.append(num)
                trades = min((len(givable), len(needed)))
                if trades < 1:
                    return
                out = random.sample(givable, trades)
                real_out = []
                for item in out:
                    for dummy in range(self.me.harbor_deals[item-1]):
                        real_out.append(item)
                get = random.sample(needed, trades)
                return (real_out, get)
            if self.me.cards.count(4) == 1 and self.me.cards.count(5) >= 3:
                needed = (4,)
                givable = []
                for num in range(1, 6):
                    if self.me.cards.count(num) > int(num > 3) + 2*int(num > 4) + self.me.harbor_deals[num-1]:
                        givable.append(num)
                if len(givable) > 0:
                    to_give = random.choice(givable)
                    return((to_give,)*self.me.harbor_deals[to_give-1], needed)
            if self.me.cards.count(4) >= 2 and self.me.cards.count(5) == 2:
                needed = (5,)
                givable = []
                for num in range(1, 6):
                    if self.me.cards.count(num) > 2*int(num > 3) + self.me.harbor_deals[num-1]:
                        givable.append(num)
                if len(givable) > 0:
                    to_give = random.choice(givable)
                    return((to_give,)*self.me.harbor_deals[to_give-1], needed)
            return None
    
    class TradeLittle(RoadHarbourer):
        
        def initialise(self):
            self.name = "Trade a little"
            self.can_settle = False
            self.did_trade = False
            self.balances = [0, 0, 0, 0, 0]
        
        def trade(self):
            if self.did_trade: return None
            self.did_trade = True
            if self.can_settle:
                needed = [num for num in range(1, 5) if num not in self.me.cards]
                givable = []
                for num in range(1, 6):
                    if self.me.cards.count(num) > int(num < 5) + self.me.harbor_deals[num-1]:
                        givable.append(num)
                trades = min((len(givable), len(needed)))
                if trades < 1:
                    return
                out = random.sample(givable, trades)
                real_out = []
                for item in out:
                    for dummy in range(self.me.harbor_deals[item-1]):
                        real_out.append(item)
                get = random.sample(needed, trades)
                return (real_out, get)
            return None
    
    class TakeTheLoot(RoadHarbourer):
        
        def initialise(self):
            self.name = "Take the loot!"
            self.can_settle = False
            self.did_trade = False
            self.balances = [0, 0, 0, 0, 0]
        
        def eval_trade(self, out_in_enemy):
            return all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)]) and len(out_in_enemy[1]) >= 2*len(out_in_enemy[0])
    
    class HarborLover(RoadHarbourer):
        
        def initialise(self):
            self.name = "Harbor Lover"
            self.can_settle = False
            self.did_trade = False
            self.balances = [0, 0, 0, 0, 0]
            self.HARBORVALUE = 0.3
            self.THREETOONEDISCOUNT = 0.2
        
        def value_hex(self, loc, vert_from):
            space = self.board.get_hex(loc)
            if space.get_num() in roll_odds: return roll_odds[space.get_num()] * (1+0.5*int(self.balances[space.prod-1] == min(self.balances)))
            elif space.prod == 7 and vert_from in space.get_harbored(): return self.THREETOONEDISCOUNT * self.HARBORVALUE * sum(self.balances)
            elif space.prod > 7 and space.prod < 13 and vert_from in space.get_harbored(): return self.HARBORVALUE * self.balances[space.prod-8]
            else: return 0
        
        def build_settlement(self, legal_choices, log_build = True):
            weights = [sum([self.value_hex(space, choice) for space in choice.get_locs()]) for choice in legal_choices]
            best = max(weights)
            choices = [idx for idx, val in enumerate(weights) if val == best]
            ans = legal_choices[random.choice(choices)]
            if log_build:
                for adj_loc in ans.get_locs():
                    adj = self.board.get_hex(adj_loc)
                    if adj.get_num() not in roll_odds:
                        continue
                    self.balances[adj.get_prod()-1] += roll_odds[adj.get_num()]
            return ans
    
    class HarborRoadGuy(HarborLover):
        
        def initialise(self):
            self.name = "Harbor Road Guy"
            self.can_settle = False
            self.did_trade = False
            self.balances = [0, 0, 0, 0, 0]
            self.HARBORVALUE = 0.3
            self.THREETOONEDISCOUNT = 0.2
            
        def find_road_choices(self, legal_choices):
            top_tier = []
            mid_tier = []
            legal_sets = self.board.get_legal_settlements()
            for side in legal_choices:
                    awesome = False
                    for vertex in side.get_vertices():
                        if vertex in legal_sets:
                            awesome = True
                            break
                    if awesome:
                        top_tier.append(side)
            if len(top_tier) > 0:
                return top_tier
            if len(mid_tier) > 0:
                return mid_tier
            return legal_choices
    
    class SmartTrader(HarborRoadGuy):
        
        def initialise(self):
            self.name = "Smart Trader"
            self.can_settle = False
            self.did_trade = False
            self.active_trades = None
            self.balances = [0, 0, 0, 0, 0]
            self.HARBORVALUE = 0.3
            self.THREETOONEDISCOUNT = 0.2
            self.ENEMYSCORETRADEWEIGHT = 0.05
            self.GAINTRADEWEIGHT = 1.5
            self.LOSETRADEWEIGHT = 1.5
            self.DEPENDENTVAR = 0.5
            self.UNCARINGLOSSTRADEWEIGHT = 0.5
        
        def build(self):
            self.did_trade = None
            return super().build()
        
        def trade(self):
            if self.active_trades == None or len(self.active_trades) == 0:
                to_use = super().trade()
                if to_use == None:
                    return to_use
                out = to_use[0]
                self.active_trades = []
                for i in range(TRADELIMIT-1):
                    self.active_trades.append((random.sample(out, random.randrange(1, len(out))), to_use[1]))
                self.active_trades.append(to_use)
                self.active_trades.sort(key=lambda x: len(x[0]), reverse = True)
                return self.active_trades.pop()
            return self.active_trades.pop()
        
        def eval_trade(self, out_in_enemy):
            if not all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)]):
                return False
            self.GAINTRADEWEIGHT = self.DEPENDENTVAR*3
            trade_score = 0
            trade_score -= (self.board.players[out_in_enemy[2]-1].score**2)*self.ENEMYSCORETRADEWEIGHT
            trade_score += (self.me.score**2)*self.ENEMYSCORETRADEWEIGHT
            reserved_cards = [card for card in self.me.cards]
            wants = []
            if self.can_settle:
                for num in range(1, 5):
                    if num in reserved_cards:
                        reserved_cards.remove(num)
                    else:
                        wants.append(num)
            while min((reserved_cards.count(4), 2)) + min((reserved_cards.count(5), 3)) + int(not self.can_settle) + int(len(self.me.settlements) == 5) > 3:
                for num in [4, 4, 5, 5, 5]:
                    if num in reserved_cards:
                        reserved_cards.remove(num)
                    else:
                        wants.append(num)
            while not self.can_settle and (bool(1 in reserved_cards) != bool(2 in reserved_cards)):
                for num in [1, 2]:
                    if num in reserved_cards:
                        reserved_cards.remove(num)
                    else:
                        wants.append(num)
            bad_gives = 0
            good_gets = 0
            for item in out_in_enemy[0]:
                if item in reserved_cards:
                    reserved_cards.remove(item)
                    trade_score -= self.UNCARINGLOSSTRADEWEIGHT
                else:
                    bad_gives += 1
            for item in out_in_enemy[1]:
                if item in wants:
                    good_gets += 1
                    wants.remove(item)
                else:
                    trade_score += self.DEPENDENTVAR
            trade_score += (good_gets**2)*self.GAINTRADEWEIGHT
            trade_score -= (bad_gives**2)*self.LOSETRADEWEIGHT
            return trade_score >= 0
        
        def pick_traded(self, uids):
            self.did_trade = None
            self.active_trades = []
            if len(uids) < 1: return None
            return min(uids, key = lambda uid: self.board.players[uid-1].score)
    
    class SecondGenPeoplePerson(Bot):
        
        def initialise(self):
            self.name = '2nd Gen Trader'
            self.production = [0, 0, 0, 0, 0]
            self.ZEROPRODMULT = 0.5
            self.LOWPRODMULT = 0.5
            self.PORTVALUE = 0.15
            self.TRIPLEHANDICAP = 0.2
            self.GOODGIVESCORE = -1.1
            self.GOODGETSCORE = 4
            self.BADGIVESCORE = -4.5
            self.FINALGOODGETBONUS = 0.5
            self.BADGETSCORE = 1
            self.CITYCONSIDERATIONLEVEL = 3
            self.CITYBIASREQUIREMENT = 1.3
            self.SPARESETTLEMENTCITYBUFF = -0.15
            self.previous_offers = []
            self.curr_target = "Road"
            self.enemy_hands = {uid : [] for uid in range(1, self.board.num_players+1) if uid != self.me.uid}
            self.to_change = False
        
        def change_goal(self):
            if len(self.me.settlements) < 5 and any([vert in self.board.get_legal_settlements() for side in self.me.roads for vert in side.vertices]):
                self.curr_target = "Settlement"
            elif len(self.me.cities) < 4 and len(self.me.settlements) > 0 and (len(self.me.settlements) == 5 or (self.production[3]+self.production[4]) >= (self.production[0]+self.production[1])*(self.CITYBIASREQUIREMENT+self.SPARESETTLEMENTCITYBUFF*len(self.me.settlements))):
                self.curr_target = "City"
            elif len(self.me.roads) < 15:
                self.curr_target = "Road"
            else:
                self.curr_target = "Development Card"
        
        def log_roll(self, roll):
            for space in self.board.hexes.values():
                if space.num == roll:
                    for vert in space.vertices:
                        if vert.owner > 0 and vert.owner != self.me.uid:
                            for dummy in range(vert.level):
                                self.enemy_hands[vert.owner].append(space.prod)
        
        def value_hex(self, to_value):
            if to_value.prod < 1:
                return 0
            elif to_value.prod < 6:
                return roll_odds[to_value.num] * (1+int(self.production[to_value.prod-1]==0)*self.ZEROPRODMULT+int(self.production[to_value.prod-1]==min(self.production))*self.LOWPRODMULT)
            elif to_value.prod == 7:
                return sum(self.production) * self.PORTVALUE * self.TRIPLEHANDICAP
            elif to_value.prod > 7:
                return self.production[to_value.prod-8] * self.PORTVALUE
                
        
        def build_settlement(self, legal_choices, actually_built = True):
            chosen_one = max(legal_choices, key = lambda choice: sum([self.value_hex(space) for space in choice.get_hexes()]))
            if actually_built:
                for space in chosen_one.get_hexes():
                    if space.prod < 1 or space.prod > 5: continue
                    self.production[space.prod-1] += roll_odds[space.num]
            return chosen_one
        
        def build_city(self, legal_choices):
            return self.build_settlement(legal_choices)
        
        def build_road(self, legal_choices):
            verts = set()
            for choice in legal_choices:
                for vert in choice.vertices:
                    verts.add(vert)
            sets = verts.union(set(self.board.get_legal_settlements()))
            if len(sets) > 0:
                good_sets = set([item for item in sets])
                for settlement in sets:
                    for side in settlement.sides:
                        if side.owner > 0 and side.owner != self.me.uid:
                            good_sets.remove(settlement)
                            break
                if len(good_sets) > 0: sets = good_sets
                for space in legal_choices:
                    for vert in space.vertices:
                        if vert in sets: return space
            return random.choice(legal_choices) # TODO
        
        def trade(self):
            needs = []
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                else: needs.append(card)
            if len(needs) == 0 or len(has) == 0: return None
            ans = (random.sample(has, random.randint(1, max((len(has)-1, 1)))), random.sample(needs, random.randint(1, max((len(needs)-1, 1)))))
            return ans
    
        def eval_trade(self, out_in_enemy):
            if not all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)]): return False
            needs = []
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                else: needs.append(card)
            bad_gives = 0
            good_gives = 0
            for item in out_in_enemy[0]:
                if item in has:
                    has.remove(item)
                    good_gives += 1
                else: bad_gives += 1
            good_gets = 0
            bad_gets = 0
            for item in out_in_enemy[1]:
                if item in needs:
                    needs.remove(item)
                    good_gets += 1
                else:
                    bad_gets += 1
            if good_gets >= len(needs): good_gets += self.FINALGOODGETBONUS
            if good_gets*self.GOODGETSCORE+bad_gets*self.BADGETSCORE+good_gives*self.GOODGIVESCORE+bad_gives*self.BADGIVESCORE > 0: return True
            return False
        
        def pick_traded(self, uids):
            if len(uids) == 0:
                return None
            return min(uids, key = lambda x: self.board.players[x-1].score)
        
        def build(self): # TODO
            if self.to_change:
                self.to_change = False
                self.change_goal()
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                else: break
            else:
                self.to_change = True
                return builds[self.curr_target]
            if len(self.me.settlements) > 0 and len(self.me.cities) < 4 and self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2:
                return builds["City"]
            if len(self.me.settlements) < 5 and any([vert in self.board.get_legal_settlements() for side in self.me.roads for vert in side.vertices]) and 1 in self.me.cards and 2 in self.me.cards and 3 in self.me.cards and 4 in self.me.cards:
                return builds["Settlement"]
            if len(self.me.roads) < 15 and 1 in self.me.cards and 2 in self.me.cards and self.curr_target != "Settlement":
                return builds["Road"]
            return None
        
        def move_robber(self):
            choices = [item for item in set(self.board.get_hexes().values())-set((self.board.get_hexes()[self.board.get_robber_loc()],)) if item.get_prod() > 0 and item.get_prod() < 7 and any([vert.owner != self.me.uid and vert.owner > 0 for vert in item.vertices])]
            damages = [sum([vert.level for vert in item.vertices])*roll_odds[item.num] for item in choices]
            best = damages.index(max(damages))
            ans = choices[best]
            return ans
        
        def get_robbed(self, cards):
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                if len(has) <= len(self.me.cards)//2: break
            return random.sample(has, len(self.me.cards)//2)
        
        def choose_steal(self, enemies):
            return max(enemies, key = lambda x: self.board.players[x-1].score)
        
        def play_dev_card(self): # TODO
            return None
        
        def play_soldier(self): # TODO
            return True
    
    class BetterBot2(SecondGenPeoplePerson):
        
        def initialise(self):
            self.name = 'Long-term planner'
            self.production = [0, 0, 0, 0, 0]
            self.ZEROPRODMULT = 0.5
            self.LOWPRODMULT = 0.5
            self.PORTVALUE = 0.15
            self.GOODGIVESCORE = -1.1
            self.GOODGETSCORE = 2
            self.BADGIVESCORE = -3
            self.BADGETSCORE = 1
            self.CITYCONSIDERATIONLEVEL = 3
            self.CITYBIASREQUIREMENT = 1.3
            self.SPARESETTLEMENTCITYBUFF = -0.15
            self.RARITYCONSTANT = 12
            self.previous_offers = []
            self.curr_target = "Road"
            self.underlying_target = "Settlement"
            self.specific_queue = []
            self.enemy_hands = {uid : [] for uid in range(1, self.board.num_players+1) if uid != self.me.uid}
            self.to_change = False
            self.options = {"Road" : (1, 2), "Settlement" : (1, 2, 3, 4), "City" : (4, 4, 5, 5, 5), "Development Card" : (3, 4, 5), "Largest Army" : ()}
            self.build_prefrences = {"Road" : 2, "Settlement" : 1, "City" : 0.8, "Development Card" : 0.33}
            self.biases = {"Road" : 3, "Settlement" : 1, "City" : 1, "Development Card" : 2.5, "Largest Army" : 2}
            self.first_trade = True
            self.done_trades = []
            self.MAXTRADEOFFERSIZE = 4
        
        def build(self):
            self.first_trade = True
            return super().build()
        
        def trade(self):
            if self.first_trade:
                if "Road Building" in self.me.dev_cards and self.curr_target == "Road":
                    return "Road Building"
                elif "Year of Plenty" in self.me.dev_cards:
                    return "Year of Plenty"
                elif "Monopoly" in self.me.dev_cards:
                    return "Monopoly"
                self.first_trade = False
                self.done_trades = []
            needs = []
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                else: needs.append(card)
            if len(needs) == 0 or len(has) == 0: return None
            if len(needs) > self.MAXTRADEOFFERSIZE:
                needs = random.sample(needs, self.MAXTRADEOFFERSIZE)
            if len(has) > self.MAXTRADEOFFERSIZE:
                has = random.sample(has, self.MAXTRADEOFFERSIZE)
            all_choices_in = combs(needs)
            all_choices_out = combs(has)
            all_choices_in.remove([])
            all_choices_out.remove([])
            choices = {(tuple(give), tuple(get)) for give in all_choices_out for get in all_choices_in}
            for item in self.done_trades:
                try:
                    choices.remove(item)
                except KeyError: pass
            if len(choices) < 1: return None
            ans = random.choice(list(choices))
            self.done_trades.append(ans)
            return ans
        
        def value_card(self, card):
            return 36/(self.RARITYCONSTANT+self.production[card-1])
    
        def eval_trade(self, out_in_enemy):
            if not all([out_in_enemy[0].count(num) <= self.me.cards.count(num) for num in range(1, 6)]): return False
            needs = []
            has = [item for item in self.me.cards]
            if self.curr_target == "Road":
                cards = [1, 2]
            elif self.curr_target == "City":
                cards = [4, 4, 5, 5, 5]
            elif self.curr_target == "Settlement":
                cards = [1, 2, 3, 4]
            elif self.curr_target == "Development Card":
                cards = [3, 4, 5]
            else:
                cards = []
            if min((self.me.cards.count(4)-cards.count(4), 2)) + min((self.me.cards.count(5)-cards.count(5), 3)) >= self.CITYCONSIDERATIONLEVEL and min((cards.count(4)//2, cards.count(5)//3)) < len(self.me.settlements):
                cards.extend((4, 4, 5, 5, 5))
            for card in cards:
                if card in has: has.remove(card)
                else: needs.append(card)
            bad_gives = 0
            good_gives = 0
            for item in out_in_enemy[0]:
                if item in has:
                    has.remove(item)
                    good_gives += self.value_card(item)
                else: bad_gives += self.value_card(item)
            good_gets = 0
            bad_gets = 0
            for item in out_in_enemy[1]:
                if item in needs:
                    needs.remove(item)
                    good_gets += self.value_card(item)
                else:
                    bad_gets += self.value_card(item)
            if good_gets*self.GOODGETSCORE+bad_gets*self.BADGETSCORE+good_gives*self.GOODGIVESCORE+bad_gives*self.BADGIVESCORE > 0: return True
            return False
        
        def build_road(self, legal_choices):
            road_to_use = self.can_build_set_after_road()
            if road_to_use is not False and road_to_use in legal_choices:
                return road_to_use
            road_to_use = self.can_build_set_after_double_road()
            if road_to_use is not False and road_to_use[0] in legal_choices:
                return road_to_use[0]
            return super().build_road(legal_choices)
        
        def value_hex(self, to_value):
            if to_value.prod < 1:
                return 0
            elif to_value.prod < 6:
                usefulness_mult = 0
                for thing in self.build_prefrences:
                    usefulness_mult += self.options[thing].count(to_value.prod)*self.build_prefrences[thing]
                return usefulness_mult * (36/max((self.production[to_value.prod-1], 1)) - 36/(self.production[to_value.prod-1]+roll_odds[to_value.num] * (1+int(self.production[to_value.prod-1]==0)*self.ZEROPRODMULT+int(self.production[to_value.prod-1]==min(self.production))*self.LOWPRODMULT)))
            elif to_value.prod == 7:
                return self.PORTVALUE
            elif to_value.prod > 7:
                return self.production[to_value.prod-8]/max((sum(self.production)*5, 1)) * self.PORTVALUE
        
        def next_step_in_plan(self):
            values = {}
            for plan in self.options:
                cost = 0
                need_to_get = list(self.options[plan])
                if plan == "City" and len(self.me.cities) > 3:
                    continue
                elif plan == "City" and len(self.me.settlements) < 1:
                    need_to_get.extend((1, 2, 3, 4))
                    if not self.can_build_settlement:
                        if not self.can_build_road(): continue
                        need_to_get.extend((1, 2))
                elif plan == "Settlement":
                    if len(self.me.settlements) > 4:
                        need_to_get.extend((4, 4, 5, 5, 5))
                    if not self.can_build_settlement():
                        if not self.can_build_road(): continue
                        need_to_get.extend((1, 2))
                if plan == "Road" and not self.can_build_road(): continue
                if plan == "Largest Army":
                    if self.me.has_largest_army or self.me.army_size + self.me.dev_cards.count("Soldier") > max(player.army_size for player in self.board.players): continue
                    need_to_get = [3, 4, 5] * max(player.army_size for player in self.board.players if player is not self.me)
                for resource in range(1, 6):
                    need = max((need_to_get.count(resource) - self.me.cards.count(resource), 0))
                    need *= 36/max((self.production[resource-1], sum(self.production)/8))*self.biases[plan]
                    if need > cost: cost = need
                values[plan] = cost
            self.underlying_target = min(values, key = lambda i: values[i])
            if self.underlying_target == "Road" or self.underlying_target == "Longest Road":
                self.curr_target = "Road"
            elif self.underlying_target == "Settlement":
                if self.can_build_settlement():
                    self.curr_target = "Settlement"
                else:
                    self.curr_target = "Road"
            elif self.underlying_target == "City":
                if len(self.me.settlements) < 1:
                    if not self.can_build_settlement():
                        self.curr_target = "Road"
                    else:
                        self.curr_target = "Settlement"
                else:
                    self.curr_target = "City"
            elif self.underlying_target == "Development Card" or self.underlying_target == "Largest Army":
                self.curr_target = "Development Card"
        
        def can_build_settlement(self):
            sets = self.board.get_legal_settlements()
            return any(any(vert in sets for vert in road.get_vertices()) for road in self.me.roads)
        
        def can_build_road(self): return len(self.me.roads) < 15
        
        def can_build_set_after_road(self):
            sets = self.board.get_legal_settlements()
            for road in self.me.roads:
                for vert in road.vertices:
                    for new in vert.sides:
                        for potential in new.vertices:
                            if potential in sets: return new
            return False
        
        def can_build_set_after_double_road(self):
            sets = self.board.get_legal_settlements()
            for road in self.me.roads:
                for vert in road.vertices:
                    for first in vert.sides:
                        for mid in first.vertices:
                            for second in mid.sides:
                                for potential in second.vertices:
                                    if potential in sets: return (first, second)
            return False
        
        def change_goal(self):
            if self.underlying_target == "Settlement":
                if self.curr_target == "Settlement":
                    self.next_step_in_plan()
                elif self.curr_target == "Road":
                    if self.can_build_settlement():
                        self.curr_target = "Settlement"
                    else:
                        self.curr_target = "Road"
            elif (self.underlying_target == "Road" or self.underlying_target == "Development Card" or self.underlying_target == "City") and self.curr_target == self.underlying_target:
                self.next_step_in_plan()
            elif self.underlying_target == "City":
                if len(self.me.settlements) < 1:
                    if self.can_build_settlement():
                        self.curr_target = "Settlement"
                    else:
                        self.curr_target = "Road"
                else:
                    self.curr_target = "City"
            elif self.underlying_target == "Largest Army" and (self.me.has_largest_army or self.me.army_size + self.me.dev_cards.count("Soldier") > max(player.army_size for player in self.board.players)):
                self.next_step_in_plan()
    
    class HumanPlayer(Bot):
        
        def initialise(self):
            self.state = -1
            self.is_active = False
            self.can_select = False
            self.info = None
            self.trade_interface = [(canvas.create_polygon(0, 0, 0, 0, fill = "#BBFFBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#004400", text = "Done")), (canvas.create_polygon(0, 0, 0, 0, fill = "#FFBBBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#440000", text = "Offer"))]
            for prod in range(1, 6):
                self.trade_interface.append((canvas.create_polygon(0, 0, 0, 0, fill = prod_to_color[prod], outline = ""), canvas.create_text(0, 0, anchor = "center", fill = prod_to_color[prod], text = 0, state = HIDDEN), canvas.create_polygon(0, 0, 0, 0, fill = prod_to_color[prod], outline = "")))
            self.wants = [0, 0, 0, 0, 0]
            self.receive_interface = [canvas.create_text(0, 0, fill = "black", anchor = "center", state = HIDDEN, text = "Get from player #%d" % -1), canvas.create_text(0, 0, fill = "black", anchor = "center", state = HIDDEN, text = "Give to player #%d" % -1), (canvas.create_polygon(0, 0, 0, 0, fill = "#BBFFBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#004400", text = "Yes")), (canvas.create_polygon(0, 0, 0, 0, fill = "#FFBBBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#440000", text = "No"))]
            for prod in range(1, 11):
                self.receive_interface.append(canvas.create_text(0, 0, anchor = "center", fill = prod_to_color[(prod-1)%5+1], text = 0, state = HIDDEN))
            self.build_interface = [(canvas.create_polygon(0, 0, 0, 0, fill = "#BBFFBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#004400", text = "Done")), canvas.create_text(0, 0, fill = "black", anchor = "center", text = "Build:", state = HIDDEN), (canvas.create_polygon(0, 0, 0, 0, fill = owner_to_light_color[self.me.uid], outline = "black", smooth = True), canvas.create_polygon(0, 0, 0, 0, fill = owner_to_dark_color[self.me.uid])), (canvas.create_polygon(0, 0, 0, 0, fill = owner_to_light_color[self.me.uid], outline = "black", smooth = True), canvas.create_polygon(0, 0, 0, 0, fill = owner_to_dark_color[self.me.uid])), (canvas.create_polygon(0, 0, 0, 0, fill = owner_to_light_color[self.me.uid], outline = "black", smooth = True), canvas.create_line(0, 0, 0, 0, fill = owner_to_dark_color[self.me.uid])), (canvas.create_polygon(0, 0, 0, 0, fill = owner_to_light_color[self.me.uid], outline = "black", smooth = True), canvas.create_polygon(0, 0, 0, 0, fill = owner_to_dark_color[self.me.uid], smooth = True))]
            self.pick_interface = [(canvas.create_polygon(0, 0, 0, 0, fill = "#FFBBBB", outline = "black", smooth = True), canvas.create_text(0, 0, anchor = "center", fill = "#440000", text = "No"))]
            for player in self.board.players:
                if player == self.me:
                    self.pick_interface.append(None)
                else:
                    self.pick_interface.append((canvas.create_polygon(0, 0, 0, 0, fill = owner_to_light_color[player.uid], outline = "black", smooth = True), canvas.create_line(0, 0, 0, 0, fill = owner_to_dark_color[player.uid])))
            self.name = "This is you!"
            self.checkboxes = [canvas.create_polygon(rounded_rect_coords(OPTIONZONECOORDS[0], OPTIONZONECOORDS[1], OPTIONZONECOORDS[0]+HEXSIZE/4, OPTIONZONECOORDS[1]+HEXSIZE/4, HEXSIZE/8), smooth = True, fill = CHECKBOXCOLORS[True], width = HEXSIZE/24, outline = "black")]
            self.checkbox_labels = [canvas.create_text(OPTIONZONECOORDS[0]+HEXSIZE/8*3, OPTIONZONECOORDS[1]+HEXSIZE/8, fill = "black", font = ("Helvetica", int(HEXSIZE/8)), text = "View trades you cannot accept", anchor = "w")]
            self.checkbox_states = [True]
            canvas.bind("<Button-1>", self.click)
        
        def receive_prompt(self, prompt, info):
            if prompt == 1 and not self.checkbox_states[0] and any([self.me.cards.count(num) < info[0].count(num) for num in range(1, 6)]):
                self.board.receive_response(False, self.me.uid)
                return
            self.is_active = True
            self.info = info
            self.state = prompt
            if prompt == 3 or prompt == 0 or prompt == 1 or prompt == 10 or prompt == 11 or prompt == 12:
                self.build_display()
                self.can_select = prompt == 0
            elif prompt == 4 or prompt == 6:
                for item in info:
                    item.do_highlight()
            elif prompt == 7:
                self.can_select = True
        
        def log_roll(self, roll):
            self.board.draw()
            true_root.update()
            time.sleep(1)
        
        def build_display(self):
            self.can_settle = True
            if len(self.me.settlements) < 5:
                legal_sets = self.board.get_legal_settlements()
                for road in self.me.roads:
                    for vertex in road.get_vertices():
                        if vertex in legal_sets:
                            break
                    else:
                        continue
                    break
                else:
                    self.can_settle = False
            if self.state == 0:
                canvas.itemconfig(self.trade_interface[0][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.trade_interface[0][0], rounded_rect_coords(BUTTONZONECOORDS[0], BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[0] + HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.trade_interface[0][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)), text = "Done")
                canvas.coords(self.trade_interface[0][1], (BUTTONZONECOORDS[0] + HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                canvas.itemconfig(self.trade_interface[1][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.trade_interface[1][0], rounded_rect_coords(BUTTONZONECOORDS[2] - HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[2], BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.trade_interface[1][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)), text = "Offer")
                canvas.coords(self.trade_interface[1][1], (BUTTONZONECOORDS[2] - HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                for arrows_idx in range(2, 7):
                    ui_item = self.trade_interface[arrows_idx]
                    x = BUTTONZONECOORDS[0] + HEXSIZE/2
                    if arrows_idx % 2 == 1:
                        x = BUTTONZONECOORDS[2] - HEXSIZE/2
                    if arrows_idx == 6:
                        x = (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2
                    y = BUTTONZONECOORDS[1] + HEXSIZE/2*(2*(arrows_idx//2)-1)
                    for item in ui_item:
                        canvas.itemconfig(item, state = NORMAL)
                    canvas.coords(ui_item[0], arrow_coords(x, y-HEXSIZE/8, False))
                    canvas.itemconfig(ui_item[1], text = self.wants[arrows_idx-2], font = ("Helvetica", int(HEXSIZE/8)))
                    canvas.coords(ui_item[1], x, y)
                    canvas.coords(ui_item[2], arrow_coords(x, y+HEXSIZE/8, True))
            elif self.state == 1:
                canvas.itemconfigure(self.receive_interface[0], state = NORMAL, text = "Get from Player #%d" % self.info[2], font = ("Helvetica", int(HEXSIZE/4)), fill = owner_to_dark_color[self.info[2]])
                canvas.coords(self.receive_interface[0], (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1] + HEXSIZE/2)
                canvas.itemconfigure(self.receive_interface[1], state = NORMAL, text = "Give to Player #%d" % self.info[2], font = ("Helvetica", int(HEXSIZE/4)), fill = owner_to_dark_color[self.info[2]])
                canvas.coords(self.receive_interface[1], (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1] + HEXSIZE*2)
                if all([self.me.cards.count(num) >= self.info[0].count(num) for num in range(1, 6)]):
                    canvas.itemconfig(self.receive_interface[2][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.receive_interface[2][0], rounded_rect_coords(BUTTONZONECOORDS[0], BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[0] + HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                    canvas.itemconfig(self.receive_interface[2][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                    canvas.coords(self.receive_interface[2][1], (BUTTONZONECOORDS[0] + HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                canvas.itemconfig(self.receive_interface[3][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.receive_interface[3][0], rounded_rect_coords(BUTTONZONECOORDS[2] - HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[2], BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.receive_interface[3][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                canvas.coords(self.receive_interface[3][1], (BUTTONZONECOORDS[2] - HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                for prod in range(1, 6):
                    canvas.itemconfig(self.receive_interface[prod+3], state = NORMAL, text = self.info[1].count(prod), font = ("Helvetica", int(HEXSIZE/2)))
                    canvas.coords(self.receive_interface[prod+3], (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2+HEXSIZE/2*(prod-3), BUTTONZONECOORDS[1] + HEXSIZE/4*5)
                    canvas.itemconfig(self.receive_interface[prod+8], state = NORMAL, text = self.info[0].count(prod), font = ("Helvetica", int(HEXSIZE/2)))
                    canvas.coords(self.receive_interface[prod+8], (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2+HEXSIZE/2*(prod-3), BUTTONZONECOORDS[1] + HEXSIZE/4*11)
            elif self.state == 3:
                canvas.itemconfig(self.build_interface[0][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.build_interface[0][0], rounded_rect_coords(BUTTONZONECOORDS[0], BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[0] + HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.build_interface[0][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                canvas.coords(self.build_interface[0][1], (BUTTONZONECOORDS[0] + HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                canvas.itemconfig(self.build_interface[1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/2)))
                canvas.coords(self.build_interface[1], ((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1]+HEXSIZE/4))
                if set(self.me.cards) >= set((1, 2, 3, 4)) and self.can_settle:
                    canvas.itemconfig(self.build_interface[2][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.build_interface[2][0], rounded_rect_coords(BUTTONZONECOORDS[0]+HEXSIZE/8, BUTTONZONECOORDS[1]+HEXSIZE/4*3, BUTTONZONECOORDS[0] + HEXSIZE/8*7, BUTTONZONECOORDS[1]+HEXSIZE/2*3, HEXSIZE/4))
                    canvas.itemconfig(self.build_interface[2][1], state = NORMAL)
                    canvas.coords(self.build_interface[2][1], settlement_coords(BUTTONZONECOORDS[0]+HEXSIZE/2, BUTTONZONECOORDS[1]+HEXSIZE/8*9))
                if self.me.cards.count(4) > 1 and self.me.cards.count(5) > 2 and len(self.me.settlements) > 0 and len(self.me.cities) < 4:
                    canvas.itemconfig(self.build_interface[3][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.build_interface[3][0], rounded_rect_coords(BUTTONZONECOORDS[2]-HEXSIZE/8*7, BUTTONZONECOORDS[1]+HEXSIZE/4*3, BUTTONZONECOORDS[2]-HEXSIZE/8, BUTTONZONECOORDS[1]+HEXSIZE/2*3, HEXSIZE/4))
                    canvas.itemconfig(self.build_interface[3][1], state = NORMAL)
                    canvas.coords(self.build_interface[3][1], city_coords(BUTTONZONECOORDS[2]-HEXSIZE/8*5, BUTTONZONECOORDS[1]+HEXSIZE/8*9))
                if self.me.cards.count(1) > 0 and self.me.cards.count(2) > 0 and len(self.me.roads) < 15:
                    canvas.itemconfig(self.build_interface[4][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.build_interface[4][0], rounded_rect_coords(BUTTONZONECOORDS[0]+HEXSIZE/8, BUTTONZONECOORDS[1]+HEXSIZE/4*7, BUTTONZONECOORDS[0] + HEXSIZE/8*7, BUTTONZONECOORDS[1]+HEXSIZE/2*5, HEXSIZE/4))
                    canvas.itemconfig(self.build_interface[4][1], state = NORMAL, width = int(HEXSIZE/18))
                    canvas.coords(self.build_interface[4][1], (BUTTONZONECOORDS[0]+HEXSIZE/8*3, BUTTONZONECOORDS[1]+HEXSIZE*2, BUTTONZONECOORDS[0]+HEXSIZE/8*5, BUTTONZONECOORDS[1]+HEXSIZE/4*9))
                if self.me.cards.count(3) > 0 and self.me.cards.count(4) > 0 and self.me.cards.count(5) > 0:
                    canvas.itemconfig(self.build_interface[5][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.build_interface[5][0], rounded_rect_coords(BUTTONZONECOORDS[2]-HEXSIZE/8*7, BUTTONZONECOORDS[1]+HEXSIZE/4*7, BUTTONZONECOORDS[2]-HEXSIZE/8, BUTTONZONECOORDS[1]+HEXSIZE/2*5, HEXSIZE/4))
                    canvas.itemconfig(self.build_interface[5][1], state = NORMAL)
                    canvas.coords(self.build_interface[5][1], [item/2 for item in card_coords(BUTTONZONECOORDS[2]*2-HEXSIZE, BUTTONZONECOORDS[1]*2+HEXSIZE/4*17)])
            elif self.state == 10:
                canvas.itemconfig(self.pick_interface[0][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.pick_interface[0][0], rounded_rect_coords((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2-HEXSIZE/2, BUTTONZONECOORDS[3] - HEXSIZE, (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2+HEXSIZE/2, BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.pick_interface[0][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                canvas.coords(self.pick_interface[0][1], ((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                things_displayed = 0
                for idx in range(len(self.board.players)):
                    if idx+1 == self.me.uid or self.pick_interface[idx+1] == None: continue
                    things_displayed += 2
                    canvas.itemconfig(self.pick_interface[idx+1][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.pick_interface[idx+1][0], rounded_rect_coords((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2-HEXSIZE/8*3, BUTTONZONECOORDS[1] + HEXSIZE/2*things_displayed, (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2+HEXSIZE/8*3, BUTTONZONECOORDS[1] + HEXSIZE/2*(things_displayed+1.5), HEXSIZE/4))
                    canvas.itemconfig(self.pick_interface[idx+1][1], state = NORMAL, width = HEXSIZE/16)
                    if idx+1 in self.info:
                        canvas.coords(self.pick_interface[idx+1][1], check_coords((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1] + HEXSIZE/2*(things_displayed+0.75), HEXSIZE/4))
                    else:
                        canvas.coords(self.pick_interface[idx+1][1], x_coords((BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1] + HEXSIZE/2*(things_displayed+0.75), HEXSIZE/4))
            elif self.state == 11:
                canvas.itemconfigure(self.receive_interface[0], state = NORMAL, text = "Play a soldier before you roll?", font = ("Helvetica", int(HEXSIZE/4)), fill = "black")
                canvas.coords(self.receive_interface[0], (BUTTONZONECOORDS[0]+BUTTONZONECOORDS[2])/2, BUTTONZONECOORDS[1] + HEXSIZE/2)
                canvas.itemconfig(self.receive_interface[2][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.receive_interface[2][0], rounded_rect_coords(BUTTONZONECOORDS[0], BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[0] + HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.receive_interface[2][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                canvas.coords(self.receive_interface[2][1], (BUTTONZONECOORDS[0] + HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
                canvas.itemconfig(self.receive_interface[3][0], state = NORMAL, width = int(HEXSIZE/16))
                canvas.coords(self.receive_interface[3][0], rounded_rect_coords(BUTTONZONECOORDS[2] - HEXSIZE, BUTTONZONECOORDS[3] - HEXSIZE, BUTTONZONECOORDS[2], BUTTONZONECOORDS[3] - HEXSIZE/4, HEXSIZE/4))
                canvas.itemconfig(self.receive_interface[3][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)))
                canvas.coords(self.receive_interface[3][1], (BUTTONZONECOORDS[2] - HEXSIZE/2, BUTTONZONECOORDS[3]-HEXSIZE/8*5))
            elif self.state == 12:
                canvas.itemconfigure(self.receive_interface[0], state = NORMAL, text = "Choose a resource type (Click a hex)", font = ("Helvetica", int(HEXSIZE/4)), fill = "black")
        
        def send_message(self, info):
            self.can_select = False
            self.me.selected_idxs = []
            self.me.draw_cards()
            if self.state == 0 or self.state == 3:
                self.me.selected_dev_idx = None
                self.me.draw_dev_cards()
            if self.state == 0:
                for item in self.trade_interface:
                    if isinstance(item, int):
                        canvas.itemconfigure(item, state = HIDDEN)
                    else:
                        for sub in item:
                            canvas.itemconfigure(sub, state = HIDDEN)
            elif self.state == 1 or self.state == 11 or self.state == 12:
                for item in self.receive_interface:
                    if isinstance(item, int):
                        canvas.itemconfigure(item, state = HIDDEN)
                    else:
                        for sub in item:
                            canvas.itemconfigure(sub, state = HIDDEN)
            elif self.state == 7:
                for item in self.trade_interface[0]:
                    canvas.itemconfigure(item, state = HIDDEN)
            elif self.state == 3:
                for item in self.build_interface:
                    if isinstance(item, int):
                        canvas.itemconfigure(item, state = HIDDEN)
                    else:
                        for sub in item:
                            canvas.itemconfigure(sub, state = HIDDEN)
            elif self.state == 10:
                for item in self.pick_interface:
                    if isinstance(item, int) or item == None:
                        canvas.itemconfigure(item, state = HIDDEN)
                    else:
                        for sub in item:
                            canvas.itemconfigure(sub, state = HIDDEN)
            self.is_active = False
            self.board.receive_response(info, self.me.uid)
        
        def card_selected(self):
            self.me.draw_panel(self.me.x, self.me.y)
            if self.state == 7:
                if len(self.me.selected_idxs) == len(self.me.cards) // 2:
                    canvas.itemconfig(self.trade_interface[0][0], state = NORMAL, width = int(HEXSIZE/16))
                    canvas.coords(self.trade_interface[0][0], rounded_rect_coords(BUTTONZONECOORDS[0], BUTTONZONECOORDS[3] - HEXSIZE/4*5, BUTTONZONECOORDS[0] + HEXSIZE*1.5, BUTTONZONECOORDS[3] - HEXSIZE/2, HEXSIZE/4))
                    canvas.itemconfig(self.trade_interface[0][1], state = NORMAL, font = ("Helvetica", int(HEXSIZE/4)), text = "Discard")
                    canvas.coords(self.trade_interface[0][1], (BUTTONZONECOORDS[0] + HEXSIZE/4*3, BUTTONZONECOORDS[3]-HEXSIZE/8*7))
                else:
                    for item in self.trade_interface[0]:
                        canvas.itemconfig(item, state = HIDDEN)
        
        def click(self, event):
            clicked = canvas.find_withtag("current")
            if len(clicked) > 0 and clicked[0] in self.checkboxes:
                self.checkbox_states[self.checkboxes.index(clicked[0])] = not self.checkbox_states[self.checkboxes.index(clicked[0])]
                canvas.itemconfig(clicked[0], fill = CHECKBOXCOLORS[self.checkbox_states[self.checkboxes.index(clicked[0])]])
            if not self.is_active:
                return
            if self.state == 0 or self.state == 3:
                chosen = False
                if len(clicked) > 0:
                    for item_idx in range(len(self.me.dev_card_depictions)):
                        if clicked[0] in self.me.dev_card_depictions[item_idx]:
                            chosen = True
                            if item_idx == self.me.selected_dev_idx and self.me.dev_cards[item_idx] != "Victory Point":
                                self.send_message(self.me.dev_cards[item_idx])
                            elif self.me.dev_cards[item_idx] != "Victory Point" and self.me.dev_cards.count(self.me.dev_cards[item_idx]) > self.me.unplayable_dev_cards.count(self.me.dev_cards[item_idx]):
                                self.me.selected_dev_idx = item_idx
                            break
                if chosen:
                    self.me.draw_dev_cards()
                    return
                else:
                    if self.me.selected_dev_idx != None:
                        self.me.selected_dev_idx = None
                        self.me.draw_dev_cards()
            if len(clicked) == 0: return
            if self.state == 0:
                if clicked[0] in self.trade_interface[0]:
                    self.send_message(None)
                    return
                elif clicked[0] in self.trade_interface[1]:
                    gives = [self.me.cards[idx] for idx in self.me.selected_idxs]
                    gets = []
                    for idx in range(len(self.wants)):
                        for dummy in range(self.wants[idx]):
                            gets.append(idx+1)
                    if len(gives) < 1 or len(gets) < 1 or any([gives.count(num) > 0 and gets.count(num) > 0 for num in range(1, 6)]):
                        return
                    self.send_message((gives, gets))
                    self.wants = [0, 0, 0, 0, 0]
                else:
                    for idx in range(1, 6):
                        if clicked[0] in self.trade_interface[idx+1]:
                            if self.trade_interface[idx+1][0] == clicked[0]:
                                self.wants[idx-1] += 1
                            elif self.trade_interface[idx+1][2] == clicked[0]:
                                self.wants[idx-1] = max((0, self.wants[idx-1]-1))
                            self.build_display()
                            return
            elif self.state == 1 or self.state == 11:
                if clicked[0] in self.receive_interface[2]:
                    self.send_message(True)
                elif clicked[0] in self.receive_interface[3]:
                    self.send_message(False)
            elif self.state == 2:
                for space in self.board.hexes.values():
                    if (clicked[0] == space.depiction or clicked[0] == space.circled or clicked[0] == space.numd) and space.get_loc() != self.board.robber_loc:
                        self.send_message(space)
                        return
            elif self.state == 3:
                if clicked[0] in self.build_interface[0]:
                    self.send_message(None)
                    return
                elif clicked[0] in self.build_interface[2]:
                    self.send_message(builds["Settlement"])
                    return
                elif clicked[0] in self.build_interface[3]:
                    self.send_message(builds["City"])
                    return
                elif clicked[0] in self.build_interface[4]:
                    self.send_message(builds["Road"])
                    return
                elif clicked[0] in self.build_interface[5]:
                    self.send_message(builds["Development Card"])
                    return
            elif self.state == 4:
                if len(clicked) == 0:
                    return
                for vertex in self.board.vertices.values():
                    if vertex.highlight == clicked[0]:
                        self.send_message(vertex)
                        return
            elif self.state == 5:
                if len(clicked) == 0:
                    return
                for vertex in self.board.vertices.values():
                    if vertex.depiction == clicked[0] and vertex.level == 1 and vertex.owner == self.me.uid:
                        self.send_message(vertex)
                        return
            elif self.state == 6:
                if len(clicked) == 0:
                    return
                for side in self.board.sides.values():
                    if side.is_highlighted and side.depiction == clicked[0]:
                        self.send_message(side)
                        return
            elif self.state == 7:
                if clicked[0] in self.trade_interface[0]:
                    self.send_message([self.me.cards[item] for item in self.me.selected_idxs])
                    return
            elif self.state == 9:
                for player in self.board.players:
                    if clicked[0] in player.player_panel and player.uid in self.info:
                        self.send_message(player.uid)
                        return
            elif self.state == 10:
                if clicked[0] in self.pick_interface[0]:
                    self.send_message(None)
                    return
                for idx in range(1, len(self.pick_interface)):
                    if self.pick_interface[idx] != None and clicked[0] in self.pick_interface[idx] and idx in self.info:
                        self.send_message(idx)
                        return
            elif self.state == 12:
                for space in self.board.hexes.values():
                    if (clicked[0] == space.depiction or clicked[0] == space.circled or clicked[0] == space.numd) and space.get_loc() != self.board.robber_loc:
                        self.send_message(space.prod)
                        return
            if self.can_select:
                if clicked[0] in self.me.card_depictions:
                    if self.me.card_depictions.index(clicked[0]) in self.me.selected_idxs:
                        self.me.selected_idxs.remove(self.me.card_depictions.index(clicked[0]))
                    else:
                        self.me.selected_idxs.append(self.me.card_depictions.index(clicked[0]))
                    self.card_selected()
    
    class Player:
        
        def __init__(self, board, uid, should_draw = False):
            self.board = board
            self.uid = uid
            self.score = 0
            self.settlements = []
            self.cities = []
            self.roads = []
            self.cards = []
            self.dev_cards = []
            self.unplayable_dev_cards = []
            self.should_draw = should_draw
            self.selected_idxs = []
            self.selected_dev_idx = None
            self.long_road_length = 0
            self.army_size = 0
            self.has_largest_army = False
            self.has_longest_road = False
            self.harbor_deals = [4, 4, 4, 4, 4]
            if should_draw:
                self.card_depictions = []
                self.dev_card_depictions = []
            self.x = 0
            self.y = 0
            self.player_panel = [canvas.create_polygon([0, 0, 0, 0], outline = "", smooth = True, fill = owner_to_light_color[self.uid]), canvas.create_polygon([0, 0, 0, 0], outline = "black", fill = "#2222AA", smooth = True), canvas.create_text(0, 0, fill = "white", anchor = "center", text = ""), canvas.create_text(0, 0, fill = owner_to_dark_color[self.uid], anchor = "w", text = ""), canvas.create_text(0, 0, fill = owner_to_dark_color[self.uid], anchor = "e", text = ""), canvas.create_line((0, 0, 0, 0), fill = owner_to_dark_color[self.uid]), canvas.create_text(0, 0, fill = "black", anchor = "w", text = ""), canvas.create_polygon((0, 0, 0, 0), fill = owner_to_dark_color[self.uid], outline = ""), canvas.create_text(0, 0, fill = "black", anchor = "w", text = ""), canvas.create_polygon((0, 0, 0, 0), fill = owner_to_dark_color[self.uid], outline = ""), canvas.create_text(0, 0, fill = "black", anchor = "w", text = ""), canvas.create_text(0, 0, fill = owner_to_dark_color[self.uid], anchor = "e", text = "1st"), canvas.create_polygon([0, 0, 0, 0], outline = "", fill = owner_to_dark_color[self.uid]), canvas.create_text(0, 0, fill = "black", anchor = "e"), canvas.create_text(0, 0, fill = owner_to_dark_color[self.uid], anchor = "e", text = "1st"), canvas.create_polygon([0, 0, 0, 0], outline = "black", fill = DEVCARDFILL, smooth = True), canvas.create_text(0, 0, fill = "black", anchor = "center", text = "")]
        
        def change_score(self, ds):
            self.score += ds
            if self.score + self.dev_cards.count("Victory Point") >= 10:
                self.board.check_over()
        
        def settlement_built(self, vertex):
            self.settlements.append(vertex)
            for space in vertex.get_locs():
                if not self.board.get_hex(space).is_harbor() or vertex not in self.board.get_hex(space).get_harbored():
                    continue
                if self.board.get_hex(space).get_prod() == 7:
                    self.harbor_deals = [min((item, 3)) for item in self.harbor_deals]
                elif self.board.get_hex(space).get_prod() > 7 and self.board.get_hex(space).get_prod() <= 12:
                    self.harbor_deals[self.board.get_hex(space).get_prod()-8] = 2
            self.change_score(1)
            self.draw_panel(self.x, self.y)
        
        def city_built(self, vertex):
            self.settlements.remove(vertex)
            self.cities.append(vertex)
            self.change_score(1)
            self.draw_panel(self.x, self.y)
        
        def road_built(self, side):
            self.roads.append(side)
            self.check_LR()
            self.draw_panel(self.x, self.y)
        
        def rolled(self):
            self.unplayable_dev_cards = []
        
        def get_dev_card(self, card):
            self.dev_cards.append(card)
            self.unplayable_dev_cards.append(card)
            self.dev_cards.sort()
            if card == "Victory Point":
                self.board.check_over()
            self.draw_panel(self.x, self.y)
        
        def lose_dev_card(self, card):
            self.dev_cards.remove(card)
            if card == "Soldier":
                self.army_size += 1
                self.check_LA()
            self.draw_panel(self.x, self.y)
        
        def check_LR(self):
            best = max([player.long_road_length for player in self.board.players])
            if len(self.roads) <= best:
                return
            self.long_road_length = max([self.get_road_len_from(road) for road in self.roads])
            if self.long_road_length > best and self.long_road_length > 4:
                for player in self.board.players:
                    player.lose_LR()
                    player.draw_panel(player.x, player.y)
                self.has_longest_road = True
                self.change_score(2)
    
        def check_LA(self):
            best = max([player.army_size for player in self.board.players if player is not self])
            if self.army_size > best and self.army_size > 2:
                for player in self.board.players:
                    player.lose_LA()
                    player.draw_panel(player.x, player.y)
                self.has_largest_army = True
                self.change_score(2)
        
        def get_road_len_from(self, start, outlaws = ()):
            legal_others = [item for item in self.roads if item not in outlaws]
            best = 1
            for vertex in start.get_vertices():
                if any([side in outlaws for side in vertex.get_sides()]): continue
                for side in vertex.get_sides():
                    if side != start and side in legal_others:
                        new = self.get_road_len_from(side, outlaws + (start,)) + 1
                        if new > best:
                            best = new
                            if new == len(self.roads):
                                return new
            return best
        
        def lose_LR(self):
            if self.has_longest_road:
                self.has_longest_road = False
                self.change_score(-2)
    
        def lose_LA(self):
            if self.has_largest_army:
                self.has_largest_army = False
                self.change_score(-2)
        
        def get_card(self, card):
            self.cards.append(card)
            self.cards.sort()
            self.draw_panel(self.x, self.y)
        
        def lose_card(self, lost):
            try:
                self.cards.remove(lost)
            except ValueError:
                raise ValueError("Player %d, with cards %s, couldn't lose card %d" % (self.uid, self.cards, lost))
            self.selected_idxs = []
            self.draw_panel(self.x, self.y)
        
        def draw_panel(self, x, y):
            self.x = x
            self.y = y
            canvas.itemconfig(self.player_panel[0], state = NORMAL, outline = "black" if self.uid == self.board.active_player_num else "", width = HEXSIZE/48)
            canvas.coords(self.player_panel[0], rounded_rect_coords(x-HEXSIZE, y-3*HEXSIZE/4, x+HEXSIZE, y+3*HEXSIZE/4, HEXSIZE/2))
            canvas.coords(self.player_panel[1], rounded_rect_coords(x-HEXSIZE/8*7, y-5*HEXSIZE/8, x-HEXSIZE/8*4.5, y-HEXSIZE/8*1.5, HEXSIZE/12))
            canvas.itemconfig(self.player_panel[2], font = ("Helvetica", int(HEXSIZE/6)), text = str(len(self.cards)))
            canvas.coords(self.player_panel[2], (x-HEXSIZE/8*5.75, y-3.25*HEXSIZE/8))
            canvas.itemconfig(self.player_panel[3], font = ("Helvetica", int(HEXSIZE/4)), text = str(self.score) + "/10")
            canvas.coords(self.player_panel[3], (x-HEXSIZE/2, y-HEXSIZE/2))
            canvas.itemconfig(self.player_panel[4], font = ("Helvetica", int(HEXSIZE/8)), text = self.board.bots[self.uid-1].get_name())
            canvas.coords(self.player_panel[4], (x+HEXSIZE/8*7, y+HEXSIZE/8*5))
            canvas.itemconfigure(self.player_panel[5], width = HEXSIZE/36)
            canvas.coords(self.player_panel[5], (x-HEXSIZE/8*7+HEXSIZE*SIDESCALE/12, y-HEXSIZE*SIDESCALE/SQRT3/4, x-HEXSIZE/8*7-HEXSIZE*SIDESCALE/12, y+HEXSIZE*SIDESCALE/SQRT3/4))
            canvas.itemconfigure(self.player_panel[6], font = ("Helvetica", int(HEXSIZE/8)), text = str(len(self.roads)) + "/15")
            canvas.coords(self.player_panel[6], (x-HEXSIZE/4*3, y))
            canvas.coords(self.player_panel[7], [item/2 for item in settlement_coords(2*x-HEXSIZE*1.75, 2*y+HEXSIZE/4*1.75)])
            canvas.itemconfigure(self.player_panel[8], font = ("Helvetica", int(HEXSIZE/8)), text = str(len(self.settlements)) + "/5")
            canvas.coords(self.player_panel[8], (x-HEXSIZE/4*3, y+HEXSIZE/8*1.65))
            canvas.coords(self.player_panel[9], [item/2 for item in city_coords(2*x-HEXSIZE*1.85, 2*y+HEXSIZE/2*1.65)])
            canvas.itemconfigure(self.player_panel[10], font = ("Helvetica", int(HEXSIZE/8)), text = str(len(self.cities)) + "/4")
            canvas.coords(self.player_panel[10], (x-HEXSIZE/4*3, y+HEXSIZE/4*1.65))
            if self.has_longest_road:
                canvas.itemconfigure(self.player_panel[11], font = ("Helvetica", int(HEXSIZE/8)), state = NORMAL)
                canvas.coords(self.player_panel[11], (x-HEXSIZE/8, y))
            else:
                canvas.itemconfig(self.player_panel[11], state = HIDDEN)
            canvas.coords(self.player_panel[12], [item/2.5 for item in sword_coords(x*2.5-HEXSIZE, y*2.5+HEXSIZE)])
            canvas.coords(self.player_panel[13], x-HEXSIZE/16*3, y+HEXSIZE/2.5)
            canvas.itemconfig(self.player_panel[13], font = ("Helvetica", int(HEXSIZE/8)), text = str(self.army_size))
            if self.has_largest_army:
                canvas.itemconfigure(self.player_panel[14], font = ("Helvetica", int(HEXSIZE/8)), state = NORMAL)
                canvas.coords(self.player_panel[14], (x+HEXSIZE/8, y+HEXSIZE/2.5))
            else:
                canvas.itemconfig(self.player_panel[14], state = HIDDEN)
            canvas.coords(self.player_panel[15], [item/3 for item in card_coords(x*3+HEXSIZE*3/4*3, y*3-HEXSIZE*1.5)])
            canvas.itemconfig(self.player_panel[16], font = ("Helvetica", int(HEXSIZE/8)), text = str(len(self.dev_cards)))
            canvas.coords(self.player_panel[16], (x+HEXSIZE/4*3, y-HEXSIZE/2))
            if self.should_draw:
                self.draw_cards()
                self.draw_dev_cards()
        
        def draw_cards(self):
            while len(self.card_depictions) < len(self.cards):
                self.card_depictions.append(canvas.create_polygon((0, 0, 0, 0), outline = "black", smooth = True))
            if len(self.card_depictions) > len(self.cards):
                for idx in range(len(self.cards), len(self.card_depictions)):
                    canvas.itemconfigure(self.card_depictions[idx], state = HIDDEN)
            if len(self.cards) == 0:
                return
            card_x_prime = min(HEXSIZE/2*CARDSIZE, abs((CARDTOPCORNERS[1][0] - CARDTOPCORNERS[0][0]-HEXSIZE/16*5*CARDSIZE)/len(self.cards)))
            card_y = (CARDTOPCORNERS[1][1] + CARDTOPCORNERS[0][1])/2
            card_xs = [CARDTOPCORNERS[0][0] + i * card_x_prime for i in range(len(self.cards))]
            for idx in range(len(self.cards)):
                shrunk_coords = card_coords(card_xs[idx]/CARDSIZE, card_y/CARDSIZE - int(idx in self.selected_idxs)*HEXSIZE/CARDSIZE/2)
                coords = [item*CARDSIZE for item in shrunk_coords]
                canvas.itemconfigure(self.card_depictions[idx], width = HEXSIZE/32*CARDSIZE, fill = prod_to_color[self.cards[idx]], state = NORMAL)
                canvas.coords(self.card_depictions[idx], coords)
                canvas.tag_raise(self.card_depictions[idx])
        
        def draw_dev_cards(self): # TODO
            while len(self.dev_card_depictions) < len(self.dev_cards):
                self.dev_card_depictions.append((canvas.create_polygon((0, 0, 0, 0), outline = "black", smooth = True, fill = DEVCARDFILL), canvas.create_text(0, 0, fill = "black", angle = 90)))
            if len(self.dev_card_depictions) > len(self.dev_cards):
                for idx in range(len(self.dev_cards), len(self.dev_card_depictions)):
                    for item in self.dev_card_depictions[idx]:
                        canvas.itemconfigure(item, state = HIDDEN)
            if len(self.dev_cards) == 0:
                return
            card_x = DEVCARDLEFTCORNERS[0][0]
            card_y_prime = min(HEXSIZE/2*DEVCARDSIZE, abs((DEVCARDLEFTCORNERS[1][1] - DEVCARDLEFTCORNERS[0][1]-HEXSIZE/16*5*DEVCARDSIZE)/len(self.dev_cards)))
            card_ys = [DEVCARDLEFTCORNERS[0][1] + i * card_y_prime for i in range(len(self.dev_cards))]
            for idx in range(len(self.dev_cards)):
                shrunk_coords = card_coords(card_ys[idx]/DEVCARDSIZE, card_x/DEVCARDSIZE)
                coords = []
                for pair in range(0, len(shrunk_coords), 2):
                    coords.append(shrunk_coords[pair+1]*DEVCARDSIZE - HEXSIZE*DEVCARDSIZE/2*int(idx == self.selected_dev_idx))
                    coords.append(shrunk_coords[pair]*DEVCARDSIZE)
                canvas.itemconfigure(self.dev_card_depictions[idx][0], width = HEXSIZE/32*DEVCARDSIZE, state = NORMAL)
                canvas.coords(self.dev_card_depictions[idx][0], coords)
                canvas.tag_raise(self.dev_card_depictions[idx][0])
                canvas.itemconfigure(self.dev_card_depictions[idx][1], state = NORMAL, text = self.dev_cards[idx], font = ("Helvetica", int(HEXSIZE*DEVCARDSIZE/16)))
                canvas.coords(self.dev_card_depictions[idx][1], (card_x - HEXSIZE/8*3*DEVCARDSIZE - HEXSIZE*DEVCARDSIZE/2*int(idx == self.selected_dev_idx), card_ys[idx]))
                canvas.tag_raise(self.dev_card_depictions[idx][1])
    
    class Hex:
        """
        A Hexagon for a Settlers board
        """
        
        def __init__(self, loc, board, num, prod, neighbors = None):
            self.num = num
            self.prod = prod
            self.loc = loc
            self.board = board
            if neighbors == None:
                self.sixneighbors = board.get_neighbors(loc)
            else:
                self.sixneighbors = neighbors
            self.vertices = []
            for item in board.get_vertices(loc, self):
                if item not in self.vertices: self.vertices.append(item)
            self.depiction = None
            self.circled = None
            self.numd = None
            self.harboring = None
            
        def get_loc(self):
            return self.loc
        
        def get_board(self):
            return self.board
        
        def get_prod(self):
            return self.prod
        
        def get_num(self):
            return self.num
        
        def get_neighbors(self):
            return self.sixneighbors
        
        def get_vertices(self):
            return self.vertices
        
        def add_neighbors(self, allneighbors):
            self.sixneighbors = allneighbors
        
        def change_number(self, new_number):
            ans = self.num
            self.num = new_number
            return ans
        
        def is_harbor(self):
            return self.prod > 6 and self.prod < 13
        
        def determine_harboring(self):
            max_dist = 0
            for change in self.board.get_adjacent((0, 0, 0)):
                curr_dist = 0
                start_loc = tuple([self.loc[idx]+change[idx] for idx in range(3)])
                curr_loc = tuple([self.loc[idx]+change[idx] for idx in range(3)])
                while curr_loc in self.board.hexes and self.board.hexes[curr_loc].get_prod() < 7 and (self.board.hexes[curr_loc].get_prod() > 0 or self.board.hexes[curr_loc].get_prod() == -1):
                    curr_dist += 1
                    curr_loc = tuple([curr_loc[idx]+change[idx] for idx in range(3)])
                if curr_dist > max_dist:
                    max_dist = curr_dist
                    self.harboring = self.board.get_hex(start_loc)
        
        def get_harbored(self):
            if not self.is_harbor(): return None
            if self.harboring == None: self.determine_harboring()
            return [vertex for vertex in self.vertices if vertex in self.harboring.vertices]
        
        def add_vertex(self, new):
            self.vertices.append(new)
        
        def draw(self, x, y):
            if self.depiction != None:
                canvas.coords(self.depiction, [x-HEXSIZE/2, y, x-HEXSIZE/4, y+HEXSIZE*SQRT3/4, x+HEXSIZE/4, y+HEXSIZE*SQRT3/4, x+HEXSIZE/2, y, x+HEXSIZE/4, y-HEXSIZE*SQRT3/4, x-HEXSIZE/4, y-HEXSIZE*SQRT3/4])
            else:
                fill = prod_to_color[self.prod]
                if self.is_harbor(): fill = prod_to_color[0]
                self.depiction = canvas.create_polygon([x-HEXSIZE/2, y, x-HEXSIZE/4, y+HEXSIZE*SQRT3/4, x+HEXSIZE/4, y+HEXSIZE*SQRT3/4, x+HEXSIZE/2, y, x+HEXSIZE/4, y-HEXSIZE*SQRT3/4, x-HEXSIZE/4, y-HEXSIZE*SQRT3/4], fill = fill, width = HEXSIZE/10, outline = "")
            if self.prod > 0 and self.prod < 7:
                if self.circled != None:
                    canvas.coords(self.circled, x - HEXSIZE / 8, y - HEXSIZE / 8, x + HEXSIZE / 8, y + HEXSIZE / 8)
                else:
                    self.circled = canvas.create_oval(x - HEXSIZE / 8, y - HEXSIZE / 8, x + HEXSIZE / 8, y + HEXSIZE / 8, fill = "#FFFFBB", outline = "black", width = 0)
                if self.numd != None:
                    canvas.coords(self.numd, x, y)
                    numfill = "#000000"
                    if self.num == 6 or self.num == 8:
                        numfill = "#FF2222"
                    canvas.itemconfig(self.numd, fill = numfill, text = self.num, font = ("Helvetica", int(HEXSIZE / 8)), anchor = "center")
                else:
                    numfill = "#000000"
                    if self.num == 6 or self.num == 8:
                        numfill = "#FF2222"
                    self.numd = canvas.create_text(x, y, fill = numfill, text = self.num, font = ("Helvetica", int(HEXSIZE / 8)), anchor = "center")
            elif self.is_harbor():
                if self.numd == None: self.numd = canvas.create_line(0, 0, 0, 0, fill = "white", dash = (2, 1))
                canvas.itemconfig(self.numd, width = int(HEXSIZE/32))
                canvas.coords(self.numd, harbor_line_coords(self.loc, self.get_harbored()[0], self.get_harbored()[1], self.board))
                if self.circled != None:
                    canvas.coords(self.circled, x - HEXSIZE / 8, y - HEXSIZE / 8, x + HEXSIZE / 8, y + HEXSIZE / 8)
                    canvas.itemconfig(self.circled, width = int(HEXSIZE/32))
                else:
                    self.circled = canvas.create_oval(x - HEXSIZE / 8, y - HEXSIZE / 8, x + HEXSIZE / 8, y + HEXSIZE / 8, fill = prod_to_color[self.prod], outline = "black", width = int(HEXSIZE/32))
    
    class Vertex:
        
        def __init__(self, locs, board):
            self.locs = locs
            self.hexes = None
            self.board = board
            self.owner = -1
            self.level = 0
            self.depiction = canvas.create_polygon((0, 0, 0, 0), state = HIDDEN, outline = "")
            self.is_highlighted = False
            self.highlight = canvas.create_oval(0, 0, 0, 0, fill = "white", width = 0, state = tk.HIDDEN)
            self.x = 0
            self.y = 0
            self.sides = []
            self.draw()
        
        def create_sides(self):
            self.sides = self.board.get_sides(self.locs)
        
        def init_hexes(self, pass_free, actual_thing):
            if self.hexes != None: return
            self.hexes = frozenset([self.board.get_hex(loc) if loc in self.board.get_hexes().keys() else actual_thing for loc in self.locs])
            for space in self.hexes:
                if self not in space.vertices:
                    space.vertices.append(self)
        
        def get_locs(self):
            return self.locs
        
        def get_hexes(self): return self.hexes
        
        def get_sides(self):
            return self.sides
        
        def built(self, owner):
            if self.level > 1: raise Exception("Cities are the max level")
            self.owner = owner
            if self.level == 1:
                self.board.players[owner-1].city_built(self)
            else:
                self.board.players[owner-1].settlement_built(self)
            self.level += 1
            self.draw()
        
        def do_highlight(self): self.is_highlighted = True
        def do_unhighlight(self): self.is_highlighted = False
        
        def draw(self, x = None, y = None):
            if x != None: self.x = x
            if y != None: self.y = y
            if self.is_highlighted:
                canvas.tag_raise(self.highlight)
                canvas.itemconfig(self.highlight, state = tk.NORMAL)
                canvas.coords(self.highlight, self.x-HEXSIZE/12, self.y-HEXSIZE/12, self.x+HEXSIZE/12, self.y+HEXSIZE/12)
            else:
                canvas.itemconfig(self.highlight, state = tk.HIDDEN)
            if self.level > 0:
                canvas.itemconfig(self.depiction, state = NORMAL, fill = owner_to_color[self.owner])
                canvas.tag_raise(self.depiction)
                if self.level > 1:
                    canvas.coords(self.depiction, city_coords(self.x, self.y))
                else:
                    canvas.coords(self.depiction, settlement_coords(self.x, self.y))
            
    
    class Side:
        
        def __init__(self, vertices, locs, board):
            self.vertices = vertices
            self.locs = locs
            self.hexes = frozenset([board.get_hex(loc) for loc in locs if loc in board.get_hexes().keys()])
            self.board = board
            self.owner = -1
            self.is_highlighted = False
            self.depiction = canvas.create_line(0, 0, 0, 0, state = HIDDEN)
        
        def built(self, owner):
            if self.owner != -1: raise Exception("This is already an owned road")
            self.board.players[owner-1].road_built(self)
            self.owner = owner
        
        def get_locs(self):
            return self.locs
        
        def get_vertices(self):
            return self.vertices
    
        def do_highlight(self): self.is_highlighted = True
        def do_unhighlight(self): self.is_highlighted = False
        
        def draw(self, x1, y1, x2, y2):
            canvas.tag_raise(self.depiction)
            canvas.coords(self.depiction, (x1, y1, x2, y2))
            if self.owner == -1 and not self.is_highlighted:
                canvas.itemconfig(self.depiction, state = HIDDEN)
                return
            canvas.itemconfig(self.depiction, state = NORMAL, fill = owner_to_color[self.owner], width = HEXSIZE / 18)
    
    
    class Board:
        
        def __init__(self, bots, bal = 2, epsilon = 4, port_care = True, force_bal = True, dup_care = True):
            self.gameover = False
            self.vertices = {}
            self.sides = {}
            self.num_players = len(bots)
            self.robber_loc = None
            self.state_text = canvas.create_text(0, 0, state = HIDDEN, anchor = "se")
            self.robber_depiction = (canvas.create_oval((0, 0, 0, 0), fill = "black"), canvas.create_oval((0, 0, 0, 0), fill = "Black"), canvas.create_rectangle((0, 0, 0, 0), fill = "black"))
            self.dice_deps = [[canvas.create_oval(0, 0, 0, 0, fill = "black", outline = "") for dummy_i in range(6)] for dummy_j in range(2)]
            for item in self.dice_deps: item.append(canvas.create_rectangle(0, 0, 0, 0, fill = "#DDBBAA", outline = ""))
            self.init_dev_cards()
            self.init_hexes(bal = bal, epsilon = epsilon, port_care = port_care, force_bal = force_bal, dup_care = dup_care)
            self.players = [Player(self, idx+1, idx == 0) for idx in range(len(bots))]
            self.bots = [bots[i](board = self, people = self.players, me = self.players[i]) for i in range(len(bots))]
            self.active_player_num = random.randrange(0, len(bots))+1
            self.state = 4
            self.background_state = 0
            self.last_state = 0
            self.button_bindings = {}
            self.first_player = self.active_player_num
            self.devs_used = []
            self.offered_trade = ()
            self.trades_left = TRADELIMIT
            self.will_trade = [None for dummy in range(self.num_players)]
            self.bots[self.active_player_num-1].receive_prompt(4, tuple(self.vertices.values()))
            self.draw()
        
        def init_dev_cards(self):
            self.dev_deck = []
            for item in DEVCARDDISTRIBUTION:
                for dummy in range(DEVCARDDISTRIBUTION[item]):
                    self.dev_deck.append(item)
            random.shuffle(self.dev_deck)
        
        def init_hexes(self, true_rand = False, bal = 2, port_care = True, force_bal = True, epsilon = 4, dup_care = True):
            types_to_use = [-1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5]
            nums_to_use = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
            avg = sum([roll_odds[item] for item in nums_to_use])/len(nums_to_use)
            locs_to_use = [(0, 0, 0), (1, 0, -1), (-1, 0, 1), (1, -1, 0), (-1, 1, 0), (0, 1, -1), (0, -1, 1), (2, 0, -2), (-2, 0, 2), (2, -2, 0), (-2, 2, 0), (0, 2, -2), (0, -2, 2), (1, 1, -2), (-1, -1, 2), (1, -2, 1), (-1, 2, -1), (-2, 1, 1), (2, -1, -1)]
            water_locs = [(3, 0, -3), (-3, 1, 2), (3, -2, -1), (-3, 3, 0), (2, -3, 1), (-1, 3, -2), (0, -3, 3), (1, 2, -3), (-2, -1, 3)]
            port_locs = [(3, -1, -2), (-3, 0, 3), (3, -3, 0), (-3, 2, 1), (1, -3, 2), (-2, 3, -1), (-1, -2, 3), (0, 3, -3), (2, 1, -3)]
            port_types = [7, 7, 7, 7, 8, 9, 10, 11, 12]
            random.shuffle(types_to_use)
            random.shuffle(nums_to_use)
            random.shuffle(locs_to_use)
            self.hexes = {}
            while len(locs_to_use) > 0:
                now_using = [locs_to_use.pop(), types_to_use.pop()]
                if not true_rand:
                    while now_using[1] in [item.get_prod() for item in self.get_neighbors(now_using[0])]:
                        types_to_use.append(now_using[1])
                        random.shuffle(types_to_use)
                        if len(set(types_to_use) - set([item.get_prod() for item in self.get_neighbors(now_using[0])])) > 0:
                            now_using[1] = types_to_use.pop()
                        else:
                            return self.init_hexes(true_rand, bal, port_care, force_bal, epsilon, dup_care)
                if now_using[1] > 0 and now_using[1] < 6:
                    now_using.append(nums_to_use.pop())
                    if force_bal and 6 in [item.get_num() for item in self.get_neighbors(now_using[0])] or 6 in [item.get_num() for item in self.hexes.values() if item.get_prod() == now_using[1]] or 8 in [item.get_num() for item in self.get_neighbors(now_using[0])] or 8 in [item.get_num() for item in self.hexes.values() if item.get_prod() == now_using[1]]:
                        if dup_care:
                            while (now_using[2] == 6 or now_using[2] == 8) or now_using[2] in [item.get_num() for item in self.get_neighbors(now_using[0])]:
                                nums_to_use.append(now_using[2])
                                random.shuffle(nums_to_use)
                                if len(set(nums_to_use) - set((6, 8)) - set([item.get_num() for item in self.get_neighbors(now_using[0])])) > 0:
                                    now_using[2] = nums_to_use.pop()
                                else:
                                    return self.init_hexes(true_rand, bal, port_care, force_bal, epsilon, dup_care)
                        else:
                            while (now_using[2] == 6 or now_using[2] == 8):
                                nums_to_use.append(now_using[2])
                                random.shuffle(nums_to_use)
                                if len(set(nums_to_use) - set((6, 8))) > 0:
                                    now_using[2] = nums_to_use.pop()
                                else:
                                    return self.init_hexes(true_rand, bal, port_care, force_bal, epsilon, dup_care)
                    elif dup_care:
                        while now_using[2] in [item.get_num() for item in self.get_neighbors(now_using[0])]:
                            nums_to_use.append(now_using[2])
                            random.shuffle(nums_to_use)
                            if len(set(nums_to_use) - set([item.get_num() for item in self.get_neighbors(now_using[0])])) > 0:
                                now_using[2] = nums_to_use.pop()
                            else:
                                return self.init_hexes(true_rand, bal, port_care, force_bal, epsilon, dup_care)
                    self.hexes[now_using[0]] = Hex(now_using[0], self, now_using[2], now_using[1])
                else:
                    self.hexes[now_using[0]] = Hex(now_using[0], self, -1, now_using[1])
            imbalances = [0, 0, 0, 0, 0]
            for space in self.hexes.values():
                if space.get_prod() > 0 and space.get_prod() < 6:
                    imbalances[space.get_prod()-1] += avg - roll_odds[space.get_num()]
            imbalance = sum([item*item for item in imbalances])
            if abs(imbalance-bal) > epsilon:
                return self.init_hexes(true_rand, bal, port_care, force_bal, epsilon, dup_care)
            for loc in water_locs:
                self.hexes[loc] = Hex(loc, self, -1, 0)
            self.build_ports(port_locs, port_types, port_care)
            self.fix_broken_hexes() # !!!
            self.robber_loc = [item.get_loc() for item in self.hexes.values() if item.get_prod() == -1][0]
        
        def fix_broken_hexes(self): # !!!
            for space in self.hexes.values():
                if len(space.vertices) < 6 and space.prod > 0 and space.prod < 6:
                    for vert in self.vertices.values():
                        if space.loc in vert.locs and vert not in space.vertices:
                            space.vertices.append(vert)
        
        def build_ports(self, port_locs, port_types, land_match = True, port_match = True):
            to_add = {}
            start_types = [item for item in port_types]
            for loc in port_locs:
                bads = set()
                if port_match:
                    double_adjs = set()
                    for adj in self.get_adjacent(loc):
                        double_adjs.update(set(self.get_adjacent(adj)))
                    for item in double_adjs:
                        if item in to_add:
                            bads.add(to_add[item])
                    if len(set(port_types) - bads) < 1:
                        self.build_ports(port_locs, start_types, land_match, port_match)
                        return
                if land_match:
                    for item in self.get_adjacent(loc):
                        if item in self.hexes and self.hexes[item].prod > 0 and self.hexes[item].prod < 6:
                            bads.add(self.get_hex(item).prod+7)
                    if len(set(port_types) - bads) < 1:
                        self.build_ports(port_locs, start_types, land_match, port_match)
                        return
                port = random.choice(list(set(port_types) - set(bads)))
                port_types.remove(port)
                to_add[loc] = port
            for info in to_add:
                self.hexes[info] = Hex(info, self, -1, to_add[info])
        
        def receive_response(self, info, uid):
            if self.active_player_num != uid and self.state != 1 and self.state != 7:
                return
            if self.gameover:
                return
            for vertex in self.vertices.values():
                vertex.do_unhighlight()
            for side in self.sides.values():
                side.do_unhighlight()
            if (self.state == 0 or self.state == 3) and isinstance(info, str) and info in DEVCARDDISTRIBUTION.keys() and self.players[uid-1].dev_cards.count(info) > self.players[uid-1].unplayable_dev_cards.count(info):
                self.players[uid-1].lose_dev_card(info)
                if info == "Soldier":
                    self.background_state = 6
                    self.last_state = self.state
                    self.state = 2
                    self.bots[self.active_player_num-1].receive_prompt(2, None)
                    return
                elif info == "Monopoly":
                    self.background_state = 6
                    self.last_state = self.state
                    self.state = 12
                    self.bots[self.active_player_num-1].receive_prompt(12, True)
                    return
                elif info == "Road Building":
                    if len(self.players[uid-1].roads) == 15:
                        self.bots[self.active_player_num-1].receive_prompt(self.state, None)
                        return
                    elif len(self.players[uid-1].roads) == 14:
                        self.background_state = 5
                    else:
                        self.background_state = 4
                    self.last_state = self.state
                    self.state = 6
                    choices = set()
                    for road in self.players[self.active_player_num-1].roads:
                        for vert in road.vertices:
                            for option in vert.sides:
                                if option.owner == -1:
                                    choices.add(option)
                    self.bots[self.active_player_num-1].receive_prompt(6, tuple(choices))
                    return
                elif info == "Year of Plenty":
                    self.background_state = 4
                    self.last_state = self.state
                    self.state = 12
                    self.bots[self.active_player_num-1].receive_prompt(12, False)
                    return
                pass # TODO
            if self.state == 0:
                self.trades_left -= 1
                if info == None or (self.trades_left < 1 and not isinstance(self.bots[uid-1], HumanPlayer)) or len(info[0]) < 1 or len(info[1]) < 1 or len(set(info[0]).intersection(set(info[1]))) > 0:
                    self.state = 3
                    self.trades_left = TRADELIMIT
                    self.bots[self.active_player_num-1].receive_prompt(3, None)
                    return
                else:
                    for idx in range(1, 6):
                        if self.players[uid-1].cards.count(idx) < info[0].count(idx) or len(info[0]) == 0 or len(info[1]) == 0:
                            self.state = 3
                            self.bots[self.active_player_num-1].receive_prompt(3, None)
                            return
                    harbor_buys = 0
                    cards_outstanding = [0, 0, 0, 0, 0]
                    for give in info[0]:
                        cards_outstanding[give-1] += 1
                        if cards_outstanding[give-1] >= self.players[uid-1].harbor_deals[give-1]:
                            cards_outstanding[give-1] = 0
                            harbor_buys += 1
                    if harbor_buys >= len(info[1]):
                        for card in info[0]:
                            self.players[uid-1].lose_card(card)
                        for card in info[1]:
                            self.players[uid-1].get_card(card)
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                        return
                    self.will_trade = [None for dummy in range(self.num_players)]
                    self.offered_trade = info
                    self.state = 1
                    for bot in self.bots:
                        if bot != self.bots[self.active_player_num-1]:
                            bot.receive_prompt(1, (self.offered_trade[1], self.offered_trade[0], self.active_player_num))
                    return
            elif self.state == 1:
                if info is True or info is False:
                    self.will_trade[uid-1] = info
                    if all([self.will_trade[item_idx] is True or self.will_trade[item_idx] is False or item_idx == self.active_player_num-1 for item_idx in range(len(self.will_trade))]):
                        if all([item is False for item in self.will_trade]):
                            true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                            return
                        self.state = 10
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(10, [i+1 for i, x in enumerate(self.will_trade) if x is True]))
                        return
            elif self.state == 2:
                if info not in self.hexes.values() or info.get_loc() == self.robber_loc:
                    return
                else:
                    self.robber_loc = info.get_loc()
                    self.state = 0
                    enemies_to_steal = []
                    for vertex in self.hexes[self.robber_loc].get_vertices():
                        if vertex.owner > 0 and vertex.owner not in enemies_to_steal and len(self.players[vertex.owner-1].cards) > 0 and vertex.owner != uid:
                            enemies_to_steal.append(vertex.owner)
                    if len(enemies_to_steal) < 2:
                        if len(enemies_to_steal) == 1:
                            steal_player = self.players[enemies_to_steal[0]-1]
                            stolen = random.choice(steal_player.cards)
                            steal_player.lose_card(stolen)
                            self.players[self.active_player_num-1].get_card(stolen)
                        if self.background_state == 3:
                            self.background_state = 2
                            if not self.roll_dice():
                                true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                            return
                        if self.background_state == 6:
                            self.background_state = 2
                            self.state = self.last_state
                            true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(self.state, None))
                            return
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                    else:
                        self.state = 9
                        self.bots[self.active_player_num-1].receive_prompt(9, enemies_to_steal)
            elif self.state == 3:
                if info == 4:
                    if len(self.players[uid-1].settlements) < 5 and 1 in self.players[uid-1].cards and 2 in self.players[uid-1].cards and 3 in self.players[uid-1].cards and 4 in self.players[uid-1].cards:
                        legal_choices = set()
                        all_choices = set(self.get_legal_settlements())
                        for road in self.players[uid-1].roads:
                            for vertex in road.get_vertices():
                                legal_choices.add(vertex)
                        legal_choices = tuple(legal_choices.intersection(all_choices))
                        if len(legal_choices) > 0:
                            self.players[uid-1].lose_card(1)
                            self.players[uid-1].lose_card(2)
                            self.players[uid-1].lose_card(3)
                            self.players[uid-1].lose_card(4)
                            self.state = 4
                            self.bots[self.active_player_num-1].receive_prompt(4, legal_choices)
                            return
                elif info == 5: 
                    if len(self.players[uid-1].settlements) > 0 and len(self.players[uid-1].cities) < 4 and self.players[uid-1].cards.count(4) > 1 and self.players[uid-1].cards.count(5) > 2:
                        legal_choices = tuple(self.players[uid-1].settlements)
                        self.players[uid-1].lose_card(4)
                        self.players[uid-1].lose_card(4)
                        self.players[uid-1].lose_card(5)
                        self.players[uid-1].lose_card(5)
                        self.players[uid-1].lose_card(5)
                        self.state = 5
                        self.bots[self.active_player_num-1].receive_prompt(5, legal_choices)
                        return
                elif info == 6:
                    if len(self.players[uid-1].roads) < 15 and 1 in self.players[uid-1].cards and 2 in self.players[uid-1].cards:
                        legal_choices = []
                        for road in self.players[uid-1].roads:
                            for vertex in road.get_vertices():
                                if vertex.owner > 0 and vertex.owner != uid:
                                    continue
                                for new in vertex.get_sides():
                                    if new not in self.players[uid-1].roads and new not in legal_choices and new.owner <= 0:
                                        legal_choices.append(new)
                        if len(legal_choices) > 0:
                            self.players[uid-1].lose_card(1)
                            self.players[uid-1].lose_card(2)
                            self.state = 6
                            self.bots[self.active_player_num-1].receive_prompt(6, tuple(legal_choices))
                            return
                elif info == 8:
                    if 3 in self.players[uid-1].cards and 4 in self.players[uid-1].cards and 5 in self.players[uid-1].cards:
                        if len(self.dev_deck) < 1: self.init_dev_cards()
                        self.players[uid-1].lose_card(3)
                        self.players[uid-1].lose_card(4)
                        self.players[uid-1].lose_card(5)
                        self.players[uid-1].get_dev_card(self.dev_deck.pop())
                        self.bots[self.active_player_num-1].receive_prompt(3, None)
                        return
                self.active_player_num = self.active_player_num % self.num_players + 1
                self.devs_used = []
                self.state = 0
                true_root.update() # !!! De-lag
                if "Soldier" in self.players[self.active_player_num-1].dev_cards:
                    self.state = 11
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(11, None)) # TODO
                    return
                if not self.roll_dice(): # TODO pre-roll
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                else:
                    return
            elif self.state == 4 and isinstance(info, Vertex):
                info.built(uid)
                if self.background_state == 0 or self.background_state == 1:
                    if self.background_state == 1:
                        for loc in info.get_locs():
                            if self.hexes[loc].get_prod() > 0 and self.hexes[loc].get_prod() < 6:
                                self.players[uid-1].get_card(self.hexes[loc].get_prod())
                    self.state = 6
                    self.bots[self.active_player_num-1].receive_prompt(6, tuple(info.get_sides()))
                elif self.background_state == 2:
                    self.state = 3
                    self.bots[self.active_player_num-1].receive_prompt(3, None)
            elif self.state == 5 and isinstance(info, Vertex):
                info.built(uid)
                if self.background_state == 2:
                    self.state = 3
                    self.bots[self.active_player_num-1].receive_prompt(3, None)
            elif self.state == 6 and isinstance(info, Side):
                info.built(uid)
                if self.background_state == 0:
                    self.state = 4
                    if uid % self.num_players + 1 == self.first_player:
                        self.background_state = 1
                        self.bots[self.active_player_num-1].receive_prompt(4, self.get_legal_settlements())
                    else:
                        self.active_player_num = self.active_player_num % self.num_players + 1
                        self.bots[self.active_player_num-1].receive_prompt(4, self.get_legal_settlements())
                elif self.background_state == 1:
                    if uid == self.first_player:
                        self.state = 0
                        self.background_state = 2
                        if not self.roll_dice():
                            self.bots[self.active_player_num-1].receive_prompt(0, None)
                        return
                    self.state = 4
                    self.active_player_num = (self.active_player_num-2) % self.num_players + 1
                    self.bots[self.active_player_num-1].receive_prompt(4, self.get_legal_settlements())
                elif self.background_state == 2:
                    self.state = 3
                    self.bots[self.active_player_num-1].receive_prompt(3, None)
                elif self.background_state == 4:
                    self.background_state = 5
                    choices = set()
                    for road in self.players[self.active_player_num-1].roads:
                        for vert in road.vertices:
                            for option in vert.sides:
                                if option.owner == -1:
                                    choices.add(option)
                    self.bots[self.active_player_num-1].receive_prompt(6, tuple(choices))
                elif self.background_state == 5:
                    self.background_state = 2
                    self.state = self.last_state
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(self.state, None))
            elif self.state == 7:
                if len(info) != len(self.players[self.active_player_num-1].cards)//2:
                    return
                else:
                    for item in info:
                        self.players[self.active_player_num-1].lose_card(item)
                    self.active_player_num = self.active_player_num % self.num_players + 1
                    while self.active_player_num != self.first_player and len(self.players[self.active_player_num-1].cards) < 8:
                        self.active_player_num = self.active_player_num % self.num_players + 1
                    if self.active_player_num == self.first_player:
                        self.state = 2
                        self.bots[self.active_player_num-1].receive_prompt(2, None)
                    else:
                        self.bots[self.active_player_num-1].receive_prompt(7, tuple(self.players[self.active_player_num-1].cards))
            elif self.state == 9:
                for vertex in self.hexes[self.robber_loc].get_vertices():
                    if vertex.owner == info:
                        break
                else:
                    return
                steal_player = self.players[info-1]
                stolen = random.choice(steal_player.cards)
                steal_player.lose_card(stolen)
                self.players[self.active_player_num-1].get_card(stolen)
                self.state = 0
                if self.background_state == 3:
                    self.background_state = 2
                    if not self.roll_dice():
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                    return
                if self.background_state == 6:
                    self.background_state = 2
                    self.state = self.last_state
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(self.state, None))
                    return
                true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
            elif self.state == 10:
                if info == None:
                    self.state = 0
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                    return
                if self.will_trade[info-1]:
                    active = self.players[self.active_player_num-1]
                    other = self.players[info-1]
                    for item in self.offered_trade[0]:
                        active.lose_card(item)
                        other.get_card(item)
                    for item in self.offered_trade[1]:
                        other.lose_card(item)
                        active.get_card(item)
                    self.state = 0
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                    return
            elif self.state == 11:
                if info:
                    self.players[self.active_player_num-1].lose_dev_card("Soldier")
                    self.state = 2
                    self.background_state = 3
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(2, None))
                else:
                    self.state = 0
                    if not self.roll_dice():
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(0, None))
                    return
            elif self.state == 12:
                if self.background_state == 2:
                    return # !!!
                elif self.background_state == 6:
                    getter = self.players[uid-1]
                    for player in self.players:
                        if player is not getter:
                            while info in player.cards:
                                player.lose_card(info)
                                getter.get_card(info)
                    self.background_state = 2
                    self.state = self.last_state
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(self.state, None))
                    return
                elif self.background_state == 4:
                    self.players[uid-1].get_card(info)
                    self.background_state = 5
                    self.bots[self.active_player_num-1].receive_prompt(12, False)
                elif self.background_state == 5:
                    self.players[uid-1].get_card(info)
                    self.background_state = 2
                    self.state = self.last_state
                    true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(self.state, None))
                        
        def get_legal_settlements(self):
            ans = list(self.vertices.values())
            idx = 0
            while idx < len(ans):
                if any([any([vertex.level > 0 for vertex in side.get_vertices()]) for side in ans[idx].get_sides()]):
                    ans.pop(idx)
                else:
                    idx += 1
            return ans
        
        def check_over(self):
            for player in self.players:
                if player.score + player.dev_cards.count("Victory Point") >= 10:
                    self.gameover = True
                    self.end()
                    return
        
        def end(self):
            gameover([player.score + player.dev_cards.count("Victory Point") for player in self.players])
        
        def get_num_players(self):
            return self.num_players
        
        def get_robber_loc(self):
            return self.robber_loc
        
        def add_hex(self, space):
            self.hexes[space.get_loc()] = space
            space.add_neighbors(self.get_neighbors(space.get_loc()))
            for neighbor in self.get_neighbors(space.get_loc()):
                neighbor.add_neighbors(self.get_neighbors(neighbor.get_loc()))
            self.make_ghosts()
        
        def get_hexes(self):
            return self.hexes
        
        def get_hex(self, loc):
            return self.hexes[loc]
            
        def get_neighbors(self, loc):
            ans = []
            choices = [(loc[0]+1, loc[1], loc[2]-1), (loc[0]+1, loc[1]-1, loc[2]), (loc[0]-1, loc[1]+1, loc[2]), (loc[0], loc[1]+1, loc[2]-1), (loc[0]-1, loc[1], loc[2]+1), (loc[0], loc[1]-1, loc[2]+1)]
            for choice in choices:
                if choice in self.hexes.keys():
                    ans.append(self.hexes[choice])
            return ans
        
        def get_vertices(self, loc, thing):
            ans = []
            adjs = self.get_adjacent(loc)
            for space in adjs[:-1]:
                for other in adjs[adjs.index(space):]:
                    if other in self.get_adjacent(space):
                        if frozenset((loc, space, other)) in self.vertices.keys():
                            ans.append(self.vertices[frozenset((loc, space, other))])
                        elif space not in self.hexes.keys():
                            break
                        elif other not in self.hexes.keys():
                            pass
                        else:
                            new = Vertex(frozenset((loc, space, other)), self)
                            new.init_hexes(loc, thing)
                            ans.append(new)
                            self.vertices[frozenset((loc, space, other))] = new
                            new.create_sides()
            return ans
    
        def get_sides(self, loc_trio):
            ans = []
            loc_trio = list(loc_trio)
            pairs = [[x for i,x in enumerate(loc_trio) if i!=omit] for omit in range(len(loc_trio))]
            for pair in pairs:
                two_trios = [frozenset((item, pair[0], pair[1])) for item in self.get_adjacent(pair[0]) if item in self.get_adjacent(pair[1])]
                if frozenset(pair) in self.sides.keys():
                    ans.append(self.sides[frozenset(pair)])
                elif any([item not in self.vertices.keys() for item in two_trios]):
                    pass
                else:
                    new = Side([self.vertices[item] for item in two_trios], frozenset(pair), self)
                    ans.append(new)
                    self.vertices[next(item for item in two_trios if item != frozenset(loc_trio))].sides.append(new)
                    self.sides[frozenset(pair)] = new
            return ans
        
        def get_adjacent(self, loc):
            return [(loc[0]+1, loc[1], loc[2]-1), (loc[0]+1, loc[1]-1, loc[2]), (loc[0]-1, loc[1]+1, loc[2]), (loc[0], loc[1]+1, loc[2]-1), (loc[0]-1, loc[1], loc[2]+1), (loc[0], loc[1]-1, loc[2]+1)]
        
        def roll_dice(self):
            for player in self.players:
                player.rolled()
            self.dice = [random.randint(1, 6) for dummy_i in range(2)]
            dice_locs = [die_coords(HEXSIZE*DICESCALE*(i+0.5), HEXSIZE*DICESCALE*0.5, self.dice[i]) for i in range(len(self.dice))]
            for die in range(2):
                for pip in range(self.dice[die]):
                    canvas.itemconfigure(self.dice_deps[die][pip], state = NORMAL)
                    canvas.coords(self.dice_deps[die][pip], dice_locs[die][pip])
                for pip in range(self.dice[die], 6):
                    canvas.itemconfigure(self.dice_deps[die][pip], state = HIDDEN)
                canvas.coords(self.dice_deps[die][-1], dice_locs[die][-1])
                canvas.tag_lower(self.dice_deps[die][-1])
            for bot in self.bots:
                bot.log_roll(sum(self.dice))
            if sum(self.dice) == 7:
                for player in self.players:
                    if len(player.cards) > 7:
                        self.state = 7
                        self.first_player = self.active_player_num
                        self.active_player_num = player.uid
                        true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(7, tuple(player.cards)))
                        return True
                self.state = 2
                true_root.after(0, lambda: self.bots[self.active_player_num-1].receive_prompt(2, None))
                return True
            for space in self.hexes.values():
                if space.get_num() == sum(self.dice) and self.robber_loc != space.get_loc():
                    for vertex in space.get_vertices():
                        for i in range(vertex.level):
                            self.players[vertex.owner-1].get_card(space.get_prod())
            return False
        
        def draw(self):
            self.center = ((3.5+PLAYERSPACING)*HEXSIZE, 3.5*HEXSIZE)
            self.hex_locs = {}
            for space in self.hexes.keys():
                x = (-space[0]) * HEXSIZE * 1.5 / 2
                y = (space[1] + (space[0])/2) * HEXSIZE / 2 * SQRT3
                self.hex_locs[space] = (x+self.center[0], y+self.center[1])
            for space in self.hexes.keys():
                self.hexes[space].draw(self.hex_locs[space][0], self.hex_locs[space][1])
            for player_idx in range(len(self.players)):
                self.players[player_idx].draw_panel(PLAYERSPACING*HEXSIZE*2/3+HEXSIZE/10, PLAYERSPACING*HEXSIZE*(player_idx+(1/PLAYERSPACING*DICESCALE)+0.5))
            canvas.coords(self.state_text, self.center[0]-1.75*HEXSIZE, self.center[1]-2.25*HEXSIZE)
            self.background_draw()
        
        def background_draw(self):
            for vertex in self.vertices.values():
                choices = [self.hex_locs[item] for item in vertex.get_locs()]
                vertex.draw((choices[0][0]+choices[1][0]+choices[2][0])/3, (choices[0][1]+choices[1][1]+choices[2][1])/3)
            for side in self.sides.values():
                locs = list(side.get_locs())
                x0 = (self.hex_locs[locs[0]][0] + self.hex_locs[locs[1]][0])/2
                y0 = (self.hex_locs[locs[0]][1] + self.hex_locs[locs[1]][1])/2
                x1 = (self.hex_locs[locs[0]][1] - y0) * SIDESCALE + x0
                y1 = (-self.hex_locs[locs[0]][0] + x0) * SIDESCALE + y0
                side.draw(x1, y1, x0*2-x1, y0*2-y1)
            canvas.tag_raise(self.state_text)
            text_fill = "#000000"
            if self.state in IMPORTANTSTATES:
                text_fill = "#FF0000"
            canvas.coords(self.state_text, self.center[0]-(1.75-int(self.state in IMPORTANTSTATES))*HEXSIZE, self.center[1]-2.25*HEXSIZE)
            canvas.itemconfig(self.state_text, state = NORMAL, text = code_to_state_str[self.state], width = HEXSIZE*(1+int(self.state in IMPORTANTSTATES)), font = ("Helvetica", int(HEXSIZE/8*(1+int(self.state in IMPORTANTSTATES)/2))), fill = text_fill)
            canvas.tag_raise(self.state_text)
            robber_x_y = self.hex_locs[self.robber_loc]
            robber_nums = robber_coords(robber_x_y[0], robber_x_y[1])
            canvas.tag_raise(self.robber_depiction[0])
            canvas.tag_raise(self.robber_depiction[1])
            canvas.tag_raise(self.robber_depiction[2])
            canvas.coords(self.robber_depiction[0], robber_nums[0])
            canvas.coords(self.robber_depiction[1], robber_nums[1])
            canvas.coords(self.robber_depiction[2], robber_nums[2])

    bots = {"Long-term planner" : BetterBot2, "HumanPlayer" : HumanPlayer, "SmartTrader" : SmartTrader, "Dead Bot" : Bot, "Foolish Bot" : FoolBot, "Take my stuff!" : TakeMyStuff, "NOBODY" : None, "Trade a little" : TradeLittle}
    
    play = tk.Toplevel(true_root)
    play.title("Settlers of Catan")
    play.geometry(str(int(1822/144*HEXSIZE)) + "x" + str(int(1025/144*HEXSIZE)))
    play.columnconfigure(0, weight = 1)
    play.rowconfigure(0, weight = 1)
    
    canvas = tk.Canvas(play, width=1200, height=800, bg='white')
    canvas.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
    
    def end():
        true_root.destroy()
        raise SystemExit
    
    def background():
        if board is not None:
            board.background_draw()
        true_root.after(34, background)
    
    def gameover(scores):
        return
    
    true_root.update()
    def board_only_setup():
        global board
        bots_this_time = [bots[item] for item in bots_to_use]
        board = Board(bots_this_time, bal, epsilon, port_care, force_bal, dup_care)
    
    def setup():
        board_only_setup()
        background()
    
    play.protocol("WM_DELETE_WINDOW", end)
    
    true_root.after(0, setup)

true_root = tk.Tk()
def launch(HEXSIZE, TRADELIMIT, bots_to_use, true_root, bal, epsilon, dup_care, force_bal, port_care):
    use = [item for item in bots_to_use if item != "NOBODY"]
    true_root.withdraw()
    play(HEXSIZE, TRADELIMIT, use, true_root, bal, epsilon, dup_care, force_bal, port_care)
size_descriptor = tk.Label(true_root, text = "Screen Size (Maximum size recommended)")
size_descriptor.grid(row = 0, column = 0, columnspan = 2)
size_selector = tk.Scale(orient=tk.HORIZONTAL, length=300, width=20, sliderlength=10, from_=50, to=144, showvalue = 0, cursor = " hand2 ")
size_selector.grid(row = 1, column = 0, columnspan = 2)
trades_descriptor = tk.Label(true_root, text = "Max trades opponents offer (Too many is annoying)")
trades_descriptor.grid(row = 0, column = 3, columnspan = 2)
trades_selector = tk.Scale(orient=tk.HORIZONTAL, length=300, width=20, sliderlength=10, from_=5, to=20, showvalue = 0, cursor = " hand2 ")
trades_selector.grid(row = 1, column = 3, columnspan = 2)
trades_selector.set(5)
size_selector.set(144)
player_1_name = tk.StringVar()
player_1_name.set("HumanPlayer")
label1 = tk.Label(true_root, text = "Player 1")
label1.grid(row = 2, column = 0)
p1 = tk.OptionMenu(true_root, player_1_name, *["HumanPlayer", "Long-term planner", "SmartTrader", "Trade a little", "Dead Bot", "Foolish Bot", "Take my stuff!"])
p1.grid(row = 3, column = 0)
player_2_name = tk.StringVar()
player_2_name.set("Long-term planner")
label2 = tk.Label(true_root, text = "Player 2")
label2.grid(row = 2, column = 1)
p2 = tk.OptionMenu(true_root, player_2_name, *["Long-term planner", "SmartTrader", "Trade a little", "Dead Bot", "Foolish Bot", "Take my stuff!"])
p2.grid(row = 3, column = 1)
player_3_name = tk.StringVar()
player_3_name.set("Long-term planner")
label3 = tk.Label(true_root, text = "Player 3")
label3.grid(row = 2, column = 3)
p3 = tk.OptionMenu(true_root, player_3_name, *["Long-term planner", "SmartTrader", "Trade a little", "Dead Bot", "Foolish Bot", "Take my stuff!"])
p3.grid(row = 3, column = 3)
player_4_name = tk.StringVar()
player_4_name.set("NOBODY")
label4 = tk.Label(true_root, text = "Player 4")
label4.grid(row = 2, column = 4)
p4 = tk.OptionMenu(true_root, player_4_name, *["NOBODY", "Long-term planner", "SmartTrader", "Trade a little", "Dead Bot", "Foolish Bot", "Take my stuff!"])
p4.grid(row = 3, column = 4)
go = tk.Button(text = "Play", bg = "red", cursor = " hand2 ", font = ("Helvetica", 50), width = 4, height = 1, command = lambda : launch(size_selector.get(), trades_selector.get(), [player_1_name.get(), player_2_name.get(), player_3_name.get(), player_4_name.get()], true_root, balance_selector.get(), precision_selector.get(), True, True, True))
go.grid(row = 0, column = 2, rowspan = 4, sticky = tk.N + tk.E + tk.S + tk.W)
board_label = tk.Label(true_root, text = "Board generation settings:", font = ("Helvetica", 30))
board_label.grid(row = 4, column = 0, columnspan = 5)
balance_label = tk.Label(true_root, text = "Board Inequality")
balance_label.grid(row = 5, column = 0, columnspan = 2)
balance_selector = tk.Scale(orient=tk.HORIZONTAL, length=300, width=20, sliderlength=10, from_=0, to=20, showvalue = 0, cursor = " hand2 ")
balance_selector.grid(row = 6, column = 0, columnspan = 2)
balance_selector.set(2)
precision_label = tk.Label(true_root, text = "Balance Precision")
precision_label.grid(row = 5, column = 3, columnspan = 2)
precision_selector = tk.Scale(orient=tk.HORIZONTAL, length=300, width=20, sliderlength=10, from_=1, to=10, showvalue = 0, cursor = " hand2 ")
precision_selector.grid(row = 6, column = 3, columnspan = 2)
precision_selector.set(3)
true_root.mainloop()