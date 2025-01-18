import pygame

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