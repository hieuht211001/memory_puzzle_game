#import library (pygame, itertools, time, random)
import pygame as pg
import random
from itertools import product
from pygame import mixer
from pygame.locals import *
from pygame.color import Color
import time

pg.init()

#set up 3 colors
color=(255,69,0)  #orange
black=(21,59,89)       #black
white=(255,255,255) #white
yeel=(239,196,122)
pink = (255,89,101)
background = pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\background2.png')
mute_button=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\mute.png')
pause_button=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\pausebutton.png')
infor_image=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\INFOR.png')
infor_icon=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\infor_icon.png')
quit_icon=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\quit_icon.png')
pause_screen=pg.image.load(r'D:\New folder (2)\memory_puzzle_game\Resources\pause_screen.png')


time_limit=10*60
start_time=time.time()

def infor_about_us():
    infor = True
    while infor:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_i:
                    infor  = False

        screen.blit(infor_image,(0,0))
        pg.display.update()
        clock.tick(5)
def infor_about_us_by_mouse():
    infor = True
    while infor:
        screen.blit(infor_image,(0,0))
        screen.blit(infor_icon,(0,0))
        pg.display.update()
        clock.tick(5)
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()   #mouse click
                mouse_clicked = True
                if 630 <= mouse_x <= 670 and 175 <= mouse_y <= 215:
                    infor  = False
    

#import background music
mixer.music.load(r'D:\New folder (2)\memory_puzzle_game\Resources\chillmusic.mp3')
mixer.music.play(-1)


#pause and unpause music function
def pause_music():
    pause_music = True
    while pause_music:
        pg.mixer.music.pause()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_s:
                    pause_music  = False
                    pg.mixer.music.unpause()
def pause_music_by_mouse():
    pause_music = True
    while pause_music:
        pg.mixer.music.pause()
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()   #mouse click
                mouse_clicked = True
                if 720 <= mouse_x <= 760 and 80 <= mouse_y <= 120:
                    pause_music  = False
                    pg.mixer.music.unpause()

#set up width and height of pygame screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SQUARE_SIZE = 50
SQUARE_GAP = 10
BOARD_WIDTH = 6
BOARD_HEIGHT = 4
X_MARGIN = (SCREEN_WIDTH - (BOARD_WIDTH * (SQUARE_SIZE + SQUARE_GAP))) // 2
Y_MARGIN = (SCREEN_HEIGHT - (BOARD_HEIGHT * (SQUARE_SIZE + SQUARE_GAP))) // 2
# the board size must be even due to pairs
assert (BOARD_HEIGHT * BOARD_WIDTH) % 2 == 0, 'The board size must be even'

# name the shapes
DIAMOND = 'diamond'
SQUARE = 'square'
TRIANGLE = 'triangle'
CIRCLE = 'circle'

# set up background color is black
BGCOLOR =(255,241,206)

# function to set text on pygame screen
def text_on_screen(text,color,x,y,size):
    myfont=pg.font.SysFont('Verdana',size)
    text=myfont.render(text,1,color)
    screen.blit(text,(x,y))

# function to set Pause (P) button in game - click P to pause then P to continue or Q to quit
def pause():
    paused = True
    while paused:
        screen.blit(pause_screen,(0,0))
        screen.blit(pause_button,(0,0))
        pg.display.update()
        clock.tick(5)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_p:
                    paused  = False
                elif event.key == pg.K_q:
                    pg.quit()
                    quit()

# function to set animation when the game is won
def game_won(revealed):
    return all(all(x) for x in revealed)

# function to set animation at the start of the game (start game by ramdomly showing 5 squares)
def start_game_animation(board):
    coordinates = list(product(range(BOARD_HEIGHT), range(BOARD_WIDTH)))
    random.shuffle(coordinates)

    revealed = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]
    draw_board(board, revealed)
    pg.display.update()
    pg.time.wait(500)

    for sz in range(0, BOARD_HEIGHT * BOARD_WIDTH, 5):
        l = coordinates[sz: sz + 5]
        for x in l:
            revealed[x[0]][x[1]] = True
            draw_square(board, revealed, *x)
        pg.time.wait(500)
        for x in l:
            revealed[x[0]][x[1]] = False
            draw_square(board, revealed, *x)

# function been followed after game won (Flashes background colors when the game is won)
def game_won_animation(board, revealed):
    color1 = Color('white')
    color2 = BGCOLOR
    for i in range(10):
        color1, color2 = color2, color1
        screen.fill(color1)
        draw_board(board, revealed)
        pg.display.update()
        pg.time.wait(300)

# function to set up the board (Generates the board of game by random shuffling)
def get_random_board(shape, colors):
    icons = list(product(shape, colors))
    num_icons = BOARD_HEIGHT * BOARD_WIDTH // 2
    icons = icons[:num_icons] * 2

    random.shuffle(icons)
    board = [icons[i:i + BOARD_WIDTH]
             for i in range(0, BOARD_HEIGHT * BOARD_WIDTH, BOARD_WIDTH)]
    return board

# function to get the coordinates of one particular square
def get_coord(x, y):

    top = X_MARGIN + y * (SQUARE_SIZE + SQUARE_GAP)
    left = Y_MARGIN + x * (SQUARE_SIZE + SQUARE_GAP)
    return top, left

# function to set the shape of the icon of square (4 type: DIANMOND, SQUARE, TRIANGLE, CIRCLE)
def draw_icon(icon, x, y):
    px, py = get_coord(x, y)
    if icon[0] == DIAMOND:
        pg.draw.polygon(screen, icon[1],
                            ((px + SQUARE_SIZE // 2, py + 5), (px + SQUARE_SIZE - 5, py + SQUARE_SIZE // 2),
                             (px + SQUARE_SIZE // 2, py + SQUARE_SIZE - 5), (px + 5, py + SQUARE_SIZE // 2)))
    elif icon[0] == SQUARE:
        pg.draw.rect(screen, icon[1],
                         (px + 5, py + 5, SQUARE_SIZE - 10, SQUARE_SIZE - 10))
    elif icon[0] == TRIANGLE:
        pg.draw.polygon(screen, icon[1],
                            ((px + SQUARE_SIZE // 2, py + 5), (px + 5, py + SQUARE_SIZE - 5),
                             (px + SQUARE_SIZE - 5, py + SQUARE_SIZE - 5)))
    elif icon[0] == CIRCLE:
        pg.draw.circle(screen, icon[1],
                           (px + SQUARE_SIZE // 2, py + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)


# function to get position
def get_pos(cx, cy):
    if cx is None or cy is None:    #fix error '<' between none and int
        return None, None
   
    if cx < X_MARGIN or cy < Y_MARGIN:  
        return None, None

    x = (cy - Y_MARGIN) // (SQUARE_SIZE + SQUARE_GAP)
    y = (cx - X_MARGIN) // (SQUARE_SIZE + SQUARE_GAP)

    if x >= BOARD_HEIGHT or y >= BOARD_WIDTH or(cx - X_MARGIN) % (SQUARE_SIZE + SQUARE_GAP) > SQUARE_SIZE or (cy - Y_MARGIN) % (SQUARE_SIZE + SQUARE_GAP) > SQUARE_SIZE:
        return None, None
    else:
        return x, y


# function to draw a particulaer square
def draw_square(board, revealed, x, y):
    coords = get_coord(x, y)
    square_rect = (*coords, SQUARE_SIZE, SQUARE_SIZE)
    pg.draw.rect(screen, BGCOLOR, square_rect)
    if revealed[x][y]:
        draw_icon(board[x][y], x, y)
    else:
        pg.draw.rect(screen, color , square_rect)
    pg.display.update(square_rect)

# function to draw the entire board
def draw_board(board, revealed):
    # function to set up timer
    elapsed_time = int(time.time()-start_time)
    remain_time = time_limit-elapsed_time
    current_minute=int(remain_time/60)
    current_second=int(remain_time - current_minute*60)
    if elapsed_time > time_limit:
        screen.fill(color)
        text_on_screen('TIME OUT',black,330,100,30)
        text_on_screen('GAME OVER',black,230,120,60)
        pg.display.update()
        quit()
        
    screen.blit(background,(0,0))
    #text_on_screen('Memory Puzzle Game -Team J',color,160,10,30)
    text_on_screen(str(current_minute)+' : '+str(current_second),color,24,300,50)

    for x in range(BOARD_HEIGHT):
        for y in range(BOARD_WIDTH):
            draw_square(board, revealed, x, y)

#Function to draw the red highlight box around the square when that square is chosen
def draw_select_box(x, y):
    px, py = get_coord(x, y)
    pg.draw.rect(screen, (11,39,110)
                 , (px - 5, py - 5, SQUARE_SIZE + 10, SQUARE_SIZE + 10), 5)

clickCounter=0
def click(event):
    global clickCounter
    clickCounter +=(1/2)


#Final function to run the game (combine of all above function to run in order)
def main():
    global screen, clock

    pg.init()

    screen = pg.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
    screen.blit(background,(400,400))
    pg.display.set_caption('어디 숨었을까? - J 팀')

    clock = pg.time.Clock()

    shape = (DIAMOND, SQUARE, TRIANGLE, CIRCLE)
    colors = ((255,168,29),(56,48,76),(246,88,99),(36,165,231))

    # There should be enough symbols
    assert len(shape) * len(colors) >= BOARD_HEIGHT * BOARD_WIDTH // 2,'There are not sufficient icons'
    board = get_random_board(shape, colors)
    revealed = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT)]  # keeps track of visibility of square

    mouse_x = 1    # 1 instead of None in order to solve Error:
    mouse_y = 1    # '<=' not supported between instances of 'int' and 'NoneType'
    mouse_clicked = False
    first_selection = None

    running = True
    start_game_animation(board)
    score=0
    while running:
        draw_board(board, revealed)
        #text_on_screen('SCORE',(255,241,206),615,330,20)
        text_on_screen(str(score),(255,241,206),740,326,22)
        #text_on_screen('ATTEMPTS',(255,241,206),615,280,20)
        text_on_screen(str(int(clickCounter)),(255,241,206),740,276,22)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = pg.mouse.get_pos()   #mouse motion
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()   #mouse motion
                mouse_clicked = True
                if 720 <= mouse_x <= 760 and 80 <= mouse_y <= 120:
                    pause_music_by_mouse()
                if 630 <= mouse_x <= 670 and 80 <= mouse_y <= 120:
                    pause()
                if 720 <= mouse_x <= 760 and 175 <= mouse_y <= 215:
                    pg.quit()
                if 630 <= mouse_x <= 670 and 175 <= mouse_y <= 215:
                    infor_about_us_by_mouse()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_i:
                    infor_about_us()
                if event.key == pg.K_q:
                    pg.quit()
                if event.key == pg.K_p:
                    pause()
                if event.key == pg.K_s:
                    pause_music()
        if 720 <= mouse_x <= 760 and 80 <= mouse_y <= 120:
            screen.blit(mute_button,(0,0))
        elif 630 <= mouse_x <= 670 and 80 <= mouse_y <= 120:
            screen.blit(pause_button,(0,0))
        elif 630 <= mouse_x <= 670 and 175 <= mouse_y <= 215:
            screen.blit(infor_icon,(0,0))
        elif 720 <= mouse_x <= 760 and 175 <= mouse_y <= 215:
            screen.blit(quit_icon,(0,0))
            
            

        x, y = get_pos(mouse_x, mouse_y)

        if x is not None and y is not None:
            if not revealed[x][y]:
                if mouse_clicked:                       #square clicked by mouse
                    revealed[x][y] = True
                    draw_square(board, revealed, x, y)
                    click(event)

                    if first_selection is None:
                        first_selection = (x, y)
                    else:
                        pg.time.wait(1000)
                        if board[x][y] != board[first_selection[0]][first_selection[1]]:
                            revealed[x][y] = False
                            revealed[first_selection[0]][first_selection[1]] = False
                        else:
                            score+=10
                        first_selection = None

                    if game_won(revealed):

                        game_won_animation(board, revealed)
                        score=0
                        
                        get_random_board(shape, colors)
                            
                        revealed = [[False] * 8 for i in range(6)]
                        start_game_animation(board)

                else:
                    draw_select_box(x, y)
        mouse_clicked = False
        pg.display.update()

    else:
        pg.quit()
        quit()

#run the game
if __name__ == '__main__':
    main()
        








