from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
import random
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.graphics import Rectangle
Builder.load_file('design.kv')

Window.size = (500, 700)

class GameScreen(Screen):
    pass

class SecondScreen(Screen):

    def game_reset(self, *args):
        third_screen = self.manager.get_screen('third')
        third_screen.reset()
        game_screen = self.manager.get_screen('game')
        my_game = game_screen.children[0]
        my_game.reset()
        self.parent.current = 'game'

class ThirdScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.consec_wins = 0
        self.streak_label = Label(text=f"WINNING: {self.consec_wins}",font_size=(Window.width/20),color=(255 / 255, 232 / 255, 31 / 255, 1),\
                             pos_hint={'center_x': 0.3, 'center_y': 0.95},font_name="font/starwars_font")

        self.add_widget(self.streak_label)

    def reset(self,*args):
        self.consec_wins = 0

    def game_reset(self, *args):
        game_screen = self.manager.get_screen('game')
        my_game = game_screen.children[0]
        my_game.reset()
        self.parent.current = 'game'

    def on_pre_enter(self):
        self.consec_wins += 1

        self.streak_label.text = f"WINNING: {self.consec_wins}"

class Life(Widget):
    pass

class Player(Widget):
    pass

class Explosion(Widget):

    def sequence_of_sprites(self, *args):
        self.animation_stage_1 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_1.bind(on_complete=self.animation_stage2)
        self.animation_stage_1.start(self)

    def animation_stage2(self, *args):
        with self.canvas:
            Rectangle(source='image/second_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_2 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_2.bind(on_complete=self.animation_stage3)
        self.animation_stage_2.start(self)

    def animation_stage3(self, *args):
        with self.canvas:
            Rectangle(source='image/third_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_3 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_3.bind(on_complete=self.animation_stage4)
        self.animation_stage_3.start(self)

    def animation_stage4(self, *args):
        with self.canvas:
            Rectangle(source='image/fourth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_4 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_4.bind(on_complete=self.animation_stage5)
        self.animation_stage_4.start(self)

    def animation_stage5(self, *args):
        with self.canvas:
            Rectangle(source='image/fifth_stage_2.png', size=(self.size), pos=(self.pos))
        self.animation_stage_5 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_5.bind(on_complete=self.animation_stage6)
        self.animation_stage_5.start(self)

    def animation_stage6(self, *args):
        with self.canvas:
            Rectangle(source='image/sixth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_6 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_6.bind(on_complete=self.animation_stage7)
        self.animation_stage_6.start(self)

    def animation_stage7(self, *args):
        with self.canvas:
            Rectangle(source='image/seventh_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_7 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_7.bind(on_complete=self.animation_stage8)
        self.animation_stage_7.start(self)

    def animation_stage8(self, *args):
        with self.canvas:
            Rectangle(source='image/eigth_stage_2.PNG', size=(self.size), pos=(self.pos))
        self.animation_stage_8 = Animation(x=self.pos[0], y=self.pos[1], duration=0.01)
        self.animation_stage_8.bind(on_complete=self.remove_explosion_object)
        self.animation_stage_8.start(self)

    def remove_explosion_object(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Missile(Widget):
    def move_down(self, *args):
        self.animation_down = Animation(x=self.pos[0], y=-self.size[1], duration=2)
        self.animation_down.bind(on_progress=self.on_route)
        self.animation_down.bind(on_complete=self.remove_missile)
        self.animation_down.start(self)

    def on_route(self, *args):
        go_on = True
        if go_on:
            if self.parent:
                if self.parent.array_of_bullets != []:
                    for bullet in self.parent.array_of_bullets:
                        if self.collide_widget(bullet):

                            position_in_array = self.parent.array_of_bullets.index(bullet)
                            del self.parent.array_of_bullets[position_in_array]
                            self.parent.bullet_on_screen = False
                            self.parent.remove_widget(bullet)
                            self.animation_down.stop(self)
                            go_on = False

        if go_on:
            if self.parent:
                if self.collide_widget(self.parent.player):
                    new_explosion = Explosion()
                    new_explosion.size = (self.parent.player.size[0], self.parent.player.size[1])
                    new_explosion.pos = (
                    self.parent.player.pos[0], self.parent.player.pos[1] + self.parent.player.size[1] / 2)
                    self.parent.add_widget(new_explosion)
                    new_explosion.sequence_of_sprites()
                    self.parent.number_of_lives -= 1

                    if self.parent.array_of_lives != []:
                        widget_to_remove = self.parent.array_of_lives[0]
                        self.parent.remove_widget(widget_to_remove)
                        del self.parent.array_of_lives[0]
                    self.animation_down.stop(self)

    def remove_missile(self, *args):
        if self.parent:
            self.parent.remove_widget(self)


class Alien(Widget):
    important_property = Window.width / 10

    important_array = [Window.width / 10, Window.width / 10 + Window.width / 5,
                       Window.width / 10 + 2 * Window.width / 5,
                       Window.width / 10 + 3 * Window.width / 5, Window.width / 10 + 4 * Window.width / 5]

    cols_left = 5

    def move_right_and_down(self, *args):
        new_x_position_for_invader = self.pos[0] + self.important_property
        self.animation_right_and_down = Animation(x=new_x_position_for_invader, duration=1.5)
        self.animation_right_and_down.bind(on_complete=self.intermediary_1)
        self.animation_right_and_down.start(self)

    def intermediary_1(self, *args):
        if self.parent:

            self.important_property = self.parent.leftmost_x
            for value in self.important_array:
                if value - 5 <= self.important_property <= value + 5:
                    self.important_property = value

            self.animation_down = Animation(y=self.pos[1] - self.size[1] / 2.5, duration=0.4)
            self.animation_down.bind(on_complete=self.move_left_and_down)
            self.animation_down.start(self)

    def move_left_and_down(self, *args):
        new_x_position_for_invader = self.pos[0] - self.important_property
        self.animation_left_and_down = Animation(x=new_x_position_for_invader, duration=1.5)
        self.animation_left_and_down.bind(on_complete=self.intermediary_2)
        self.animation_left_and_down.start(self)

    def intermediary_2(self, *args):
        if self.parent:

            self.important_property = Window.width - (self.parent.rightmost_x) - self.size[0]
            for value in self.important_array:
                if value - 5 <= self.important_property <= value + 5:
                    self.important_property = value

            self.animation_down = Animation(y=self.pos[1] - self.size[1] / 2.5, duration=0.4)
            self.animation_down.bind(on_complete=self.move_right_and_down)
            self.animation_down.start(self)


class Bullet(Widget):
    continue_on = True

    def move_up(self, *args):
        if self.parent:
            self.animation_up = Animation(x=self.pos[0], y=self.parent.height, duration=1.0)
            self.animation_up.bind(on_complete=self.remove_bullet)
            self.animation_up.bind(on_progress=self.on_travel)
            self.animation_up.start(self)

    def remove_bullet(self, *args):
        if self.parent:
            self.parent.bullet_on_screen = False
            del self.parent.array_of_bullets[0]
            self.parent.remove_widget(self)

    def on_travel(self, *args):
        go_on = True
        if self.parent:
            if go_on:
                for invader in self.parent.array_of_aliens:
                    if self.collide_widget(invader):
                        position_in_array = self.parent.array_of_aliens.index(invader)
                        new_explosion = Explosion()
                        new_explosion.size = (invader.size[0], invader.size[1])
                        new_explosion.pos = (invader.pos[0], invader.pos[1])
                        self.parent.add_widget(new_explosion)
                        new_explosion.sequence_of_sprites()

                        del self.parent.array_of_aliens[position_in_array]
                        self.parent.remove_widget(invader)
                        self.animation_up.stop(self)
                        go_on = False

class Game(Widget):
    travel_direction = 'right'
    bullet_on_screen = False
    array_of_bullets = []
    array_of_lives = []
    number_of_lives = 3
    array_of_aliens = []
    num_cols = 5
    laser = SoundLoader.load('sound/laser.mp3') #เปลี่ยนเสียงเลเซอร์
    bg = SoundLoader.load('sound/music.mp3') #เปลี่ยนเสียงbackground

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self) 
        self._keyboard.bind(on_key_down=self.on_key_down) #เชื่อมกับคีย์บอร์ด
        self._keyboard.bind(on_key_up=self.on_key_up) #เชื่อมกับคีย์บอร์ด
        self.pressed_keys = set()
        
        self.bg.loop = True  # Loop bg sound
        self.bg.play() #play bg sound

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
        step = 200 * dt #ปรับความเร็ว

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


    def on_size(self, *args):
        x_spacing_between_aliens = self.parent.size[1] / 10
        y_start = self.parent.size[1] - self.parent.size[1] / 12
        y_spacing_between_aliens = self.parent.size[1] / 15

        for x in range(5):
            for y in range(5):
                new_alien = Alien()
                new_alien.size = (Window.width / 10, Window.width / 10)
                new_alien.pos = (x_spacing_between_aliens * x, y_start - y * y_spacing_between_aliens)
                self.array_of_aliens.append(new_alien)

        self.player.size = (self.parent.size[0] / 6, self.parent.size[0] / 8)

        #SCHEDULING
        Clock.schedule_interval(self.process_keys, 1/60)
        Clock.schedule_interval(self.aliens_shooting, 1) #วาดกระสุน
        Clock.schedule_interval(self.check_win, 1 / 60)
        Clock.schedule_interval(self.check_loss, 1 / 60)
        Clock.schedule_interval(self.check_player_alien_collision, 1 / 60)
        Clock.schedule_interval(self.number_of_columns_left, 1 / 360)

        # ADDING ALIENS
        for invader in self.array_of_aliens:
            self.add_widget(invader)
        # STARTING THE ALIENS MOVING
        for invader in self.array_of_aliens:
            invader.move_right_and_down()
        
        # 3 MINI HEARTS REPRESENTING LIVES REMAINING
        for i in range(self.number_of_lives):
            life = Life()
            life.size = (Window.width / 20, Window.width / 20)
            life.pos = (Window.width - (i + 1) * life.size[0] - (i + 1) * (Window.width / 30), Window.height - life.size[1])
            self.array_of_lives.append(life)
            self.add_widget(life)

    def check_win(self, *args):
        if self.array_of_aliens == []:
            if self.parent.parent:
                self.parent.parent.current = 'third'

    def check_loss(self, *args):
        if self.number_of_lives <= 0:
            if self.parent.parent:
                self.parent.parent.current = 'second'

    def check_player_alien_collision(self, *args):
        for invader in self.array_of_aliens:
            if invader.pos[1] <= (self.player.pos[1] + self.player.size[1]):
                if self.parent.parent:
                    self.parent.parent.current = 'second'
    
    def number_of_columns_left(self, *args):
        if self.array_of_aliens != []:
            x_coordinates_array = []
            for invader in self.array_of_aliens:
                x_coordinates_array.append(invader.pos[0])
            x_coordinates_set = list(set(x_coordinates_array))
            x_coordinates_set = sorted(x_coordinates_set)
            self.leftmost_x = min(x_coordinates_set)
            self.rightmost_x = max(x_coordinates_set)
            columns_left = len(x_coordinates_set)
            self.num_cols = columns_left
    

    def alien_shoot_missile(self, instance):
        new_missile = Missile()

        self.add_widget(new_missile)
        new_missile.size = (self.parent.size[0] / 60, self.parent.size[0] / 10)
        new_missile.pos = (instance.pos[0] + instance.size[0] / 2 - (self.parent.size[0] / 100),
                           instance.pos[1] - (self.parent.size[0] / 20))
        new_missile.move_down()


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

    def reset(self, *args): 

        self.clear_widgets()
        self.add_widget(self.player)
        self.add_widget(self.my_label)

        self.travel_direction = 'right'
        self.bullet_on_screen = False
        self.array_of_bullets = []
        self.array_of_lives = []
        self.number_of_lives = 3
        self.array_of_aliens = []
        self.num_cols = 5
        self.laser = SoundLoader.load('sound/laser.mp3') #เปลี่ยนเสียงเลเซอร์
        self.bg = SoundLoader.load('sound/music.mp3') #เปลี่ยนเสียงbackground
    

        Clock.unschedule(self.check_win)
        Clock.unschedule(self.check_loss)
        Clock.unschedule(self.aliens_shooting)
        Clock.unschedule(self.check_player_alien_collision)
        Clock.unschedule(self.number_of_columns_left)
        Clock.unschedule(self.process_keys)

        x_spacing_between_aliens = self.parent.size[1] / 10
        y_start = self.parent.size[1] - self.parent.size[1] / 12
        y_spacing_between_aliens = self.parent.size[1] / 15

        for x in range(5):
            for y in range(5):
                new_alien = Alien()
                new_alien.size = (Window.width / 10, Window.width / 10)
                new_alien.pos = (x_spacing_between_aliens * x, y_start - y * y_spacing_between_aliens)
                self.array_of_aliens.append(new_alien)

        self.player.size = (self.parent.size[0] / 6, self.parent.size[0] / 8)       
        
        #SCHEDULING
        Clock.schedule_interval(self.process_keys, 1/60)
        Clock.schedule_interval(self.aliens_shooting, 1) #วาดกระสุน
        Clock.schedule_interval(self.check_win, 1 / 60)
        Clock.schedule_interval(self.check_loss, 1 / 60)
        Clock.schedule_interval(self.check_player_alien_collision, 1 / 60)
        Clock.schedule_interval(self.number_of_columns_left, 1 / 360)

        # ADDING ALIENS
        for invader in self.array_of_aliens:
            self.add_widget(invader)
        # STARTING THE ALIENS MOVING
        for invader in self.array_of_aliens:
            invader.move_right_and_down()
        
        # 3 MINI HEARTS REPRESENTING LIVES REMAINING
        for i in range(self.number_of_lives):
            life = Life()
            life.size = (Window.width / 20, Window.width / 20)
            life.pos = (Window.width - (i + 1) * life.size[0] - (i + 1) * (Window.width / 30), Window.height - life.size[1])
            self.array_of_lives.append(life)
            self.add_widget(life)
            
class SpaceInvadersApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(ThirdScreen(name='third'))
        return sm


        
if __name__ == '__main__':
    SpaceInvadersApp().run()