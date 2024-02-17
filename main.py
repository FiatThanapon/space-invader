from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_file('design.kv')

Window.size = (500, 700)

class Alien(Widget):
    pass


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

class Life(Widget):
    pass


class Game(Widget):
    travel_direction = 'right'
    bullet_on_screen = False
    array_of_bullets = []
    number_of_lives = 3
    array_of_lives = []
    array_of_aliens = []


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self) 
        self._keyboard.bind(on_key_down=self.on_key_down) #เชื่อมกับคีย์บอร์ด
        self._keyboard.bind(on_key_up=self.on_key_up) #เชื่อมกับคีย์บอร์ด
        self.pressed_keys = set()
        self.create_aliens()
        Clock.schedule_interval(self.process_keys, 0)

    
    def create_aliens(self):
        x_spacing_between_aliens = self.width / 1.1  # ปรับระยะห่าง x
        y_start = self.height + 500 #เปลี่ยนตำแหน่ง x
        x_start = self.width + 300  #เปลี่ยนตำแหน่ง y
        y_spacing_between_aliens = self.height / 2  # ปรับระยะห่าง y

        for x in range(5):#แถวเอเลี่ยน
            for y in range(5):#หลักเอเลี่ยน
                new_alien = Alien()
                new_alien.size = (self.width / 1.5, self.width / 2)  # ปรับขนาดเอเลี่ยน
                new_alien.pos = (x_start - x * x_spacing_between_aliens, y_start - y * y_spacing_between_aliens) #ตัวกำหนดตำแหน่ง
                self.array_of_aliens.append(new_alien)
                self.add_widget(new_alien)


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
            cur_x = max(cur_x - step, 0)  # ไม่เคลื่อนที่เกินขอบ

        if self.pressed_keys.issuperset({'d'}):
            cur_x = min(cur_x + step, self.width - self.player.width)  # ไม่เคลื่อนที่เกินขอบ

        if self.pressed_keys.issuperset({'spacebar'}):
            if not self.bullet_on_screen:
                new_bullet = Bullet()

                self.add_widget(new_bullet)
                new_bullet.size = (self.width / 60, self.width / 16)
                new_bullet.pos = (self.player.center_x - (self.width / 160), self.player.top)
                self.array_of_bullets.append(new_bullet)
                new_bullet.move_up()
                self.bullet_on_screen = True

        self.player.x = cur_x

        
        spacing = Window.width / 40
        new_life_1 = Life()
        new_life_1.size = (Window.width / 15, Window.width / 15)
        new_life_1.pos = (Window.width - (3 * Window.width / 15) - (3 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_1)
        self.add_widget(new_life_1)

        new_life_2 = Life()
        new_life_2.size = (Window.width / 15, Window.width / 15)
        new_life_2.pos = (Window.width - (2 * Window.width / 15) - (2 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_2)
        self.add_widget(new_life_2)

        new_life_3 = Life()
        new_life_3.size = (Window.width / 15, Window.width / 15)
        new_life_3.pos = (Window.width - (1 * Window.width / 15) - (1 * spacing), Window.height - Window.width / 15)
        self.array_of_lives.append(new_life_3)
        self.add_widget(new_life_3)

class SpaceInvadersApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    SpaceInvadersApp().run()