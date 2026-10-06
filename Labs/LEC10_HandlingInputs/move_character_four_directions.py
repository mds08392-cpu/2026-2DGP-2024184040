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
FRAME_DELAY = 0.05  # 프레임 간격(초)
SPEED = 10  # 한 프레임당 이동 거리(픽셀)
CANVAS_W, CANVAS_H = 1280, 1024

running = True
x, y = 640, 512  # 캐릭터 위치
frame = 0
dir_x, dir_y = 0, 0  # 방향키로 정해지는 이동 방향 (-1, 0, 1)
face_dir = 1  # 바라보는 방향 (1: 오른쪽, -1: 왼쪽)


def handle_events():
    global running, dir_x, dir_y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


while running:
    clear_canvas()
    background.draw(640, 512)
    if dir_x != 0 or dir_y != 0:
        row = ROW_RUN_RIGHT if face_dir > 0 else ROW_RUN_LEFT  # 이동 중에는 이동 애니메이션
    else:
        row = ROW_IDLE_RIGHT if face_dir > 0 else ROW_IDLE_LEFT  # 마지막으로 바라본 방향의 IDLE
    character.clip_draw(frame * CELL, row, CELL, CELL, x, y)
    update_canvas()

    handle_events()
    if dir_x != 0:
        face_dir = dir_x  # 좌우로 움직일 때만 바라보는 방향이 바뀐다
    x += dir_x * SPEED
    y += dir_y * SPEED
    x = max(CELL // 2, min(x, CANVAS_W - CELL // 2))  # 좌우 경계에서 멈춤
    frame = (frame + 1) % FRAME_COUNT
    delay(FRAME_DELAY)

close_canvas()
