from pico2d import *

open_canvas(1280, 1024)

background = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

# animation_sheet.png: 칸 100 x 100, 한 행에 8프레임 (y는 이미지 아래쪽 기준)
CELL = 100
FRAME_COUNT = 8
ROW_IDLE_RIGHT = 300
ROW_IDLE_LEFT = 200
ROW_RUN_RIGHT = 100
ROW_RUN_LEFT = 0

running = True
x, y = 640, 512  # 캐릭터 위치
frame = 0


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


while running:
    clear_canvas()
    background.draw(640, 512)
    character.clip_draw(frame * CELL, ROW_IDLE_RIGHT, CELL, CELL, x, y)
    update_canvas()

    handle_events()
    frame = (frame + 1) % FRAME_COUNT
    delay(0.05)

close_canvas()
