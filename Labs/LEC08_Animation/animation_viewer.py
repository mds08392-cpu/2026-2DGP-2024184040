from pico2d import *

open_canvas()

background = load_image('background_black.png')

hero_walk_left = load_image('hero_walk_left.png')
hero_walk_right = load_image('hero_walk_right.png')
hero_attack_left = load_image('hero_attack_left.png')
hero_attack_right = load_image('hero_attack_right.png')

# hero_walk_right: 256x49, 4프레임(각 64x49)
WALK_FRAME_W, WALK_FRAME_H = 64, 49
WALK_FRAME_COUNT = 4
SCALE = 6

running = True
frame = 0
while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    clear_canvas()
    background.draw(400, 300)
    hero_walk_right.clip_draw(frame * WALK_FRAME_W, 0, WALK_FRAME_W, WALK_FRAME_H,
                              400, 300, WALK_FRAME_W * SCALE, WALK_FRAME_H * SCALE)
    update_canvas()

    frame = (frame + 1) % WALK_FRAME_COUNT
    delay(0.15)

close_canvas()