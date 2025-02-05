import random

while True:
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    dice3 = random.randint(1, 6)

    total = dice1 + dice2 + dice3
    
    if total <= 10:
        break

print(dice1, dice2, dice3,"=" ,total)

