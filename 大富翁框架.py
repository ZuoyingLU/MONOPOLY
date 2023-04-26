import tkinter as tk
import random

class Property:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0
        self.properties = []
        self.cash = 100000
    
    def __str__(self):
        return f"{self.name} ($(self.cash))"

    def move(self,step):
        self.position = (self.position + step) % 20
    
    def buy_property(self,property):
        self.properties.append(property)
        self.cash -= property.price

class Board:
    def __init__(self):
        self.map = []
        self.properties = [

        ]
    def get_property(self,round):
        indexget_property = round -1
        return self.properties[indexget_property]

class Game:
    def __init__(self,player_names):
        self.board = Board()
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.current_property = None
    
    def roll_dice(self):
        dice_value = random.randint(1,6)
        self.players[self.current_player_index].move(dice_value)
        self.check_property()
        tk.messagebox.showinfo("Result of dice",f"{self.players[self.current_player_index].name} throw {dice_value} point")
    
        if self.current_property: #通过check_property返回值
            property_owner = None

            for player in self.players: #找地块主人
                if self.current_property.name in player.properties:
                    property_owner = player
                    break

        if property_owner:
            if property_owner == self.players[slef.current_player_index]:
                tk.messagebox.showinfo("已经拥有","你已经拥有该地块！")
            else:
                rent = self.current_property.price // 2
                self.players[slef.current_player_index].cash -= rent
                property_owner += rent
                tk.messagebox.showinfo("付钱",f"{self.current_property.name} 属于 {property_owner.name}! 你需要支付 {rent} ")
        
        elif property_owner == False:
            response = tk.messagebox.askyesno("购买", f"你可以购买 {self.current_property.name}。价格为 ${self.current_property.price}。你是否购买？")

            if response:
                self.players[self.current_player_index].buy_property(self.current_property)

        self.next_player()

    #下级代码
    def check_property(self): #判断是否房区（地图包含随机事件）
        position = self.board.map[self.players[self.current_player_index].position]
        if isinstance(position,Property):
            self.current_property = position
        else:
            self.current_property = None
            
    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_winner(self): #进行排序（无胜利条件 需要添加胜利条件）
        sorted_players = sorted(self.players, key = lambda player : player.cash, reverse = True)

        if sorted_players[0].cash == sorted_players[1].cash:
            return None
        else:
            return sorted_players[0]

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.game = None
    
    def start(self):
        self.root.title("Monopoly")
        tk.Label(self.root, text='Welcome to Monopoly').pack()

        num_players = tk.StringVar()
        tk.Label(self.root, text = "Please enter the number of the game").pack()
        tk.Entry(self.root, textvariable = num_players).pack()

        player_names = []
        
        def add_player():
            name = tk.StringVar()
            tk.Label(self.root, text = f"Please putin names of the {len(player_names) + 1}'s name:").pack()
            tk.Entry(self.root, textvariable = name).pack()
            player_names.append(name)
            print(player_names)

        tk.Button(self.root, text = "Add Player", command = add_player).pack()

        def start_game():
            names = [name.get() for name in player_names]
            self.game = Game(names)
            self.play_game()

        tk.Button(self.root, text = "Begin the Game", command = start_game).pack()
        
        self.root.mainloop()

    def play_game(self):
        tk.Label(self.root, text = "Game Begin").pack()
        
        while not self.game.get_winner():
            tk.Label(self.root,text = f"当前玩家:{self.game.players[self.game.current_player_index].name}").pack()

            tk.Button(self.root, text = "Throw indice", command = self.game.roll_dice).pack()
            tk.Button(self.root, text = "Next Round", command= self.game.next_player).pack()

            self.root.mainloop()
    
            winner = self.game.get_winner
            tk.messagebox.showinfo("Game Over", f"{winner.name} win the game")


if __name__ == "__main__":
    app = Application()
    app.start()
