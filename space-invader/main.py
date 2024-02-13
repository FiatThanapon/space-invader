from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder

class Player(Widget):
    pass

class SpaceGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self) 
        self._keyboard.bind(on_key_down=self.on_key_down) #เชื่อมกับคีย์บอร์ด
        self._keyboard.bind(on_key_up=self.on_key_up) #เชื่อมกับคีย์บอร์ด
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers): #กดคีย์บอร์ด
        self.pressed_keys.add(keycode[1])

    def on_key_up(self, keyboard, keycode): #ไม่กดคีย์บอร์ด
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])

    def move_step(self, dt): #เลื่อนซ้ายขวา
        cur_x = self.player.x
        step = 300 * dt #ปรับความเร็ว

        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step

        self.player.x = cur_x

class SpaceInvadersApp(App):
    def build(self):
        return SpaceGame()

if __name__ == '__main__':
    Builder.load_file('design.kv')
    SpaceInvadersApp().run()
