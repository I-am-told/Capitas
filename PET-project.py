import random

while True:
    balance = random.randint(4, 22)
    rival = random.randint(15, 27)
    increase = input(f'\nYour balance: {balance} \n Do you want to add yor balance? (y/n) ')

    while increase == 'y':
        cards = [2, 3, 4, 10, 11]
        random_cards = random.choice(cards)
        balance += random_cards
        increase = input(f'\nNow your balance: {balance} \n Do you want to add yor balance? (y/n) ')

    if increase == 'n':
        if balance == rival:
            print(f'\nBalance your rival {rival}  \nDead heat')
        elif rival < balance <= 21 or 21 <= balance < rival or (rival > 21 and balance <= 21):
            print(f'\nBalance your rival {rival}  \nYou win!!!')
        elif balance < rival <= 21 or 21 <= rival < balance or (balance > 21 and rival <= 21):
            print(f'\nBalance your rival {rival}  \nYou lose')
        else:
            print(f'\nBalance your rival: {rival} -------  ПРОВЕРОЧКА!')

    play = input('\nDo you want to play again? (y/n) ')
    if play == 'n':
        break

