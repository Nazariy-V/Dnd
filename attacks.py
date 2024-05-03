import random 
def attack(roll):
    amount,dice = map(int,roll[0].split("d"))
    return (sum([random.randint(1,dice) for i in range(amount)]),roll[1]//5)
def longsword():
    return ((1,8), 5)
def shortsword():
    return ((1,6), 5)
def shortbow():
    return ((10,60), 80)
