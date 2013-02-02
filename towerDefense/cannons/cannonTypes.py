'''
Source Name:           cannonTypes.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 5:
        - Changed from balance of cannon stats.
    Revision 4:
        - Consolidated all of the cannon classes into one file.
    Revision 3:
        - Wrote rest of cannon classes
    Revision 2:
        - Added upgrade arrays
    Revision 1:
        - Wrote basic cannon class
'''
import pygame
from . import cannon

# Basic cannon, does average damage, average speed, and average attack.
class BasicCannon(cannon.Cannon):
    Cost = [5, 20, 50, 150]
    Speed = [3, 3, 3, 5]
    Range = [2, 3, 3, 4]
    Damage = [3, 5, 8, 12]


    def __init__(self, x = -1, y = -1):
        cannon.Cannon.__init__(self, x, y, "Basic Cannon", "basic", BasicCannon.Cost, BasicCannon.Speed, BasicCannon.Range, BasicCannon.Damage)


    def getInstance(self):
        return BasicCannon()
    
# Freeze cannon, slows down monsters for 30 frames
class FreezeCannon(cannon.Cannon):
    Cost = [20, 50, 100, 250]
    Speed = [2, 2, 4, 5]
    Range = [3, 3, 4, 5]
    Damage = [0, 0, 0, 0]

    def __init__(self, x = -1, y = -1):
        cannon.Cannon.__init__(self, x, y, "Freeze Cannon", "freeze", FreezeCannon.Cost, FreezeCannon.Speed, FreezeCannon.Range, FreezeCannon.Damage)
        self.freeze = True

    def getInstance(self):
        return FreezeCannon()
    
# Sniper cannon, has high range to pick off monsters.
class SniperCannon(cannon.Cannon):
    Cost = [15, 100, 150, 300]
    Speed = [2, 3, 3, 3]
    Range = [4, 5, 5, 7]
    Damage = [4, 5, 5, 6]


    def __init__(self, x = -1, y = -1):
        cannon.Cannon.__init__(self, x, y, "Sniper Cannon", "sniper", SniperCannon.Cost, SniperCannon.Speed, SniperCannon.Range, SniperCannon.Damage)


    def getInstance(self):
        return SniperCannon()
    
# Splash cannon, hits multiple targets.
class SplashCannon(cannon.Cannon):
    Cost = [10, 50, 150, 300]
    Speed = [4, 4, 5, 5]
    Range = [2, 2, 3, 4]
    Damage = [2, 3, 4, 5]

    def __init__(self, x = -1, y = -1):
        cannon.Cannon.__init__(self, x, y, "Splash Cannon", "splash", SplashCannon.Cost, SplashCannon.Speed, SplashCannon.Range, SplashCannon.Damage)

    def getInstance(self):
        return SplashCannon()