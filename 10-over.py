import pygame
import math
import random
import time

pygame.init()
# Variable Definition & Asset Loading
# Game Screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Background
background = pygame.image.load("./media/level0/stars.png")

# Sound
pygame.mixer.music.load("./media/level0/background.wav")
pygame.mixer.music.play(-1)

# Player
playerImg = pygame.image.load("./media/level0/spaceship.png")
playerX = 370
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImgFile = pygame.image.load("./media/level0/ufo.png")
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6  # Change this to change MAX number of enemies

# Bullet
bulletImg = pygame.image.load("./media/level0/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score Board
score_value = 0
font = pygame.font.Font("./fonts/Square.ttf", 24)
textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font("./fonts/Square.ttf", 128)  # create the font for game over
level_won_font = pygame.font.Font("./fonts/Square.ttf", 128)


def depopulate_array(arr):
    i = 0
    while i < len(arr):
        arr.pop(i)


def create_enemy_list(total_enemy):
    depopulate_array(enemyImg)
    depopulate_array(enemyX)
    depopulate_array(enemyY)
    depopulate_array(enemyX_change)
    depopulate_array(enemyY_change)

    for x in range(total_enemy):
        enemyImg.append(enemyImgFile)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)


# Function to swap the assets of the game from one folder to another
def swap_assets(level_number):
    global background, playerImg, enemyImgFile, bulletImg

    # Swap Image assets to ones stored in a new level assets folder
    background = pygame.image.load("./media/level" + level_number + "/stars.png")
    playerImg = pygame.image.load("./media/level" + level_number + "/spaceship.png")
    enemyImgFile = pygame.image.load("./media/level" + level_number + "/ufo.png")
    bulletImg = pygame.image.load("./media/level" + level_number + "/bullet.png")

    # Swap the BGM to a new song in a new level assets folder
    pygame.mixer.music.unload
    pygame.mixer.music.load("./media/level" + level_number + "/background.wav")
    pygame.mixer.music.play(-1)
    


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state

    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) +
                         math.pow(enemyY - bulletY, 2))

    if distance < 27:
        return True
    else:
        return False


def game_over():  # display the game over text
    if level == 4:
             over_font = game_over_font.render("YOU WON!", True, (255, 255, 255))
             screen.blit(over_font, (100, 250))
   
    else:
     over_font = game_over_font.render("GAME OVER", True, (255, 255, 255))
     screen.blit(over_font, (100, 250))


# display level won text
level_num = "1"
score_total = 0

def level_won(level_number):
    level_message = "Level " + level_number + " Won!"
    win_message = level_won_font.render(level_message, True, (255, 255, 255))
    screen.blit(win_message, (100, 250))
    


# Game Loop
create_enemy_list(num_enemies)
level = 0
score_thresh = 3  # the threshold taht a user's score must surpass to complete the wincon
win_con = False
running = True
while running:

    # Game Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = pygame.mixer.Sound("./media/level" + str(level) + "/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Screen Attributes
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Move player based on input
    playerX += playerX_change

    # Min & Max Bounds of Player Movement
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_enemies):

        # Game Over
        if enemyY[i] > 440:  # trigger the end of the game
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = pygame.mixer.Sound("./media/level0/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Animation
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    # test for the win condition, and swap level and assets if true
    if score_value >= score_thresh:
        print("from level " +str(level))
        score_thresh += 3
        level += 1
        print("to level "+str(level))

        if level == 4:
                end_message = level_won_font.render("You won!", True, (255, 255, 255))
                screen.blit(end_message, (100, 250))
                for j in range(num_enemies):
                 enemyY[j] = 2000
                 
                 break
                bullet_state = "disabled"
        else:
         level_won(str(level))
         if level <= 3:
          swap_assets(str(level))
          create_enemy_list(num_enemies + random.randint(1, 4))

    pygame.display.update()
