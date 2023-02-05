# Добрый день. Я хотел создать нечто бОльшее чем просто игра двух людей в крестики нолики
# В моей программе компьютер не просто рандомно выбирает клетку, хотя подобное поведение так же предусмотерно
# Он Хочет победить, у него есть стратегии которых он придерживается
# Возможно, в каких то моментах можно было применить другие решения, более питонвские
# Где-то мне не хватило для этого опыта
# Но где-то я намерено не использовал такие решения, как, например, инлайновые условия
# В угоду читаемости кода


import random

def your_turn(): # Ход игрока

    global field, y, strategies, strategy0, strategy1, strategy2, \
        strategy3, strategy4, strategy5, strategy6, strategy7, strategy8  # Некрасивая конструкция, но другого решения я не нашел, так как эти переменные используются во всех функциях
                                                                          # И если "вынести их за скобки" то при новой игре, например, какие-то клетки поля, уже будут заняты
    p = 1   # Переключатель                                               # А так можно играть "бесконечно"
    while p:    # Работет пока переключатель - истина
        turn = int(input('\n'' Your move, enter cell number: ' ))
        if not (field[turn-1])[0]:  # Если на рабочем поле в клетке с индексом turn-1(а это соответствующая клетка для демонстрации) - ничего нет то:
            field[turn-1] = ['X']    # Эта самая клетка становится иксом
            p = 0   # Меняем значение переключателя - останаливаем бесконечный цикл
            print()
            print(*field[0:3])    # Из работающих способов красиво(правильно) вывести поле в консоль еще был цикл for в цикле for
            print(*field[3:6])    # Но я подумал что эти лишние циклы ни к чему, дейтвительно проще и "дешевле" сделать так как я сделал
            print(*field[6:9])    # Хоть это и противоречит философии Python - don't repeat yourself
        else:
            print('\n'' Cell is occupied, choose another cell')   # Запускает цикл по новому если клетка занята чем то


def comp_turn():

    global field, y, strategies, strategy0, strategy1, strategy2, \
        strategy3, strategy4, strategy5, strategy6, strategy7, strategy8

    print('\n''Computer move''\n')

    rand = random.randint(0, 2)     # "Рандомная" стратегия, была добавлена что бы сделать поведение компьтера более непредсказуемым
                                    # При чем шансы, что компьютер выберет победную стратегию по отношению к рандомной оставляет 2 к 3
    if rand == 2:
        (field[random.randint(0, 8)])[0] = '0'
    else:
        if (y == None) or (any([(field[y[0]][0]) == 'X', (field[y[1]][0]) == 'X', (field[y[2]][0]) == 'X'])): # Если в выбранной стратегии есть икс или это первый ход
            while True:
                y = random.choice(strategies)    # Случайным образом выбираем стратегию
                if not (field[y[0]][0]) and not (field[y[1]][0]) and not (field[y[2]][0]): # Если в клетках выбранной стратегии ничего нет то:
                    (field[random.choice(y)])[0] = '0'   # Выбираем рандомный индекс из стратегии и ставим туда ноль
                    break # Останавливаем while. Если условие выше не выполняется то запускаем цикл снова (выбираем другую стратегию)

        else: # Если НЕ первый ход (y != None, то есть стратегия уже есть), и если на предыдущем ходу в стратегию не был добавлен X
            for i, j in enumerate([(field[y[0]][0]), (field[y[1]][0]), (field[y[2]][0])]): # Перебираем клетки выбранной стратегии на рабочем поле
                if not j:  # Если какое-то значение из перебранных выше клеток - false (то есть пустая строка), то:
                    (field[y[i]][0]) = '0' # Берем индекс этой клетки из стратегии и вставляем его в соответствующий адрес на рабочем поле
                    break # Останавлвиаем for, что бы все клетки в стратегии не стали 0 за один ход


    print(*field[0:3]) # Не могу без слез на это смотреть
    print(*field[3:6])
    print(*field[6:9])

def game():

    global field, y, strategies, strategy0, strategy1, strategy2, \
        strategy3, strategy4, strategy5, strategy6, strategy7, strategy8

    field_for_demonstration = [    # Данное поле показывается один раз в начале игры, что бы игрок понимал механику и правила игры
        (1), (2), (3),             # То есть что бы он понимал, что например "Если он хочет поставить крестик  в центре поля ему нужно нажать 5"
        (4), (5), (6),             # Можно было бы сделать нумерацию с нуля, но я подумал что не все игроки могут быть программистами, и что бы
        (7), (8), (9)]             # Такого человека не вводить в заблуждение я сдедал поле для демонстарции правил именно таким
                                   # Логику с номером клетки соответсвующим индексу - я осуществил далее в стратегиях

    field = [                   # Рабочее поле, сюда будут вноситься крестики и нолики, и это поле будет выводиться после каждого хода
        [''], [''], [''],
        [''], [''], [''],
        [''], [''], ['']]

    y = None   # Вообще я хотел назвать эту переменную сomp_strategy, но так как я ее использую часто
               # и в сложных конструкциях, то это сильно бы загромождало код

    print(*field_for_demonstration[0:3])  # Миксер мне в глаза
    print(*field_for_demonstration[3:6])
    print(*field_for_demonstration[6:9])

    strategy0 = (0, 1, 2)   # Собственно выигрышные комбинации(стратегии)
    strategy1 = (3, 4, 5)
    strategy2 = (6, 7, 8)
    strategy3 = (0, 3, 6)   # Где-то читал что если есть возможность использовать tuple - надо использовать tuple
    strategy4 = (1, 4, 7)   # Он вроде как дешевле
    strategy5 = (2, 5, 8)
    strategy6 = (0, 4, 8)
    strategy7 = (2, 4, 6)

    strategies = (strategy0, strategy1, strategy2, strategy3, strategy4, strategy5, strategy6, strategy7)
    # Список стратегий, из них комп выбирает если не выбрал "рандомную" стратегию

    while True:   # Зацикливание игры, что бы можно было начать заново не прерывая работу программы


        your_turn()

        if any([
            all([(field[strategy0[0]][0]) == 'X', (field[strategy0[1]][0]) == 'X', (field[strategy0[2]][0]) == 'X']),
            all([(field[strategy1[0]][0]) == 'X', (field[strategy1[1]][0]) == 'X', (field[strategy1[2]][0]) == 'X']),
            all([(field[strategy2[0]][0]) == 'X', (field[strategy2[1]][0]) == 'X', (field[strategy2[2]][0]) == 'X']),
            all([(field[strategy3[0]][0]) == 'X', (field[strategy3[1]][0]) == 'X', (field[strategy3[2]][0]) == 'X']),
            all([(field[strategy4[0]][0]) == 'X', (field[strategy4[1]][0]) == 'X', (field[strategy4[2]][0]) == 'X']),
            all([(field[strategy5[0]][0]) == 'X', (field[strategy5[1]][0]) == 'X', (field[strategy5[2]][0]) == 'X']),
            all([(field[strategy6[0]][0]) == 'X', (field[strategy6[1]][0]) == 'X', (field[strategy6[2]][0]) == 'X']),
            all([(field[strategy7[0]][0]) == 'X', (field[strategy7[1]][0]) == 'X', (field[strategy7[2]][0]) == 'X'])]):

            # Прверка на выигрыш, делается после каждого хода. Как сделать ее менее громоздкой я так и не понял

            a = input('\n' 'You win!!!' '\n' '\n' 'Do you want to play again? (y/n): ')
            if a == 'y':
                return game()
            break


        comp_turn()

        if any([
            all([(field[strategy0[0]][0]) == '0', (field[strategy0[1]][0]) == '0', (field[strategy0[2]][0]) == '0']),
            all([(field[strategy1[0]][0]) == '0', (field[strategy1[1]][0]) == '0', (field[strategy1[2]][0]) == '0']),
            all([(field[strategy2[0]][0]) == '0', (field[strategy2[1]][0]) == '0', (field[strategy2[2]][0]) == '0']),
            all([(field[strategy3[0]][0]) == '0', (field[strategy3[1]][0]) == '0', (field[strategy3[2]][0]) == '0']),
            all([(field[strategy4[0]][0]) == '0', (field[strategy4[1]][0]) == '0', (field[strategy4[2]][0]) == '0']),
            all([(field[strategy5[0]][0]) == '0', (field[strategy5[1]][0]) == '0', (field[strategy5[2]][0]) == '0']),
            all([(field[strategy6[0]][0]) == '0', (field[strategy6[1]][0]) == '0', (field[strategy6[2]][0]) == '0']),
            all([(field[strategy7[0]][0]) == '0', (field[strategy7[1]][0]) == '0', (field[strategy7[2]][0]) == '0'])]):

            # Вместо этой большой конструкции конкретно здесь можно было бы написать
            # if all([(field[y[0]][0]) == '0', (field[y[1]][0]) == '0', (field[y[2]][0]) == '0'])
            # Но, если бы компьтер выбрал "рандомную" стратегию, то y - остался бы None, и была бы ошибка

            a = input('\n' 'You lose' '\n' '\n' 'Do you want to play again? (y/n): ')
            if a == 'y':
                return game()
            break

game()

