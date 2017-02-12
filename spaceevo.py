import random, time, pygame, sys
from pygame.locals import *

FPS = 60
GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_HEIGHT = 55
PLAYER_WIDTH = 55
ALIEN_HEIGHT = 55
ALIEN_WIDTH = 55
MISSILE_WIDTH = 26
ALIEN_Y_DIMENSION = 400
INITIAL_ALIEN_COUNT = 10
PLAYER_SPEED = 7
MAX_ENEMY_SPEED = 3
PLAYER_MISSILE_SPEED = -6
ENEMY_MISSILE_SPEED = 6
PLAYER_SHOT_FREQUENCY = 0.35
ALIEN_ATTACK_FREQUENCY = 60
START_GAME_ATTACK_DELAY = 1.5
MAX_ALIEN_AGE = 50

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
            if self.x > 0:
                self.x -= PLAYER_SPEED
        elif (keys[K_RIGHT] or keys[K_d]):
            if self.x < GAME_WIDTH - PLAYER_WIDTH:
                self.x += PLAYER_SPEED
        elif (keys[K_SPACE]):
            if(time.time() > lastShotFired + PLAYER_SHOT_FREQUENCY):
                player.shoot()

    def shoot(self):
        global lastShotFired
        lastShotFired = time.time()
        playerMissiles.append(Missile(player.x, player.y, 'data/player_missile.bmp'))

class Alien(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)
        self.alive = True
        self.canMove = random.choice([True, False])
        self.canAttack = random.choice([True, False])
        self.attackDice = None
        self.dx = random.randint(-MAX_ENEMY_SPEED, MAX_ENEMY_SPEED)
        self.dy = self.dx
        self.width = ALIEN_WIDTH
        self.height = ALIEN_HEIGHT
        self.timeCreated = time.time()
        self.age = None

    def movement(self):
        if (self.canMove == True):
            if (self.x + self.dx > GAME_WIDTH - self.width) or (self.x + self.dx < self.width):
                self.dx = -self.dx
            if(self.y + self.dy < self.width) or (self.y + self.dy > ALIEN_Y_DIMENSION):
                self.dy = -self.dy
            self.x += self.dx
            self.y += self.dy

    def shoot(self):
        enemyMissiles.append(Missile(self.x, self.y, 'data/alien_missile.bmp'))

    def update(self):
        self.age = time.time() - self.timeCreated
        self.attackDice = random.randint(0, ALIEN_ATTACK_FREQUENCY)
        if (self.age >= MAX_ALIEN_AGE):
            self.alive = False
        if self.canAttack:
            self.bitmap = pygame.image.load('data/alien_attack.bmp')
            self.bitmap.set_colorkey((255, 0, 128))
            if (self.attackDice == ALIEN_ATTACK_FREQUENCY) and (self.age > START_GAME_ATTACK_DELAY):
                self.shoot()

class Missile(Sprite):
    def __init__(self, xpos, ypos, filename):
        Sprite.__init__(self, xpos, ypos, filename)
        self.outOfBounds = False

    def checkBounds(self):
        if self.y < 0:
            self.outOfBounds = True

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
mothership = Sprite(0, 0, 'data/mothership.bmp')

enemies = []
playerMissiles = []
enemyMissiles = []

x = 0
for count in range(INITIAL_ALIEN_COUNT):
    enemies.append(Alien(random.randint(ALIEN_WIDTH, GAME_WIDTH - ALIEN_WIDTH),
                         random.randint(ALIEN_HEIGHT, ALIEN_Y_DIMENSION),
                         'data/alien.bmp'))
    x += 1

player = Player(GAME_WIDTH/2, 500, 'data/player.bmp')

while True:
    screen.blit(backdrop, (0, 0))
    mothership.render()

    # --- DRAWS ---

    for count in range(len(enemies)):
        enemies[count].movement()
        enemies[count].render()

    for count in range(len(playerMissiles)):
        playerMissiles[count].y += PLAYER_MISSILE_SPEED
        playerMissiles[count].render()

    for count in range(len(enemyMissiles)):
        enemyMissiles[count].y += ENEMY_MISSILE_SPEED
        enemyMissiles[count].render()

    # --- EVENTS ---

    for m in enemyMissiles:
        if collisionDetection(player.x, player.y, m.x, m.y):
            if (player.isDamaged == False):
                player = Player(player.x, player.y, 'data/damagedplayer.bmp')
                player.isDamaged = True
                timeSincePlayerWasHit = time.time()
            elif (player.isDamaged == True) and (time.time() > timeSincePlayerWasHit + 2):
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
        m.checkBounds()
    playerMissiles = [m for m in playerMissiles if not m.outOfBounds]

    for m in enemyMissiles:
        m.checkBounds()
    enemyMissiles = [m for m in enemyMissiles if not m.outOfBounds]

    enemies = [e for e in enemies if e.alive]

    for e in enemies:
        e.update()

    player.render()
    player.controls()



    pygame.display.update()
    FPSCLOCK.tick(FPS)
