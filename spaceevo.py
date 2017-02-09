import random, time, pygame, sys
from pygame.locals import *

FPS = 60
GAME_WIDTH = 800
GAME_HEIGHT = 600
INITIAL_ALIEN_COUNT = 10
MISSILE_WIDTH = 26
PLAYER_SPEED = 8
PLAYER_MISSILE_SPEED = -15
PLAYER_SHOT_DELAY = 0.35
ENEMY_MISSILE_SPEED = 10
ENEMY_SPEED = 5

class Player:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))

    def controls(self):
        global lastShotFired
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]):
            if self.x > 10:
                self.x -= PLAYER_SPEED
        elif (keys[K_RIGHT] or keys[K_d]):
            if self.x < GAME_WIDTH:
                self.x += PLAYER_SPEED
        elif (keys[K_SPACE]):
            if(time.time() > lastShotFired + PLAYER_SHOT_DELAY):
                lastShotFired = time.time()
                player.shoot()

    def shoot(self):
        playerMissiles.append(PlayerMissile(player.x, player.y, 'data/player_missile.bmp'))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class PlayerMissile:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.outOfBounds = False
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))

    def update(self):
        if self.y < 0:
            self.outOfBounds = True

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class Alien:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class AlienMissile:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

def collisionDetection(s1_x, s1_y, s2_x, s2_y):
    if (s1_x > s2_x - MISSILE_WIDTH) and (s1_x < s2_x + MISSILE_WIDTH) and (s1_y > s2_y - MISSILE_WIDTH) and (s1_y < s2_y + MISSILE_WIDTH):
        return 1
    else:
        return 0

# --- MAIN ---
global lastShotFired
pygame.init()
FPSCLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.key.set_repeat(1, 1)
pygame.display.set_caption('SpaceEVO')
backdrop = pygame.image.load('data/sevobackground.bmp')
lastShotFired = time.time()

enemies = []
playerMissiles = []

x = 0
for count in range(INITIAL_ALIEN_COUNT):
    enemies.append(Alien(50 * x + 50, 50, 'data/alien_1.bmp'))
    x += 1

player = Player(GAME_WIDTH/2, 500, 'data/player.bmp')
enemymissile = AlienMissile(0, GAME_HEIGHT, 'data/alien_missile.bmp')

while True:
    screen.blit(backdrop, (0, 0))

    # --- DRAW ---

    for count in range(len(enemies)):
        enemies[count].x += ENEMY_SPEED
        enemies[count].render()

    if enemies[len(enemies)-1].x > GAME_WIDTH or enemies[0].x < 10:
        ENEMY_SPEED = -ENEMY_SPEED
        for count in range(len(enemies)):
            enemies[count].y += 5

    for count in range(len(playerMissiles)):
        playerMissiles[count].y += PLAYER_MISSILE_SPEED
        playerMissiles[count].render()

    if enemymissile.y >= GAME_HEIGHT and len(enemies) > 0:
        enemymissile.x = enemies[random.randint(0, len(enemies)-1)].x
        enemymissile.y = enemies[0].y

    # --- EVENTS ---

    if collisionDetection(player.x, player.y, enemymissile.x, enemymissile.y):
        quit()
        sys.exit()

    if len(enemies) == 0:
        pygame.quit()
        sys.exit()

    for gameevent in pygame.event.get():
        if gameevent.type == QUIT:
            pygame.quit()
            sys.exit()

    # --- UPDATES ---

    for m in playerMissiles:
        m.update()
    playerMissiles = [m for m in playerMissiles if not m.outOfBounds]


    enemymissile.render()
    enemymissile.y += ENEMY_MISSILE_SPEED

    player.render()
    player.controls()

    pygame.display.update()
    FPSCLOCK.tick(FPS)
