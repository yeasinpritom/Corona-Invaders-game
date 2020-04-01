import pygame
import random
import math
from pygame import mixer

# initialization
pygame.init()
# screen
screen = pygame.display.set_mode((800, 600))

# Background

background = pygame.image.load('back.png')
# bg sound
mixer.music.load('bg.wav')
mixer.music.play(-1)

# Adding caption and logo and bgcolor
pygame.display.set_caption("                                                                                               Human Invaders Corona")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)  # for setting thr icon into the display. Have to be equal or less than 32 pixels.

# player A

playerimage = pygame.image.load(
    'arcadespace.png')  # For uploading a image. Have to be png(portable network graphics, which was created as an altermative of GIF(graphics interchange format)) file and not less than 64 pixels,
playerx = 370  # x axis start from leftside.
playery = 520  # y axis start from top .
xchange = 0
ychange = 0


def player(x, y):
    screen.blit(playerimage, (x, y))  # blit means setting the image that we want to set in the desired co-ordinate.


# Enemy
enemyimage = []
enemyx = []
enemyy = []
enemychx = []
enemychy = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyimage.append(pygame.image.load ('enemy.png'))  # For uploading a image. Have to be png(portable network graphics, which was created as an altermative of GIF(graphics interchange format)) file and not less than 64 pixels,
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(40, 250))
    enemychx.append(2.2)
    enemychy.append(30)


def enemy(x, y, i):
    screen.blit(enemyimage[i], (x, y))  # blit means setting the image that we want to set in the desired co-ordinate.


# Bullet

bullet_state = "ready"
bulletimage = pygame.image.load(
    'bullet.png')  # For uploading a image. Have to be png(portable network graphics, which was created as an altermative of GIF(graphics interchange format)) file and not less than 64 pixels,
bulletx = 0  # x axis start from leftside.
bullety = 480  # y axis start from top .
bulletchx = 0
bulletchy = 5


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimage,
                (x + 5, y ))  # blit means setting the image that we want to set in the desired co-ordinate.


# collision

def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow((bulletx - enemyx), 2) + (math.pow((bullety - enemyy), 2)))
    if distance < 27:
        return True
    else:
        return False


# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over
over = pygame.font.Font('freesansbold.ttf', 40)


def game_over():
    last = over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(last, (250, 250))


# screen stability

running = True
while running:
    screen.fill((0, 0, 0))  # for filling the screen bg with RGB colors.

    # backgrounf image

    screen.blit(background, (0, 0))
    for any in pygame.event.get():  # for getting every event in the display.
        if any.type == pygame.QUIT:  # If we type cross or quite, only then the display will stop.
            running = False
        if any.type == pygame.KEYDOWN:
            if any.key == pygame.K_LEFT:
                xchange = -1.5
            if any.key == pygame.K_RIGHT:
                if playerx < 800:
                    xchange = +1.5
            if any.key == pygame.K_UP:
                ychange = -1.5
            if any.key == pygame.K_DOWN:
                ychange = + 1.5
            if any.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("gun.wav")
                    bullet_sound.play()
                    bulletx = playerx  # we are saving the playerx for one space pressing .
                    # print(bulletx)
                    bullety = playery
                    bullet(bulletx, bullety)
        if any.type == pygame.KEYUP:
            if any.key == pygame.K_LEFT or any.key == pygame.K_RIGHT:
                xchange = 0
            elif any.key == pygame.K_UP or any.key == pygame.K_DOWN:
                ychange = 0

    # player movement
    playerx += xchange
    playery += ychange

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    if playery <= 460:
        playery = 460
    elif playery >= 530:
        playery = 520

    # Enemy movement

    for i in range(num_of_enemy):

        # game over control

        if enemyy[i] > 460:
            for j in range(num_of_enemy):
                enemyy[j] = 2000
                game_over()
            break
        enemyx[i] += enemychx[i]
        if enemyx[i] >= 736:
            enemyx[i] = 736
            enemyy[i] = enemyy[i] + enemychy[i]
            enemychx[i] *= -1
        elif enemyx[i] <= 0:
            enemyx[i] = 0
            enemyy[i] = enemyy[i] + enemychy[i]
            enemychx[i] *= -1
            # collision
        collision_set = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision_set:
            colli_sound = mixer.Sound('collision.wav')
            colli_sound.play()
            bullety = playery
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(40, 250)
        enemy(enemyx[i], enemyy[i], i)
        # bullet movement

    if bullety <= 0:
        bullety = playery
        bullet_state = "ready"
    if bullet_state is "fire":
        bullet(bulletx, bullety)
        bullety -= bulletchy
    show_score(textX, textY)
    player(playerx, playery)
    pygame.display.update()  # For updating the display.
