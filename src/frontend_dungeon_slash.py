from backend_dungeon_slash import * # Importing the backend module
import random 
from random import randint 
import time
import os 
import platform

start = None 
enemy = Enemy()
player = None

def main():
    print_intro() 
    loading()
    play()

def print_intro():
    global start
    global player
    print("Hello!")
    player = Player()
    print(f'''
         Welcome to the Dungeon Slash game {player.name}!
    In this game, you will navigate through a dungeon,
                    filled with monsters.
   
      [Enter Y to start or any key to exit the game.]
    ''')
    text_input = input(">: ")
    user_input = text_input[:10] #Taking the first 10 characters of input to prevent long inputs
    user_input = text_input.replace(" ", "") #Removing spaces from input to beautify
    del text_input #Deleting potentially sensitive input 
    clear_terminal()
    if user_input == 'Y' or user_input == 'y' and len(user_input) == 1:
        print("Starting the game...")
        del user_input
        start = True 
        time.sleep(2)
    else: 
        print("Exiting the game...")
        time.sleep(2)
        exit() 
    
def loading():
 if start == True:
      print('loading...')
      time.sleep(2)
      clear_terminal()
 else: 
     print("There was an error loading the game.")
     time.sleep(1.5)
     exit()

def play():
    enemy_turn = False 
    player_turn = True 
    global player
    global enemy
    enemy()
    while start == True: 
     if len(enemies) > 0:
        if player_turn == True and enemy_turn == False: 
            print("It is your turn!")
            time.sleep(1.5)
            player._choose_enemy()
            player_turn = False 
            enemy_turn = True 
        elif player_turn == False and enemy_turn == True: 
            print("It is the enemy's turn!")
            time.sleep(1.5)
            enemy._damage_player()
            time.sleep(1.5)
            player._check_player_health()
            time.sleep(1.5) 
            clear_terminal()
            enemy_turn = False
            player_turn = True
        else: 
            raise RuntimeError("There was an error in the player/enemy turn system.")
     else: 
          enemy()
          print(f"All enemies here are dead so you venture deeper!")
          time.sleep(2)
          clear_terminal()
          play()

def clear_terminal():
    # Check the operating system and clear the terminal accordingly
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux" or platform.system() == "Darwin": # For MacOS and Linux
        os.system("clear")
    else:
        print("\n" * 100) #For unindentified systems to get 100 new lines of code in terminal.
        

if __name__ == "__main__":
    main()