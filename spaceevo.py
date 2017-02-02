from pygame import *
import random

SPRITE_WIDTH = 32
GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_SPEED = 5
PLAYER_MISSILE_SPEED = -5
ENEMY_MISSILE_SPEED = 5
ENEMY_SPEED = 3

class Sprite:
	def __init__(self, xpos, ypos, filename):
		self.x = xpos
		self.y = ypos
		self.bitmap = image.load(filename)
		self.bitmap.set_colorkey((255, 0, 128))
	def set_position(self, xpos, ypos):
		self.x = xpos
		self.y = ypos
	def render(self):
		screen.blit(self.bitmap, (self.x, self.y))

def collisionDetection(s1_x, s1_y, s2_x, s2_y):
        if (s1_x > s2_x - SPRITE_WIDTH) and (s1_x < s2_x + SPRITE_WIDTH) and (s1_y > s2_y - SPRITE_WIDTH) and (s1_y < s2_y + SPRITE_WIDTH):
                return 1
        else:
                return 0

init()
screen = display.set_mode((GAME_WIDTH,GAME_HEIGHT))
key.set_repeat(1, 1)
display.set_caption('SpaceEVO')
backdrop = image.load('data/sevobackground.bmp')


enemies = []

x = 0
for count in range(10):
  enemies.append(Sprite(50 * x + 50, 50, 'data/alien_1.bmp'))
  x += 1

player = Sprite(20, 400, 'data/player.bmp')
ourmissile = Sprite(0, GAME_HEIGHT, 'data/player_missile.bmp')
enemymissile = Sprite(0, GAME_HEIGHT, 'data/alien_missile.bmp')

quit = 0
ENEMY_SPEED = 3

while quit == 0:
  screen.blit(backdrop, (0, 0))

  # Initialize and render aliens
  for count in range(len(enemies)):
    enemies[count].x += ENEMY_SPEED
    enemies[count].render()

  # Aliens reach right edge
  if enemies[len(enemies)-1].x > GAME_WIDTH:
    ENEMY_SPEED = -ENEMY_SPEED
    for count in range(len(enemies)):
      enemies[count].y += 5

  # Aliens reach left edge
  if enemies[0].x < 10:
    ENEMY_SPEED = -ENEMY_SPEED
    for count in range(len(enemies)):
      enemies[count].y += 5

  # Render player missile if on screen
  if ourmissile.y < GAME_HEIGHT-1 and ourmissile.y > 0:
    ourmissile.render()
    ourmissile.y += PLAYER_MISSILE_SPEED

  # Render enemy missile if on screen
  if enemymissile.y >= GAME_HEIGHT and len(enemies) > 0:
    enemymissile.x = enemies[random.randint(0, len(enemies)-1)].x
    enemymissile.y = enemies[0].y

  # Player is hit
  if collisionDetection(player.x, player.y, enemymissile.x, enemymissile.y):
    quit = 1

  # Alien is hit
  for count in range(0, len(enemies)):
    if collisionDetection(ourmissile.x, ourmissile.y, enemies[count].x, enemies[count].y):
      del enemies[count]
      break

  # Out of Aliens
  if len(enemies) == 0:
    quit = 1

  # Handle keyboard input
  for ourevent in event.get():
    if ourevent.type == QUIT:
      quit == 1
    if ourevent.type == KEYDOWN:
      if ourevent.key == K_RIGHT and player.x < GAME_WIDTH:
        player.x += PLAYER_SPEED
      if ourevent.key == K_LEFT and player.x > 10:
        player.x -= PLAYER_SPEED
      if ourevent.key == K_SPACE:
        ourmissile.x = player.x
        ourmissile.y = player.y

  enemymissile.render()
  enemymissile.y += ENEMY_MISSILE_SPEED

  player.render()

  display.update()
  time.delay(5)
