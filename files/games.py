import random
import time
from os import system, name
import keyboard
import math


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


class MiniGame():
    def __init__(self, n):
        self.flag_continuation = 1
        self.score = 0
        self.frame_color = 15
        self.flag_update = 0
        self.game_name = ''
        self.need_points = 0
        self.n = n

    def on_press(self, key):
        if key.name == 'esc':  # and self.need_points<=self.score:
            self.flag_continuation = 0
        if key.name in ['right', 'left', 'up', 'down']:
            self.flag_update = 1
        # УБРАТЬ
        if key.name == 'd' or key.name == 'в':
            print('!!!!!!!!!!!!!!!!!!!!!!!!')
            self.score = self.need_points

    def end_play(self):
        # time.sleep(1)
        # clear()
        # with open(f'records_{self.game_name}.txt') as f:
        #     record = float(f.readline().strip())
        # file = open(f'records_{self.game_name}.txt', 'w')
        # if self.score > record:
        #     print('Новый рекорд!')
        #     record = self.score
        # print(record, file=file)
        # file.close()
        # print(f'счёт: {self.score}')
        # time.sleep(2)
        clear()

    def clear(self, n):
        self.__init__(n)


class Fish(MiniGame):

    def __init__(self, n):
        super().__init__(n)
        self.n = [4, 7, 10, 13, 16, 19][n - 1]
        self.game_map = [[(0, 0)] * (self.n * 2) for _ in range(self.n)]
        self.player_symbol = chr(9605)
        self.player_pos = 0
        self.time_update = self.time_color = time.time()
        self.game_name = 'fish'

    def on_press(self, key):
        if self.flag_update == 0:
            if key.name == 'right':
                self.player_pos = (self.player_pos + 1) % (self.n * 2)
            elif key.name == 'left':
                self.player_pos = (self.player_pos - 1) % (self.n * 2)
        super().on_press(key)

    def to_console(self, x):
        if x[0] == 0:
            return f'\u001b[38;5;{15}m '
        if x[0] == 1:
            return f'\u001b[38;5;{x[1]}m{chr(10708)}'
        return f'\u001b[38;5;{x[1]}m{chr(11517)}'

    def play(self):

        while self.flag_continuation:
            if self.need_points <= self.score:
                self.flag_continuation = 0
                continue
            self.time_sleep = time.time()
            if time.time() - self.time_update > 0.1 * ((19 - self.n) ** 0.5):
                self.time_update = time.time()
                for i in range(self.n - 1, 0, -1):
                    for j in range(self.n * 2):
                        self.game_map[i][j] = self.game_map[i - 1][j]
                point = sorted(
                    {random.randint(0, (self.n * 2) - 1) for _ in range(random.randint(0, round(self.n ** 0.5 // 2)))})
                self.game_map[0] = [(0, 0)] * (self.n * 2)
                for i in range(len(point)):
                    if random.randint(1, 3) == 1:
                        self.game_map[0][point[i]] = (1, random.choice([4, 6, 12, 14, 21, 27, 33]))
                    else:
                        self.game_map[0][point[i]] = (2, random.choice([2, 10, 22, 28, 34, 64, 58, 100]))
            clear()
            if time.time() - self.time_color >= 0.5:
                self.frame_color = 15
            desk = f'\u001b[38;5;{15}m{self.score}/{self.need_points}\n'
            desk += f'\u001b[38;5;{self.frame_color}m{chr(9556) + chr(9552) * (self.n * 2) + chr(9559)}\n\u001b[38;5;{15}m'
            desk += '\n'.join([f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m' + ''.join(
                map(self.to_console, self.game_map[i])) + f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m'
                               for i in
                               range(self.n - 1)]) + '\n'
            desk += f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m'

            for i in range(self.n * 2):
                if i in [(self.player_pos + j) % (self.n * 2) for j in range(4)]:
                    desk += f'\u001b[38;5;{15}m{self.player_symbol}'
                else:
                    desk += self.to_console(self.game_map[-1][i])

            desk += (f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m' + '\n' +
                     f'\u001b[38;5;{self.frame_color}m{chr(9562) + chr(9552) * (self.n * 2) + chr(9565)}\u001b[38;5;{15}m')
            print(desk)

            for i in range(self.n * 2):
                if i in [(self.player_pos + j) % (self.n * 2) for j in range(4)]:
                    if self.game_map[-1][i][0] != 0:
                        if self.game_map[-1][i][0] == 1:
                            self.score += 2
                            self.frame_color = 120
                            self.time_color = time.time()
                        else:
                            self.score -= 1
                            self.frame_color = 197
                            self.time_color = time.time()
                        self.game_map[-1][i] = (0, 0)

            # print()
            self.flag_update = 0
            while time.time() - self.time_sleep < 0.1:
                pass
            keyboard.on_press(self.on_press)

        super().end_play()


class Ant_npc():
    def __init__(self, x, y, color):
        self.x, self.y, self.color = x, y, color

    def update(self, x1, y1, game_map):
        if abs((x1 - self.x) ** 2 + (y1 - self.y) ** 2) < 9:
            if abs(y1 - self.y) < abs(x1 - self.x):
                self.y += 1 * int(self.y >= y1)
                self.y -= 1 * int(self.y < y1)
                if self.y <= 0:
                    self.y = 1
                elif self.y > len(game_map[0]) - 1:
                    self.y = len(game_map[0]) - 2
            else:
                self.x += 1 * int(self.x >= x1)
                self.x -= 1 * int(self.x < x1)
                if self.x <= 0:
                    self.x = 1
                elif self.x > len(game_map) - 1:
                    self.x = len(game_map) - 2

        else:
            if random.randint(0, 1):
                self.x += random.choice([-1, 1])
                if self.x <= 0:
                    self.x = 1
                elif self.x > len(game_map) - 1:
                    self.x = len(game_map) - 2
            else:
                self.y += random.choice([-1, 1])
                if self.y <= 0:
                    self.y = 1
                elif self.y > len(game_map[0]) - 1:
                    self.y = len(game_map[0]) - 2


class Ants(MiniGame):

    def __init__(self, n):
        super().__init__(n)
        self.n = [4, 7, 10, 13, 16, 19][n - 1]
        self.game_map = [[0] * (self.n * 2) for _ in range(self.n)]
        self.direction = (1, 0)
        self.player_pos = [self.n // 2, 0]
        self.ants_list = [Ant_npc(0, 0, random.choice([222, 214, 215, 216, 172, 130, 11, 3]))]
        self.time_update = self.time_color = time.time()
        self.game_name = 'ants'

    def on_press(self, key):
        if self.flag_update == 0:
            if key.name == 'up':
                self.direction = (-1, 0)
            elif key.name == 'down':
                self.direction = (1, 0)
            elif key.name == 'right':
                self.direction = (0, 1)
            elif key.name == 'left':
                self.direction = (0, -1)
        super().on_press(key)

    def to_console(self, x):
        if type(x) == int:
            if x == 0:
                return f' '
            if x == 1:
                return f'\u001b[38;5;{15}m{chr(9604)}'
        if x[0] == 2:
            return f'\u001b[38;5;{x[1]}m{chr(9670)}\u001b[38;5;{15}m'

    def play(self):

        while self.flag_continuation:
            if self.need_points <= self.score:
                self.flag_continuation = 0
                continue
            clear()
            self.time_sleep = time.time()

            if time.time() - self.time_update > 0.2 * (2 - self.n / 16):
                self.time_update = time.time()
                for i in range(len(self.ants_list)):
                    self.game_map[self.ants_list[i].x][self.ants_list[i].y] = 0
                    self.ants_list[i].update(*self.player_pos, self.game_map)
                if random.randint(0, 8) == 0 and len(self.ants_list) <= self.n:
                    self.ants_list.append(
                        Ant_npc(random.randint(0, self.n - 1), random.randint(0, (self.n * 2) - 1),
                                random.choice([222, 214, 215, 216, 172, 130, 11, 3])))
                for i in range(len(self.ants_list)):
                    self.game_map[self.ants_list[i].x][self.ants_list[i].y] = (2, self.ants_list[i].color)

            self.game_map[self.player_pos[0]][self.player_pos[1]] = 0
            self.player_pos = [(self.player_pos[0] + self.direction[0]), (self.player_pos[1] + self.direction[1])]
            self.player_pos[0] = 0 if self.player_pos[0] <= 0 else self.n - 1 if self.player_pos[0] > self.n - 1 else \
                self.player_pos[0]
            self.player_pos[1] = 0 if self.player_pos[1] <= 0 else (self.n * 2) - 1 if self.player_pos[1] > (
                    self.n * 2) - 1 else self.player_pos[1]
            ants_list_new = []
            for ant in self.ants_list:
                if ant.x == self.player_pos[0] and ant.y == self.player_pos[1]:
                    self.score += 1
                    self.frame_color = 120
                    self.time_color = time.time()
                else:
                    ants_list_new.append(ant)
            self.ants_list = ants_list_new.copy()
            self.game_map[self.player_pos[0]][self.player_pos[1]] = 1
            if time.time() - self.time_color >= 1:
                self.frame_color = 15
            desk = f'\u001b[38;5;{15}m{self.score}/{self.need_points}\n'
            desk += f'\u001b[38;5;{self.frame_color}m{chr(9556) + chr(9552) * (self.n * 2) + chr(9559)}\n\u001b[38;5;{15}m'
            desk += '\n'.join(map(lambda x: f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m' + ''.join(
                map(self.to_console, x)) + f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m',
                                  self.game_map))
            desk += '\n' + f'\u001b[38;5;{self.frame_color}m{chr(9562) + chr(9552) * (self.n * 2) + chr(9565)}\u001b[38;5;{15}m'

            print(desk)
            # print()

            self.flag_update = 0
            while time.time() - self.time_sleep < 0.1 * (2 - self.n / 16):
                pass
            keyboard.on_press(self.on_press)
        super().end_play()


class BerriesMaze(MiniGame):
    def __init__(self, n):
        super().__init__(n)
        self.n = [4, 6, 8, 10, 12, 14][n - 1]
        self.size = 2 * self.n + 1
        self.player_symbol = chr(9605)
        self.player_pos = [1, 1]
        self.game_name = 'berries'
        self.berries = []

        self.game_map = self.generate_maze()
        self.maze_for_conversion = [[0] * self.size] + self.game_map + [[0] * self.size]
        for i in range(len(self.maze_for_conversion)):
            self.maze_for_conversion[i].append(0)
            line_m = [0]
            for j in range(len(self.maze_for_conversion[i]) - 1):
                if self.maze_for_conversion[i][j] == 1 and self.maze_for_conversion[i][j + 1] == 1:
                    line_m.append(1)
                    line_m.append(1)
                elif self.maze_for_conversion[i][j]:
                    line_m.append(1)
                    line_m.append(0)
                else:
                    line_m.append(0)
                    line_m.append(0)
            self.maze_for_conversion[i] = line_m.copy()
        self.de_m = ['']

        for i in range(1, len(self.maze_for_conversion) - 1):
            for j in range(1, len(self.maze_for_conversion[i]) - 1):
                self.de_m[-1] += self.to_console(i, j)
            self.de_m.append('')

    def generate_maze(self):
        maze = [[1 for _ in range(self.size)] for _ in range(self.size)]

        for i in range(1, self.size - 1, 2):
            for j in range(1, self.size - 1, 2):
                maze[i][j] = 0

        stack = []
        visited = set()
        stack.append((1, 1))
        visited.add((1, 1))

        while stack:
            current_cell = stack[-1]
            x, y = current_cell
            neighbors = []

            if x - 2 > 0 and (x - 2, y) not in visited:
                neighbors.append((x - 2, y))
            if x + 2 < self.size - 1 and (x + 2, y) not in visited:
                neighbors.append((x + 2, y))
            if y - 2 > 0 and (x, y - 2) not in visited:
                neighbors.append((x, y - 2))
            if y + 2 < self.size - 1 and (x, y + 2) not in visited:
                neighbors.append((x, y + 2))

            if neighbors:
                next_cell = random.choice(neighbors)
                nx, ny = next_cell
                maze[(x + nx) // 2][(y + ny) // 2] = 0
                stack.append(next_cell)
                visited.add(next_cell)
            else:
                stack.pop()

        return maze

    def on_press(self, key):
        if self.flag_update == 0:
            if key.name == 'right':
                if self.game_map[self.player_pos[0]][self.player_pos[1] + 1] != 1:
                    self.player_pos[1] += 1
                elif self.player_pos[1] == self.size - 2 and self.player_pos[0] == self.size - 2:
                    self.player_pos[0] = self.player_pos[1] = 1
            elif key.name == 'left':
                if self.game_map[self.player_pos[0]][self.player_pos[1] - 1] != 1:
                    self.player_pos[1] -= 1
                elif self.player_pos[1] == 1 and self.player_pos[0] == 1:
                    self.player_pos[0] = self.player_pos[1] = self.size - 2
            elif key.name == 'up':
                if self.game_map[self.player_pos[0] - 1][self.player_pos[1]] != 1:
                    self.player_pos[0] -= 1
                elif self.player_pos[1] == 1 and self.player_pos[0] == 1:
                    self.player_pos[0] = self.player_pos[1] = self.size - 2
            elif key.name == 'down':
                if self.game_map[self.player_pos[0] + 1][self.player_pos[1]] != 1:
                    self.player_pos[0] += 1
                elif self.player_pos[1] == self.size - 2 and self.player_pos[0] == self.size - 2:
                    self.player_pos[0] = self.player_pos[1] = 1

        super().on_press(key)

    def to_console(self, i, j):
        if i in range(1, len(self.maze_for_conversion) - 1) and j in range(1, len(self.maze_for_conversion[i]) - 1):
            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9580)

            if self.maze_for_conversion[i - 1][j] == 0 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9574)
            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 0:
                return chr(9577)

            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [0, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9568)
            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 0] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9571)

            if self.maze_for_conversion[i - 1][j] == 0 and self.maze_for_conversion[i][j - 1:j + 2] == [0, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9556)
            if self.maze_for_conversion[i - 1][j] == 0 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 0] and \
                    self.maze_for_conversion[i + 1][j] == 1:
                return chr(9559)
            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [0, 1, 1] and \
                    self.maze_for_conversion[i + 1][j] == 0:
                return chr(9562)
            if self.maze_for_conversion[i - 1][j] == 1 and self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 0] and \
                    self.maze_for_conversion[i + 1][j] == 0:
                return chr(9565)

            if self.maze_for_conversion[i][j - 1:j + 2] == [1, 1, 1] or self.maze_for_conversion[i][j - 1:j + 2] == [1,
                                                                                                                     1,
                                                                                                                     0] or \
                    self.maze_for_conversion[i][j - 1:j + 2] == [0, 1, 1]:
                return chr(9552)
            if self.maze_for_conversion[i][j] == 1 and (
                    self.maze_for_conversion[i - 1][j] == 1 or self.maze_for_conversion[i + 1][j] == 1):
                return chr(9553)
        if self.maze_for_conversion[i][j] == 0:
            return ' '
        return str(self.maze_for_conversion[i][j])

    def to_color(self, x, color):
        return f'\u001b[38;5;{color}m{x}\u001b[38;5;{64}m'

    def play(self):

        while self.flag_continuation:
            if self.need_points <= self.score:
                self.flag_continuation = 0
                continue
            # print(f'\u001b[38;5;{64}m', end='')
            self.time_sleep = time.time()
            clear()
            desk = f'\u001b[38;5;{15}mОчки:{self.score}/{self.need_points}\n\u001b[38;5;{64}m'
            i = j = 0
            if random.randint(0, self.size) == 0 and len(self.berries) <= self.size // 2:
                while self.game_map[i][j] != 0 or self.player_pos[0] == i and self.player_pos[1] == j or any(
                        [i == self.berries[q][0] and j == self.berries[q][1] for q in range(len(self.berries))]):
                    i, j = random.randint(0, len(self.game_map) - 1), random.randint(0, len(self.game_map[0]) - 1)
                self.berries.append(
                    [i, j, random.choice([214, 204, 202, 198, 197, 196, 168, 166, 160, 130, 125, 124, 88, 9, 1])])
            # i = j = 0
            for i in range(1, len(self.maze_for_conversion) - 1):
                for j in range(1, len(self.maze_for_conversion[i]) - 1):
                    if (self.player_pos[1] + 1) * 2 == (j + 1) and self.player_pos[0] == i - 1:
                        desk += self.to_color(self.player_symbol, 15)
                    else:
                        f_ = 1
                        for b in self.berries:
                            if f_ and b[0] == i - 1 and (b[1] + 1) * 2 == j + 1:
                                desk += self.to_color(chr(9670), b[2])
                                f_ = 0
                        if f_:
                            desk += self.de_m[i - 1][j - 1]
                desk += '\n'

            for i in range(len(self.berries)):
                if self.berries[i][0] == self.player_pos[0] and self.berries[i][1] == self.player_pos[1]:
                    self.berries.pop(i)
                    self.score += 1
                    break

            print(desk)
            # print(f'\u001b[38;5;{15}m{self.score}/{self.need_points}')
            # print(self.player_pos, self.size, len(self.game_map), len(self.game_map[0]))

            self.flag_update = 0
            while time.time() - self.time_sleep < 0.1:
                pass
            keyboard.on_press(self.on_press)
        super().end_play()


class Fight(MiniGame):
    def __init__(self, n):
        super().__init__(n)
        self.n = 1 + 0.5 * n
        self.health_hero = self.health_enemy = 10
        self.alf = 'qwertyuiopasdfghjklzxcvbnm'
        self.ru_alf = 'йцукенгшщзфывапролдячсмить'
        self.game_name = 'fight'
        self.game_map = []
        self.flag_error = 0
        self.time_update = self.time_color = time.time()
        self.last_res = 0
        self.score = 0

    def on_press(self, key):
        if self.flag_update == 0:
            if key.name == '1':
                self.health_enemy = 0
                self.health_hero = 10
                self.flag_right = 1
            if key.name in self.alf or key.name in self.ru_alf:
                if key.name == self.letter or key.name == self.ru_letter:
                    self.health_enemy -= 1
                    self.health_hero += 1
                    self.flag_right = 1
                    self.frame_color = 120
                else:
                    self.health_enemy += 1
                    self.health_hero -= 1
                    self.flag_error = 1
                    self.frame_color = 197
            self.time_color = time.time()
            self.flag_update = 1
        # super().on_press(key)

    def to_console(self, x):
        if x == 0:
            return ' '
        if x == 1:
            return chr(9608)
        if x == 2:
            return chr(9673)
        if x == 3:
            return chr(9675)
        if x == 4:
            return chr(9680)

    def play(self):
        self.time_start = time.time()
        time_update = time.time()
        self.last_res = 0
        self.flag_right = 1
        while self.flag_continuation:
            print(f'\u001b[38;5;{15}m', end='')
            self.time_sleep = time.time()
            clear()

            if time.time() - time_update >= self.n or self.flag_error or self.flag_right:
                self.letter = random.choice(list(self.alf))
                self.ru_letter = self.ru_alf[self.alf.index(self.letter)]
                if self.flag_error == 0 and self.flag_right == 0:
                    self.health_enemy += 1
                    self.health_hero -= 1
                    self.flag_error = 1
                    self.frame_color = 197
                    self.time_color = time.time()
                self.flag_error = self.flag_right = 0
                self.game_map = [
                    [2] * (self.health_enemy // 2) + [4] * (self.health_enemy % 2) + [3] * (
                            (20 - self.health_enemy) // 2) + [0] * 10 + [2] * (self.health_hero // 2) + [4] * (
                            self.health_hero % 2) + [3] * ((20 - self.health_hero) // 2)]
                self.game_map.append([])
                i = 0
                for m in en_alf_cap[self.letter]:
                    self.game_map[-1] = [0] * 10 + m + [0] * 10
                    i += 1
                    self.game_map.append([])

                time_update = time.time()
            a = math.ceil(10 / self.n * (time.time() - time_update))
            self.game_map[-1] = [2] * a + [3] * (10 - a) + [0] * 20
            if time.time() - self.time_color >= 1:
                self.frame_color = 15

            desk = f'\u001b[38;5;{self.frame_color}m{chr(9556) + chr(9552) * (10 * 3) + chr(9559)}\n\u001b[38;5;{15}m'
            desk += '\n'.join(map(lambda x: f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m' + ''.join(
                map(self.to_console, x)) + f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m',
                                  self.game_map))
            desk += '\n' + f'\u001b[38;5;{self.frame_color}m{chr(9562) + chr(9552) * (10 * 3) + chr(9565)}\u001b[38;5;{15}m'

            # desk = '\n'.join(map(lambda x: ''.join(map(self.to_console, x)), self.game_map))
            # print(*self.game_map, sep='\n')
            # print()
            print(desk)
            # print(f'\u001b[38;5;{15}m{self.score}')

            self.flag_update = 0
            while time.time() - self.time_sleep < 0.1:
                pass
            keyboard.on_press(self.on_press)
            if self.health_enemy == 0:
                self.flag_continuation = 0
                self.last_res = 1
            elif self.health_hero == 0:
                self.flag_continuation = 0
                self.last_res = -1
        super().end_play()


class Map():
    def __init__(self):
        self.full_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1],
                         [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0],
                         [0, 3, 0, 3, 0, 4, 3, 3, 3, 4, 0, 3],
                         [0, 0, 3, 0, 3, 0, 3, 3, 0, 3, 3, 0],
                         [3, 3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 0],
                         [0, 3, 3, 3, 3, 5, 0, 3, 0, 3, 5, 0],
                         [0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0],
                         [0, 0, 0, 3, 3, 5, 0, 0, 3, 0, 3, 0],
                         [0, 5, 3, 0, 0, 3, 3, 3, 0, 4, 0, 0],
                         [0, 0, 0, 4, 0, 0, 3, 0, 3, 0, 3, 0],
                         [3, 3, 0, 0, 0, 4, 0, 3, 0, 0, 0, 3]]
        self.map_mow = []
        self.flag_continuation = 1
        self.frame_color = 15
        self.flag_update = 0
        self.time_sleep = self.time_color = time.time()
        self.player_pos = [4, 2]
        self.game_map = []
        self.choose = 0
        self.game_name = 'none'
        self.games = {'berries': BerriesMaze(1), 'ants': Ants(1), 'fish': Fish(1), 'fight': Fight(1)}
        self.fight_res = 0
        self.fight = 0
        self.eat_points = 1
        self.task_points_need = {'berries': 0, 'ants': 0, 'fish': 0, 'fight': 0}
        self.task_points_now = {'berries': 0, 'ants': 0, 'fish': 0, 'fight': 0}
        self.flag_notify = self.esc = 0

    def clear(self):
        self.flag_continuation = 1
        self.frame_color = 15
        self.flag_update = 0
        self.time_sleep = self.time_color = time.time()
        self.player_pos = [4, 2]
        self.game_map = []
        self.choose = 0
        self.game_name = 'none'
        self.fight_res = 0
        self.fight = 0
        self.eat_points = 1

    def generate_task(self):
        self.task_points_now['berries'] = 0
        self.task_points_now['ants'] = 0
        self.task_points_now['fish'] = 0
        self.task_points_now['fight'] = 0
        self.task_points_need['berries'] = self.n * random.randint(10, 30)
        self.task_points_need['ants'] = self.n * random.randint(5, 15)
        self.task_points_need['fish'] = self.n * random.randint(20, 50)
        self.task_points_need['fight'] = self.n

    def map(self, n):
        if n == 1:
            self.map_mow = []
            for i in range(8):
                self.map_mow.append([])
                for j in range(8):
                    self.map_mow[-1].append(self.full_map[i][j])
            self.player_pos = [4, 1]

        elif n == 2 or n == 3:
            self.map_mow = []
            for i in range(8):
                self.map_mow.append([])
                for j in range(4, 12):
                    self.map_mow[-1].append(self.full_map[i][j])
            self.player_pos = [4, 1]
        elif n == 4:
            self.map_mow = []
            for i in range(8):
                self.map_mow.append([])
                for j in range(12):
                    self.map_mow[-1].append(self.full_map[i][j])
            self.player_pos = [4, 1]
        elif n == 5:
            self.map_mow = []
            for i in range(8):
                self.map_mow.append([])
                for j in range(12):
                    self.map_mow[-1].append(self.full_map[i][j])
            self.map_mow[7][9] = 6
            self.player_pos = [4, 1]
        elif n == 6:
            self.map_mow = []
            for i in range(12):
                self.map_mow.append([])
                for j in range(12):
                    self.map_mow[-1].append(self.full_map[i][j])
            self.map_mow[7][9] = 6
            self.player_pos = [4, 1]
        self.n = n
        for a in self.games:
            self.games[a].clear(n)

    def to_console(self, x):
        if x == 0:
            return '  '
        elif x == 1:
            return f'\u001b[38;5;{random.choice([4, 6, 12, 21, 33, 37, 38, 39, 44, 45, 69, 75, 80, 81, 87])}m{chr(8776)} ' + f'\u001b[38;5;{15}m'
        elif x == 2:
            return 'R '
        elif x == 3:
            return f'\u001b[38;5;{random.choice([2, 22, 28])}m^ ' + f'\u001b[38;5;{15}m'
        elif x == 4:
            return 'B '
        elif x == 5:
            return 'A '
        elif x == 6:
            return 'S '
        elif x == 7:
            return 'Y '
        elif x == 8:
            return chr(9605) + ' '

    def on_press(self, key):
        self.game_map[self.player_pos[0]][self.player_pos[1]] = self.map_mow[self.player_pos[0]][self.player_pos[1]]
        if not self.flag_update:
            if key.name == 'right' and self.player_pos[1] < len(self.map_mow[0]) - 1:
                self.player_pos[1] += 1
            elif key.name == 'left' and self.player_pos[1]:
                self.player_pos[1] -= 1
            elif key.name == 'up' and self.player_pos[0]:
                self.player_pos[0] -= 1
            elif key.name == 'down' and self.player_pos[0] < len(self.map_mow) - 1:
                self.player_pos[0] += 1
            elif key.name == 'esc':
                self.flag_continuation = 0
                self.flag_notify = 1
                # if self.n == 6 and all([self.task_points_need[x]<=self.task_points_now[x] for x in self.games]):
                #     self.flag_continuation=0

            elif key.name == 'enter':
                # print('!!!!!!!!!!!!!!!!!!!!!!', self.game_map[self.player_pos[0]][self.player_pos[1]])
                self.choose = 1
            elif key.name == 'f' or key.name == 'а':
                self.fight = 1
            self.flag_update = 1

    def play(self):
        # a=self.n
        # self.__init__()
        # self.map(a)
        self.game_map = [self.map_mow[i].copy() for i in range(len(self.map_mow))]
        self.flag_notify = 0
        # self.source = 1
        while self.flag_continuation:

            # print(f'\u001b[38;5;{15}mздоровье {chr(9673) * self.health_points + chr(9675) * (10 - self.health_points)}')
            # print(f' сытость {chr(9673) * self.eat_points + chr(9675) * (10 - self.eat_points)}')

            self.time_sleep = time.time()
            clear()
            # print(*self.game_map, sep='\n')
            # print(self.player_pos[0],self.player_pos[1])
            self.game_map[self.player_pos[0]][self.player_pos[1]] = 8
            desk = f'\u001b[38;5;{15}mздоровье {chr(9673) * self.health_points + chr(9675) * (10 - self.health_points)}\n' + f' сытость {chr(9673) * self.eat_points + chr(9675) * (10 - self.eat_points)}\n'
            desk += f'\u001b[38;5;{15}m{chr(9556) + chr(9552) * (len(self.game_map[0]) * 2) + chr(9559)}\n'
            desk += '\n'.join([chr(9553) + ''.join(map(self.to_console, x)) + chr(9553) for x in self.game_map]) + '\n'
            # desk += f'\u001b[38;5;{self.frame_color}m{chr(9553)}\u001b[38;5;{15}m'
            desk += chr(9562) + chr(9552) * (len(self.game_map[0]) * 2) + chr(9565)
            # desk += chr(9553) + chr(9562) + chr(9552) * (len(self.game_map) * 2) + chr(9565)
            print(desk)
            print('Для выхода из карты завершите задание:')
            print(
                f'\u001b[38;5;{87}mЗАДАНИЕ: {", ".join([x[0] + " " + str(x[1]) for x in self.task_points_need.items()])}')
            print(
                f'\u001b[38;5;{217}mНАБРАНО: {", ".join([x[0] + " " + str(x[1]) for x in self.task_points_now.items()])}')
            print(f'\u001b[38;5;{241}minf')
            print('R - река, здесь можно ловить рыбу')
            print('B - тут белочки спрятали свои запасы: ягоды и орехи')
            print('A - муровейники')
            if self.n >= 5:
                print('S - горячий источник, дает одно очко здоровья, однако получить его можно раз в день')
            if self.choose == 1:
                if self.map_mow[self.player_pos[0]][self.player_pos[1]] in [2, 4, 5, 6, 7]:
                    # self.flag_continuation = 0
                    a = self.map_mow[self.player_pos[0]][self.player_pos[1]]
                    if a == 2:
                        self.game_name = 'fish'
                    elif a == 4:
                        self.game_name = 'berries'
                    elif a == 5:
                        self.game_name = 'ants'
                    elif a == 6:
                        self.game_name = 'source'
                        if not self.source and self.health_points < 10:
                            self.health_points += 1
                            self.source = 1
                        elif self.source:
                            print('Сегодня Уэбб уже использовал источник')
                    if a in [2, 4, 5]:
                        self.games[self.game_name].clear(self.n)
                        self.games[self.game_name].need_points = self.task_points_need[self.game_name] - \
                                                                 self.task_points_now[self.game_name]
                        self.games[self.game_name].play()
                        self.task_points_now[self.game_name] += self.games[self.game_name].score
                        self.eat_points = int(sum([self.task_points_now[x] / (self.task_points_need[x] / 3) for x in
                                                   ['berries', 'ants', 'fish']])) + 1
            if self.fight:
                self.game_name = 'fight'
                self.games[self.game_name].clear(self.n)
                self.games[self.game_name].play()
                self.fight_res = self.games[self.game_name].last_res
                if self.fight_res == 1:
                    self.task_points_now['fight'] += 1
                elif self.fight_res == -1:
                    self.health_points -= 1
                self.fight = 0
            self.flag_update = 0
            self.choose = 0
            while time.time() - self.time_sleep < 0.3:
                pass
            keyboard.on_press(self.on_press)
            if self.health_points <= 0:
                self.flag_continuation = 0
            if all([self.task_points_need[x] <= self.task_points_now[x] for x in self.games]):
                self.flag_continuation = 0

en_alf_cap = {
    'q': [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]
    ],
    'w': [
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 0]
    ],
    'e': [
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'r': [
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    ],
    't': [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    ],
    'y': [
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    ],
    'u': [
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'i': [
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
    ],
    'o': [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'p': [
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    ],
    'a': [
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    ],
    's': [
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'd': [
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ],
    'f': [
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    ],
    'g': [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'h': [
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    ],
    'j': [
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
    ],
    'k': [
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    ],
    'l': [
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'z': [
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'x': [
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0]
    ],
    'c': [
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0]
    ],
    'v': [
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    ],
    'b': [
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ],
    'n': [
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    ],
    'm': [
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1]
    ]
}
