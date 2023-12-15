# coding: utf8
import json

from files.games import *
import traceback


class MainQuest():
    def __init__(self):
        with open('files/data.json') as f:
            self.data = json.load(f)
        with open('files/text.txt', encoding="UTF-8") as f:
            self.text = f.read().split('\n')
        self.i_text = self.data["i_text"]
        self.level = self.data["level"]
        self.line = self.text[self.i_text]
        self.map_interval = self.data["map_interval"]
        if self.map_interval[0] == -1:
            self.map_interval[0] = 23
            for i in range(len(self.text)):
                if self.text[i] == '*map*':
                    self.map_interval.append(i)

        self.task_points_now = dict()
        self.task_points_need = dict()
        self.task_points_now['berries'], self.task_points_now['ants'], self.task_points_now['fish'], \
            self.task_points_now['fight'] = self.data["task_points_now"]
        self.task_points_need['berries'], self.task_points_need['ants'], self.task_points_need['fish'], \
            self.task_points_need['fight'] = self.data["task_points_need"]
        self.i_line = 0
        self.f_click = 0
        self.flag_continuation = 1
        self.map = Map()
        self.map.map(self.level)
        self.health_points = self.data["health"]
        self.eat_points = self.data["eat"]
        self.source = self.data["source"]
        self.end = 0
        self.f_game = 0
        self.esc = self.data["esc"]

    def on_press(self, key):
        if self.f_click == 0:
            if key.name == 'enter':
                if self.i_line >= len(self.line):
                    if self.i_text < len(self.text) - 1:
                        self.i_text += 1
                    else:
                        self.i_text -= 1
                    self.line = self.text[self.i_text]
                    self.i_line = 0
                    if self.i_text >= 23:
                        self.eat_points = 10 - int(
                            (self.i_text - self.map_interval[0]) / (self.map_interval[1] - self.map_interval[0]) * 10)
                else:
                    self.i_line = len(self.line) - 1
            elif key.name == 'esc' and not self.f_game:
                self.flag_continuation = 0
            self.f_click = 1

    def to_exit(self, x):
        print(f'\u001b[38;5;{15}нажмите Y, если хотите {x}')
        self.ans = 0
        self.f_ex = 1

        def check_y(key):
            # print(key.name.lower())
            if key.name.lower() == 'y' or key.name.lower() == 'н':
                self.ans = 1
            self.f_ex = 0

        while self.f_ex:
            keyboard.on_press(check_y)

    def play(self):
        with open('files/screensaver.txt') as screensaver:
            print(screensaver.read())
        print('                        Жизнь серого медведя                       ')
        if self.data["new_game"]:
            print('''Здравствуй, дорогой друг!
Эта история о взрослении медвежонка по имени Уэб, на долю которого выпало немало испытаний
Ты можешь преодолеть трудности вместе с ним!''')
            input(f'''\u001b[38;5;{241}minf: Для выбора варианта и продолжения текста используется кнопка Enter, для выхода кнопка Escape
Управление осуществляется клавишами со стрелками на клавиатуре и клавишами английской раскладки\u001b[38;5;{15}m''')
            self.data["new_game"] = 0

        while self.flag_continuation:

            self.t_update = time.time()
            if self.i_line < len(self.line):
                if self.line[0] == '#':
                    self.f_game = 0
                    self.level += 1
                    self.map.map(self.level)
                    clear()
                    print(f'Часть {self.level}')
                    time.sleep(2)
                    if self.i_text < len(self.text) - 1:
                        self.i_text += 1
                    self.line = self.text[self.i_text]
                    self.i_line = 0
                elif 'inf' in self.line:
                    clear()
                    print(f'\u001b[38;5;{241}m{self.line[:(self.i_line + 1)]}')
                    self.i_line += 1
                elif self.line[0] == '*':
                    self.f_game = 1
                    game_name = self.line.strip('*')
                    clear()
                    print(game_name)
                    if self.i_text < len(self.text) - 1:
                        self.i_text += 1
                    self.line = self.text[self.i_text]
                    self.i_line = 0
                    if game_name == 'map':
                        self.map_interval.pop(0)
                        self.map.clear()
                        self.map.health_points = self.health_points
                        self.map.map(self.level)
                        self.map.source = self.source
                        if self.esc == 0:
                            self.map.generate_task()
                        else:
                            self.map.task_points_need = self.task_points_need.copy()
                            self.map.task_points_now = self.task_points_now.copy()
                            self.esc = 0
                        self.map.play()

                        self.eat_points = self.map.eat_points
                        self.health_points = self.map.health_points
                        self.source = self.map.source
                        if self.map.fight_res == 1:
                            if self.eat_points < 10:
                                self.eat_points += 1
                        elif self.map.fight_res == -1:
                            if self.health_points > 1:
                                self.health_points -= 1
                            else:
                                print('Здоровье на нуле\nУеб умер')
                                self.flag_continuation = 0
                                self.end = 1
                        if self.map.flag_notify:
                            self.flag_continuation = 0
                            self.task_points_now = self.map.task_points_now.copy()
                            self.task_points_need = self.map.task_points_need.copy()
                            self.i_text -= 1
                            self.line = self.text[self.i_text]
                            self.i_line = 0
                            self.esc = 1

                    elif game_name == 'fight':
                        self.map.games['fight'].clear(self.level)
                        self.map.games['fight'].play()
                        if self.map.games['fight'].last_res == 1:
                            with open('files/win.txt') as f:
                                text = f'\u001b[38;5;{87}m'
                                for line in f:
                                    text += ''.join(
                                        map(lambda x: (x == '1') * chr(9608) + (x == '0') * ' ', line)) + '\n'
                                print(text)
                            self.line = self.line.split('/')[0]
                            if self.eat_points < 10:
                                self.eat_points += 1
                        elif self.map.games['fight'].last_res == -1:
                            with open('files/lose.txt') as f:
                                text = f'\u001b[38;5;{217}m'
                                for line in f:
                                    text += ''.join(
                                        map(lambda x: (x == '1') * chr(9608) + (x == '0') * ' ', line)) + '\n'
                                print(text)
                            self.line = self.line.split('/')[1]
                            if self.health_points > 1:
                                self.health_points -= 1
                            else:
                                print('Здоровье на нуле\nУеб умер')
                                self.flag_continuation = 0
                                self.end = 1
                        time.sleep(1)
                    else:
                        self.map.games[game_name].clear(self.level)
                        self.map.games[game_name].need_points = 10
                        self.map.games[game_name].play()
                        with open('files/done.txt') as f:
                            text = f'\u001b[38;5;{15}m'
                            for line in f:
                                text += ''.join(
                                    map(lambda x: (x == '1') * chr(9608) + (x == '0') * ' ', line)) + '\n'
                            print(text)
                        self.eat_points += int(
                            self.map.games[game_name].score / (self.map.games[game_name].need_points / 3))
                        time.sleep(1)

                elif 'gun' in self.line:
                    self.health_points -= 2
                    clear()
                    with open('files/gun.txt') as f:
                        print(f.read())
                    time.sleep(0.5)
                    clear()
                    with open('files/bang.txt', encoding='UTF-8') as f:
                        f = f.read().split()
                        i = 1
                        for _ in range(4):
                            bang = ''
                            for line in f:
                                bang += ''.join(map(lambda x: (x == '1' and i or x == '0' and not i) * chr(9608) + (
                                        x == '0' and i or x == '1' and not i) * ' ', line)) + '\n'
                            print(bang)
                            i = not i
                            time.sleep(0.15)
                            clear()
                    if self.i_text < len(self.text) - 1:
                        self.i_text += 1
                    self.line = self.text[self.i_text]
                    self.i_line = 0
                else:
                    clear()
                    print(
                        f'\u001b[38;5;{15}mздоровье {chr(9673) * self.health_points + chr(9675) * (10 - self.health_points)}')
                    print(f' сытость {chr(9673) * self.eat_points + chr(9675) * (10 - self.eat_points)}')
                    print(f'{self.line[:(self.i_line + 1)]}')
                    self.i_line += 1
                    self.f_game = 0
            self.t_update = time.time()
            while time.time() - self.t_update <= 0.05:
                pass
            self.f_click = 0
            keyboard.on_press(self.on_press)
            if self.flag_continuation == 0 and self.end != 1:
                self.to_exit('выйти')
                if not self.ans:
                    self.flag_continuation = 1
            if self.end == 1:
                self.to_exit('начать сначала')
                if self.ans:
                    self.data = {
                        "new_game": 1,
                        "i_text": 0,
                        "level": 0,
                        "task_points_need": [
                            0,
                            0,
                            0,
                            0
                        ],
                        "task_points_now": [
                            0,
                            0,
                            0,
                            0
                        ],
                        "health": 10,
                        "eat": 1,
                        "map_interval": [
                            -1
                        ],
                        "source": 0,
                        "esc": 0
                    }
                    with open('files/data.json', 'w') as f:
                        json.dump(self.data, f, ensure_ascii=False, indent=4)
                    self.__init__()
        self.data = {
            "new_game": 0,
            "i_text": self.i_text,
            "level": self.level,
            "task_points_need": [
                self.task_points_need['berries'],
                self.task_points_need['ants'],
                self.task_points_need['fish'],
                self.task_points_need['fight']
            ],
            "task_points_now": [
                self.task_points_now['berries'],
                self.task_points_now['ants'],
                self.task_points_now['fish'],
                self.task_points_now['fight']
            ],
            "health": self.health_points,
            "eat": self.eat_points,
            "map_interval": self.map_interval,
            "source": self.source,
            "esc": self.esc
        }
        with open('files/data.json', 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print('ok')
        time.sleep(2)


try:
    m = MainQuest()
    m.play()
except Exception:
    print(traceback.format_exc())
    while 1:
        pass
