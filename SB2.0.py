import random

'''При написании этой программы я руководствовался правилом №1 - программа должна быть гибкой.
В моей игре настраиваемая длина поля (от 5 до 15), больше нежелательно, т.к. визуально будет тяжело играть.
Возможно играть с несколькими игроками (как ботами, так и реальными людьми), 
количество игроков так же имеет чисто визуальное ограничение. Например, если игроков будет трое, то 
рекомендованная максимальная длина поля - 10.
Есть режим игры "Команда на команду", при чем если играет несколько реальных людей - то они по умолчанию
все в одной команде, поскольку они видят поля друг друга в консоли, очевидно.
Компьютер ходит наугад до тех пор, пока не ранит корабль противника. Последующие его ходы, а так же
ходы его союзников, направлены на уничтожение раненого корабля.
'''

print('''
    Приветствуем Вас в игре Морской бой
    Формат ввода координат: x y 
    где x - номер строки
        y - номер столбца
    Желаем удачи!
''')

your_name = input('Как Вас зовут? ')
LEN_FIELD = int(input(f'{your_name}, введите длину поля (от 5 до 15): '))
NUMBERS_OF_PLAYERS = int(input('Сколько будет игроков включая Вас? (максимум 5) '))

# Размер отступа, будет использоваться при выводе информации в консоль.
SIZE_INDENT = LEN_FIELD * NUMBERS_OF_PLAYERS * 5

class GettingInfo:
    '''Экземпляр этого класса будет хранить в себе базовую информацию о игре'''
    def __init__(self):
        self.PLAYERS_LIST = []
        self.command_mode = False
        self.name_team0 = ''
        self.name_team1 = ''

    # Функция ничего не возвращает, нужна для сбора информации об игре.
    def get_game_info(self) -> None:
        player_self = Player(your_name)        # Используя ранее полученное имя, создаем экземпляр класса Player.
        self.PLAYERS_LIST.append(player_self)  # Добавляем его в список игроков.

        if NUMBERS_OF_PLAYERS == 2:            # Если играют двое, то соперник по умолчанию относится к классу Comp.
            billet = Comp(input(f'Как зовут Вашего соперника? '))
            billet.team = 1                    # Свойство .team всегда отражает принадлежность объекта к той или иной
            self.PLAYERS_LIST.append(billet)   # команде независимо от того, включен командный режим или нет.

        if NUMBERS_OF_PLAYERS > 2:
            command_mode = input('Включить режим "Команда на команду"? (да/нет) ')
            if command_mode == 'да':
                self.name_team0 = 'Орда' #input('Введите название вашей команды: ')
                self.name_team1 = 'Альянс' #input('Введите название команды соперника: ')
                self.command_mode = True
                for i in range(1, NUMBERS_OF_PLAYERS):
                    billet = input(f'Как зовут следующего игрока? ')
                    comp_or_player = input(f'{billet} - человек или компьютер? (чел/комп) ')
                    if comp_or_player == 'чел':
                        i = Player(billet)     # Если в игру вступает реальный игрок - он автоматически становится
                    else:                      # союзником игрока.
                        i = Comp(billet)
                        team = input(f'{billet} - в вашей команде? (да/нет) ')
                        if team == 'нет':      # Описан только вариант "нет", поскольку по умолчанию, при создании
                            i.team = 1         # любого игрока ему присваивается .team = 0.
                    self.PLAYERS_LIST.append(i)
            else:                              # Если выключен командный режим, то каждый играет сам за себя.
                for i in range(1, NUMBERS_OF_PLAYERS):
                    # Поскольку реальные игроки всегда играют в одной команде, то при выключенном командном режиме
                    # все соперники реального игрока это боты.
                    billet = Comp(input(f'Как зовут вышего {i}-го соперника? '))
                    billet.team = i            # Каждому присваивается уникальный номер команды.
                    self.PLAYERS_LIST.append(billet)


class Errors(Exception):
    '''Классы исключений'''
    pass

class WrongCoords(Errors):
    pass

class WrongRangeCoords(WrongCoords):
    def __str__(self):
        return f'{f"Координаты должны быть в диапазоне между 1 и {LEN_FIELD}":^{SIZE_INDENT}}'

class WrongLenCoords(WrongCoords):
    def __str__(self):
        return f'{f"Координаты должны состоять из двух чисел":^{SIZE_INDENT}}'

class WrongUniqCoords(WrongCoords):
    def __str__(self):
        return f'{f"Эти координаты уже использовались":^{SIZE_INDENT}}'


class Ship:
    '''Класс корабля, хранящий в себе список точек корабля, '''
    def __init__(self, l):
        self.l = l                             # Количество палуб корабля (длина).
        self.list_point_ship = []              # Список точек коробля на поле.


class Field:
    '''Класс игрового поля. В нем описываются все свойства всех участников игры.
    Содержит методы для создания игрового поля, методы по получению координат вокруг кораблей, метод по обработке
    входящих координат, и др. От класса Field будут наследоваться классы Player и Comp'''

    def __init__(self, name):
        self.name = name                                                       # Имя участника игры.
        self.field = [[" "] * LEN_FIELD for _ in range(LEN_FIELD)]             # Собственно само поле.

        # Доступные точки. Нужны при расстановке кораблей. Изначально = ВСЕ точки поля.
        self.available_points = [(_, __) for _ in range(LEN_FIELD) for __ in range(LEN_FIELD)]

        # Количество и размеры кораблей. Расчитывается функцией. Зависит от длины поля (LEN_FIELD).
        self.available_ships = self.calc_available_ship(LEN_FIELD)
        self.ships = []                       # Здесь будут храниться корабли участника (объекты класса Ship).

        # Список точек всех короблей участника игры. Представляет собой список из списков этих точек.
        self.list_point_ships = []
        self.team = 0                         # Номер команды участника.
        self.enemies = []                     # Список противников. Хранит объекты классов Comp и Player

        # Список из списков ходов. Индекс каждого вложенного списка соответствует индексу противника в свойстве .enemies
        self.list_moves = []

        # Список из списков уничтоженных кораблей противника. Индекс так же соотвествует индексу противника в свойстве
        # .enemies. Нужно для расчета зоны вокруг уничтоженных кораблей, для дальнейшего ее занесения в список
        # сделанных ходов, что бы впредь по этим точкам не производить выстрелы.
        self.destroyed_ship_enemies = []
        self.lose = False                     # Меняется на True в случае уничтожения всех собственных кораблей.

        # Список из полей. Каждое поле "показывается" соответствующему противнику. Такая сложность была необходима
        # что бы точки (уничтоженные/раненные/мимо) были видны только тем противникам, которые по этим точкам стреляли.
        # Так же сохранен единый порядок индексации как и в .list_moves и в .destroyed_ship_enemies.
        self.field_for_enemy = []

        # Список из списков раненых кораблей. Каждый список соответствует противнику, по кот. был произведен выстрел.
        # Нужен для расчета (при ходе бота) "добивания" раненого корабля. После ранения точка добавляется в этот список
        # по индексу противника. Следующий ход бота должен быть направлен на уничтожение раненого корабля. Бот не может
        # стрелять по другим точкам пока в списке соответсвующего противника есть хотя бы одна точка. И посему, после
        # уничтожения раненого корабля, список соотвествующего противника отчищается.
        self.injured_enemy = []

    # Добавляет в списки .list_moves, .field_for_enemy, .destroyed_ship_enemies, .injured_enemy пустые списки по
    # индексу противников из списка .enemies
    def get_enemies(self) -> None:

        # Фильтруем список всех участников игры. Остаются только те, у которых
        # номер команды не соответствует  текущему объекту.
        enemies = [i for i in judge.PLAYERS_LIST if i.team != self.team]
        self.enemies = enemies
        for i in range(len(self.enemies)):
            self.list_moves.append([])
            self.field_for_enemy.append([[" "] * LEN_FIELD for _ in range(LEN_FIELD)])
            self.destroyed_ship_enemies.append([])
            self.injured_enemy.append([])

    # Расчет доступных кораблей в зависимости от длины игрового поля.
    @staticmethod
    def calc_available_ship(LEN_FIELD) -> tuple:
        if LEN_FIELD < 8:
            return (3, 2, 2, 1, 1, 1, 1)
        elif LEN_FIELD >=8 and LEN_FIELD <= 12:
            return (4, 3, 3, 2, 2, 2, 1, 1, 1, 1)
        else:
            return (5, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1)

    # Создание корабля. Принимает в себя длину корабля.
    def create_ship(self, l) -> Ship:
        ship = Ship(l)
        self.ships.append(ship)
        return ship

    # Расчет зоны контроля (зоны в одну клетку вокруг корабля). Принимает в себя список из точек корабля.
    @staticmethod
    def zone_control(list_point) -> list:
        lst = []                              # Временный список, из него потом будут отфильтрован результат.
        result = []
        for i in list_point:                  # Для каждой точки в списке, который принимает функция в качестве
            lst.append((i[0], i[1] + 1))      # аргумента, мы находим все точки во всех направлениях. Получается, что
            lst.append((i[0] + 1, i[1] + 1))  # для каждой точки в списке расчитывается адреса еще 8 точек.
            lst.append((i[0] + 1, i[1]))
            lst.append((i[0] + 1, i[1] - 1))
            lst.append((i[0], i[1] - 1))
            lst.append((i[0] - 1, i[1] - 1))
            lst.append((i[0] - 1, i[1]))
            lst.append((i[0] - 1, i[1] + 1))
        for point in lst:                     # Затем мы фильтруем полученный список:

            # Во-перых отсекаем точки самого корабля, которые были переданы в качестве аргумента, если рассматриваемый
            # корабль НЕ однопалубный, то таких точек будет несколько. Во-вторых избегаем повторений. Ну а далее
            # просто отсекаем точки, которые выходят за пределы поля.
            if point not in list_point and point not in result:
                if point[0] >=0 and point[1] >= 0 and point[0] < LEN_FIELD and point[1] < LEN_FIELD:
                    result.append(point)
        return result

    # Здесь возвращаются координаты на север/юг/запад/восток от переданной точки. Используется при расчете хода компа.
    @staticmethod
    def cross(point) -> list:
        lst_cross = []
        lst_cross.append((point[0], point[1] + 1))
        lst_cross.append((point[0] + 1, point[1]))
        lst_cross.append((point[0], point[1] - 1))
        lst_cross.append((point[0] - 1, point[1]))
        return lst_cross

    # Данная функция находит все точки уничтоженного корабля. Это нужно для того, что бы, при уничтожении очередного
    # корабля, атакующему участнику игры, был передан список точек этого корабля. В процессе игры информация
    # о точках своего корабля уничтожается, то есть, после ранения или уничтожения корабля информация о том, какие точки
    # он занимал на поле - нигде не сохраняется. Я решил эту проблему именно таким способом не случайно.
    # Можно было просто создать дублирующий список при создании всех кораблей, и хранить эту информацию в нем, и при
    # уничтожении корабля циклом искать совпадения по последней точке (точка, после отработки которой атакуюущему
    # участнику игры приходит ответ - "убил"), и передавать данный список. Но мое решение показалось мне безопаснее.
    # Таким образом сохраняется один из главных принципов игры - защищающийся может передавать в ответ только три
    # состояния: "мимо", "ранил", "убил".
    # Функция принимает на вход точку, после обработки которой пришел ответ "убил",
    # и индекс объекта, по которому был совершен данный выстрел.
    def find_ship_points(self, point, obj_index) -> list:
        lst_destroyed_ship = [point]          # Первая точка в списке точек уничтоженного корабля собственно переданная
        cnt = 1                               # точка.
        while cnt:
            cnt = 0

            # Далее с помощью функции .cross находим точки наверх/вниз/направо/налево от Последней в списке точек
            # уничтоженного корабля. На первой итерации цикла это будет переданная точка.
            next_cross_list = self.cross(lst_destroyed_ship[-1])
                                                                    # Далее в данном списке мы будем искать совпадения
            for j in next_cross_list:                               # с точками из списка попаданий по соответсвующему
                for i in self.destroyed_ship_enemies[obj_index]:    # игроку. Найдя такое совпадение - добавляем его
                    if i == j and i not in lst_destroyed_ship:      # в список и меняем состояние счетчика на True, что
                        lst_destroyed_ship.append(j)                # бы запустилась следующая итерация цикла. Если
                        cnt += 1                                    # такого совпадения не нашлось - то мы добрались до
                                                                    # последней точки уничтоженного корабля и не меняем
                                                                    # состояние счетчика. Тем самым выходим из цикла.

        # Теперь этот список можно отправлять в функцию zone_control
        return lst_destroyed_ship

    # Эта функция рассчитывает возможные места на поле для создания корабля с длиной, переданной в качестве аргумента.
    def calc_possible_position(self, l) -> list:
        t_possible_position_list = []         # Временный список возможных позиций (списков точек).
        possible_position_list = []           # Итоговый список возможных позиций. Потом из него будет выбрана только
        result = []                           # одна позиция. И передана в result.
        if l != 1:                                              # Если длина корабля больше одной точки:
            for i, point in enumerate(self.available_points):   # Для каждой точки будет 4 возможных "направления".
                lst_east = [self.available_points[i]]           # Берем первую точку из списка доступных точек (для
                lst_south = [self.available_points[i]]          # расчета места для первого корабля это будут вообще
                lst_west = [self.available_points[i]]           # все точки поля), и добавляем ее первой (базовой) в
                lst_north = [self.available_points[i]]          # список каждого каждого из направлений
                for j in range(1, l):                           # Затем "отходим" от этой точки на количество точек
                    lst_east.append((point[0], point[1] + j))   # равному длине корабля. То есть, к первой (базовой)
                    lst_south.append((point[0] + j, point[1]))  # точке, мы последовательно прибавляем сначала одну,
                    lst_west.append((point[0], point[1] - j))   # затем другу, и так пока не дойдем до длины корабля.
                    lst_north.append((point[0] - j, point[1]))  # И так для каждого из направлений.
                t_possible_position_list.append(lst_east)     # Затем во временный список добавляем каждое направление
                t_possible_position_list.append(lst_south)
                t_possible_position_list.append(lst_west)
                t_possible_position_list.append(lst_north)
            for possible_position in t_possible_position_list:  # Далее необходимо отфильтровать временный список
                cnt = 0                                         # Нужно избавиться от тех возможных позиций, в которых:
                for j in possible_position:                     # уже есть корабли; точки находятся в зоне конроля уже
                    if j in self.available_points:              # существующих кораблей; точки выходят за пределы поля
                        cnt += 1                                # К счастью для этого достаточно лишь проверить точки
                if cnt == len(possible_position):               # на наличие их в списке доступных точек.
                    possible_position_list.append(possible_position)
            # Есле ВСЕ точки возможной позиции находятся в списке доступных точек, то мы добавляем эту позицию в уже
            # постоянный список позиций (а не временный).

            # Далее нам нужно сделать так, что бы расстановка кораблей была не только максимально непредсказуемой но и,
            # желательно, занимала как можно меньше клеток зоны контроля (это важно для победы - чем больше полностью
            # свободных точек, тем будет труднее искать противнику корабли, особенно однопалубные). Но и ставить все
            # корабли у края поля - так же не выход. Поэтому стратегия расстановки кораблей сделана такой:
            v = random.randint(1,2)           # 50 на 50 шанс того, что позиция будет выбрана либо случайным образом
            if v == 1:                        # либо с учетом наименьшей зоны контроля.
                result = random.choice(possible_position_list)
            else:
                # Здесь ключом будет индекс позиции, а его значением - количество точек зоны контроля
                zones = {}
                random.shuffle(possible_position_list)                          # Перемешиваем позиции
                for i, possible_position in enumerate(possible_position_list):  # Перебираем список позиций
                    zone_control = []
                    for j in self.zone_control(possible_position): # Перебираем точки из зоны контроля выбранной позиции
                        if j in self.available_points:             # Если точка есть в списке доступных точек, то
                            zone_control.append(j)                 # добавляем эту точку в зону контроля
                    # Здесь мы намеренно не проверяем пересечение зоны контроля одной возможной позиции с другой, так
                    # как зона контроля может пересекаться друг с другом, а вот с другими кораблями - нет. Поэтому нам
                    # было важно проверить точки зоны контроля только на наличие их в доступных.

                    zones[i] = len(zone_control)                   # После проверки добавляем информацию в словарь

                # Далее мы должны сделать так, что бы не во всех 100 процентах случаев корабли стояли у стенки, а такой
                # эффект будет если мы будем всегда выбирать позицию с наименьшей зоной конроля. Поэтому позиция
                # выбирается рандомно из первых 25 процентов.
                percent = random.randint(0, int(len(zones) / 4))

                # Наконец сортируем словарь по наименьшему значению и выбираем из него индекс выбранный выше.
                result = possible_position_list[sorted(zones.items(), key= lambda x: x[1])[percent][0]]

        if l == 1:                                                 # Если длина корабля 1 (однопалубный), то смысла в
            result = [random.choice(self.available_points)]        # поиске возмодной позиции нет. Мы просто выбираем
                                                                   # рандомно одну тчоку из списка достпынх точек.

        self.ships[-1].list_point_ship = result    # Теперь добавляем точки выбранной позиции в объект Ship
        self.list_point_ships.append(result)       # и в список точек кораблей объекта Field.
        for q in result:
            self.available_points.remove(q)        # Удаляем точки позиции из списка доступных точек.
        for w in self.zone_control(result):
             try:
                self.available_points.remove(w)    # И пытаемся удалить точки зоны контроля выбраной позиции из все того
             except ValueError:                    # же списка. "Пытаемся", потому что если точка уже удалена, а мы
                 pass                              # попытаемся ее удалить, то выйдет ошибка.
        return result

    # Функция, создающая все корабли участника игры
    def placement_ships(self) -> None:                # Проходимся циклом по списку доступных кораблей, где l это значение этого
        for l in self.available_ships:        # списка, а значения этого списка - это как раз длИны доступных кораблей.
            self.create_ship(l)               # Создаем объекты Ship
            self.calc_possible_position(l)    # Находим места на поле для данных объектов

    # Создание игрового поля
    def create_field(self) -> None:
        while True:
            try:
                self.placement_ships()        # Пытаемся создать все корабли
                for ship_points in self.list_point_ships:
                    for i, j in ship_points:
                        self.field[i][j] = '■'
                return
            except (IndexError):
                self.field = [[" "] * LEN_FIELD for _ in range(LEN_FIELD)]
                self.available_points = [(_, __) for _ in range(LEN_FIELD) for __ in range(LEN_FIELD)]
                self.ships = []
                self.list_point_ships = []
                pass
                # Данная ошибка возникает если новый корабль некуда ставить из-за того,
                # что все клетки уже заняты (список available_points пустой). В таком случае мы "обнуляем"
                # все поля класса Field и пытаемся создать игровое поле заново

    # Функция обработки входящих координат
    def input_coord(self, point) -> int:
        for i, ship in enumerate(self.list_point_ships): # Список из списка точек всех кораблей.
            for j, k in enumerate(ship):                 # В нем проходимся по каждому кораблю и если переданная точка
                if point == k:                           # совпадает с точкой из списка то
                    self.list_point_ships[i].pop(j)      # удаляем эту точку из этого списка точек корабля

                    if self.list_point_ships[i]:         # Если список точек данного корабля Не пуст, значит ранил
                        return 1                         # возвращаем 1.
                    if not self.list_point_ships[i]:     # Если список пуст, значит убил.
                        self.ships[i] = False            # Заменяем пустой список в списке кораблей на False.
                        cnt = [x for x in self.ships if not x]  # В счетчике считаем количество уничтоженных кораблей.
                        if len(cnt) == len(self.ships):         # Если уничтожены Все корабли
                            return 3                            # то возвращаем 3.
                        else:
                            return 2                            # Возвращаем 2 если уничтожены не все корабли.

        return 0         # И наконец возввращаем 0 если точек совпадений не нашлось, значит мимо.

    # Данная функция будут переопределена в дочерних классах.
    def output_coord(self):
        pass


class DemoFields:
    '''Данный класс не будет иметь своих экземпляров, он нужен для демонстрации поля в консоль'''

    # Принимает список игроков (player_list), а так же здесь регулируется опция тумана войны.
    @classmethod
    def demonstration(cls, *args, hidden_mode = False):
        for obj in args:                       # В переданных объектах
            team = ''
            if judge.command_mode:
                if obj.team == 0:              # ищем тех, кто с реальным игроком в одной команде.
                    team = judge.name_team0    # Присваиваем переменной team название команды.
                else:
                    team = judge.name_team1    # Те кто не с ним в команде, присваиванием название другой команды.

                                               # Если включен командный режим, то рядом с именем участника игры
            if judge.command_mode:             # отбражается название его команды.
                print(f'{f"{obj.name}" + "(" + team + ")":^{(LEN_FIELD * 4) + 2}}', end='       ')
            else:
                print(f'{f"{obj.name}":^{(LEN_FIELD * 4) + 2}}', end='       ')
        print('')                              # Отступы гибкие, подстраиваются под длину поля.

        for _ in range(len(args)):             # Расстановка горизонтальных чисел.
            print('   ', end='')
            for j in range(LEN_FIELD):
                print(f'{j + 1:^3} ', end='')  # Отцентровка посередине.
            print('     ', end='')             # Отступы статичны, так как здесь гибкость обеспечивает длина поля.

        for line in range(LEN_FIELD):
            print('')                          # Отрисовка самого поля. В каждом "q" (строка в консоли) последовательно
            for obj in args:                   # проходимся циклом по строке поля соответствующего объекта.

                if hidden_mode:                # Если включен туман войны
                    if not obj.team:           # и если объект в команде игрока то выводим его "обычное" поле,
                                               # со всеми кораблями и нанесенными выстрелами.
                        print(f"{line + 1:>2}| " + " | ".join(obj.field[line]) + " |     ", end='')

                    else:                      # Если объект не в команде игрока то выводим его поле для врагов.
                        print(f"{line + 1:>2}| " + " | ".join(obj.field_for_enemy[0][line]) + " |     ", end='')
                                               # Здесь индекс 0 потому что в каждом списке полей для врагов именно 0 это
                                               # индекс поля для демонстрации игроку, т.к. он первый в списке врагов.

                else:                          # Если выключен туман войны, то у всех отображается их "обычные" поля
                    print(f"{line + 1:>2}| " + " | ".join(obj.field[line]) + " |     ", end='')
        return ''                              # Отцентровка цифр по правому краю; отступы так же статичны



class Player(Field):
    '''Класс описывающий поведение реального игрока. Наследуется от класса Field, и,
     так как не имеет своего конструктора, принимает все свойства родительского класса'''

    # Функция получения исходящих координат (координат выстрела).
    def output_coord(self, enemy) -> tuple:
        while True:
            try:
                print(f'{f"Введите координаты":^{SIZE_INDENT}}')
                point = tuple(map(lambda x: int(x) - 1, input(' '*(int(SIZE_INDENT/2)-2)).split()))

                # Отлов исключений:
                if len(point) != 2:
                    raise WrongLenCoords
                if point[0] < 0 or point[0] >= LEN_FIELD or point[1] < 0 or point[1] >= LEN_FIELD:
                    raise WrongRangeCoords
                if point in self.list_moves[enemy]:
                    raise WrongUniqCoords

            except ValueError:
                print(f'{f"Координаты должны состоять из цифр":^{SIZE_INDENT}}')
                pass
            except WrongCoords as a:
                print(a)
                pass

            else:
                break
        for allies in judge.PLAYERS_LIST:       # Добавляем выбранную точку в списки всех своих союзников и в свой тоже.
            if allies.team == self.team:
                allies.list_moves[enemy].append(point)

        return point


class Comp(Field):
    '''Класс описывающий поведение бота. Так же наследует от Field все свойства'''

    # Функция поиска случайной точки.
    def random_shot(self, enemy) -> tuple:
        while True:
            try:                                         # Такая точка дожна быть в пределах поля и
                point = (random.randint(0, LEN_FIELD-1), random.randint(0, LEN_FIELD-1))
                if point in self.list_moves[enemy]:      # ее не должно быть в списке уже отработанных точек этого врага
                    raise WrongUniqCoords
            except WrongCoords:
                pass
            else:
                break
        return point

    # Проверка точки на наличие ее в пределах поля, а так же на отсутствие ее в списке уже отработанных точек.
    def check_point(self, point, enemy) -> bool:
        if point[0] < 0 or point[0] >= LEN_FIELD or point[1] < 0 or point[1] >= LEN_FIELD:
            return False
        elif point in self.list_moves[enemy]:
            return False
        else:
            return True

    # Собственно функция вывода координат выстрела. Принимает в себя индекс противника,
    # по которому будет совершаться выстрел.
    def output_coord(self, enemy) -> tuple:

        # Если список раненных кораблей противника не пустой:
        if self.injured_enemy[enemy]:

            # Если есть пока только одно попадание, то у нас не достаточно информации о том куда именно стрелять дальше
            if len(self.injured_enemy[enemy]) == 1:
                list_cross = self.cross(self.injured_enemy[enemy][0])   # Поэтому мы вызываем метод .cross
                cnt = 0                                                 # и проверяем каждую клетку с помощью метода
                for i in list_cross:                                    # .check_point.
                    if not self.check_point(i, enemy):      # Дело в том, что при игре где каждый сам за себя
                        cnt += 1                            # бывает такое, что ранил корабль противника один участник
                if cnt == 4:                                # а убил другой. Тогда нам нужно убедиться что вокруг
                    point = self.random_shot(enemy)         # этой единственной точки еще есть неизведанные точки
                    self.injured_enemy[enemy].clear()       # куда можно было бы выстрелить. Если таких точек нет
                else:                                       # значит кто то вас опередил, и нужно удалить точку из
                    while True:                             # списка раненых кораблей, и выбрать просто любую точку поля
                        point = random.choice(list_cross)   # Если неизвестная точка все же есть, то бьем туда.
                        if self.check_point(point, enemy):
                            break

            # Если в списке раненых кораблей более одной точки, то информации уже достаточно, для того
            # что бы попытаться найти следующую палубу.
            else:
                if self.injured_enemy[enemy][0][0] == self.injured_enemy[enemy][1][0]:  # Значит корабль горизонтмальный
                    east = 0                                                # Находим самую Правую точку
                    for i, j in self.injured_enemy[enemy]:
                        if j > east:
                            east = j                                        # и создаем точку с координатами
                    point = (self.injured_enemy[enemy][1][0], east + 1)     # на единицу правее
                    if not self.check_point(point, enemy):                  # Проверяем данную точку, если она не
                        west = LEN_FIELD                                    # проходит проверку, то ищем самую
                        for i, j in self.injured_enemy[enemy]:              # левую точку.
                            if j < west:
                                west = j
                        point = (self.injured_enemy[enemy][1][0], west - 1) # Проверку осущестим позже.

                else:                                # Если корабль не горизонтальный, значит он вертикальный, очевидно.
                    north = 0
                    for i, j in self.injured_enemy[enemy]:                    # По такой же схеме находим самую
                        if i > north:                                         # верхнюю и самую нижнюю точки
                            north = i
                    point = (north + 1, self.injured_enemy[enemy][1][1])
                    if not self.check_point(point, enemy):
                        south = LEN_FIELD
                        for i, j in self.injured_enemy[enemy]:
                            if i < south:
                                south = i
                        point = (south - 1, self.injured_enemy[enemy][1][1])

            # Бывает что кто-то другой добил корабль, поэтому мы проверяем полученную точку, и если она "мимо"
            # то опять же просто выбираем любые координаты и очищаем список список раненых кораблей, что бы не
            # напороться на эту же проблему в следующий раз.
            if not self.check_point(point, enemy):
                point = self.random_shot(enemy)
                self.injured_enemy[enemy].clear()

        # Если список раненых кораблей пустой, значит опять же выбираем рандомные координаты.
        else:
            point = self.random_shot(enemy)

        for allies in judge.PLAYERS_LIST:       # Добавляем выбранную точку в списки всех своих союзников и в свой тоже.
            if allies.team == self.team:
                allies.list_moves[enemy].append(point)
        return point


class Game():
    '''Класс игры. Тут описаны методы взаимодейтсвия между участниками игры'''

    # Создание игры
    def create_game(self) -> None:
        for i in judge.PLAYERS_LIST:            # Проходимся по всем участникам игры что бы:
            i.create_field()                    # создать их поля
            i.get_enemies()                     # присвоить каждому из них списки врагов.
        print(DemoFields.demonstration(*judge.PLAYERS_LIST))

    # Проверка на победителя. Будет вызываться после Каждого полного уничтожения каго-либо из участников игры.
    # Принимает в качестве аргумента объект - атакующий участник игры, который и уничтожил кого-либо.
    def check_winner(self, current) -> bool:
        win = 0
        for v in current.enemies:               # Проходимся по списку врагов
            if v.lose == True:                  # Если враг уничтожен то увеличиваем счетчик
                win += 1
        if win == len(current.enemies):         # Если длина уничтоженных врагов равна общей длине списка врагов
            if judge.command_mode:              # То выводим соответствующую информацию в консоль
                if current.team == 0:
                    print(f'{f"Команда {judge.name_team0} выиграла!!!":^{SIZE_INDENT}}''\n')
                if current.team == 1:
                    print(f'{f"Команда {judge.name_team1} выиграла!!!":^{SIZE_INDENT}}''\n')
            if not judge.command_mode:
                print(f'{f"{current.name} выиграл!!!":^{SIZE_INDENT}}''\n')
            print(f'{f"Конец игры":^{SIZE_INDENT}}')
            return True
        else:
            return False

    # Управляющая функция очереди ходов.
    def move_order(self) -> bool:
        for current in judge.PLAYERS_LIST:      # current - Текущий участник игры из списка участников.
            if current.lose == True:            # Если он уже уничтожен - переходим к следующему участнику.
                continue

            # В этом цикле текущий учатник игры должен обойти всех своих противников по очереди.
            for i, target in enumerate(current.enemies):

                # Читать как: "если хожу я или ходят на меня то"
                if current.team == 0 or target.team == 0:  # переменная index нужна для того, что бы информация
                    index = 0                              # о состоянии поля для противников вносилась именно в те
                else:                                      # поля, которые позволят нам корректно отобразить игру
                    index = i                              # с включенным туманом войны

                if target.lose == True:        # Если противник уже уничтожен - пропускаем его и переходим к следующему.
                    continue

                while True:
                    around_destroyed_ship = []
                    print(f'{f"Ходит {current.name}":^{SIZE_INDENT}}')
                    if NUMBERS_OF_PLAYERS > 2:
                        if isinstance(current, Player):
                            print(f'{f"Ваша цель - {target.name}":^{SIZE_INDENT}}')

                    coord_shot = current.output_coord(i)              # Получаем координаты выстрела.
                    if isinstance(current, Comp):
                        print(f'{f"Его цель - {target.name}":^{SIZE_INDENT}}')
                        cs_for_demo = tuple(map(lambda x: x + 1, coord_shot))

                        # Если выстрел делается по кому-то из вашей команды либо кем-то из вашей команды.
                        if not target.team or not current.team:
                            print(f'{f"Произведен выстрел по координатам: {cs_for_demo}":^{SIZE_INDENT}}')
                        input(f'{f"Для продолжения нажмите Enter":^{SIZE_INDENT}}')

                    shot = target.input_coord(coord_shot)  # Непосредственно сам выстрел происходит здесь.
                    # Переменная shot принимает в себя результат выполнения метода .input_coord.

                    # Если shot возвращает один - значит ранил.
                    if shot == 1:
                        # Добавляем выбранную точку во все  списки своих союзников и свою тоже.
                        for allies in judge.PLAYERS_LIST:
                            if allies.team == current.team:
                                allies.list_moves[i].append(coord_shot)
                                allies.injured_enemy[i].append(coord_shot)
                                allies.destroyed_ship_enemies[i].append(coord_shot)

                        # "Красим" точку "ранил" во всех полях.
                        target.field[coord_shot[0]][coord_shot[1]] = 'X'
                        target.field_for_enemy[index][coord_shot[0]][coord_shot[1]] = 'X'
                        print(DemoFields.demonstration(*judge.PLAYERS_LIST))
                        print(f'{f"-----Ранил!-----":^{SIZE_INDENT}}''\n')
                        continue  # Завершаем эту итерацию цикла и переходим к следующему ходу по ЭТОМУ же противнику.

                    # 2 - значит убил. 3 - значит полностью уничтожил противника
                    if shot == 2 or shot == 3:
                        # Добавляем выбранную точку во все  списки своих союзников и свою тоже.
                        for allies in judge.PLAYERS_LIST:
                            if allies.team == current.team:
                                allies.list_moves[i].append(coord_shot)
                                allies.injured_enemy[i].clear()
                                allies.destroyed_ship_enemies[i].append(coord_shot)

                        # Передаем в метод .zone_control в качестве аргумента найденные с помощью метода
                        # .destroyed_ship_points точки убитого корабля. Таким образом мы получаем все точки
                        # вокруг корабля и теперь можем пометить их как "мимо".
                        around_destroyed_ship = current.zone_control(current.find_ship_points(coord_shot, i))

                        for d in around_destroyed_ship:
                            for allies in judge.PLAYERS_LIST:
                                if allies.team == current.team:
                                    allies.list_moves[i].append(d)
                            # Окрашиваем зону вокруг корабля во всех полях.
                            target.field[d[0]][d[1]] = '.'
                            target.field_for_enemy[index][d[0]][d[1]] = '.'

                        # "Красим" точку "убил" во всех полях.
                        target.field[coord_shot[0]][coord_shot[1]] = 'X'
                        target.field_for_enemy[index][coord_shot[0]][coord_shot[1]] = 'X'
                        print(DemoFields.demonstration(*judge.PLAYERS_LIST))
                        print(f'{f"-----Убил!-----":^{SIZE_INDENT}}''\n')

                        # Дополнительно надо сделать проверку на победителя, если был полностью уничтожен противник.
                        if shot == 3:
                            target.lose = True              # удаляем игрока из списка игроков
                            print(f'{f"{target.name} побежден!":^{SIZE_INDENT}}''\n')

                            if self.check_winner(current):  # Проверяем на победителя
                                return False  # Возвращаем False если победитель найден.
                            break             # Ломаем цикл while и переходим к следующему врагу в цикле for

                        continue              # continue (в данном случае) сработает если shot == 2

                    # если shot взвращает 0 значит мимо.
                    if not shot:
                        if target.field[coord_shot[0]][coord_shot[1]] == ' ':
                            target.field[coord_shot[0]][coord_shot[1]] = '.'
                        target.field_for_enemy[index][coord_shot[0]][coord_shot[1]] = '.'
                        print(DemoFields.demonstration(*judge.PLAYERS_LIST))
                        print(f'{f"-----Мимо-----":^{SIZE_INDENT}}''\n')
                        break
        return True

    def start_game(self):
        self.create_game()
        while True:
            if not self.move_order():
                return ''



judge = GettingInfo()             # Объект, хранящий в себе базовые параметры игры
judge.get_game_info()             # Сбор информации о будущей партии

game = Game()
game.start_game()                 # Запуск игры

