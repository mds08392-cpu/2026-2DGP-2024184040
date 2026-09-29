from pico2d import *

open_canvas()

character = load_image('character_hero.png')

clear_canvas()
character.clip_draw(0, character.h - 140, 100, 140, 400, 300, 300, 420)
update_canvas()

delay(3)
close_canvas()