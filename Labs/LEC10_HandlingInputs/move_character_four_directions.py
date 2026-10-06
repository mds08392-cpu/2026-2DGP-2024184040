from pico2d import *

open_canvas(1280, 1024)

background = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False


clear_canvas()
background.draw(640, 512)
update_canvas()
delay(2)

close_canvas()
