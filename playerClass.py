import random
import math
from hit_functions import roll_damage

'''
The Player class has the bulk of the nasty hit logic. 
From the intialization, it has the following attributes:
    - role: The player's role (mage, or range)
    - current_weapon: The weapon that the player is using.
    - cooldown: If the player is on a cooldown from using a weapon, this is the cooldown (in ticks).
    - setup_type: A method for determining if shadow setups are being used or not.
    - hit_counter: A way of ensuring that tick limits aren't violated, and for weapon swapping
        - This is primarily enforced with bp->2tbow tick fill, and chally->scy tick fill.
    - flag: A flag for when a boss changes in a certain pattern to determine the hit type. (bp2tbow, chally)
    - bp2tbow_count: Counter to help ensure bp2tbow is done properly.
    - last_attack_tick: Used to ensure cooldown is enforced. The tick last attacked on.
    - chalbred_count: A counter to ensure that the Mage doesn't do too many specs.
        - By default, the no lightbearer setups can do 2 chally's, the LB setups can do 3.
'''
class Player:
    def __init__(self, role, setup_type=None):
        self.role = role
        self.current_weapon = None
        self.cooldown = 0
        self.setup_type = setup_type if setup_type else {}
        self.hit_counter = 0
        self.flag = None
        self.bp2tbow_count = 0  
        self.last_attack_tick = -1  
        self.chalbred_count = 0  

    '''
    This function is responsible for weapon choosing logic.
    Self contains all of the info about weapons for a given player.
    Boss contains all of the boss info that is relevant to know what to attack with.
    '''
    def choose_weapon(self, boss):

        # Magic Boss Phase 
        # Switches to whatever magic weapon the player has (either shadow, or sang)
        if boss.phase == 'magic': 
                return self.role.weapons['magic']

        # Ranged Boss Phase
        if boss.phase == 'ranged' and boss.prev_phase == 'magic':  # Mage -> Range is BP->2tbow conditions. 
            if self.role.role == 'mager' and self.setup_type == 'shadow': # Shadow setup can't do BP->2tbow, just use normal ranged weapon.
                return self.role.weapons['ranged']
            else: # bp 2 tbow logic, a bit backwards but whatever
                if self.flag == 'bp2tbow':
                    if self.hit_counter == 0: # if no blowpipes have occured yet, then blowpipe
                        return self.role.weapons['blowpipe'] 
                    else: # if you've hit already with blowpipe, switch to tbow
                        return self.role.weapons['ranged']
                else:
                    if self.setup_type != 'shadow': 
                        self.flag = 'bp2tbow' # assign the bp 2tbow flag to non-shadow users (either sang user, or ranger)
                        self.hit_counter = 0 # reset hit counter
                        return self.role.weapons['blowpipe'] # use blowpipe
                    return self.role.weapons['ranged']  # if not bp2tbow, and shadow, use ranged weapon again (don't ask)

        if boss.phase == 'ranged' and boss.prev_phase == 'melee': # no special fills for melee -> range
            return self.role.weapons['ranged']

        if boss.phase == 'melee' and boss.prev_phase == None: # initial boss phase
            return self.role.weapons['melee']

        if boss.phase == 'melee' and boss.prev_phase == 'ranged': # no special fills for range -> melee
            return self.role.weapons['melee']
        
        if boss.phase == 'melee' and boss.prev_phase == 'magic': # chally fill on ranger
            if self.role.role == 'mage' and self.setup_type != 'shadow': # only magers can chally fill, and they can't fill if shadowing
                self.flag = 'chalbred' # set flag to indicate chally being used 
                return self.role.weapons['chalbred'] # use chally
            else:
                return self.role.weapons['melee'] # if ranger, or a shadow user, just use a scythe instead.
            
    '''
    roll_hit is responsible for rolling hits for various weapons.
    Unfortunately, the chally logic is a bit dumb so it's a bit of a mess implementing.
    '''

    def roll_hit(self, boss):
        if self.flag == 'chalbred' and self.chalbred_count < 3 and self.role.role == 'std_weapons_mage_lb': # LB users get 3 challys
            self.current_weapon = self.role.weapons['chalbred']
            self.chalbred_count += 1 # add one chally to the counter
            self.flag = None # remove the flag 
        elif self.flag == 'chalbred' and self.chalbred_count < 2 and self.role.role == 'std_weapons_mage': # Ultor users get 2 challys
            self.current_weapon = self.role.weapons['chalbred']
            self.chalbred_count += 1 # add one chally to the counter
            self.flag = None # remove the flag
        else:
            self.current_weapon = self.choose_weapon(boss) # if not challying, just pick weapon like normal

        atk_roll = self.current_weapon.accuracy # accuracy of the chosen weapon
        def_roll = boss.get_defence_roll(self.current_weapon.style) # def roll of the boss given the style **ZERO DEF ASSUMPTION**
        dmg = 0 # initialize 0 dmg

        if self.current_weapon.name == 'scythe':
                hit1_max = self.current_weapon.max_hit
                hit2_max = math.floor(hit1_max/2)
                hit3_max = math.floor(hit2_max/2)
                big = roll_damage(hit1_max) if random.randint(0, atk_roll) > random.randint(0, def_roll) else 0
                med = roll_damage(hit2_max) if random.randint(0, atk_roll) > random.randint(0, def_roll) else 0
                small = roll_damage(hit3_max) if random.randint(0, atk_roll) > random.randint(0, def_roll) else 0
                dmg = big + med + small

        elif self.current_weapon.name == 'chalbred':
            atk_roll1 = self.current_weapon.accuracy
            atk_roll2 = math.floor(atk_roll1)
            dmg1 = roll_damage(self.current_weapon.max_hit) if random.randint(0, atk_roll1) > random.randint(0, def_roll) else 0
            dmg2 = roll_damage(self.current_weapon.max_hit) if random.randint(0, atk_roll2) > random.randint(0, def_roll) else 0
            dmg = dmg1 + dmg2
            
        else:
            dmg = roll_damage(self.current_weapon.max_hit) # for normal weapons, roll hits as normal

        if self.flag == 'bp2tbow': # bp 2 tbow counter
            self.hit_counter += 1 
            if self.hit_counter == 1:
                self.bp2tbow_count += 1  # Increment bp2tbow count only once per valid condition
            if self.hit_counter == 3:
                self.flag = None  # Reset the flag after the sequence is complete
                self.hit_counter = 0  # Reset hit counter after completing the sequence

        if self.chalbred_count > 0 and self.current_weapon.name == 'chalbred':
            self.flag = None  # Reset the flag after one hit
            self.current_weapon = self.role.weapons['melee']  # Switch to scythe after chalbred

        return dmg

    def attack(self, boss, current_tick):
        if current_tick < self.last_attack_tick + self.cooldown:  # can't hit off cooldown
            return 0
        if current_tick - boss.last_phase_change_tick <= 1:  # need a tick to react
            return 0
        dmg = self.roll_hit(boss) # hit the boss 
        self.cooldown = self.current_weapon.speed # apply cooldown
        self.last_attack_tick = current_tick # when was the last hit
        return boss.take_dmg(dmg) # apply damage to the boss

'''
The Role class is primarily used to grab weapons and Player names for the simulation.
The only components are 'role', and 'weapons'.
'''
class Role:
    def __init__(self, role, weapons):
        self.role = role
        self.weapons = weapons
    
    def __str__(self):
        return self.role

'''
The Weapon class stores how different weapons behave and their characteristics.
This is described in main.py, as well.

The 'Weapons' class takes inputs as such:
    (name, accuracy, max_hit, speed, style), and the previous string is how it is referred to.
    i.e, calling player.role.weapons['magic'] calls the magic weapon for a certain player.

Some setups have special items, like blowpipe or chalbred. This is for tick fills.
'''
class Weapon:
    def __init__(self, name, accuracy, max_hit, speed, style):
        self.name = name
        self.accuracy = accuracy
        self.max_hit = max_hit
        self.speed = speed
        self.style = style
    
    def __str__(self):
        return self.name
