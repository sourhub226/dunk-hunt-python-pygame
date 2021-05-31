import pygame, sys, random
from pygame.locals import *
from tkinter import messagebox, Tk

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

duckInitialx = 0
duckInitialy = 0
direction = "up"
duckx = 0
ducky = 0
choice = 0
popupSpeed = 100
score = 0
cross = 0
clicked = False


def refresh():
    pygame.display.update()
    fpsClock.tick(FPS)


def blitCross():
    global cross, score
    if 1 <= cross <= 3:
        SCREEN.blit(red_cross, (screenWidth - 165, 55))
    if 2 <= cross <= 3:
        SCREEN.blit(red_cross, (screenWidth - 165 + 47, 55))
    if cross >= 3:
        SCREEN.blit(red_cross, (screenWidth - 165 + 47 + 47, 55))
        refresh()
        messagebox.showinfo(title="Game Over", message=f"Game over\nScore: {score}")
        pygame.quit()
        sys.exit()
    refresh()


def mousePosition():
    global choice
    mousex, mousey = pygame.mouse.get_pos()
    if choice == 0:
        if (duckCoor[0][0] <= mousex <= (duckCoor[0][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif choice == 1:
        if (duckCoor[1][0] <= mousex <= (duckCoor[1][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif choice == 2:
        if (duckCoor[2][0] <= mousex <= (duckCoor[2][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    elif choice == 3:
        if (duckCoor[3][0] <= mousex <= (duckCoor[3][0] + 90)) and (
            (duckCoor[0][1] - 130) <= mousey <= (duckCoor[0][1] - 5)
        ):
            return True
    return False


def check_score():
    global popupSpeed
    if 5 <= score < 10:
        popupSpeed = 50
    elif 10 <= score < 20:
        popupSpeed = 20


def randomDuck():
    global duckInitialx, duckInitialy, duckx, ducky, choice
    # choice=3
    choice = random.choice([0, 1, 2, 3])
    # print(f"\t\t\t{choice} ")
    duckInitialx = duckCoor[choice][0]
    duckInitialy = duckCoor[0][1]
    duckx = duckInitialx
    ducky = duckInitialy


def blitOnScreen():
    global duckx, ducky, score, cross
    # mousex, mousey = pygame.mouse.get_pos()

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(duckPic, (duckx, ducky))
    SCREEN.blit(background_overlay, (0, 0))
    SCREEN.blit(scoreimg, (screenWidth - 220, 0))
    font = pygame.font.Font(None, 60)
    myScore = font.render(str(score), 1, (84, 58, 36))
    SCREEN.blit(myScore, (screenWidth - 80, 8))
    # SCREEN.blit(crosshair, (mousex-(crosshair.get_width()/2),mousey-(crosshair.get_height()/2)))
    blitCross()


def up():
    global direction, duckx, ducky, duckInitialx, duckInitialy
    while direction != "down":
        # popupSpeed=check_score()
        if direction == "up":
            ducky -= 10
            if ducky <= duckInitialy - 120:
                # duckVisible=True
                direction = "down"
        blitOnScreen()


def down():
    global direction, duckx, ducky, duckInitialx, duckInitialy, clicked, cross, score
    while direction != "up":
        if direction == "down":
            ducky += 10
            if ducky >= duckInitialy:
                # duckVisible=False
                direction = "up"
        blitOnScreen()


def delay_loop():
    global popupSpeed, score, clicked, cross
    x = 0
    while not x >= popupSpeed:
        check_score()
        x += 1
        # print(x)
        clicked = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and mousePosition():
                print("click")
                score += 1
                clicked = True
                return clicked
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
        if not clicked:
            # score-=1
            cross += 1
            # blitCross()
        delay_loop()
