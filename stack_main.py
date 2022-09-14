from ast import main
import pygame
import random
import os
import sys

# Global variables
fps=30
SCREENWIDTH=350
SCREENHIEGHT=650
SCREEN=pygame.display.set_mode((SCREENWIDTH, SCREENHIEGHT))
GAME_BLOCKS={}
BACKGROUND='Pic/Game.png'

def welcomeScreen():
    exit=False
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Background.mp3'))
                    pygame.mixer.music.load('Music/Background.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
                if event.key==pygame.K_h:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Navigation.wav'))
                    keys_to_use()
            else:
                with open('Hiscore.txt', 'r') as f:
                    hiscore=f.read()
                    hiscore=int(hiscore)
                SCREEN.blit(GAME_BLOCKS['welcome'], (0,0))
                SCREEN.blit(GAME_BLOCKS['score'][hiscore], (170, 412))
                pygame.display.update()
                CLOCK.tick(fps)
    pygame.quit()
    quit()

def keys_to_use():
    exit=False
    while not exit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Navigation.wav'))
                    welcomeScreen()
            else:
                SCREEN.blit(GAME_BLOCKS['keys'], (0,0))
                pygame.display.update()
                CLOCK.tick(fps)
    pygame.quit()
    quit()

def stack_master():
    exit=True
    while not exit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit=True
            else:
                SCREEN.blit(GAME_BLOCKS['winner'], (0,0))
                pygame.display.update()
                CLOCK.tick(fps)
    pygame.quit()
    quit()
'''
0=2
1=4
2=8
3=16
4=32
5=64
6=128
7=256
8=512
9=1024
10=2048
11=4096
12=8192
13=16384
'''
def gameloop():
    STACK=[
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1],
    [-1,-1,-1,-1,-1]]
    POSITIONS=[
    [(35,229), (90,229), (145,229), (200,229), (255,229)],
    [(35,285), (90,285), (145,285), (200,285), (255,285)],
    [(35,340), (90,340), (145,340), (200,340), (255,340)], 
    [(35,395), (90,395), (145,395), (200,395), (255,395)], 
    [(35,450), (90,450), (145,450), (200,450), (255,450)], 
    [(35,505), (90,505), (145,505), (200,505), (255,505)], 
    [(35,560), (90,560), (145,560), (200,560), (255,560)]]
    BLOCK_PLACED=True
    BLIT_LIST=[]
    SPEED=60
    score=0
    block_value=3
    game_exit=False
    score=3
    a=0
    b=2
    t=0
    if(not os.path.exists('Hiscore.txt')):
        with open('Hiscore.txt', 'w') as f:
            f.write('3')
    with open('Hiscore.txt', 'r') as f:
        hiscore=f.read()
        hiscore=int(hiscore)
    while not game_exit:
        if score==13:
            stack_master()
        if BLOCK_PLACED:
            value=random.randint(0,block_value)
            BLOCK_PLACED=False
        check=False
        t=t+1
        block_pos=POSITIONS[a][b]
        SCREEN.blit(GAME_BLOCKS['Game'], (0,0))
        SCREEN.blit(GAME_BLOCKS['block'][value], block_pos)
        SCREEN.blit(GAME_BLOCKS['score'][score],(140,33))
        SCREEN.blit(GAME_BLOCKS['score'][hiscore], (150, 88))
        for i in BLIT_LIST:
            SCREEN.blit(GAME_BLOCKS['block'][i[0]], i[1])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    game_exit=True
                if event.key==(pygame.K_s and pygame.K_b) and SPEED<60:
                        SPEED=SPEED+10
                if event.key==pygame.K_LEFT:
                    if b==0:
                        b=0
                    elif STACK[a][b-1]==-1:
                        b=b-1
                if event.key==pygame.K_RIGHT:
                    if b==4:
                        b=4
                    elif STACK[a][b+1]==-1:
                        b=b+1
                if event.key==pygame.K_SPACE:
                    a=drop_now(a,b,STACK)
                    if(a==0):
                        game_over(hiscore, score)
                    else:
                        STACK[a][b]=value
                        BLIT_LIST.append([value,POSITIONS[a][b]])
                        value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
                        if value>score:
                            score=value
                            if (block_value<8) and (block_value<score):
                                block_value=score
                        if (SPEED>10) and (score%2==0):
                            SPEED=SPEED-10
                        if score>int(hiscore):
                            hiscore=score
                    a=0
                    BLOCK_PLACED=True
                    check=True
        if t%SPEED==0 and (not check):
            if(a==6):
                STACK[a][b]=value
                BLIT_LIST.append([value,POSITIONS[a][b]])
                value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
                if value>score:
                    score=value
                    if (block_value<8) and (block_value<score):
                        block_value=score
                if (SPEED>10) and (score%2==0):
                    SPEED=SPEED-10
                if score>int(hiscore):
                    hiscore=score
                a=0
                BLOCK_PLACED=True
            else:
                c=drop(a,b,STACK)
                if(c==0):
                    game_over(hiscore, score)
                elif(a==c):
                    STACK[a][b]=value
                    BLIT_LIST.append([value,POSITIONS[a][b]])
                    value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
                    if value>score:
                        score=value
                        if (block_value<8) and (block_value<score):
                            block_value=score
                    if (SPEED>10) and (score%2==0):
                        SPEED=SPEED-10
                    if score>int(hiscore):
                        hiscore=score
                    a=0
                    BLOCK_PLACED=True
                else:
                    a=c
        pygame.display.update()
        CLOCK.tick(fps)
    pygame.quit()
    quit()

def drop(a,b,STACK):
    if STACK[a+1][b]==-1 and a<6:
        a=a+1
    return a

def drop_now(a,b,STACK):
    while a<6 and STACK[a+1][b]==-1:
        a=a+1
    return a

def game_over(hiscore, score):
    exit=False
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Gameover.wav'))
    pygame.mixer.music.load('Music/Gameover.wav')
    pygame.mixer.music.play()
    with open('Hiscore.txt', 'w') as f:
        f.write(str(hiscore))
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('Music/Navigation.wav'))
                    pygame.mixer.music.load('Music/Navigation.wav')
                    pygame.mixer.music.play()
                    welcomeScreen()
            else:
                SCREEN.blit(GAME_BLOCKS['gameover'], (0,0))
                SCREEN.blit(GAME_BLOCKS['score'][score], (195, 389))
                pygame.display.update()
                CLOCK.tick(fps)
    pygame.quit()
    quit()

def check_drop(a,b,POSITIONS,BLIT_LIST,STACK):
    while STACK[a-1][b]!=-1:
        value=STACK[a-1][b]
        STACK[a][b]=value
        STACK[a-1][b]=-1
        BLIT_LIST.remove([value, POSITIONS[a-1][b]])
        BLIT_LIST.append([value, POSITIONS[a][b]])
        merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
        a=a-1
    return STACK,BLIT_LIST

def merge(a, b, value, STACK, POSITIONS, BLIT_LIST):
    if(b>0 and STACK[a][b]==STACK[a][b-1]) and (b<4 and STACK[a][b]==STACK[a][b+1]) and (a<6 and STACK[a][b]==STACK[a+1][b]):
        STACK[a+1][b]=value+3
        STACK[a][b-1]=-1
        STACK[a][b+1]=-1
        STACK[a][b]=-1
        BLIT_LIST.remove([value,POSITIONS[a+1][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b-1]])
        BLIT_LIST.remove([value,POSITIONS[a][b-1]])
        BLIT_LIST.append([value+3, POSITIONS[a+1][b]])
        value=value+3
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b-1,POSITIONS,BLIT_LIST,STACK)
        STACK, BLIT_LIST=check_drop(a,b+1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a+1, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(b>0 and STACK[a][b]==STACK[a][b-1]) and (b<4 and STACK[a][b]==STACK[a][b+1]):
        STACK[a][b]=value+2
        STACK[a][b-1]=-1
        STACK[a][b+1]=-1
        BLIT_LIST.remove([value,POSITIONS[a][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b-1]])
        BLIT_LIST.remove([value,POSITIONS[a][b+1]])
        BLIT_LIST.append([value+2, POSITIONS[a][b]])
        value=value+2
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b-1,POSITIONS,BLIT_LIST,STACK)
        STACK, BLIT_LIST=check_drop(a,b+1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(b>0 and STACK[a][b]==STACK[a][b-1]) and (a<6 and STACK[a][b]==STACK[a+1][b]):
        STACK[a+1][b]=value+2
        STACK[a][b-1]=-1
        STACK[a][b]=-1
        BLIT_LIST.remove([value,POSITIONS[a+1][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b-1]])
        BLIT_LIST.remove([value,POSITIONS[a][b]])
        BLIT_LIST.append([value+2, POSITIONS[a+1][b]])
        value=value+2
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b-1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a+1, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(b<4 and STACK[a][b]==STACK[a][b+1]) and (a<6 and STACK[a][b]==STACK[a+1][b]):
        STACK[a+1][b]=value+2
        STACK[a][b+1]=-1
        STACK[a][b]=-1
        BLIT_LIST.remove([value,POSITIONS[a+1][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b+1]])
        BLIT_LIST.remove([value,POSITIONS[a][b]])
        BLIT_LIST.append([value+2, POSITIONS[a+1][b]])
        value=value+2
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b+1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a+1, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(b>0 and STACK[a][b]==STACK[a][b-1]):
        STACK[a][b]=value+1
        STACK[a][b-1]=-1
        BLIT_LIST.remove([value, POSITIONS[a][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b-1]])
        BLIT_LIST.append([value+1,POSITIONS[a][b]])
        value=value+1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b-1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(b<4 and STACK[a][b]==STACK[a][b+1]):
        STACK[a][b]=value+1
        STACK[a][b+1]=-1
        BLIT_LIST.remove([value, POSITIONS[a][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b+1]])
        BLIT_LIST.append([value+1,POSITIONS[a][b]])
        value=value+1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        pygame.mixer.music.load('Music/Merge.wav')
        pygame.mixer.music.play()
        STACK, BLIT_LIST=check_drop(a,b+1,POSITIONS,BLIT_LIST,STACK)
        value, STACK, BLIT_LIST=merge(a, b, value, STACK, POSITIONS, BLIT_LIST)
    elif(a<6 and STACK[a][b]==STACK[a+1][b]):
        STACK[a+1][b]=value+1
        STACK[a][b]=-1
        BLIT_LIST.remove([value, POSITIONS[a+1][b]])
        BLIT_LIST.remove([value,POSITIONS[a][b]])
        BLIT_LIST.append([value+1, POSITIONS[a+1][b]])
        value=value+1
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Music/Merge.wav'))
        value, STACK, BLIT_LIST=merge(a+1, b, value, STACK, POSITIONS, BLIT_LIST)
    else:
        return value, STACK, BLIT_LIST
    return value, STACK, BLIT_LIST
# Main function
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init()
    CLOCK=pygame.time.Clock()
    pygame.display.set_caption('STACKS by Shampita')
    GAME_BLOCKS['block']=(
        pygame.image.load('Pic/2b.png').convert_alpha(),
        pygame.image.load('Pic/4b.png').convert_alpha(),
        pygame.image.load('Pic/8b.png').convert_alpha(),
        pygame.image.load('Pic/16b.png').convert_alpha(),
        pygame.image.load('Pic/32b.png').convert_alpha(),
        pygame.image.load('Pic/64b.png').convert_alpha(),
        pygame.image.load('Pic/128b.png').convert_alpha(),
        pygame.image.load('Pic/256b.png').convert_alpha(),
        pygame.image.load('Pic/512b.png').convert_alpha(),
        pygame.image.load('Pic/1024b.png').convert_alpha(),
        pygame.image.load('Pic/2048b.png').convert_alpha(),
        pygame.image.load('Pic/4096b.png').convert_alpha(),
        pygame.image.load('Pic/8192b.png').convert_alpha(),
        pygame.image.load('Pic/16384b.png').convert_alpha(),
    )
    GAME_BLOCKS['welcome']=pygame.image.load('Pic/welcome.png').convert_alpha()
    GAME_BLOCKS['keys']=pygame.image.load('Pic/keys.png').convert_alpha()
    GAME_BLOCKS['gameover']=pygame.image.load('Pic/gameover.png').convert_alpha()
    GAME_BLOCKS['winner']=pygame.image.load('Pic/winner.png').convert_alpha()
    GAME_BLOCKS['Game']=pygame.image.load(BACKGROUND).convert()
    GAME_BLOCKS['score']=(
        pygame.image.load('Pic/1.png').convert_alpha(),
        pygame.image.load('Pic/2.png').convert_alpha(),
        pygame.image.load('Pic/3.png').convert_alpha(),
        pygame.image.load('Pic/4.png').convert_alpha(),
        pygame.image.load('Pic/5.png').convert_alpha(),
        pygame.image.load('Pic/6.png').convert_alpha(),
        pygame.image.load('Pic/7.png').convert_alpha(),
        pygame.image.load('Pic/8.png').convert_alpha(),
        pygame.image.load('Pic/9.png').convert_alpha(),
        pygame.image.load('Pic/10.png').convert_alpha(),
        pygame.image.load('Pic/11.png').convert_alpha(),
        pygame.image.load('Pic/12.png').convert_alpha(),
        pygame.image.load('Pic/13.png').convert_alpha(),
        pygame.image.load('Pic/14.png').convert_alpha(),
    )

    while True:
        welcomeScreen()