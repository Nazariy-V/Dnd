import random 
def attack(roll):
    amount,dice = map(int,roll[0].split("d"))
    return (sum([random.randint(1,dice) for i in range(amount)]),roll[1]//5)
