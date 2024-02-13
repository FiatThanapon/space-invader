from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
Builder.load_file('design.kv')

class main_ship(Widget):
    pass


class SpaceInvaders(App):
    def build(self):
        game = main_ship()
        return game


if __name__ == '__main__':
    SpaceInvaders().run()