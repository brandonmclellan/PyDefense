'''
Source Name:           monster.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 3:
        - Balanced monster stats
    Revision 2:
        - Wrote other monster classes
    Revision 1:
        - Wrote Normal monster class
'''
from .monster import Monster
import math

#Normal Monster, most common, has no special attributes.
class NormalMonster(Monster):
    #The base stats for a normal monster
    BaseHealth = 6
    BaseSpeed = 2
    BaseScore = 5
    BaseCash = 3
    
    def __init__(self, wave, path):
        Monster.__init__(self, "normal", NormalMonster.BaseSpeed, path)
        
        # Set the stats based on current wave.
        self.health = NormalMonster.BaseHealth + (0.25 * wave)
        self.speed = NormalMonster.BaseSpeed
        self.score = NormalMonster.BaseScore + (1 * wave)
        self.cash = NormalMonster.BaseCash + math.floor(0.5 * wave)
        
#Fast Monster, fastest monster in game.
class FastMonster(Monster):
    #The base stats for a fast monster
    BaseHealth = 8
    BaseSpeed = 4
    BaseScore = 8
    BaseCash = 5
    
    def __init__(self, wave, path):
        Monster.__init__(self, "fast", FastMonster.BaseSpeed, path)
        
        # Set the stats based on current wave.
        self.health = FastMonster.BaseHealth + (0.25 * wave)
        self.speed = FastMonster.BaseSpeed
        self.score = FastMonster.BaseScore + (1 * wave)
        self.cash = FastMonster.BaseCash + math.floor(0.5 * wave)
        
#Immune monster, cannot be slowed by frost cannon
class ImmuneMonster(Monster):
    #The base stats for a immune monster
    BaseHealth = 8
    BaseSpeed = 3
    BaseScore = 10
    BaseCash = 8
    
    def __init__(self, wave, path):
        Monster.__init__(self, "immune", ImmuneMonster.BaseSpeed, path)
        
        # Set the stats based on current wave.
        self.health = FastMonster.BaseHealth + (0.25 * wave)
        self.speed = FastMonster.BaseSpeed
        self.score = FastMonster.BaseScore + (1 * wave)
        self.cash = FastMonster.BaseCash + math.floor(0.5 * wave)
        self.immune = True
        
# Boss Monster, has alot of health and few of them.
class BossMonster(Monster):
    #The base stats for a boss monster
    BaseHealth = 20
    BaseSpeed = 2
    BaseScore = 8
    BaseCash = 5
    
    def __init__(self, wave, path):
        Monster.__init__(self, "boss", BossMonster.BaseSpeed, path)
        
        # Set the stats based on current wave.
        self.health = FastMonster.BaseHealth + (1 * wave)
        self.speed = FastMonster.BaseSpeed
        self.score = FastMonster.BaseScore + (1 * wave)
        self.cash = FastMonster.BaseCash + math.floor(0.5 * wave)
        