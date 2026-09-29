from pico2d import *

open_canvas()

background = load_image('background_black.png')

background.draw(400, 300)
update_canvas()
delay(3)

close_canvas()