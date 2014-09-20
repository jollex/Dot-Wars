import pygame, random, sys, math
from pygame.locals import *

gameName = 'Dot Wars'

# game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
PLAYER_SPEED = 10
SPEED_BOOST = 4
SHOT_SPEED = 20
ENEMY_SPEED = 5
PLAYER_RADIUS = 15
ENEMY_RADIUS = 10
POWERUP_RADIUS = 15
SHOT_RADIUS = 4
ENEMY_HEALTH = 3
PLAYER_HEALTH = 1
SHOOTING_RATE = 2
FPS = 30
TEXT_COLOR = (51, 27, 16)
SHOTGUN_SPREAD = 6
FONT_SIZE = 32
BIG_FONT_SIZE = 56
TITLE_FONT_SIZE = 128

# enemy spawning constants
SPAWN_BUFFER = 100
BLOCK_SWITCH_RATE = 10 * FPS
ENEMY_MIN_SPAWN_TIME = .5 * FPS
ENEMY_MAX_SPAWN_TIME = 2.5 * FPS

# powerup spawning constants
DESPAWN_TIME = 8 * FPS
POWERUP_TIME = 12 * FPS
POWERUP_MIN_SPAWN_TIME = 15 * FPS
POWERUP_MAX_SPAWN_TIME = 30 * FPS
NUMBER_OF_POWERUPS = 3
POWERUP_NAMES = {1:'speed', 2:'shotgun', 3:'shield'}


# image files
backgroundFile = 'res/background.png'
playerFile = 'res/player.png'
playerAngleFile = 'res/player-angle.png'
playerShield = 'res/player-shield.png'
shotFile = 'res/shot.png'
enemyFile = 'res/enemy.png'
speedFile = 'res/speed.png'
shotgunFile = 'res/shotgun.png'
shieldFile = 'res/shield.png'
startFile = 'res/start.png'
menuFile = 'res/menu.png'

# sound files
soundtrackFile = 'res/soundtrack.ogg'
enemyDeathFile = 'res/enemy-death.wav'
powerupFile = 'res/powerup.wav'
shotSoundFile = 'res/shot.wav'
shotgunSoundFile = 'res/shotgun.wav'
clickFile = 'res/click.wav'

class Player():
    # initialize the player's many variables
    def __init__(self, surface):
        self.surface = surface
        self.centerX = surface.get_width() / 2
        self.centerY = surface.get_height() / 2
        self.image = pygame.image.load(playerFile)
        self.shieldImage = pygame.image.load(playerShield)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = self.centerX - self.width / 2
        self.y = self.centerY - self.height / 2
        self.direction = (0, -1)
        self.shots = []
        self.powerups = []
        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False
        self.shooting = False
        self.shotCounter = 0
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.shotgun = False
        self.shield = False

    # handle events
    def event(self, e):
        # if player presses arrow or WASD key, moves in that direction
        if e.type == KEYDOWN:
            if e.key == K_LEFT or e.key == ord('a'):
                self.moveLeft = True
                self.moveRight = False
            if e.key == K_RIGHT or e.key == ord('d'):
                self.moveLeft = False
                self.moveRight = True
            if e.key == K_UP or e.key == ord('w'):
                self.moveUp = True
                self.moveDown = False
            if e.key == K_DOWN or e.key == ord('s'):
                self.moveUp = False
                self.moveDown = True
        # stops moving if the key is released
        if e.type == KEYUP:
            if e.key == K_LEFT or e.key == ord('a'):
                self.moveLeft = False
            if e.key == K_RIGHT or e.key == ord('d'):
                self.moveRight = False
            if e.key == K_UP or e.key == ord('w'):
                self.moveUp = False
            if e.key == K_DOWN or e.key == ord('s'):
                self.moveDown = False
        # player shoots if left mouse button is clicked
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            self.shooting = True
        # stops shooting if it's released
        if e.type == MOUSEBUTTONUP and e.button == 1:
            self.shooting = False
        # updates the direction the player is facing when the mouse is moved
        if e.type == MOUSEMOTION:
            self.direction = (e.pos[0], e.pos[1])

    def update(self):
        # iterates through each powerup the player has
        for powerup in list(self.powerups):
            # applies powerup effects
            if powerup.name == 'speed':
                self.speed = PLAYER_SPEED + SPEED_BOOST
            elif powerup.name == 'shotgun':
                self.shotgun = True
            elif powerup.name == 'shield':
                self.shield = True

            # updates the powerup's remaining time
            powerup.powerupTime -= 1

            # if powerup is out of time, removes the powerup and its effect
            if powerup.powerupTime <= 0:
                if powerup.name == 'speed':
                    player.speed = PLAYER_SPEED
                elif powerup.name == 'shotgun':
                    player.shotgun = False
                elif powerup.name == 'shield':
                    player.shield == False
                self.powerups.remove(powerup)

        # moves the player
        if self.moveLeft and self.centerX > PLAYER_RADIUS:
            if self.centerX - self.speed < PLAYER_RADIUS:
                self.centerX = PLAYER_RADIUS
            else:
                self.centerX -= self.speed
        if self.moveRight and self.centerX + PLAYER_RADIUS < WINDOW_WIDTH:
            if self.centerX + self.speed > WINDOW_WIDTH - PLAYER_RADIUS:
                self.centerX = WINDOW_WIDTH - PLAYER_RADIUS
            else:
                self.centerX += self.speed
        if self.moveUp and self.centerY > PLAYER_RADIUS:
            if self.centerY - self.speed < PLAYER_RADIUS:
                self.centerY = PLAYER_RADIUS
            else:
                self.centerY -= self.speed
        if self.moveDown and self.centerY + PLAYER_RADIUS < WINDOW_HEIGHT:
            if self.centerY + self.speed > WINDOW_HEIGHT - PLAYER_RADIUS:
                self.centerY = WINDOW_HEIGHT - PLAYER_RADIUS
            else:
                self.centerY += self.speed

        # updates player's top-left coordinate as well
        self.x = self.centerX - self.width / 2
        self.y = self.centerY - self.height / 2

        # moves all shots
        for shot in self.shots:
            shot.x += shot.vx
            shot.y += shot.vy
            shot.centerX += shot.vx
            shot.centerY += shot.vy

        # updates player's angle
        x = self.centerX - self.direction[0]
        y = self.centerY - self.direction[1]
        angle = ((180 * (math.atan2(y, x) / math.pi)) - 90) % 360

        # changes player's image according to angle
        if angle > 337.5 or angle <= 22.5:
            self.image = pygame.image.load(playerFile)
        elif angle <= 67.5:
            self.image = pygame.image.load(playerAngleFile)
        elif angle <= 112.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerFile), -90)
        elif angle <= 157.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerAngleFile), -90)
        elif angle <= 202.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerFile), -180)
        elif angle <= 247.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerAngleFile), -180)
        elif angle <= 292.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerFile), -270)
        elif angle <= 337.5:
            self.image = pygame.transform.rotate(pygame.image.load(playerAngleFile), -270)

        # spawns shot if player is shooting
        self.shotCounter += 1
        if self.shooting and self.shotCounter >= SHOOTING_RATE:
            self.shotCounter = 0

            # if the shotgun powerup is in effect, shoots 3 shots
            if self.shotgun:
                radians1 = math.radians(SHOTGUN_SPREAD)
                radians2 = math.radians(-SHOTGUN_SPREAD)
                cos1 = math.cos(radians1)
                sin1 = math.sin(radians1)
                cos2 = math.cos(radians2)
                sin2 = math.sin(radians2)

                x1 = self.direction[0] * cos1 - self.direction[1] * sin1
                y1 = self.direction[0] * sin1 + self.direction[1] * cos1
                x2 = self.direction[0] * cos2 - self.direction[1] * sin2
                y2 = self.direction[0] * sin2 + self.direction[1] * cos2

                shot1 = Shot(self.centerX, self.centerY, x1, y1)
                shot2 = Shot(self.centerX, self.centerY, x2, y2)
                shot3 = Shot(self.centerX, self.centerY, self.direction[0], self.direction[1])

                self.shots.append(shot1)
                self.shots.append(shot2)
                self.shots.append(shot3)

                shotgunSound.play()
            # otherwise, shoots one
            else:
                shot = Shot(self.centerX, self.centerY, self.direction[0], self.direction[1])
                self.shots.append(shot)

                shotSound.play()

        # removes all shots that are out of the screen
        for shot in list(self.shots):
            if shot.x < 0 or shot.x > WINDOW_WIDTH or shot.y < 0 or shot.y > WINDOW_HEIGHT:
                self.shots.remove(shot)

    def draw(self):
        # draws each shot
        for shot in self.shots:
            self.surface.blit(shot.image, (shot.x, shot.y))

        # draws the player
        for powerup in self.powerups:
            # overlays the player over the shield image if the player
            # has the shield powerup
            if powerup.name == 'shield':
                if powerup.powerupTime < 2 * FPS:
                    if powerup.powerupTime % 8 < 4:
                        self.surface.blit(self.shieldImage, (self.x, self.y))
                else:
                    self.surface.blit(self.shieldImage, (self.x, self.y))
        self.surface.blit(self.image, (self.x, self.y))

class Shot():
    # initializes the shot
    def __init__(self, x, y, destX, destY):
        self.image = pygame.image.load(shotFile)
        self.centerX = x
        self.centerY = y
        self.x = self.centerX - self.image.get_width() / 2
        self.y = self.centerY - self.image.get_height() / 2

        # shot's velocity depends on where the shot is aimed at
        d = SHOT_SPEED / distance((self.centerX, self.centerY), (destX, destY))
        self.vx = (destX - self.centerX) * d
        self.vy = (destY - self.centerY) * d

class Enemy():
    # initializes the enemy
    def __init__(self, x, y):
        self.image = pygame.image.load(enemyFile)
        self.centerX = x
        self.centerY = y
        self.x = self.centerX - self.image.get_width() / 2
        self.y = self.centerY - self.image.get_height() / 2
        self.vx = self.vy = 0
        self.direction = (0, -1)
        self.health = ENEMY_HEALTH

    def update(self, destX, destY):
        # update velocities to be moving towards player
        if distance((self.centerX, self.centerY), (destX, destY)) <= ENEMY_SPEED:
            d = 0
        else:
            d = ENEMY_SPEED / distance((self.centerX, self.centerY), (destX, destY))
        self.vx = (destX - self.centerX) * d
        self.vy = (destY - self.centerY) * d

        # update position
        self.centerX += self.vx
        self.centerY += self.vy
        self.x += self.vx
        self.y += self.vy

class Powerup():
    # initializes the powerup
    def __init__(self, name, x, y):
        self.centerX = x
        self.centerY = y
        self.despawnTime = DESPAWN_TIME
        self.powerupTime = POWERUP_TIME
        self.name = name
        self.image = pygame.image.load('res/' + name + '.png')
        self.x = self.centerX - self.image.get_width() / 2
        self.y = self.centerY - self.image.get_width() / 2

    # updates the powerup
    def update(self):
        # decreases the powerups time left before it despawns
        self.despawnTime -= 1

# updates everything in the world
def updateWorld(player, enemies, powerups):
    global alive, enemiesKilled, enemyKillsNeeded, duringLevel

    # updates the player
    player.update()

    # decreases the health of the player if the player is touching and enemy
    # and doesn't have a shield
    for enemy in enemies:
        enemy.update(player.centerX, player.centerY)
        if distance((enemy.centerX, enemy.centerY), (player.centerX, player.centerY)) < ENEMY_RADIUS + PLAYER_RADIUS and not player.shield:
            player.health -= 1

    # updates all powerups and removes ones that have run out of time,
    # also checks if a powerup is within range of the player and gets picked
    # up if it is
    for powerup in list(powerups):
        powerup.update()
        if powerup.despawnTime <= 0:
            powerups.remove(powerup)
        if distance((powerup.centerX, powerup.centerY), (player.centerX, player.centerY)) < POWERUP_RADIUS + PLAYER_RADIUS:
            powerupSound.play()
            powerups.remove(powerup)
            player.powerups.append(powerup)

    checkCollisions()
    removeDeadEnemies()
    spawnPowerups()
    spawnEnemies()

    # if the player's health drops to 0, ends the game
    if player.health <= 0:
        alive = False

    # if the player has killed enough enemies, ends the level
    if enemiesKilled == enemyKillsNeeded:
        duringLevel = False

# checks if any of the enemies are hit by shots
def checkCollisions():
    global enemies, player

    # if any of the shots hits an enemy, it decreases the enemy's health
    # and removes that shot
    for e in enemies:
        for shot in list(player.shots):
            if distance((e.centerX, e.centerY), (shot.centerX, shot.centerY)) < SHOT_RADIUS + ENEMY_RADIUS:
                e.health -= 1
                player.shots.remove(shot)

# removes any dead enemies
def removeDeadEnemies():
    global enemies, enemiesKilled

    # if an enemies health is zero or lower, it gets removed and the counter
    # for enemies killed is incremented
    for e in list(enemies):
        if e.health <= 0:
            enemyDeathSound.play()
            enemies.remove(e)
            enemiesKilled += 1

# spawns enemies at random intervals
def spawnEnemies():
    global timeSinceLastSwitch, timeSinceLastSpawn, block, spawnRate, enemies

    # increments the time since the last enemy was spawned and the time
    # since the spawning block last changed
    timeSinceLastSwitch += 1
    timeSinceLastSpawn += 1

    # if it's time to switch spawning blocks, it chooses a random one
    if timeSinceLastSwitch >= BLOCK_SWITCH_RATE:
        timeSinceLastSwitch = 0
        block = random.randint(1, 4)

    # if it's time to spawn a new enemy it spawns one in the current spawning
    # block and changes the time needed before the next spawn to a random
    # number between the minimum and maximum enemy spawning times
    if timeSinceLastSpawn >= spawnRate:
        timeSinceLastSpawn = 0
        spawnRate = random.randint(ENEMY_MIN_SPAWN_TIME, ENEMY_MAX_SPAWN_TIME)
        randomSpawn(block)

# spawns on enemy in the given block
def randomSpawn(spawningBlock):
    global enemies

    # intializes the x and y coordinates of the enemy to be spawned
    x = y = 0

    # picks a random x and y position for the enemy to spawn in the
    # appropriate block
    if spawningBlock == 1:
        x = random.randint(ENEMY_RADIUS, WINDOW_WIDTH - ENEMY_RADIUS)
        y = -ENEMY_RADIUS
    elif spawningBlock == 2:
        x = WINDOW_WIDTH + ENEMY_RADIUS
        y = random.randint(ENEMY_RADIUS, WINDOW_HEIGHT - ENEMY_RADIUS)
    elif spawningBlock == 3:
        x = random.randint(ENEMY_RADIUS, WINDOW_WIDTH - ENEMY_RADIUS)
        y = WINDOW_HEIGHT + ENEMY_RADIUS
    elif spawningBlock == 4:
        x = -ENEMY_RADIUS
        y = random.randint(ENEMY_RADIUS, WINDOW_HEIGHT - ENEMY_RADIUS)

    # if the potential spawning coordinate is too close to the player,
    # calls itself again to find a better spot, otherwise spawn an enemy
    # at the coordinate
    if distance((x, y), (player.centerX, player.centerY)) < SPAWN_BUFFER:
        randomSpawn(spawningBlock)
    else:
        enemies.append(Enemy(x, y))

# spawns powerups at random intervals
def spawnPowerups():
    global timeSinceLastPowerup, powerupSpawnRate, POWERUP_NAMES, powerups

    # increments the time since the last powerup was spawned
    timeSinceLastPowerup += 1

    # if it's time to spawn a powerup, picks a random location on the screen
    # and a random powerup out of the list of powerups and adds the new
    # powerup to the list of powerups in the world
    # also changes the time it will take to spawn the next powerup
    if timeSinceLastPowerup == powerupSpawnRate:
        timeSinceLastPowerup = 0
        powerupSpawnRate = random.randint(POWERUP_MIN_SPAWN_TIME, POWERUP_MAX_SPAWN_TIME)

        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        name = random.randint(1, NUMBER_OF_POWERUPS)

        powerups.append(Powerup(POWERUP_NAMES[name], x, y))

# simple helper function to calculate the distance between two points
def distance(pos, dest):
    return math.sqrt((pos[0] - dest[0]) ** 2 + (pos[1] - dest[1]) ** 2)

# start screen
def waitForStart():
    mainClock.tick(FPS)

    # displays start screen
    start = pygame.image.load(startFile)
    startRect = start.get_rect()
    startRect.center = (WINDOW_WIDTH  / 2, WINDOW_HEIGHT/ 2)

    titleFont = pygame.font.Font('res/AGaramondPro-Bold.otf', TITLE_FONT_SIZE)
    titleText = titleFont.render(gameName, 1, TEXT_COLOR)
    titleRect = titleText.get_rect()
    titleRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 5)

    windowSurface.blit(background, (0, 0))
    windowSurface.blit(titleText, titleRect)
    windowSurface.blit(start, startRect)
    pygame.display.update()

    # waits for player to click on start button
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if e.type == MOUSEBUTTONDOWN and e.button == 1 and startRect.collidepoint(e.pos):
                clickSound.play()
                return

# death screen
def playerDied():
    global enemiesKilled, enemyKillsNeeded,  level, alive, highScore

    # stops the music
    pygame.mixer.music.stop()

    # updates high score
    if enemiesKilled > highScore:
        highScore = enemiesKilled

    # resets game variables for amount of enemies killed, what level the
    # player is on, and sets the player to alive so the game loop can
    # run again
    enemiesKilled = 0
    enemyKillsNeeded = 10
    level = 1
    alive = True

    # displays game over text and instructions
    gameOverText = font.render('GAME OVER', 1, TEXT_COLOR)
    gameOverRect = gameOverText.get_rect()
    gameOverRect.centerx = WINDOW_WIDTH / 2
    gameOverRect.bottom = (WINDOW_HEIGHT / 2) - 5
    clickText = font.render('Click to play again', 1, TEXT_COLOR)
    clickRect = clickText.get_rect()
    clickRect.centerx = WINDOW_WIDTH / 2
    clickRect.top = (WINDOW_HEIGHT / 2) + 5
    highScoreText = font.render('High Score: %s' % highScore, 1, TEXT_COLOR)
    highScoreRect = highScoreText.get_rect()
    highScoreRect.centerx = (WINDOW_WIDTH / 2)
    highScoreRect.centery = (WINDOW_HEIGHT / 4)

    windowSurface.blit(highScoreText, highScoreRect)
    windowSurface.blit(gameOverText, gameOverRect)
    windowSurface.blit(clickText, clickRect)

    pygame.display.update()

    # waits for player to click
    while True:
        mainClock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                pygame.mixer.music.play(-1)
                return

# pause screen
def pauseScreen():
    global white

    # stop music
    pygame.mixer.music.pause()

    # displays the resume and quit buttons
    resume = pygame.image.load(menuFile)
    resumeRect = resume.get_rect()
    resumeRect.centerx = WINDOW_WIDTH / 2
    resumeRect.bottom = (WINDOW_HEIGHT / 2) - 5
    quit = pygame.image.load(menuFile)
    quitRect = quit.get_rect()
    quitRect.centerx = WINDOW_WIDTH / 2
    quitRect.top = (WINDOW_HEIGHT / 2) + 5

    # overlays the text over the buttons
    fontBig = pygame.font.Font("res/freesansbold.ttf", BIG_FONT_SIZE)
    resumeText = fontBig.render('Resume', 1, TEXT_COLOR)
    resumeTextRect = resumeText.get_rect()
    resumeTextRect.center = resumeRect.center
    quitText = fontBig.render('Quit', 1, TEXT_COLOR)
    quitTextRect = quitText.get_rect()
    quitTextRect.center = quitRect.center

    # displays the current high score
    highScoreText = font.render('High Score: %s' % highScore, 1, TEXT_COLOR)
    highScoreRect = highScoreText.get_rect()
    highScoreRect.centerx = (WINDOW_WIDTH / 2)
    highScoreRect.centery = (WINDOW_HEIGHT / 4)

    windowSurface.blit(white, (0, 0))
    windowSurface.blit(resume, resumeRect)
    windowSurface.blit(quit, quitRect)
    windowSurface.blit(resumeText, resumeTextRect)
    windowSurface.blit(quitText, quitTextRect)
    windowSurface.blit(highScoreText, highScoreRect)

    pygame.display.update()

    # waits for the player to click a button
    while True:
        mainClock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pygame.mixer.music.unpause()
                    return
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                if resumeRect.collidepoint(e.pos):
                    clickSound.play()
                    pygame.mixer.music.unpause()
                    return
                if quitRect.collidepoint(e.pos):
                    clickSound.play()
                    pygame.quit()
                    sys.exit()

# in between levels screen
def nextLevel():
    global level, enemiesKilled, enemyKillsNeeded, duringLevel, white, ENEMY_MIN_SPAWN_TIME, ENEMY_MAX_SPAWN_TIME, BLOCK_SWITCH_RATE

    # makes enemies spawn faster and switch spawning block sooner
    if ENEMY_MIN_SPAWN_TIME > .1 * FPS:
        ENEMY_MIN_SPAWN_TIME -= 5
    if ENEMY_MAX_SPAWN_TIME > .5 * FPS:
        ENEMY_MAX_SPAWN_TIME -= 10
    if BLOCK_SWITCH_RATE > 2 * FPS:
        BLOCK_SWITCH_RATE -= 2

    # adds 1 to the level the player is on, increments the amount of
    # enemies that need to be killed to advance, and says that the player
    # is in a level so the game loop can run
    level += 1
    enemyKillsNeeded += 5 + enemiesKilled
    duringLevel = True

    # displays instructions to continue
    windowSurface.blit(white, (0, 0))

    continueText = font.render('Click to continue to level %s' % level, 1, TEXT_COLOR)
    continueRect = continueText.get_rect()
    continueRect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    windowSurface.blit(continueText, continueRect)

    pygame.display.update()

    # waits for player to click
    while True:
        mainClock.tick(FPS)

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                return

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(gameName)

# set up sounds
pygame.mixer.init()
pygame.mixer.music.load(soundtrackFile)
enemyDeathSound = pygame.mixer.Sound(enemyDeathFile)
enemyDeathSound.set_volume(.8)
powerupSound = pygame.mixer.Sound(powerupFile)
powerupSound.set_volume(.5)
shotSound = pygame.mixer.Sound(shotSoundFile)
shotSound.set_volume(.2)
shotgunSound = pygame.mixer.Sound(shotgunSoundFile)
shotgunSound.set_volume(.2)
clickSound = pygame.mixer.Sound(clickFile)

# sets up font used for making text
font = pygame.font.Font("res/freesansbold.ttf", FONT_SIZE)

# loads background image and transparent image
background = pygame.image.load(backgroundFile)
white = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
white.fill((255, 255, 255))
white.set_alpha(64)

waitForStart()

# intializes game variables
alive = True
duringLevel = True
level = 1
enemiesKilled = 0
enemyKillsNeeded = 10
highScore = 0

# start music
pygame.mixer.music.play(-1)

# game loop
while True:
    mainClock.tick(FPS)

    # initialize player, enemies, powerups, and their variables
    player = Player(windowSurface)
    enemies = []
    powerups = []
    spawnRate = ENEMY_MIN_SPAWN_TIME
    block = 1
    timeSinceLastSwitch = 0
    timeSinceLastSpawn = 0
    powerupSpawnRate = POWERUP_MIN_SPAWN_TIME
    timeSinceLastPowerup = 0

    # level loop
    while alive and duringLevel:
        mainClock.tick(FPS)

        # handles events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # pauses the game if the player presses ESC
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pauseScreen()
                player.shooting = False
                player.moveDown = player.moveLeft = player.moveRight = player.moveUp = False
            player.event(event)

        # updates components of the world
        updateWorld(player, enemies, powerups)

        # draws the world and its components
        windowSurface.blit(background, (0, 0))
        player.draw()
        for enemy in enemies:
            windowSurface.blit(enemy.image, (enemy.x, enemy.y))
        for powerup in powerups:
            windowSurface.blit(powerup.image, (powerup.x, powerup.y))

        # displays the level counter
        levelText = font.render('Level %s' % level, 1, TEXT_COLOR)
        windowSurface.blit(levelText, (0, 1))

        # displays the kill counter
        enemiesText = font.render('Enemies Killed: %s' % enemiesKilled, 1, TEXT_COLOR)
        enemiesRect = enemiesText.get_rect()
        enemiesRect.topleft = (WINDOW_WIDTH / 2, 1)
        windowSurface.blit(enemiesText, enemiesRect)

        pygame.display.update()

    # if loop ended because player died, displays death screen
    if not alive:
        playerDied()
    # if loop ended because player finished level, displays next level screen
    if not duringLevel:
        nextLevel()
