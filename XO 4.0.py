import random

print(''' 
-------------------       
|  1  |  2  |  3  |       Rules for entering numbers on the field
-------------------
|  4  |  5  |  6  |       For example, if you want to put X in the center of the field - you need to enter the number 5
-------------------
|  7  |  8  |  9  |       Good luck
-------------------      
        ''')


while True:
    choice = input('    Choose who you are (X/0): ')
    if choice.lower() == 'x':
        player, comp = ' X ', ' 0 '
        break
    elif choice == '0':
        player, comp = ' 0 ', ' X '
        break
    else:
        print('Wrong, try again')

first_turn = random.randint(0, 1)    # 50/50 того, что игрок будет ходить первым.
                                     # Сделано, поскольку тот кто ходит первый имеет большое преимущество, что вносит дисбаланс
if first_turn:
    print('\n'"You're lucky, your first turn")
else:
    print('\n'"Gandalf said you go second")

field = ['   ' for i in range(3) for j in range(3)]

 # Выигрышные комбинации(стратегии)
 # Где-то читал что если есть возможность использовать tuple - надо использовать tuple
 # он вроде как дешевле и быстрее
 # В моей маленькой программе это не критично конечно
 # но нужно учиться делать правильно с самого начала своего IT-пути

strategies = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
angle = (0, 2, 6, 8)
move_counter_comp = 0

def field_demonstration():
    print('-------------------')
    for i in range(3):
        for j in range(3):
            print('| ' + field[i*3 + j] + ' ', end='')
        print('|')
        print('-------------------')


def player_turn():

    while True:
        turn = int(input('\n'' Your turn, enter cell number: '))
        if turn not in range(1, 10):
            print('\n'' Wrong number, try again')
        elif field[turn - 1] == '   ':
            field[turn - 1] = player
            break
        else:
            print('\n'' Cell is occupied, choose another cell')


def computer_turn():

    global move_counter_comp

    print('\n''Computer turn''\n')

    if not move_counter_comp: # Первый ход компа
        while True:                                        # Намерено не использовал цикл for, поскольку в таком случае
            choice_comp_strategy = random.randint(0,4)     # проверка будет идти по порядку
            if choice_comp_strategy == 4:                  # а это сделает игру компа предсказуемой
                random_angle = random.choice(angle)        # В 4 из 5 случаев компьютер поставит свой символ в центре,
                if field[random_angle] == '   ':           # что, в таком случае, практически гарантирует ему победу
                    field[random_angle] = comp
                    return
            else:
                if field[4] == '   ':
                    field[4] = comp
                    return

    elif move_counter_comp == 1:  # второй ход компа
        if dont_get_win():
            return
        if field[4] == comp:     # если центральная клетка занята компом то
            while True:
                random_angle = random.choice(angle)   # комп занимает одну из угловых клеток
                if field[random_angle] == '   ':
                    field[random_angle] = comp
                    return
        elif field[4] == '   ':    # Конечно маловероятно что к третьему(или второму) ходу из общих игровых ходов
            field[4] = comp        # центральная клетка будет свободна, но описать этот случай все же надо
            return
        elif field[4] == ' X ':
            for i in angle:
                if field[i] == '   ':      # Ситуация где все углы заняты на третьем(или втором) общем ходу в игре - невозможна технически
                    field[i] = comp        # поэтому такое ветвление даже не делалось
                    return

    elif move_counter_comp == 2:   # третий ход компа
        if dont_get_win():
            return
        if field[4] == comp:         # Здесь описан алгоритм постановки вилки для игрока, если компом занят центр и один из углов
            for i in angle:
                if field[i] == comp:
                    if (i == 8 or i == 0) and (field[2] == '   ' or field[6] == '   '):
                        if field[2] == '   ':
                            field[2] = comp
                            return
                        if field[6] == '   ':
                            field[6] = comp
                            return
                    if (i == 2 or i == 6) and (field[0] == '   ' or field[8] == '   '):
                        if field[0] == '   ':
                            field[0] = comp
                            return
                        if field[8] == '   ':
                            field[8] = comp
                            return
        elif field[4] != comp:
            while True:
                random_angle = random.choice(angle)   # комп занимает одну из угловых клеток
                if field[random_angle] == '   ':
                    field[random_angle] = comp
                    return
        else:
            while True:
                random_cell = random.randint(0, 8)
                if field[random_cell] == '   ':
                    field[random_cell] = comp
                    return

    elif move_counter_comp == 3:  # Четвертый ход компа
        if dont_get_win():
            return
        else:
            while True:
                random_cell = random.randint(0, 8)
                if field[random_cell] == '   ':
                    field[random_cell] = comp
                    return


def dont_get_win():

    for st in strategies:  # по стратегии в стратегиях
        count_comp = 0                                   # Важно было сделать первой проверкой именно проверку всех стратегий компа
        maybe = 0                                        # поскольку если объединить проверки в один цикл, может случиться так,
        for i in st:                                     # что первой попадется выиграшная комбинация игрока, в итоге комп
            if field[i] == '   ':                        # заблокирует его стратегию, хотя мог завершить игру своей победой
                maybe = i
            if field[i] == comp:
                count_comp += 1
        if count_comp == 2 and field[maybe] == '   ':    # вторая проверка на наличие пустой клетки нужна потому что бывают ситуации
            field[maybe] = comp                          #
            return True
    for st in strategies:
        count_player = 0
        maybe = 0
        for i in st:
            if field[i] == '   ':
                maybe = i
            if field[i] == player:
                count_player += 1
        if count_player == 2 and field[maybe] == '   ':
            field[maybe] = comp
            return True
    return False


def check_winner():

    for st in strategies:
        count_player = 0
        count_comp = 0
        for i in st:
            if field[i] == player:
                count_player += 1
            if field[i] == comp:
                count_comp += 1

        if count_player == 3:
            print('\n' 'Y O U   W I N!!!')
            return True

        if count_comp == 3:
            print('\n''-' * 5 + 'ПОТРАЧЕНО')
            return True

    return False


def game():

    global move_counter_comp

    move_counter = 0
    if first_turn:
        while move_counter <= 7:
            player_turn()
            field_demonstration()
            move_counter += 1
            if check_winner():
                return
            computer_turn()
            field_demonstration()
            move_counter_comp += 1
            move_counter += 1
            if check_winner():
                return

    else:
        while move_counter <= 7:
            computer_turn()
            field_demonstration()
            move_counter_comp += 1
            move_counter += 1
            if check_winner():
                return
            player_turn()
            field_demonstration()
            move_counter += 1
            if check_winner():
                return

    return print('S T A N D O F F')

game()