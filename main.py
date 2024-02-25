from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random

Builder.load_file('design.kv')

Window.size = (500, 700)

class Alien_bullet(Widget):
    def move_down(self, *args):
        self.animation_down = Animation(x=self.pos[0], y=-self.size[1], duration=2)
        self.animation_down.bind(on_progress=self.on_route)
        self.animation_down.bind(on_complete=self.remove_missile)
        self.animation_down.start(self)

    def on_route(self, *args):
        if self.parent and self.parent.array_of_bullets:
            for bullet in self.parent.array_of_bullets:
                if self.collides(bullet):
                    self.parent.array_of_bullets.remove(bullet)
                    self.parent.remove_widget(bullet)
                    self.parent.remove_widget(self)
                    return

    def remove_missile(self, *args):
        print("Removing missile")
        if self.parent and self in self.parent.array_of_alien_bullets:
            self.parent.array_of_alien_bullets.remove(self)
        if self.parent:
            self.parent.bullet_on_screen = False
            self.parent.remove_widget(self)



class Alien(Widget):
    pass


class Bullet(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.continue_on = True

    def move_up(self, *args):
        if self.parent:
            self.animation_up = Animation(x=self.pos[0], y=self.parent.height, duration=1.0) # เพิ่ม duration เพื่อไม่ให้ player ยิงได้เร็วเกินไป
            self.animation_up.bind(on_complete=self.remove_bullet)
            self.animation_up.start(self)

    def remove_bullet(self, *args):
        if self.parent:
            self.parent.bullet_on_screen = False
            self.parent.array_of_bullets.remove(self)
            self.parent.remove_widget(self)

class Player(Widget):
    pass

class Life(Widget):
    pass

class Game(Widget):
    travel_direction = 'right'
    bullet_on_screen = False
    array_of_bullets = []
    array_of_alien_bullets = [] #เพิ่มarrayของกระสุนเอเลี่ยน
    array_of_lives = []
    number_of_lives = len(array_of_lives)
    array_of_aliens = []
    laser = SoundLoader.load('sound/laser.mp3') #เปลี่ยนเสียงเลเซอร์
    bg = SoundLoader.load('sound/music.mp3') #เปลี่ยนเสียงbackground

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self) 
        self._keyboard.bind(on_key_down=self.on_key_down) #เชื่อมกับคีย์บอร์ด
        self._keyboard.bind(on_key_up=self.on_key_up) #เชื่อมกับคีย์บอร์ด
        self.pressed_keys = set()
        self.create_aliens()
        self.create_Life()
        print(self.number_of_lives)
        Clock.schedule_interval(self.process_keys, 1/60)
        Clock.schedule_interval(self.check_hero_bullet_collisions, 1/60) #เรียกใช้คำสั่งตรวจสอบว่ายิงโดนไหม
        Clock.schedule_interval(self.aliens_shooting, 1) #วาดกระสุน
        Clock.schedule_interval(self.check_alien_bullet_collisions, 1/60) #เรียกใช้คำสั่งตรวจสอบว่าโดนกระสุนเอเลี่ยนไหม
        self.bg.loop = True  # Loop bg sound
        self.bg.play() #play bg sound

    def check_loss(self, *args):
        if self.number_of_lives <= 0:
            if self.parent.parent:
                self.parent.parent.current = 'Loss'

    def create_aliens(self):
        x_spacing_between_aliens = self.width / 1.1 # ปรับระยะห่าง x
        y_start = self.height + 500 #เปลี่ยนตำแหน่ง x
        x_start = self.width + 300 #เปลี่ยนตำแหน่ง y
        y_spacing_between_aliens = self.height / 2 # ปรับระยะห่าง y

        for x in range(5): #แถวเอเลี่ยน
            for y in range(5): #หลักเอเลี่ยน
                new_alien = Alien()
                new_alien.size = (self.width / 1.5, self.width / 2) # ปรับขนาดเอเลี่ยน
                new_alien.pos = (x_start - x * x_spacing_between_aliens, y_start - y * y_spacing_between_aliens) #ตัวกำหนดตำแหน่ง
                self.array_of_aliens.append(new_alien)
                self.add_widget(new_alien)

    def create_Life(self):
        spacing = self.width / 2.5 #เปลี่ยนระยะห่าง 
        pos_y = self.width + 570 #เปลี่ยนตำแหน่ง y
        pos_x = self.width + 380 #เปลี่ยนตำแหน่ง x
        for i in range(1, 4):
            new_life = Life()
            new_life.size = (self.width / 3, self.width / 3)
            new_life.pos = (pos_x - (i * spacing), pos_y)
            self.array_of_lives.append(new_life)
            self.add_widget(new_life)
        self.number_of_lives = len(self.array_of_lives)
        return self.number_of_lives #คืนจำนวนของชีวิต
    
    def check_hero_bullet_collisions(self, dt):
        #ตรวจสอบการชนกันระหว่างกระสุนกับเอเลี่ยน
        for bullet in self.array_of_bullets:
            for alien in self.array_of_aliens:
                if self.collides(bullet, alien):
                    #ลบกระสุนและเอเลี่ยนเมื่อมันมาชนกัน
                    self.remove_widget(bullet)
                    self.array_of_bullets.remove(bullet)
                    self.remove_widget(alien)
                    self.array_of_aliens.remove(alien)
                    return  
    
    def check_alien_bullet_collisions(self, dt):
    # Check if alien bullets collide with the player
        for bullet in self.array_of_alien_bullets:
            if self and self.collides(bullet, self.player):
                self.number_of_lives -= 1
                print(self.number_of_lives)
                if self.array_of_lives:
                    Life = self.array_of_lives[-1]
                    self.remove_widget(Life)
                    del self.array_of_lives[-1]
                self.remove_widget(bullet) #ทำให้ภาพกระสุนหายไปเมื่อชน
                self.array_of_alien_bullets.remove(bullet) #ทำให้ออปเจ็คของกระสุนหายไปเมื่อชน จะไม่ทำให้เกิดการชนซ้ำ
                


    def collides(self, rect1, rect2):
        #ตรวจสอบว่า rect1 และ rect2 ทับซ้อนกันหรือไม่
        r1x, r1y = rect1.pos
        r2x, r2y = rect2.pos
        r1w, r1h = rect1.size
        r2w, r2h = rect2.size

        return r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y
    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard.unbind(on_key_up=self.on_key_up)
        self._keyboard = None

    def on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])

    def on_key_up(self, keyboard, keycode):
        if keycode[1] in self.pressed_keys:
            self.pressed_keys.remove(keycode[1])


    def process_keys(self, dt): #เลื่อนซ้ายขวา
        cur_x = self.player.x
        step = 300 * dt #ปรับความเร็ว

        if self.pressed_keys.issuperset({'a'}):
            cur_x = max(cur_x - step, 0) #ไม่เคลื่อนที่เกินขอบ

        if self.pressed_keys.issuperset({'d'}):
            cur_x = min(cur_x + step, self.width - self.player.width) #ไม่เคลื่อนที่เกินขอบ

        if self.pressed_keys.issuperset({'spacebar'}):
            if not self.bullet_on_screen:
                self.laser.play() #เล่นเสียงlaser
                new_bullet = Bullet()
                self.add_widget(new_bullet)
                new_bullet.size = (self.width / 60, self.width / 16)
                new_bullet.pos = (self.player.center_x - (self.width / 160), self.player.top)
                self.array_of_bullets.append(new_bullet)
                new_bullet.move_up()
                self.bullet_on_screen = True
        self.player.x = cur_x

        if not self.array_of_bullets:
            self.bullet_on_screen = False


    def alien_shoot_missile(self, instance):
        new_missile = Alien_bullet()

        self.add_widget(new_missile)
        new_missile.size = (self.parent.size[0] / 60, self.parent.size[0] / 10)
        new_missile.pos = (instance.pos[0] + instance.size[0] / 2 - (self.parent.size[0] / 100),
                           instance.pos[1] - (self.parent.size[0] / 20))
        new_missile.move_down() #ตรงนี้ทำให้กระสุนเอเลียนขยับ
        self.array_of_alien_bullets.append(new_missile)

    def aliens_shooting(self, *args):
        x_coordinates_array = []
        for invader in self.array_of_aliens:
            x_coordinates_array.append(invader.pos[0])

        unique_arrays_x = []
        for value in set(x_coordinates_array):
            temp_array = []
            for invader in self.array_of_aliens:
                if invader.pos[0] == value:
                    temp_array.append(invader)
            unique_arrays_x.append(temp_array)

        for group in unique_arrays_x:
            y_vals = []
            for saucer in group:
                y_vals.append(saucer.pos[1])
            lowest_y = min(y_vals)
            for saucer in group:
                chance_variable = random.randint(1, 3)
                if saucer.pos[1] == lowest_y and chance_variable == 1:
                    self.alien_shoot_missile(saucer)
                    pass

class SpaceInvadersApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    SpaceInvadersApp().run()