import math 
import random
import pygame

sw = 800
sh = 500
ps_x = 370
ps_y = 380
es_y_min = 50
es_y_max = 150
es_x = 4
es_y = 40
bs_y = 10
cd = 27

pygame.init()
screen = pygame.display.set_mode((sw,sh))

background = pygame.image.load('bg.png')
pygame.display.set_caption('space invader')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerimg = pygame.image.load('player.png')
playerx = ps_x
playery = ps_y
playerx_change = 0

enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
enemies = 6

for i in range(enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,sw-64))
    enemyy.append(random.randint(es_y_min,es_y_max))
    enemyx_change.append(es_x)
    enemyy_change.append(es_y) 

    
bulletImg = pygame.image.load('bullet.png')
bulletx = 0
bullety = ps_y
bulletx_change = 0
bullety_change = bs_y
bullet_state = 'ready'
#score
score_value = 0
font = pygame.font.Font(None, 32)
textx = 10
texty = 10

over_font = pygame.font.Font(None, 64)

def show_score(x,y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x,y):
    screen.blit(playerimg,(x,y))

def enemy(x, y, i):
    screen.blit(enemyimg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyx , enemyy, bulletx, bullety ):
    distance = math.sqrt((enemyx - bulletx) ** 2 + (enemyy - bullety) **2)
    return distance < cd

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
               playerx_change = - 5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE and bullet_state == 'ready':

                bulletx = playerx
                fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP and event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
            playerx_change = 0

    playerx += playerx_change
    playerx = max(0,min(playerx, sw - 64))
    
    for i in range(enemies):
        if enemyy[i] > 340:
            for i in range(enemies):
                enemyy[i] = 2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i] 
        if enemyx[i] <= 0 or enemyx[i] >= sw - 64:
            enemyx_change[i] *= -1 
            enemyy[i] += enemyy_change[i]

        if isCollision(enemyx[i], enemyy[i], bulletx, bullety):
            bullety = ps_y
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, sw - 64 )
            enemyy[i] = random.randint(es_y_min, es_y_max)
        enemy(enemyx[i], enemyy[i],i)
    if bullety <= 0:
       bullety = ps_y
       bullet_state = 'ready'
    elif bullet_state =='fire':
         fire_bullet(bulletx, bullety)
         bullety -= bullety_change
    
    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()


    



