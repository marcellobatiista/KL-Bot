import json
import pyautogui
import pydirectinput

from pynput.keyboard import Key, Listener


class ConfigJSON:
    config = None

    def __init__(self):
        self.load()

    def load(self):
        try:
            self.config = json.load(open('hunt.json'))
        except FileNotFoundError:
            self.config = {
                'map_1': {
                    'way': []
                }
            }

    def add_way(self, x, y):
        map_1 = self.config['map_1']['way']

        if len(map_1) == 0:
            map_1.append([0, 0])

        last_way = map_1[-1]
        map_1.append([last_way[0] + x, last_way[1] + y])

        self.config['map_1']['way'] = map_1

    def read_way(self):
        return self.config['map_1']['way']

    def save_way(self):
        try:
            self.config['map_1']['way'].remove([0, 0])
        except ValueError:
            pass

        with open('hunt.json', 'w') as file:
            json.dump(self.config, file, indent=4)


class CaveBot(ConfigJSON):
    top_map = None
    bottom_map = None
    right_map = None
    left_map = None

    py_direct_input = pydirectinput

    def __init__(self, kakelebot):
        super().__init__()

        self.kakeleBot = kakelebot

        self.largura_init_map = self.kakeleBot.KAKELE.width - 166
        self.altura_init_map = 31
        self.largura_max_map = self.altura_max_map = 150

        self.local_event_move()

        self.way = self.read_way()
        self.index_way = 0

        self.thread_waypoint = None
        self.thread_loadway = None

    async def auto_walk(self):
        await self.kakeleBot.sleep_bot()

        while self.thread_loadway:
            self.index_way = 0
            while self.index_way < len(list(self.way)) and self.thread_loadway:

                x, y = self.way[self.index_way][0], self.way[self.index_way][1]
                an_x, an_y = self.way[self.index_way - 1][0], self.way[self.index_way - 1][1]

                if x == an_x:
                    if y <= an_y:
                        await self.walk_and_check_wall('up')
                    elif y >= an_y:
                        await self.walk_and_check_wall('down')
                elif y == an_y:
                    if x >= an_x:
                        await self.walk_and_check_wall('right')
                    elif x <= an_x:
                        await self.walk_and_check_wall('left')

                self.index_way = self.index_way + 1

    async def walk_and_check_wall(self, key):
        wall = {'up': self.bottom_map,
                'down': self.top_map,
                'right': self.left_map,
                'left': self.right_map}

        screen_map = pyautogui.screenshot(region=wall[key])
        pydirectinput.press(key)
        pos = pyautogui.locateOnScreen(screen_map)

        if pos is not None:
            await self.kakeleBot.sleep_bot()
            await self.walk_and_check_wall(key)
        else:
            self.way = self.read_way()

    def on_release(self, key):
        if key == Key.left:
            self.add_way(-1, 0)
        elif key == Key.right:
            self.add_way(1, 0)
        elif key == Key.up:
            self.add_way(0, -1)
        elif key == Key.down:
            self.add_way(0, 1)

        if key == Key.esc:
            return False

    def start_way(self):
        with Listener(on_release=self.on_release) as listener:
            listener.join()

    def local_event_move(self):
        vertical = self.altura_max_map / 2
        horizontal = self.largura_max_map / 2

        self.top_map = (self.largura_init_map, self.altura_init_map, self.largura_max_map, vertical)
        self.bottom_map = (self.largura_init_map, vertical + self.altura_init_map, self.largura_max_map, vertical)
        self.right_map = (self.largura_init_map + horizontal, self.altura_init_map, horizontal, self.altura_max_map)
        self.left_map = (self.largura_init_map, self.altura_init_map, horizontal, self.altura_max_map)

# cb = CaveBot()
# cb.auto_walk()
# cb.start_way()
# cb.save_way()
