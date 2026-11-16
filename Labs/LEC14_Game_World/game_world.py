# world = [] #일차원 리스트
world = [ [], [] ]

def add_object(o,depth = 0): #depth = 0 기본값 즉 0 번 레이어에 추가
    world[depth].append(o)

#게임 월드에 객체 추가 layer 을 지정
def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return # 더 이상 찾을 필요가 없기 때문에 리턴으로 종료

# 게임로직
def update():
    for layer in world:
        for o in layer[:]:  # 복사본 순회 (update 중 remove_object 안전)
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()
