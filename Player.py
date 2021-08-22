import json
import sys
import os

class Player():
    '''
     3 attributes:
     id = discord id of player
     balance = monetary balance of player (float)
     holdings = assets/holdings of a player (dict)

     Every player gets their own csv file because I don't know how async will interface 
     with i/o and i don't want to have to spend hours debugging some
     race condition when 2 people try to read/write in the same millisecond
     then everyones data gets corrupted
     '''

    # load player data, generate new if none exists
    def __init__(self, id, balance=0.0, holdings={}):

        startbalance = 50000 # last 2 digits are pennies

        self.id = id  # integer: discord id

        # attempt to load balance/holdings from file, else generate new data
        try:
            with open(f"players/{id}.csv", "r") as player_file:
                data = player_file.read()
                data = data.split(",")

                if len(data) != 3:  # sanity check
                    print("Alert: data has too many parameters:", data)

                self.balance = int(data[1])
                self.holdings = json.loads(data[2])

        except FileNotFoundError:
            print("No previous data found for player", id)
            self.balance = startbalance
            self.holdings = {}

        except:
            print("Data could not be loaded, error:", sys.exc_info()[0])
            self.balance = startbalance
            self.holdings = {}

    # save data
    def save(self):
        with open(f"players/{self.id}.csv", "w") as player_file:
            player_file.write(
                f"{self.id},{self.balance},{json.dumps(self.holdings)}")


def player_exists(id):
    return os.path.isfile(f"players/{id}.csv")
