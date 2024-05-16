import pygame
import random
import time
import math
import sys

clock = pygame.time.Clock()
width = 940
length = 1688
ani_left = 0
ani_right = 0
angle = 0
ret_angle = 0
bullet_x = 0
bullet_y = 0
bg_y = 0
bullets = []
enemies = []
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.lives = 3
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        screen.blit(player_img, (self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10

    def draw(self, win):
        screen.blit(bullet_img, (self.x, self.y))

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.lives = 1 + level//10
        if self.lives > 5:
            self.lives = 5
        self.enemyimg = enemy_img[self.lives - 1]
    def draw(self, win):
        screen.blit(self.enemyimg, (self.x, self.y))

def redrawGameWindow(bg_y):
    screen.blit(background, (0, bg_y - screen_height))  # screen.fill((0, 255, 0))
    if bg_y > 0:
        screen.blit(background, (0, bg_y))

    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    text_screen = font.render(text + str(score), True, (0, 0, 0))
    lives_text_screen = font.render("Lives: " + "♥"*player.lives, True, (255, 0, 0))
    level_text_screen = font.render("level: " + str(level), True, (0, 0, 0))
    screen.blit(text_screen, (0, 0))
    screen.blit(lives_text_screen, (0, 30))
    screen.blit(level_text_screen, (0, 60))
    pygame.display.update()

ignore_list = []

pygame.init() # запуск
player_ydir = 0
player_xdir = 0
counter = 0
background=pygame.image.load("Backgrounds/background1.png")
font = pygame.font.Font('freesansbold.ttf', 32)
text = "Score: "
screen_height = background.get_height()
screen_width = background.get_width()
screen = pygame.display.set_mode((length, width))
super_distance = 0
score = 0
level = 100
enemies_num = 10
enemies_present = 0
time_interval = 20
player_img = pygame.image.load("PNG/playerShip2_red.png")
player_img_master = pygame.image.load("PNG/playerShip2_red.png").convert()
enemy_img = [pygame.image.load("PNG/Enemies/enemyBlack1.png"), pygame.image.load("PNG/Enemies/enemyRed1.png"), pygame.image.load("PNG/Enemies/enemyYellow1.png"), pygame.image.load("PNG/Enemies/enemyGreen1.png"), pygame.image.load("PNG/Enemies/enemyBlue1.png")]
bullet_img = pygame.image.load("PNG/Lasers/laserRed15.png").convert()
bullet_img_master = pygame.image.load("PNG/Lasers/laserRed15.png").convert()
player = Player(844, 470, 112, 75)
screen = pygame.display.set_mode((length, width))
cond = 1
#bullet.rect.y = 500000000
#bullet.rect.x = 500000000
time_start = time.time()
while 1:
    clock.tick(144)
    if cond == 1:
        for enemy in enemies:
            enemy.vel = 4 + level//10
            if enemy.vel > 10:
                enemy.vel = 10
        enemies_num = 10 + 2*(level - 1)
        if enemies_num > 100:
            enemies_num = 100
        time_interval = 5 - level/2
        if time_interval < 0:
            time_interval = 0.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:  # если нажата клавиша
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 3:
                        bullets.append(Projectile(round(player.x + player.width // 2 - 5), round(player.y + player.height // 2 - 50), 9, 37))
                #if event.key == pygame.K_z:
                #    if len(enemies) < 10000:
                #        enemies.append(Enemy(random.randint(50, 1638), 5, 93, 84, enemy_img[random.randint(0, len(enemy_img)-1)]))
        if time.time() - time_start >= time_interval:
            time_start = time.time()
            if enemies_present < enemies_num:
                enemies.append(
                    Enemy(random.randint(50, 1638), 5, 93, 84))
                enemies_present += 1
            if len(enemies) == 0 and enemies_present == enemies_num:
                level+=1
                print("level " + str(level) + " began!")
                enemies_present = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.vel:
            player.x -= player.vel
            player.left = True
            player.right = False
            player.standing = False
        elif keys[pygame.K_RIGHT] and player.x < 1688 - player.width - player.vel:
            player.x += player.vel
            player.right = True
            player.left = False
            player.standing = False
        else:
            player.standing = True
            player.walkCount = 0
        if keys[pygame.K_UP] and player.y > player.vel:
            player.y -= player.vel
            player.left = True
            player.right = False
            player.standing = False
        elif keys[pygame.K_DOWN] and player.y < 1688 - player.width - player.vel:
            player.y += player.vel
            player.right = True
            player.left = False
            player.standing = False
        else:
            player.standing = True
            player.walkCount = 0

        if player.y < 650:
            player.y = 650
        if player.y > 870:
            player.y = 870
        for bullet in bullets:
            if bullet.y < 1000 and bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        for enemy in enemies:
            if enemy.y < 1000 and enemy.y > 0:
                enemy.y += enemy.vel
            else:
                enemy.y = 5
                enemy.x = random.randint(50, 1638)
            for bullet in bullets:
                super_distance = math.sqrt(
                    (bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
                if super_distance < 90:
                    enemy.lives -= 1
                    enemy.enemyimg = enemy_img[enemy.lives - 1]
                    bullets.pop(bullets.index(bullet))
                    if enemy.lives == 0:
                        score += 1
                        if enemies.index(enemy) in ignore_list:
                            ignore_list.pop(id(enemy))
                        enemies.pop(enemies.index(enemy))
                    if score%15 == 0 and score != 0:
                        player.lives += 1
            dead = math.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
            if dead <= 35:
                player.lives -= 1
                enemy.lives -= 1
                if id(enemy) in ignore_list:
                    player.lives += 1
                    enemy.lives += 1
                else:
                    ignore_list.append(id(enemy))
                if enemy.lives == 0:
                    if enemies.index(enemy) in ignore_list:
                        try:
                            ignore_list.pop(id(enemy))
                        except Exception:
                            pass
                    enemies.pop(enemies.index(enemy))
                if player.lives == 0:
                    background = pygame.image.load("Backgrounds/lost.png")
                    cond = 2
            else:
                if id(enemy) in ignore_list and len(ignore_list):
                    #print(len(ignore_list))
                    try:
                        ignore_list.pop(id(enemy))
                    except Exception:
                        pass
        bg_y += 1
        if bg_y >= screen_height:  # дест = destination чтобы фон двигался
            bg_y = 0
        redrawGameWindow(bg_y)
    elif cond == 2:
        for enemy in enemies:
            enemies.pop(enemies.index(enemy))
        screen.blit(background, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:  # если нажата клавиша
                if event.key == pygame.K_r:
                    cond = 1
                    background = pygame.image.load("Backgrounds/background1.png")

sys.exit()