import random

'''
Hit functions for sim.

roll_damage:
    - Takes in a max hit, then rolls from 0 to the max hit. If it rolls a 0
      then it gets replaced with a 1, as this is post accuracy check and rolls are (1,1-max)
'''
def roll_damage(max_hit):
    damage = random.randint(0, max_hit)
    if damage == 0:
        damage = 1
    return damage


