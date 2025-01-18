import pygame
import random
import time
import math
import sys
import threading

pygame.mixer.init()
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
damage_multiplier = 1
speed_multiplier = 1
bullets = []
bossBullets = []
enemies = []
upgrades = []

StarterSongs = [pygame.mixer.Sound("sounds/StarterSong.mp3"), pygame.mixer.Sound("sounds/StarterSong2.mp3"), pygame.mixer.Sound("sounds/StarterSong3.mp3"),
                pygame.mixer.Sound("sounds/StarterSong4.mp3"), pygame.mixer.Sound("sounds/StarterSong5.mp3")]
MiddleSongs = [pygame.mixer.Sound("sounds/MiddleSong.mp3"), pygame.mixer.Sound("sounds/MiddleSong2.mp3")]
BossSongs = [pygame.mixer.Sound("sounds/Halloween.mp3"), pygame.mixer.Sound("sounds/BossHorror.mp3")]

BulletSound = pygame.mixer.Sound("sounds/Bullet.mp3")
BossBulletSound = pygame.mixer.Sound("sounds/BossBullet.mp3")
BossVictorySound = pygame.mixer.Sound("sounds/BossVictory.mp3")
BulletHurtSound = pygame.mixer.Sound("sounds/BulletHurt.mp3")
GameOverSound = pygame.mixer.Sound("sounds/GameOver.mp3")
HyperBulletSound = pygame.mixer.Sound("sounds/HyperBullet.mp3")
UpgradeSound = pygame.mixer.Sound("sounds/UpgradesClaiming.mp3")

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

class Upgrades(object):
    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.vel = 2
        self.width = width
        self.height = height
        self.type = type
        self.img = upgrade_img[self.type]

    def draw(self, win):
        screen.blit(self.img, (self.x, self.y))

class Projectile(object):
    def __init__(self, x, y, width, height):
        global speed_multiplier
        self.x = x
        self.y = y
        self.x_vel = 0
        self.width = width
        self.height = height
        self.vel = 5 * speed_multiplier

    def draw(self, win):
        if self.x_vel == 0:
            screen.blit(bullet_img, (self.x, self.y))
        else:
            theta = -180*math.atan(self.x_vel/self.vel)/math.pi
            screen.blit(pygame.transform.rotate(pygame.image.load("PNG/Lasers/laserRed15.png"), theta), (self.x, self.y))

class Hyper_Charged_Projectile(object):
    def __init__(self, x, y, width, height):
        global speed_multiplier
        self.x = x
        self.y = y
        self.x_vel = 0
        self.width = width
        self.height = height
        self.vel = 0.3

    def draw(self, win):
        screen.blit(hyper_img, (self.x, self.y))

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.lives = random.randint(1, 1 + level // 10)
        if self.lives > 5:
            self.lives = 5
        self.enemyimg = enemy_img[self.lives - 1]

    def draw(self, win):
        screen.blit(self.enemyimg, (self.x, self.y))
class Boss(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.lives = 500*level//10
        self.bossimg = boss_img

    def draw(self, win):
        screen.blit(self.bossimg, (self.x, self.y))

class BossProjectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.width = width
        self.height = height
        self.vel = 10

    def draw(self, win):
        screen.blit(bossBullet_img, (self.x, self.y))


def play_background_music():
    while True:  # Loop forever, you can add a condition to stop if needed
        if isBoss:
            for song in BossSongs:
                song.play()  # Play the current song
                while pygame.mixer.get_busy():  # Wait until the song finishes
                    if not isBoss or cond == 2:
                        pygame.mixer.stop()
                        break

                    pygame.time.Clock().tick(10)  # Check every 10 milliseconds to allow other events to run
                if not isBoss or cond == 2:
                    break
        else:
            for song in StarterSongs:
                song.play()  # Play the current song
                while pygame.mixer.get_busy():  # Wait until the song finishes
                    if isBoss or cond == 2:
                        pygame.mixer.stop()
                        break
                    pygame.time.Clock().tick(10)  # Check every 10 milliseconds to allow other events to run
                if isBoss or cond == 2:
                    break

def redrawGameWindow(bg_y):
    screen.blit(background, (0, bg_y - screen_height))
    if bg_y > 0:
        screen.blit(background, (0, bg_y))

    player.draw(screen)
    #print(isHyper)
    if isHyper:
        hyper.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    for bossBullet in bossBullets:
        bossBullet.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for upgrade in upgrades:
        upgrade.draw(screen)
    if isBoss:
        boss.draw(screen)

    text_screen = font.render(text + str(score), True, (150, 200, 255))
    shield_text_screen = font.render(text_shield, True, (150, 200, 255))
    stop_text_screen = font.render(text_stop, True, (150, 200, 255))
    lives_text_screen = font.render("Lives: " + "♥" * player.lives, True, (255, 0, 0))
    level_text_screen = font.render("level: " + str(level), True, (150, 200, 255))
    hyper_text_screen = font.render(hyper_text, True, (150, 200, 255))
    if isBoss:
        boss_text_screen = font.render("Boss Lives:" + str(boss.lives), True, (150, 200, 255))

    screen.blit(text_screen, (0, 30))
    screen.blit(lives_text_screen, (0, 0))
    screen.blit(level_text_screen, (0, 60))
    screen.blit(hyper_text_screen, (0, 90))
    screen.blit(shield_text_screen, (0, 120))
    screen.blit(stop_text_screen, (0, 150))
    if isBoss:
        screen.blit(boss_text_screen, (0, 120))
    pygame.display.update()

ignore_list = []

pygame.init()
player_ydir = 0
player_xdir = 0
counter = 0
background = pygame.image.load("Backgrounds/background1.png")
font = pygame.font.Font('freesansbold.ttf', 32)
text = "Score: "
text_shield = "SHIELD time left: "
text_stop = "STOP time left: "
hyper_text = ""
screen_height = background.get_height()
screen_width = background.get_width()
screen = pygame.display.set_mode((length, width))
super_distance = 0
hyper_distance = 0
boss_distance = 0
hyper_boss_distance = 0
player_distance = 0
hyper_num = 2
score = 0
level = 1
enemies_num = 10
enemies_present = 0
time_interval = 20
time_shield = 0
shield = False
time_stop = 0
stop = False
isHyper = False
isBoss = False
boss_img = pygame.transform.scale(pygame.image.load("PNG/Enemies/enemyBlue4.png"), (279, 252))
hyper_img = pygame.transform.scale(pygame.image.load("PNG/Lasers/hyper.png"), (256, 256))
player_img = pygame.image.load("PNG/playerShip2_red.png")
enemy_img = [pygame.image.load("PNG/Enemies/enemyBlack1.png"), pygame.image.load("PNG/Enemies/enemyRed1.png"), pygame.image.load("PNG/Enemies/enemyYellow1.png"), pygame.image.load("PNG/Enemies/enemyGreen1.png"), pygame.image.load("PNG/Enemies/enemyBlue1.png")]
upgrade_img = [pygame.image.load("PNG/Upgrades/double_bullet.png"), pygame.image.load("PNG/Upgrades/speed_bullet.png"), pygame.image.load("PNG/Upgrades/super_lives.png"), pygame.image.load("PNG/Upgrades/super_shield.png"), pygame.image.load("PNG/Upgrades/time_stop.png")]
bullet_img = pygame.image.load("PNG/Lasers/laserRed15.png").convert()
bossBullet_img = pygame.image.load("PNG/Lasers/laserBlue16.png").convert()
player = Player(844, 470, 112, 75)
screen = pygame.display.set_mode((length, width))
cond = 1
time_start = time.time()
time_start = time.time()

background_thread = threading.Thread(target=play_background_music, daemon=True)
background_thread.start()


while 1:
    clock.tick(144)
    if cond == 1:
        for enemy in enemies:
            enemy.vel = 4 + level // 10
            if enemy.vel > 10:
                enemy.vel = 10
        enemies_num = 10 + 2 * (level - 1)
        if enemies_num > 100:
            enemies_num = 100
        time_interval = 5 - level / 2
        if time_interval < 0:
            time_interval = 0.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 3 * damage_multiplier and not isHyper:
                        BulletSound.play()
                        if damage_multiplier == 1:
                            bullets.append(Projectile(round(player.x + player.width // 2 - 5), round(player.y + player.height // 2 - 50), 9, 37))
                        if damage_multiplier == 2:
                            bullets.append(Projectile(round(player.x + player.width // 2 - 15),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                            bullets.append(Projectile(round(player.x + player.width // 2 + 7.5),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                        if damage_multiplier == 4:
                            bullets.append(Projectile(round(player.x + player.width // 2 - 30),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                            bullets[-1].x_vel = -2
                            bullets.append(Projectile(round(player.x + player.width // 2 - 15),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                            bullets.append(Projectile(round(player.x + player.width // 2 + 7.5),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                            bullets.append(Projectile(round(player.x + player.width // 2 + 7.25),
                                                      round(player.y + player.height // 2 - 50), 9, 37))
                            bullets[-1].x_vel = 2
                elif event.key == pygame.K_RETURN and not isHyper and hyper_num > 0:
                    hyper = Hyper_Charged_Projectile(round(player.x + player.width // 2 - 127.5), round(player.y + player.height // 2 - 50), 128, 128)
                    hyper_num -= 1
                    HyperBulletSound.play()
                    isHyper = True
        if level%10 == 0 and isBoss == False:
            boss = Boss(random.randint(50, 1638), 5, 279, 252)
            isBoss = True
            bossBulletTime = time.time()
            bossGoalPos = 0
        if isBoss == True:
            bossGoalPos = player.x
            if bossGoalPos - 80 > boss.x:
                boss.x += 1
            elif bossGoalPos - 80 < boss.x:
                boss.x -= 1
            if time.time() - bossBulletTime >= 0.5:
                bossBullets.append(BossProjectile(round(boss.x + boss.width // 2 - 5), round(boss.y + boss.height // 2 + 50), 9, 37))
                bossBulletTime = time.time()
                BossBulletSound.play()
            for bossBullet in bossBullets:
                player_distance = math.sqrt((bossBullet.x - player.x) ** 2 + (bossBullet.y - player.y) ** 2)
                if player_distance < 60:
                    player.lives -= 2
                    BulletHurtSound.play()
                    bossBullets.pop(bossBullets.index(bossBullet))
                    pass
                if player.lives <= 0:
                    background = pygame.image.load("Backgrounds/lost.png")
                    cond = 2
                if bossBullet.y < 1000 and bossBullet.y > 0:
                    bossBullet.y += bossBullet.vel
                else:
                    bossBullets.pop(bossBullets.index(bossBullet))



        if time.time() - time_start >= time_interval:
            time_start = time.time()
            if enemies_present < enemies_num:
                enemies.append(Enemy(random.randint(50, 1638), 5, 93, 84))
                enemies_present += 1
            if len(enemies) == 0 and enemies_present == enemies_num and isBoss == False:
                level += 1
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
                bullet.x += bullet.x_vel
            else:
                bullets.pop(bullets.index(bullet))
        if isHyper:
            if isBoss:
                if hyper.y < 1000 and hyper.y > 0:
                    hyper.y -= hyper.vel*5
                else:
                    isHyper = False
            else:
                if hyper.y < 1000 and hyper.y > 0:
                    hyper.y -= hyper.vel
                else:
                    isHyper = False
        for upgrade in upgrades:
            if upgrade.y < 1000 and upgrade.y > 0:
                upgrade.y += upgrade.vel
            elif upgrade.y > 1000:
                upgrades.pop(upgrades.index(upgrade))
            upg_distance = math.sqrt((player.x - upgrade.x) ** 2 + (player.y - upgrade.y) ** 2)
            if upg_distance < 60:
                UpgradeSound.play()
                if upgrade.type == 0:
                    if damage_multiplier == 1:
                        damage_multiplier = 2
                    elif damage_multiplier == 2:
                        damage_multiplier = 4
                    elif damage_multiplier == 4:
                        hyper_num += 1
                elif upgrade.type == 1:
                    speed_multiplier = 2
                elif upgrade.type == 2:
                    player.lives += 3
                elif upgrade.type == 3:
                    shield = True
                    time_shield = time.time()
                    player_img = pygame.image.load("PNG/playerShip2_red_shield.png")
                elif upgrade.type == 4:
                    stop = True
                    time_stop = time.time()
                upgrades.pop(upgrades.index(upgrade))
        hyper_text = "HC BULLETS: " + "♥"*hyper_num

        if shield:
            #print(int(time.time() - time_shield))
            text_shield = "SHIELD time left: " + "♥"*(10 - int(time.time() - time_shield))
            if time.time() - time_shield >= 10:
                shield = False
                player_img = pygame.image.load("PNG/playerShip2_red.png")
        else:
            text_shield = ""
        if stop:
            text_stop = "TIME STOP left: " + "♥"*(10 - int(time.time() - time_stop))
            if time.time() - time_stop >= 10:
                for enemy in enemies:
                    enemy.vel = 4
                stop = False
            else:
                for enemy in enemies:
                    enemy.vel = 0.5
        else:
            text_stop = ""

        if isBoss:
            for bullet in bullets:
                boss_distance = math.sqrt((bullet.x - (boss.x + 126)) ** 2 + (bullet.y - boss.y) ** 2)
                if boss_distance < 130:
                    boss.lives -= 1
                    BulletHurtSound.play()
                    bullets.pop(bullets.index(bullet))
            #print(boss.lives)
            if isHyper:
                hyper_boss_distance = math.sqrt((hyper.x - (boss.x + 126)) ** 2 + (hyper.y - boss.y) ** 2)
                if hyper_boss_distance < 200:
                    boss.lives -= 100
                    isHyper = False
            if boss.lives <= 0:
                isBoss = False
                BossVictorySound.play()
                score += 10
                hyper_num += 2
                player.lives += 5
                for bossBullet in bossBullets:
                    bossBullets.pop(bossBullets.index(bossBullet))
                level += 1
        enemies_to_remove = []
        for enemy in enemies:
            if enemy.y < 1000 and enemy.y > 0:
                enemy.y += enemy.vel
            else:
                enemy.y = 5
                enemy.x = random.randint(50, 1638)
            if isHyper:
                hyper_distance = math.sqrt(((hyper.x+100) - enemy.x) ** 2 + (hyper.y - enemy.y) ** 2)
                if hyper_distance < 150:
                    enemy.lives = 0
                    score += 2
                    enemies_to_remove.append(enemy)
            for bullet in bullets:
                super_distance = math.sqrt((bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
                if super_distance < 90:
                    enemy.lives -= 1
                    BulletHurtSound.play()
                    enemy.enemyimg = enemy_img[enemy.lives - 1]
                    bullets.pop(bullets.index(bullet))
                    if enemy.lives == 0:
                        score += 1
                        enemies_to_remove.append(enemy)
                        if score % (10 + 5 * level//10) == 0 and score != 0:
                            upgrades.append(Upgrades(random.randint(0, 1688), 10, 40, 40, random.randint(0, 4)))
                        if score % (20 + 5 * level//10) == 0 and score != 0:
                            player.lives += 1
            dead = math.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
            if dead <= 35:
                if not shield:
                    player.lives -= 1
                enemy.lives -= 1
                BulletHurtSound.play()
                if enemy.lives == 0:
                    enemies_to_remove.append(enemy)
                if player.lives == 0:
                    background = pygame.image.load("Backgrounds/lost.png")
                    GameOverSound.play()
                    cond = 2

        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.pop(enemies.index(enemy))

        bg_y += 1
        if bg_y >= screen_height:
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    cond = 1
                    player.lives = 3
                    damage_multiplier = 1
                    speed_multiplier = 1
                    super_distance = 0
                    hyper_distance = 0
                    boss_distance = 0
                    hyper_boss_distance = 0
                    player_distance = 0
                    hyper_num = 5
                    score = 0
                    level = 1
                    enemies_num = 10
                    enemies_present = 0
                    time_interval = 20
                    time_shield = 0
                    shield = False
                    time_stop = 0
                    stop = False
                    isHyper = False
                    isBoss = False
                    #if isBoss:
                    #    boss.lives -= 100
                    background = pygame.image.load("Backgrounds/background1.png")

sys.exit()
