from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_file('design.kv')

Window.size = (500, 700)


class Bullet(Widget):
    continue_on = True

    def move_up(self, *args):
        if self.parent:
            self.animation_up = Animation(x=self.pos[0], y=self.parent.height, duration=0.75)
            self.animation_up.bind(on_complete=self.remove_bullet)
            #self.animation_up.bind(on_progress=self.on_travel)
            self.animation_up.start(self)

    def remove_bullet(self, *args):
        if self.parent:
            self.parent.bullet_on_screen = False
            del self.parent.array_of_bullets[0]
            self.parent.remove_widget(self)


class Player(Widget):
    pass


class Game(Widget):
    travel_direction = 'right'
    bullet_on_screen = False
    array_of_bullets = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self) 
        self._keyboard.bind(on_key_down=self.on_key_down) #เชื่อมกับคีย์บอร์ด
        self._keyboard.bind(on_key_up=self.on_key_up) #เชื่อมกับคีย์บอร์ด
        self.pressed_keys = set()
        Clock.schedule_interval(self.process_keys, 0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers): #กดคีย์บอร์ด
        self.pressed_keys.add(keycode[1])

    def on_key_up(self, keyboard, keycode): #ไม่กดคีย์บอร์ด
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])

    def process_keys(self, dt): #เลื่อนซ้ายขวา
        cur_x = self.player.x
        step = 300 * dt #ปรับความเร็ว

        if self.pressed_keys.issuperset({'a'}):
            print('a')
            cur_x -= step
        if self.pressed_keys.issuperset({'d'}):
            print('d')
            cur_x += step

        if self.pressed_keys.issuperset({'spacebar'}):
            print('spacebar')
            if not self.bullet_on_screen:
                new_bullet = Bullet()

                self.add_widget(new_bullet)
                new_bullet.size = (self.parent.size[0] / 60, self.parent.size[0] / 16)
                new_bullet.pos = (self.player.pos[0] + self.player.size[0] / 2 - (self.parent.size[0] / 160),
                                self.player.pos[1] + self.player.size[1]) 
                self.array_of_bullets.append(new_bullet)
                new_bullet.move_up()
                self.bullet_on_screen = True

        self.player.x = cur_x

class SpaceInvadersApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    SpaceInvadersApp().run()