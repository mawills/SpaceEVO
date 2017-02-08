from pygame import *
import random

GAME_WIDTH = 800
GAME_HEIGHT = 600
INITIAL_ALIEN_COUNT = 10
MISSILE_WIDTH = 26
PLAYER_SPEED = 5
PLAYER_MISSILE_SPEED = -3
PLAYER_SHOT_DELAY = 400
ENEMY_MISSILE_SPEED = 2
ENEMY_SPEED = 1

class Sprite:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class Player:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class PlayerMissile:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class Alien:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

class AlienMissile:
    def __init__(self, xpos, ypos, filename):
        self.x = xpos
        self.y = ypos
        self.bitmap = image.load(filename)
        self.bitmap.set_colorkey((255, 0, 128))
    def render(self):
        screen.blit(self.bitmap, (self.x, self.y))

# s1 is player/alien sprite, s2 is player missile/alien missle sprite
def collisionDetection(s1_x, s1_y, s2_x, s2_y):
    if (s1_x > s2_x - MISSILE_WIDTH) and (s1_x < s2_x + MISSILE_WIDTH) and (s1_y > s2_y - MISSILE_WIDTH) and (s1_y < s2_y + MISSILE_WIDTH):
        return 1
    else:
        return 0

init()
screen = display.set_mode((GAME_WIDTH,GAME_HEIGHT))
key.set_repeat(1, 1)
display.set_caption('SpaceEVO')
backdrop = image.load('data/sevobackground.bmp')


enemies = []
playerMissiles = []
lastShotFired = time.get_ticks()

x = 0
for count in range(INITIAL_ALIEN_COUNT):
    enemies.append(Sprite(50 * x + 50, 50, 'data/alien_1.bmp'))
    x += 1

player = Player(GAME_WIDTH/2, 500, 'data/player.bmp')
ourmissile = PlayerMissile(0, GAME_HEIGHT, 'data/player_missile.bmp')
enemymissile = AlienMissile(0, GAME_HEIGHT, 'data/alien_missile.bmp')

while True:
    screen.blit(backdrop, (0, 0))

    # Move and render aliens
    for count in range(len(enemies)):
        enemies[count].x += ENEMY_SPEED
        enemies[count].render()

    # Move and render player missiles
    for count in range(len(playerMissiles)):
        playerMissiles[count].y += PLAYER_MISSILE_SPEED
        playerMissiles[count].render()

  # Aliens reach left or right edge
    if enemies[len(enemies)-1].x > GAME_WIDTH or enemies[0].x < 10:
        ENEMY_SPEED = -ENEMY_SPEED
        for count in range(len(enemies)):
            enemies[count].y += 5

  # Render enemy missile if on screen
    if enemymissile.y >= GAME_HEIGHT and len(enemies) > 0:
        enemymissile.x = enemies[random.randint(0, len(enemies)-1)].x
        enemymissile.y = enemies[0].y

  # Player is hit
    if collisionDetection(player.x, player.y, enemymissile.x, enemymissile.y):
        pygame.quit()
        sys.exit()

  # Alien is hit
    for count in range(0, len(enemies)):
        if collisionDetection(enemies[count].x, enemies[count].y, ourmissile.x, ourmissile.y):
            del enemies[count]
            break

  # Out of Aliens
    if len(enemies) == 0:
        pygame.quit()
        sys.exit()

  # Handle keyboard input
    for ourevent in event.get():
        if ourevent.type == QUIT:
            pygame.quit()
            sys.exit()
    if ourevent.type == KEYDOWN:
        if ourevent.key == K_RIGHT and player.x < GAME_WIDTH:
            player.x += PLAYER_SPEED
        if ourevent.key == K_LEFT and player.x > 10:
            player.x -= PLAYER_SPEED
        if ourevent.key == K_SPACE:
            if time.get_ticks() > lastShotFired + PLAYER_SHOT_DELAY:
                lastShotFired = time.get_ticks()
                playerMissiles.append(PlayerMissile(player.x, player.y, 'data/player_missile.bmp'))


    enemymissile.render()
    enemymissile.y += ENEMY_MISSILE_SPEED

    player.render()

    display.update()
    time.delay(5)
