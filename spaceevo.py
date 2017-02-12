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
MAX_ENEMY_SPEED = 3
ALIEN_Y_DIMENSION = 400
ALIEN_HEIGHT = 55
PLAYER_WIDTH = 55
ALIEN_WIDTH = 55

class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = pygame.image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))

    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class Player(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)
        self.isDamaged = False

    def controls(self):
        global lastShotFired
        keys = pygame.key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]):
            if self.x > PLAYER_WIDTH:
                self.x -= PLAYER_SPEED
        elif (keys[K_RIGHT] or keys[K_d]):
            if self.x < GAME_WIDTH:
                self.x += PLAYER_SPEED
        elif (keys[K_SPACE]):
            if(time.time() > lastShotFired + PLAYER_SHOT_DELAY):
                player.shoot()

    def shoot(self):
        global lastShotFired
        lastShotFired = time.time()
        playerMissiles.append(PlayerMissile(player.x, player.y, 'data/player_missile.bmp'))

class Alien(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)
        self.alive = True
        self.canMove = random.choice([True, False])
        self.dx = random.randint(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.dy = self.dx
        self.width = ALIEN_WIDTH
        self.height = ALIEN_HEIGHT

    def movement(self):
        if (self.canMove == True):
            if (self.x + self.dx > GAME_WIDTH - self.width) or (self.x + self.dx < self.width):
                self.dx = -self.dx
            if(self.y + self.dy < self.width) or (self.y + self.dy > ALIEN_Y_DIMENSION):
                self.dy = -self.dy
            self.x += self.dx
            self.y += self.dy

class PlayerMissile(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)
        self.outOfBounds = False

    def update(self):
        if self.y < 0:
            self.outOfBounds = True

class AlienMissile(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)

def collisionDetection(s1_x, s1_y, s2_x, s2_y):
    if ((s1_x > s2_x - MISSILE_WIDTH) and
        (s1_x < s2_x + MISSILE_WIDTH) and
        (s1_y > s2_y - MISSILE_WIDTH) and
        (s1_y < s2_y + MISSILE_WIDTH)):
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
timeSincePlayerWasHit = time.time()

enemies = []
playerMissiles = []

x = 0
for count in range(INITIAL_ALIEN_COUNT):
    enemies.append(Alien(random.randint(ALIEN_WIDTH, GAME_WIDTH - ALIEN_WIDTH),
                         random.randint(ALIEN_HEIGHT, ALIEN_Y_DIMENSION),
                         'data/alien_1.bmp'))
    x += 1

player = Player(GAME_WIDTH/2, 500, 'data/player.bmp')
enemymissile = AlienMissile(0, GAME_HEIGHT, 'data/alien_missile.bmp')

while True:
    screen.blit(backdrop, (0, 0))

    # --- DRAWS ---

    for count in range(len(enemies)):
        enemies[count].movement()
        enemies[count].render()

    for count in range(len(playerMissiles)):
        playerMissiles[count].y += PLAYER_MISSILE_SPEED
        playerMissiles[count].render()

    if enemymissile.y >= GAME_HEIGHT and len(enemies) > 0:
        enemymissile.x = enemies[random.randint(0, len(enemies)-1)].x
        enemymissile.y = enemies[0].y

    # --- EVENTS ---

    if collisionDetection(player.x, player.y, enemymissile.x, enemymissile.y):
        if (player.isDamaged == False):
            player = Player(player.x, player.y, 'data/damagedplayer.bmp')
            player.isDamaged = True
        elif (player.isDamaged == True) and (time.time() > timeSincePlayerWasHit - 2):
            quit()
            sys.exit()

    for m in playerMissiles:
        for e in enemies:
            if collisionDetection(m.x, m.y, e.x, e.y):
                m.outOfBounds = True
                e.alive = False

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

    enemies = [e for e in enemies if e.alive]

    enemymissile.render()
    enemymissile.y += ENEMY_MISSILE_SPEED

    player.render()
    player.controls()

    pygame.display.update()
    FPSCLOCK.tick(FPS)
