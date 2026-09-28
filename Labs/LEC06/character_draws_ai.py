# 실습 과제 - AI 버전 (원, 사각형, 삼각형 그리기)
from pico2d import *
import math

open_canvas(800, 600)
character = load_image('character.png')


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)


def draw_side(start, end, steps=50):
    x0, y0 = start
    x1, y1 = end
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        draw_character(x, y)


def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)


def move_rectangle():
    A = (50, 50)
    B = (750, 50)
    C = (750, 550)
    D = (50, 550)
    draw_side(A, B)
    draw_side(B, C)
    draw_side(C, D)
    draw_side(D, A)


def move_triangle():
    A = (100, 100)
    B = (700, 100)
    C = (400, 500)
    draw_side(A, B)
    draw_side(B, C)
    draw_side(C, A)


while True:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()
