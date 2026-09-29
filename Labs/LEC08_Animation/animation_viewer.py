from pico2d import *

open_canvas()

background = load_image('background_black.png')

hero_walk_left = load_image('hero_walk_left.png')
hero_walk_right = load_image('hero_walk_right.png')
hero_attack_left = load_image('hero_attack_left.png')
hero_attack_right = load_image('hero_attack_right.png')

background.draw(400, 300)
update_canvas()
delay(3)

close_canvas()