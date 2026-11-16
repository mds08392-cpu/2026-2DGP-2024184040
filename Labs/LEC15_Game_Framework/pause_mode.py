from pico2d import *
import game_framework
import game_world

image = None


def init():
    global image
    image = load_image('pause.png')


def finish():
    global image
    del image


def update():
    pass


def render():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()


def pause():
    pass


def resume():
    pass
