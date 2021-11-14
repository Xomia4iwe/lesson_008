# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


from termcolor import cprint
from random import randint


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.mess = 0
        self.cat_food = 30

    def __str__(self):
        return '{}:В доме еды осталось {}, денег осталось {}. Беспорядка в доме {}, еды для кота {}'.format(
            self.__class__.__name__, self.food, self.money, self.mess, self.cat_food)


class Human:

    def __init__(self, name=None):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    def __str__(self):
        return 'У {}, степень сытости {}, а уровень счастья {}'.format(self.name, self.fullness, self.happiness)

    def eat(self):
        if self.house.food >= 30:
            self.fullness += 30
            self.house.food -= 30
            print('{} поел 20 еды!'.format(self.name))
        else:
            print('В Холодильнике кончилась еда!!!!')

    def pet_a_cat(self):
        self.happiness += 5
        self.fullness -= 10
        if self.happiness > 100:
            self.happiness = 100
        print('{} погладил кота!'.format(self.name))

    def go_to_house(self, house):
        self.house = house
        print('{} вьехал в дом!'.format(self.name))

    def cleaning_house(self):
        if self.house.mess > 90:
            self.happiness -= 10
            print('{} живет в грязи!'.format(self.name))
        else:
            print('{} рад(а), что чисто!'.format(self.name))

    def alive(self):
        if self.fullness <= 0 or self.happiness < 0:
            print('{} умер'.format(self.name))
            return True
        return False


class Husband(Human):

    def __init__(self, name):
        super().__init__(name)

    def act(self):
        monet = randint(1, 3)
        super().cleaning_house()
        if not super().alive():
            if self.fullness < 20:
                self.eat()
            elif self.house.money <= 100:
                self.work()
            elif self.happiness <= 50:
                self.gaming()
            elif self.happiness <= 20 and monet == 1:
                self.gaming()
            elif self.happiness <= 20 and monet == 2 or 3:
                self.pet_a_cat()
            return True
        else:
            return False

    def work(self):
        self.fullness -= 10
        self.happiness -= 20
        self.house.money += 150
        print('{} сходил на работу!'.format(self.name) if self.fullness > 0
              else '{} умер на работе!'.format(self.name))

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        if self.happiness > 100:
            self.happiness = 100
        print('{} целый день играл в WoT!'.format(self.name) if self.fullness > 0
              else '{} умер, но победил в WoT !'.format(self.name))


class Wife(Human):

    def __init__(self, name):
        super().__init__(name=name)
        self.number_fur_coats = 0

    def act(self):
        super().cleaning_house()
        if not super().alive():
            if self.fullness <= 10 and self.house.food > 0:
                self.eat()
            elif self.house.food <= 60:
                self.shopping()
            elif self.happiness <= 10 and self.house.mess >= 70:
                self.clean_house()
            elif self.house.cat_food <= 20:
                self.buy_cat_food()
            elif 50 < self.house.mess:
                self.clean_house()
            elif self.happiness <= 30 and self.house.money >= 350:
                self.buy_fur_coat()
            elif self.happiness <= 20:
                self.pet_a_cat()
            return True
        else:
            return False

    def buy_cat_food(self):
        self.fullness -= 10
        self.house.money -= 20
        self.house.cat_food += 20
        print('{} купила 20 еды коту!'.format(self.name))

    def shopping(self):
        self.fullness -= 10
        if self.house.money >= 60:
            self.house.money -= 60
            self.house.food += 60
            print('{} купила 60 еды!'.format(self.name))
        else:
            piece = self.house.money
            self.house.food += piece
            self.house.money -= piece
            print('{} купила {} еды!'.format(self.name, piece))

    def clean_house(self):
        self.fullness -= 10
        self.happiness -= 5
        self.house.mess -= 100
        if self.house.mess < 0:
            self.house.mess = 0
        print('{} убралась!'.format(self.name) if self.fullness > 0 else
              '{} умерла убираясь!')

    def buy_fur_coat(self):
        if self.house.money >= 350:
            self.fullness -= 10
            self.happiness += 60
            self.number_fur_coats += 1
            self.house.money -= 350
            if self.happiness > 100:
                self.happiness = 100
            print('{} купила шубу!'.format(self.name))
        else:
            print('{} хотела купить шубу, но денег в доме не хватает!'.format(self.name))


class Cat:
    def __init__(self, name=None):
        self.name = name
        self.fullness = 30
        self.house = None

    def __str__(self):
        return 'У {}, степень сытости {},'.format(self.name, self.fullness)

    def go_to_house(self, house):
        self.house = house
        print('Кота {} принесли в дом!'.format(self.name))

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 3)
        if self.fullness <= 10:
            self.eat()
        elif dice == 1:
            self.eat()
        elif dice == 2:
            self.sleep()
        else:
            self.soil()

    def eat(self):
        if self.house.cat_food >= 10:
            self.fullness += 20
            self.house.cat_food -= 10
            cprint('Кот {} поел'.format(self.name), color='yellow')
        else:
            cprint('У кота {} нет еды'.format(self.name), color='red')

    def sleep(self):
        self.fullness -= 10
        cprint('Кот {} спал целый день'.format(self.name), color='green')

    def soil(self):
        self.fullness -= 10
        self.house.mess += 5
        cprint('Кот {} рвал обои'.format(self.name), color='green')


class Child(Human):

    def __init__(self, name=None):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    def __str__(self):
        return super().__str__()

    def go_to_house(self, house):
        self.house = house
        print('В семье родился ребенок {}'.format(self.name))

    def act(self):
        if self.fullness <= 20:
            self.eat()
        else:
            self.sleep()

    def eat(self):
        if self.house.food >= 20:
            self.fullness += 10
            self.house.food -= 10
            cprint('{} поел 10 еды!'.format(self.name), color='green')

    def sleep(self):
        self.fullness -= 10
        return cprint('Ребенок {} спал целый день'.format(self.name), color='green')


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
murzik = Cat(name='Мурзик')
kolya = Child(name='Коля')
serge.go_to_house(home)
masha.go_to_house(home)
murzik.go_to_house(home)
kolya.go_to_house(home)

for day in range(1, 365):
    cprint('================== День {} =================='.format(day), color='red')
    home.mess += 5
    serge.act()
    masha.act()
    murzik.act()
    kolya.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(kolya, color='cyan')
    cprint(home, color='cyan')
    print('Жена купила ', masha.number_fur_coats, ' шуб')

######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
kolya = Child(name='Коля')
murzik = Cat(name='Мурзик')

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    kolya.act()
    murzik.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(kolya, color='cyan')
    cprint(murzik, color='cyan')

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')
