from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_file('design.kv')

Window.size = (500, 700)

def collides(rect1, rect2):
    r1x, r1y = rect1[0]
    r2x, r2y = rect2[0]
    r1w, r1h = rect1[1]
    r2w, r2h = rect2[1]

    return r1x < r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2h

class Alien(Widget):
    pass

class Bullet(Widget):
    continue_on = True

    def move_up(self, *args):
        if self.parent:
            self.animation_up = Animation(x=self.pos[0], y=self.parent.height, duration=0.75)
            self.animation_up.bind(on_complete=self.remove_bullet)
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
        self._keyboard.bind(on_key_down=self.on_key_down)
        self._keyboard.bind(on_key_up=self.on_key_up)
        self.pressed_keys = set()
        self.create_aliens()
        Clock.schedule_interval(self.process_keys, 0)

    def create_aliens(self):
        x_spacing_between_aliens = self.width / 1.1
        y_start = self.height + 500
        x_start = self.width + 300
        y_spacing_between_aliens = self.height / 2

        for x in range(5):
            for y in range(5):
                new_alien = Alien()
                new_alien.size = (self.width / 1.5, self.width / 2)
                new_alien.pos = (x_start - x * x_spacing_between_aliens, y_start - y * y_spacing_between_aliens)
                self.array_of_aliens.append(new_alien)
                self.add_widget(new_alien)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])

    def on_key_up(self, keyboard, keycode):
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])

    def process_keys(self, dt):
        cur_x = self.player.x
        step = 300 * dt

        if self.pressed_keys.issuperset({'a'}):
            cur_x = max(cur_x - step, 0)

        if self.pressed_keys.issuperset({'d'}):
            cur_x = min(cur_x + step, self.width - self.player.width)

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
        for i in range(1, 4):
            new_life = Life()
            new_life.size = (Window.width / 15, Window.width / 15)
            new_life.pos = (Window.width - (i * Window.width / 15) - (i * spacing), Window.height - Window.width / 15)
            self.array_of_lives.append(new_life)
            self.add_widget(new_life)

class SpaceInvadersApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    SpaceInvadersApp().run()
