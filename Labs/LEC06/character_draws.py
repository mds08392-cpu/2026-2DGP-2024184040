# 실습 과제 진행
from pico2d import *
import math
#매천음 해야할 작업
open_canvas(800, 600)
character = load_image('character.png')

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.01)
def draw_top():
    for x in range(50, 751, 5):
        draw_character(x, 550)

def draw_right():
    for y in range(551, 50, -5):
        draw_character(751, y)

def draw_bottom():
    for x in range(751 , 50, -5):
        draw_character(x,50)
        
def draw_left():
    for y in range(50, 551, 5):
        draw_character(50, y)

def drawSide(start,end):
    t = 0
    x0 = start[0]
    x1 = end[0]
    y0 = start[1]
    y1 = end[1]
    while t <= 1:
        x0 = x0 + (x1 - x0) * t
        y0 = y0 + (y1 - y0) * t
        t += 1 / 100
        draw_character(x0,y0)

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x,y)

def move_rectangle():
    draw_top()
    draw_right()
    draw_bottom()
    draw_left()

def move_triangle():
    A = (100,100)
    B = (700,100)
    C = (400,500)
    drawSide(A,B)
    drawSide(B,C)
    drawSide(C,A)
    pass

while True:
    #move_circle()
    #move_rectangle()
    move_triangle()
    pass
close_canvas()