import random 
def attack(roll):

    return (sum([random.randint(1,roll[0][1]) for i in range(roll[0][0])]),roll[1]//5)
def longsword():
    return ((1,8), 5)
def shortsword():
    return ((1,6), 5)
def shortbow():
    return ((1,6), 80)
