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
        player, comp = ' X ', ' 0 '                  # Даем право Игроку определиться
        break
    elif choice == '0':
        player, comp = ' 0 ', ' X '
        break
    else:
        print('Wrong, try again')

first_turn = random.randint(0, 1)
# Только в одном случае из двух игрок будет ходить первым.
# Сделано, поскольку тот, кто ходит первый имеет большое преимущество, что вносит существенный дисбаланс.
# Я гарантирую, что если комп будет ходить первый, то игрок Никогда не выиграет, максимум ничья

if first_turn:
    print('\n'"You're lucky, your first turn")
else:
    print('\n'"Gandalf said you go second")

field = ['   ' for i in range(3) for j in range(3)]  # Игровое поле
angle = [0, 2, 6, 8]                                 # Угловые клетки
move_counter_comp = 0                                # Счетчик ходов компа

strategies = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
# Выигрышные комбинации(стратегии)
# Где-то слышал что если есть возможность использовать tuple - надо использовать tuple, он вроде как дешевле и быстрее.
# В моей маленькой программе это не критично конечно, но нужно учиться делать правильно с самого начала своего IT-пути


comp_strategy = random.randint(0, 1)                 # Выбор стратегии компа

move_1 = random.choice(angle)                        # Выбираем любой угол для "первой" стратегии компа

def field_demonstration():                           # Функция демонстрации игрового поля
                                                     # используется после каждого хода
    print('-------------------')
    for i in range(3):
        for j in range(3):
            print('| ' + field[i*3 + j] + ' ', end='')
        print('|')
        print('-------------------')


def player_turn():                                   # Функция хода Игрока

    while True:
        turn = int(input('\n'' Your turn, enter cell number: '))
        if turn not in range(1, 10):
            print('\n'' Wrong number, try again')
        elif field[turn - 1] == '   ':
            field[turn - 1] = player
            break
        else:
            print('\n'' Cell is occupied, choose another cell')


# "Первая" стратегия компа. Возможна Только если комп ходит первым. Но, то факт, что комп ходит первым - не гаранирует
# что будет выбрана именно эта стратегия. Данная стратегия заключается в расстановке символом компа по углам поля
# для постановки вилки.
def first_strategy_comp():

    if not move_counter_comp:                        # Первый ход компа в этой стратегии
        field[move_1] = comp
        angle.pop(angle.index(move_1))               # Удаляем выбранный угол из списка углов
        return True
    if move_counter_comp == 1:                       # Второй ход компа в этой стратегии
        move_2 = 8 - move_1                          # Выбираем противоположный угол.
# Здесь была мысль создать реверс игрового поля (по типу reverse_field = [i for i in range (8, -1, -1)]), и искать
# противположные точки там, но, как оказалось, это нужно в программе всего в двух местах. Затем, я заметил что если от 8
# отнять индекс игрового поля, то мы получим индекс клетки напротив и в итоге решил использовать именно этот способ.

        if field[move_2] == player:                  # Если выбранный противоположный угол занят компом -
            angle.pop(angle.index(move_2))           # удаляем его из списка углов
            move_2 = random.choice(angle)            # выбираем новый угол
            field[move_2] = comp                     # и ставим туда символ компа, даже без проверки поскольку это
            angle.pop(angle.index(move_2))           # третий общий ход игры и все занятые клетки нам уже известны
            return True                              # Вновь удаляем "использованный" угол и выходим из функции
        else:
            field[move_2] = comp                     # А если выбранный угол Не занят Игроком (т.е. не сработал if)
            angle.pop(angle.index(move_2))           # то смело заполняем клетку символом компа
            return True
    if move_counter_comp == 2:                       # Третий ход компа в этой стратегии
        move_3 = random.choice(angle)
        if field[move_3] == player:                  # Алгоритм такой же как на втором ходу
            angle.pop(angle.index(move_3))           # цель - заполнить еще один угол
            move_3 = random.choice(angle)
            field[move_3] = comp                     # Удалять угол из списка углов нет смысла
            return True                              # т.к. на этом этапе он там остался один
        else:
            field[move_3] = comp
            return True
# Расписывать дальнейшие ходы в этой стратегии не имеет смысла,
# т.к. на этом этапе Игроку уже должна быть поставлена вилка, далее свое дело сделает функция dont_get_win()


# Здесь описан алгоритм постановки вилки для игрока в случае если компом занят центр и один из углов,
# а один из углов к третьему ходу компа в этой ветке уже скорее всего занят
def fork():

    occup_angle = None                               # Здесь будет индекс занятого угла
    for i in angle:
        if field[i] == comp:                         # Находим занятый угол и
            occup_angle = i                          # записываем индекс в переменную
            angle.pop(angle.index(i))                # Удаляем данный угол из списка углов
            angle.pop(angle.index(8 - i))            # Удаляем противоположный угол

# Далее нам нужно будет выяснить в какой именно угол из двух, оставшихся в списке (которые так же являются смежными,
# т.к. противоположный мы удалили выше), компу следует поставить символ. Вилка сработает только если между уже занятым и
# углом-претендентом - нет символа Игрока. Для этого нужно найти индексы этих боковых клеток, имея на руках только
# индексы углов. Находим среднее между этими двумя числами(индексами) и получаем необходимый индекс.

    side_cell_1 = int((occup_angle + angle[0]) / 2)
    side_cell_2 = int((occup_angle + angle[1]) / 2)
    side_cell = [side_cell_1, side_cell_2]

    for a, b in zip(side_cell, angle):               # Перебираем одновременно и угол и боковую клетку на "незанятость"
        if field[a] == field[b] == '   ':            # и если условие соблюдено то
            field[b] = comp                          # ставим символ компа в соответствующий угол
            return True                              # Игроку поставлена вилка
        return False                                 # Если в обеих боковых клетках стоят символы Игрока
                                                     # то вилка не сработала, возвращаем False

def computer_turn():                                 # Функция хода компа

    global move_counter_comp

    print('\n''Computer turn''\n')

    # Первый ход компа:
    if not move_counter_comp:
        if not comp_strategy and not first_turn:
            first_strategy_comp()                    # "Первая" стратегия. Активируется только если комп начинает игру
            return
        if comp_strategy == 1 and field[4] == '   ': # Следующая стратегия. Заключается в "захвате" центральной клетки
            field[4] = comp                          # Если центр пустой - занимаем центр
            return
        else:                                        # Следующая стратегия. Срабатывает если выбрана случайным образом
            while True:                              # ИЛИ если не сработала предыдущая стратегия (центр был занят)
                random_angle = random.choice(angle)  # Заключается в "захвате" одного их углов
                if field[random_angle] == '   ':
                    field[random_angle] = comp
                    return


# Далее мы вызываем функцию dont_get_win(), которая срабатывает Всегда в начале хода компа, кроме первого хода,
# т.к. на первом ходу ее использование не имеет смысла.
    if dont_get_win():
        return

    # Второй ход компа:
    if move_counter_comp == 1:
        if not comp_strategy:                        # Если комп выбрал "первую" стратегию сначала то запускаем функцию,
            first_strategy_comp()                    # которая отвечает за эту стратегию
            return
        else:                                        # Проверку на центральную клетку уже не делаем
            while True:                              # поскольку она была осуществлена в первом ходе
                random_angle = random.choice(angle)  # и на данный момент уже принадлежит либо Игроку либо компу
                if field[random_angle] == '   ':
                    field[random_angle] = comp       # Поэтому нам просто нужно занять любой свободный угол
                    return

    # Третий ход компа:
    if move_counter_comp == 2:                       # Если функция dont_get_win() вернула False
        if not comp_strategy:                        # И если не выбрана "первая" стратегия
            first_strategy_comp()
            return
        if field[4] == comp and fork():              # То проверяем центр, если там стоит символ компа, то ставим вилку
           return
        elif field[4] != comp:                       # Если центр занят, или вилку поставить не удалось
            while True:                              # то ставим символ компа в любой свободный угол.
                random_angle = random.choice(angle)
                if field[random_angle] == '   ':
                    field[random_angle] = comp
                    return
        else:                                        # Если и свободных углов не нашлось, то комп ставит символ просто в
            while True:                              # любой рандомной клетке поля
                random_cell = random.randint(0, 8)
                if field[random_cell] == '   ':
                    field[random_cell] = comp
                    return

    # Четвертый ход компа
    if move_counter_comp == 3:                       # Если до этого момента нет победителя, и в начале этого хода
        while True:                                  # не сработала функция dont_get_win(),
            random_cell = random.randint(0, 8)       # то комп просто рандомно ставит где-нибудь свой символ,
            if field[random_cell] == '   ':          # поскольку такая партия это уже почти точно ничья
                field[random_cell] = comp
                return


def dont_get_win():                                  # Помимо организации стратегии защиты (это когда Игроку осталась
                                                     # одна клетка до выигрыша), функция проверяет так же аналогичную
    # Перебор для компа                              # ситуацию для компа
    for st in strategies:
        count_comp = 0                               # Важно было сделать первой проверку ВСЕХ стратегий именно компа
        maybe_1 = 10                                 # поскольку если объединить проверки компа и Игрока в один цикл,
        for i in st:                                 # может случиться так, что первой попадется выиграшная комбинация
            if field[i] == player:                   # Игрока, в итоге комп поставит свой символ заблокировав стратегию
                break                                # Игрока, хотя мог завершить игру своей победой уже на этом ходу
            if field[i] == '   ':
                maybe_1 = i                          # Алгоритм работы цикла описан ниже
            if field[i] == comp:
                count_comp += 1
        if count_comp == 2 and maybe_1 != 10:        # По умолчанию maybe равно 10, поскольку иногда эта переменная
            field[maybe_1] = comp                    # может остаться без изменений с последней итерации цикла, и тогда
            return True                              # (если бы, например, по умолчанию maybe был бы 0) комп ставил бы
    # Перебор для Игрока                             # свой символ не там где надо
    for st in strategies:
        count_player = 0
        maybe_2 = 10                                 # Алгоритм работы цикла: перебираем все выигрышные комбинации,
        for j in st:                                 # проверяем наличие в них символа Игрока, если находим
            if field[i] == comp:                     # то увеличиваем счетчик. Если по пути попадается пустая клетка
                break                                # то записываем ее (индекс) как претендента на внесение в нее
            if field[j] == '   ':                    # символа компа. Если по пути попадается клетка компа то сразу
                maybe_2 = j                          # останавливаем эту итерацию цикла и переходим к следующей
            if field[j] == player:                   # комбинации.
                count_player += 1
        if count_player == 2 and maybe_2 != 10:      # Если было найдено две клетки компа в комбинации И третья клетка
            field[maybe_2] = comp                    # комбинации свободна - ставим туда символ компа
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
        while move_counter < 8:
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
        while move_counter < 8:
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