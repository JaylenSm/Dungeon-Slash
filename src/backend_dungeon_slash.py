from random import *
import random
import time
import threading

critical_hit = dict() #Creating a dictionary to store critical hit values for players and enemies
random_value = dict() #Creating a dictionary to store random values for players and enemies
enemies = list() #Creating a list to store enemy instances
player_health = list() #Creating a variable to store player health


class Player(): #Class utilized to create instances of players
    _player = None
    _experience = [0, 100]
    __slots__ = ['name', '__level', '__health',] #Limiting the local attributes of instances (Memory efficient/ Improves performance/ Input sanitization))
 #__slots__ tells Python to only allocate space for the attributes listed in the tuple, 
 # rather than creating a __dict__ for each instance. 
 # This can save memory and improve performance,
 #  especially when creating many instances of a class. 

    def __new__(cls, *args, **kwargs): #Creating a singleton instance of the Player class
        if not cls._player:
            cls._player = super().__new__(cls)
        return cls._player

    def __init__(self, name=' ', __level=abs(1), __health=abs(100)): #Setting the default level to 1 & utilizing the __level variable to make it "private"
        if not isinstance(name, str) or not isinstance(__level, int) or not isinstance(__health, int): #Sanitizing user inputs 
            raise TypeError('Name must be a string and level must be an integer and health must be an integer')
        self.name = name
        if name == str(' '):
            self.name = input('Enter your name: ') #Prompting user for input
        self.name = self.name[:10] #Limiting the name to 11 characters
        self.name = self.name.strip() #Removing trailing spaces from input to beautify
        if len(self.name) > 10:
            raise ValueError('Name cannot be longer than 11 characters')
        self.__level = __level
        self.__health = __health * __level
        player_health.extend([str(self.__health), str(self.__health)])
        if self.__health < 0: 
            raise ValueError('Health cannot be negative')

    def __repr__(self):
        return f'<Player: name={self.name}, __level={self.__level}, __health={self.__health}>' #Debugging purposes
    
    def __str__(self):
        return f'<{self.name}: Level {self.__level}: HP {player_health[0]}/{player_health[1]}: XP {self._experience[0]}/{self._experience[1]}>' #Output to user
    
    def _get_attack_power(self):
        random_value.update({self.name: int(randint(1, 10) * self.__level * 15)})
        if int(random_value[self.name]/self.__level/15) > int(self.__level/2):
            return random_value.pop(self.name)
        else:
            critical_hit.update({self.name:
                                 (random_value.pop(self.name)
                                  * 2 * self.__level)})
            print('Critical hit!')
            return critical_hit.pop(self.name)
        
    def _check_enemy_death(self): 
        for i, enemy in enumerate(enemies):
            if enemy[2] <= 0:
                print(f'You have defeated the {enemy[0]} enemy!')
                self._level_up()
                del enemies[i]
            else: 
                pass

    def _check_player_health(self):
        if len(player_health) > 0 and int(player_health[0]) > 0:
            print(f'You have been hit and your current health is {player_health[0]}/{player_health[1]}!')
            self.__health = int(player_health[0])
        elif len(player_health) > 0 and int(player_health[0]) < 0:
            print('You have died!')
            time.sleep(2)
            exit()

        elif int(player_health[0]) <= 0:
            print('You have died!')
            time.sleep(2)
            exit()
        else:
            pass
        
    def _choose_enemy(self):
        if len(enemies) > 0:
            print(f'You have {len(enemies)} enemies to choose from:')
            for i, enemy in enumerate(enemies):
               print(f'<Enemy[{i+1}]: {enemy[0]}>')
            stored_choice = input('''Press [Q] to quit the game
or press [S] to view your stats or 
Choose an enemy by entering the number: ''')
            choice = stored_choice[:10] #Limiting input to 10 characters and preventing input issues by storing input
            choice = stored_choice.strip() #Removing trailing spaces from input for QoL
            del stored_choice
            if int(choice.isdigit()) and 1 <= int(choice) <= len(enemies):
                chosen_enemy = enemies[int(choice) - 1]
                print(f'''You have chosen the {chosen_enemy[0]} enemy!
                      [F]ight, [S]tats, [I]nteract, [B]ack, [P]ass, [Q]uit''')
                user_input = input('Choose an action: ').lower()
                action = user_input[:10]
                action = user_input.strip() #Removing trailing spaces from input for QoL
                del user_input
                if action == 'f': #Fight option which calls _get_attack_power method
                    attack_power = self._get_attack_power()
                    chosen_enemy[2] -= attack_power
                    if chosen_enemy[2] > 0:
                        print(f'''You attacked the {chosen_enemy[0]} for {attack_power} damage! 
                              {chosen_enemy[0]} has {chosen_enemy[2]} hp left!''')
                        #self._choose_enemy() #testing purposes
                    else: 
                         self._check_enemy_death() 
                         #self._choose_enemy()
                elif action == 's': #Stats option which shows the stats of the chosen enemy 
                    print(f'Enemy: {chosen_enemy[0]} at level {chosen_enemy[1]} with {chosen_enemy[2]} hp!')
                    time.sleep(1.5)
                    self._choose_enemy()
                elif action == 'i': #Interact option which allows the player to interact with the enemy

                    def tempf(): #temporary attack function
                        attack_power = self._get_attack_power()
                        chosen_enemy[2] -= attack_power
                        if chosen_enemy[2] > 0:
                            print(f'''You attacked the {chosen_enemy[0]} for {attack_power} damage! 
                                {chosen_enemy[0]} has {chosen_enemy[2]} hp left!''')
                           # self._choose_enemy() #testing purposes
                        else:
                             self._check_enemy_death()
                            # self._choose_enemy() #Testing purposes
                        
                    def tempb(): #temporary back function
                        print('Going back to the enemy list...')
                        time.sleep(2)
                        self._choose_enemy()

                    if chosen_enemy[1] > self.__level: 
                        print(f'This {chosen_enemy[0]} enemy seems a little stronger than you!')
                        user_input = input('Do you want to [F]ight or [B]ack? ').lower()
                        user_input = user_input[:10] 
                        user_input = user_input.strip() 
                        if user_input == 'f':
                         tempf()
                         del user_input
                         del tempf
                         time.sleep(1.5)
                        elif user_input == 'b': 
                         tempb()
                         del user_input
                         del tempb
                        else: 
                            print('Invalid action. Please try again.')
                            time.sleep(2)
                            self._choose_enemy()
                    if chosen_enemy[1] == self.__level:
                        print(f'This {chosen_enemy[0]} enemy seems not be too out of your level')
                        user_input = input('Do you want to [F]ight or [B]ack? ').lower()
                        user_input = user_input[:10] 
                        user_input = user_input.strip() 
                        if user_input == 'f':
                            tempf()
                            time.sleep(1.5)
                        elif user_input == 'b': 
                            tempb()
                        else:
                            print('Invalid action. Please try again.')
                            time.sleep(2)
                            self._choose_enemy()
                    if chosen_enemy[1] < self.__level:
                        print(f"This {chosen_enemy[0]} enemy won't be a problem for you!")
                        user_input = input('Do you want to [F]ight or [B]ack? ').lower()
                        user_input = user_input[:10]
                        user_input = user_input.strip()
                        if user_input == 'f':
                            tempf()
                            time.sleep(1.5)
                        elif user_input == 'b': 
                            tempb()
                        else: 
                            print('Invalid action. Please try again.')
                            time.sleep(2)
                            self._choose_enemy()
                elif action == 'b':
                    print('Going back to the enemy list...')
                    time.sleep(2)
                    self._choose_enemy()
                elif action == 'p':  #Pass option allows player to regen enemies 
                    enemies.clear() 
                    temp_enemy = Enemy() 
                    temp_enemy()
                    del temp_enemy
                    print('Regenerating enemies...')
                    time.sleep(2)
                    self._choose_enemy()
                elif action == 'q':
                    print('Exiting the game...')
                    time.sleep(2)
                    exit()
                else:
                    print('Invalid action. Please try again.')
                    time.sleep(2)
                    self._choose_enemy()
            elif choice.lower() == 'q':
                print('Exiting the game...')
                time.sleep(2)
                exit()
            elif choice.lower() == 's':
                print(self)
                time.sleep(1.5)
                self._choose_enemy()
            else: 
                print('Invalid choice. Please try again.')
                time.sleep(2)
                self._choose_enemy()
        else: 
            raise IndexError('No enemies available to choose from!')
    
    def _level_up(self): 
        def _level_up_check():   
            if len(enemies) > 0: 
                self._gain_experience()
                if self._experience[0] >= self._experience[1]:
                    while self._experience[0] >= self._experience[1]:
                        self.__level = self.__level + 1
                        self._experience[0] = int(self._experience[0] - self._experience[1])
                        self._experience[1] = int(self._experience[1] + 100)
                        print("Debug")
                        if self._experience[0] < self._experience[1]:
                            break
                    print(f'''You have leveled up to level {self.__level} and healed!
                      Current experience: {self._experience[0]}/{self._experience[1]}''')
                    player_health[1] = str(int(player_health[1]) + 100)
                    player_health[0] = player_health[1]
            else:
                 pass
        threaded_method = threading.Thread(target=_level_up_check)
        threaded_method.start()


    def _gain_experience(self): 
        for i, enemy in enumerate(enemies):
            if enemy[2] <= 0:
             self._experience[0] = int(self._experience[0] + (50 * enemy[1]))
             print(f"You have gained {self._experience[0]} experience points!")
            else: 
                pass
          
class Enemy(): #Class utilized to create instances of enemies
    stored_index = list() #Creating a variable to store the index of the enemy
    __slots__ = ['_kind', '__elevel', '__ehealth']

    def __init__(self, _kind=' ', __elevel=abs(1), __ehealth=abs(100)):
        if _kind == ' ':
            _kind = random.choice(['Goblin', 'Orc', 'Troll', 'Dragon', 'Vampire'])
            if _kind not in ['Goblin', 'Orc', 'Troll', 'Dragon', 'Vampire']:
                raise ValueError('Invalid enemy type') #Preventing arbitrary input and limiting to 5 types of enemies
        if not isinstance(_kind, str) or not isinstance(__elevel, int):  
            raise TypeError('Name must be a string and level must be an integer')
        self._kind = _kind[:10] 
        if len(self._kind) > 10:
            raise ValueError('Name cannot be longer than 10 characters')  
        self.__elevel = __elevel
        if len(player_health) > 0 and int(player_health[1]) > 100: 
            self.__elevel = int(abs(randint(1,3) * int(player_health[1]) / 100))
        self.__ehealth = __ehealth * int(self.__elevel * 2 / 1.5)
        if self.__ehealth != __ehealth * int(self.__elevel * 2 / 1.5): 
            return ValueError("Health check failed")
         
    def __repr__(self):
        return f'<Enemy: __kind={self._kind}, __level={self.__elevel}, __ehealth={self.__ehealth}>' 
    
    def __str__(self): 
        return f'<Enemy: {self._kind} at level {self.__elevel}>' 

    @classmethod        
    def _damage_player(cls):
        if len(player_health) > 0 and int(player_health[0]) > 0:
            random_enemy = randint(0, (len(enemies)-1))
            cls.stored_index.append(random_enemy)
            for instance, i in enumerate(enemies[cls.stored_index[0]]):
               # print(i) #testing purposes
               # print(enemies[self.stored_index[0]][0])
                if i == enemies[cls.stored_index[0]][0]:
                    cls._get_attack_power()
                    cls.stored_index.clear()
                    break
                else:
                    raise RuntimeError('Something went wrong with Enemy turn!')
                
    @classmethod
    def _get_attack_power(cls):
        enemy_name = enemies[cls.stored_index[0]][0]
        enemy_level = enemies[cls.stored_index[0]][1]
        random_value.update({enemy_name: (randint(1,10) * enemy_level)})
        if random_value[enemy_name] > (1 * enemy_level):
            if int(player_health[0][0]) > 0:
              player_health[0] = str(int(player_health[0]) - random_value[enemy_name])
            print(f'Enemy {enemy_name} hit the player for {random_value.pop(enemy_name)}!')
            time.sleep(1.5)
        else:
             critical_hit.update({enemy_name: 
                                  (random_value.pop(enemy_name) 
                                   * 2 * enemy_level)})
             player_health[0] = str(int(player_health[0]) - critical_hit[enemy_name])
             print(f'Critical hit of {critical_hit.pop(enemy_name)} damage against player by {enemy_name}!')
             time.sleep(1.5)

    def _enemy_update(self):
        creature_name = list()
        if len(enemies) > 1:
            for i, enemy in enumerate(enemies):
                creature_name.append(enemy[0])
        elif len(enemies) <= 1:
            creature_name = [i for sublist in enemies for i in sublist if i == self._kind]
        #print(creature_name) #Debugging purposes
        if self.__ehealth > 0: 
            if self._kind not in ['Goblin', 'Orc', 'Troll', 'Dragon', 'Vampire'] and self.__ehealth != int(self.__ehealth):
                return ValueError('Not a valid enemy type and/or enemy health is not an integer. Stop hacking!')
            elif self._kind in creature_name:
                while self._kind in creature_name:
                    for i in range(2,10):
                        if self._kind in creature_name:
                           if not self._kind[-1].isdigit():
                                self._kind = self._kind + str(i) 
                           elif self._kind[-1].isdigit() and self._kind[-1] != str(i):
                               self._kind = self._kind.replace(self._kind[-1], str(i))   
                        else:
                            break            
                    if self._kind not in creature_name: 
                        enemies.append([self._kind, self.__elevel, self.__ehealth])
                        break
            elif self._kind not in creature_name: 
                enemies.append([self._kind, self.__elevel, self.__ehealth])
        else: 
            raise ValueError('Enemy health cannot be negative')
  
    def __call__(self): 
        number_of_enemies = randint(1,3) 
        generated_enemies = list()
        if len(enemies) < 1:
            for i in range(number_of_enemies):
              generated_enemies.append(Enemy())
            for instance in generated_enemies: 
             instance._enemy_update() #Calling the "_enemy_alive" method to 
             #update the enemies dictionary with the generated instances 
        elif len(enemies) > 3: 
            raise ValueError("Something went wrong with generating enemies!")
        else: 
            pass
        
        
                    

       
__all__ = ['Player', 'Enemy', 'enemies', 
           'critical_hit', 'random_value', 'player_health'] #Mass Exporting
        

        


if __name__ == '__main__':  
    enemy = Enemy(_kind='Goblin') 
    #enemy2 = Enemy(_kind='Goblin')
    #enemy3 = Enemy(_kind='Goblin')
    #enemy4 = Enemy(_kind='Goblin')
    #print(enemy) 
    #print(enemy2)
    #print(enemy3)
    #print(enemy._get_attack_power())
    #enemy._enemy_update()
    #enemy2._enemy_update()
    #enemy3._enemy_update() 
    #enemy4._enemy_update()
    #print(enemies)
    #enemy._kind = 'Troll'
    #print(enemy)
    #print(enemy._get_attack_power())
    #print(enemy2._get_attack_power())
    #print(enemy3._get_attack_power()) 
    enemy() 
    #print(enemies)
    #print(enemies[0][1])
    
    player = Player(name = 'Bob')
    #player._get_attack_power()
    print(player._level_up)
    #player._choose_enemy()
    #print(player_health)
    #print(type(enemies[0][0]))
    #enemy._damage_player()
    #print(enemies)
