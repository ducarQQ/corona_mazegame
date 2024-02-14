#話題：コロナウイルス感染者が今病院にいます。でも薬まだありません。
#医者さんが薬を探しに行きます。でも、今コロナウイルスが流行っているので、
# ウイルスに近づいたら感染されると失敗です。逆に、薬を取れて、患者さん
# を助けられたら、成功になります。

#import
import pgzrun
#mapを作る
TILE_SIZE = 64
WIDTH = TILE_SIZE * 15
HEIGHT = TILE_SIZE * 15
tiles = ['floor', 'wall', 'patient', 'door', 'medical']
unlock = 0
#maze
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 4, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 2, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 3, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
#doctor、covidの配置
doctor = Actor("doctor", anchor=(0, 0), pos=(7 * TILE_SIZE, 7 * TILE_SIZE))
covid = Actor("covid", anchor=(0, 0), pos=(9 * TILE_SIZE, 6 * TILE_SIZE))
covid.yv = -1
def draw():
    screen.clear()
    for y in range(15):
        for x in range(15):
            screen.blit(tiles[maze[y][x]], (x * TILE_SIZE, y * TILE_SIZE))
    doctor.draw()
    covid.draw()
#doctor,covid を動かす
def on_key_down(key):
    
    row = int(doctor.y / TILE_SIZE)
    column = int(doctor.x / TILE_SIZE)
    
    if key == keys.UP:
        row = row - 1
    if key == keys.DOWN:
        row = row + 1
    if key == keys.LEFT:
        column = column - 1
    if key == keys.RIGHT:
        column = column + 1

    tile = tiles[maze[row][column]]
    if tile == 'floor':
        doctor.x = column * TILE_SIZE
        doctor.y = row * TILE_SIZE
#薬を探す、あったらドアを開けられる    
    global unlock
    if tile == 'patient':
        print("成功")
        exit()
    elif tile == 'medical':
        unlock = unlock + 1
        maze[row][column] = 0 #floor
    elif tile == 'door' and unlock > 0:
        unlock = unlock - 1
        maze[row][column] = 0 #floor

# covidに逃げよう、近づいたら感染される
    row = int(covid.y / TILE_SIZE)
    column = int(covid.x / TILE_SIZE)
    row = row + covid.yv
    tile = tiles[maze[row][column]]
    if not tile == 'wall':
        x = column * TILE_SIZE
        y = row * TILE_SIZE
        animate(covid, duration=0.1, pos=(x, y))
    else:
        covid.yv = covid.yv * -1
    if covid.colliderect(doctor):
        print("感染された")
        exit()

pgzrun.go()