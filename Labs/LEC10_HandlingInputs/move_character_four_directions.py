from pico2d import *

open_canvas(1280, 1024)

background = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

clear_canvas()
background.draw(640, 512)
update_canvas()
delay(2)

close_canvas()
