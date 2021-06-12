import pygame
import sys
import random
from tkinter import messagebox, Tk

from pygame.constants import MOUSEBUTTONDOWN, QUIT


Tk().withdraw()
screenWidth = 800
screenHeight = 600
SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
SCREEN.set_alpha(None)
pygame.display.set_caption("Duck Hunt")
# pygame.mouse.set_visible(False)

FPS = 60  # frames per second setting
fpsClock = pygame.time.Clock()

duckPic = pygame.image.load("assets/duck_edit.png").convert_alpha()
duckWidth = int(duckPic.get_width() / 3)
duckHeight = int(duckPic.get_height() / 3)
duckPic = pygame.transform.scale(duckPic, (duckWidth, duckHeight))

background = pygame.image.load("assets/background.png").convert_alpha()
background_overlay = pygame.image.load("assets/overlay.png").convert_alpha()
scoreimg = pygame.image.load("assets/score.png").convert_alpha()
red_cross = pygame.image.load("assets/red_cross.png").convert_alpha()
# crosshair=pygame.image.load('assets/crosshair.png').convert_alpha()

duckCoor = [(350, 390), (450, 390), (550, 390), (650, 390)]


class Global:
    def __init__(self):
        self.duckInitialx = 0
        self.duckInitialy = 0
        self.direction = "up"
        self.duckx = 0
        self.ducky = 0
        self.choice = 0
        self.popupSpeed = 100
        self.score = 0
        self.cross = 0
        self.clicked = False


Global = Global()


def refresh():
    pygame.display.update()
    fpsClock.tick(FPS)


def blitCross():
    # global cross, score
    if 1 <= Global.cross <= 3:
        SCREEN.blit(red_cross, (screenWidth - 165, 55))
    if 2 <= Global.cross <= 3:
        SCREEN.blit(red_cross, (screenWidth - 165 + 47, 55))
    if Global.cross >= 3:
        SCREEN.blit(red_cross, (screenWidth - 165 + 47 + 47, 55))
        refresh()
        messagebox.showinfo(
            title="Game Over", message=f"Game over\nScore: {Global.score}"
        )
        pygame.quit()
        sys.exit()
    refresh()


def mousePosition():
    # global choice
    mousex, mousey = pygame.mouse.get_pos()
    if Global.choice == 0:
        if (duckCoor[0][0] <= mousex <= (duckCoor[0][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif Global.choice == 1:
        if (duckCoor[1][0] <= mousex <= (duckCoor[1][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif Global.choice == 2:
        if (duckCoor[2][0] <= mousex <= (duckCoor[2][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif Global.choice == 3:
        if (duckCoor[3][0] <= mousex <= (duckCoor[3][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    return False


def check_score():
    # global popupSpeed
    if 5 <= Global.score < 10:
        Global.popupSpeed = 50
    elif 10 <= Global.score < 20:
        Global.popupSpeed = 20


def randomDuck():
    # global duckInitialx, duckInitialy, duckx, ducky, choice
    # choice=3
    Global.choice = random.choice([0, 1, 2, 3])
    # print(f"\t\t\t{choice} ")
    Global.duckInitialx = duckCoor[Global.choice][0]
    Global.duckInitialy = duckCoor[0][1]
    Global.duckx = Global.duckInitialx
    Global.ducky = Global.duckInitialy


def blitOnScreen():
    # global duckx, ducky, score, cross
    # mousex, mousey = pygame.mouse.get_pos()

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(duckPic, (Global.duckx, Global.ducky))
    SCREEN.blit(background_overlay, (0, 0))
    SCREEN.blit(scoreimg, (screenWidth - 220, 0))
    font = pygame.font.Font(None, 60)
    myScore = font.render(str(Global.score), 1, (58, 31, 4))
    SCREEN.blit(myScore, (screenWidth - 80, 8))
    # SCREEN.blit(crosshair, (mousex-(crosshair.get_width()/2),mousey-(crosshair.get_height()/2)))
    blitCross()


def up():
    # global direction, duckx, ducky, duckInitialx, duckInitialy
    while Global.direction != "down":
        # popupSpeed=check_score()
        if Global.direction == "up":
            Global.ducky -= 10
            if Global.ducky <= Global.duckInitialy - 120:
                # duckVisible=True
                Global.direction = "down"
        blitOnScreen()


def down():
    # global direction, duckx, ducky, duckInitialx, duckInitialy, clicked, cross, score
    while Global.direction != "up":
        if Global.direction == "down":
            Global.ducky += 10
            if Global.ducky >= Global.duckInitialy:
                # duckVisible=False
                Global.direction = "up"
        blitOnScreen()


def delay_loop():
    for _ in range(Global.popupSpeed):
        check_score()

        Global.clicked = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and mousePosition():
                print("click")
                Global.score += 1
                Global.clicked = True
                return
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        blitOnScreen()


if __name__ == "__main__":
    pygame.init()
    while True:
        randomDuck()
        up()
        delay_loop()
        down()
        if not Global.clicked:
            # score-=1
            Global.cross += 1
            # blitCross()
        delay_loop()
