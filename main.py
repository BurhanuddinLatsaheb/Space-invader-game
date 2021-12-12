import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()
# screen creation
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('space_background.jpg')

# sounds
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space_invaders.png')
pygame.display.set_icon(icon)

# Player
PlayerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
EnemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    EnemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see the bullet
# Fire - The bullet is currently moving
BulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('game.ttf', 32)

textX = 10
textY = 10

gameover = pygame.font.Font('game.ttf', 64)
playagain = pygame.font.Font('game.ttf', 32)


def show_score(x, y):
    score = font.render("SCORE : " + str(score_value), True, (0, 250, 154))
    screen.blit(score, (x, y))


def game_over():
    game_over = gameover.render("GAME OVER ", True, (0, 250, 154))
    screen.blit(game_over, (250, 250))
    play_again = playagain.render("Press Y to play again and Q to quit ", True, (0, 250, 154))
    screen.blit(play_again, (200, 350))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 20))


def check_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    return False


# Game Loop

def mainloop():
    running = False
    global playerX
    global playerY
    global playerX_change
    global playerY_change
    global enemyX
    global enemyY
    global enemyX_change
    global enemyY_change
    global bullet_state
    global bulletX
    global bulletY
    global bulletX_change
    global bulletY_change
    global score_value
    while not running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # for checking keystroke
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.7
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.7
                if event.key == pygame.K_UP:
                    playerY_change = -0.3
                if event.key == pygame.K_DOWN:
                    playerY_change = 0.3
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletSOund = mixer.Sound('bullet.wav')
                        bulletSOund.play()
                        bulletX = playerX
                        fireBullet(bulletX, bulletY)
                if event.key == pygame.K_y:
                    mainloop()
                if event.key == pygame.K_q:
                    pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0
        # PLAYER MOVEMENT
        playerX += playerX_change
        playerY += playerY_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        if playerY <= 0:
            playerY = 0
        if playerY >= 536:
            playerY = 536

        # ENEMY MOVEMENT
        for i in range(num_of_enemies):
            if enemyY[i] > 200:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000

                game_over()
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.5
                enemyY[i] += enemyY_change[i]
            collision = check_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                collisionSOund = mixer.Sound('explosion.wav')
                collisionSOund.play()

                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                print(score_value)
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # BULLET MOVEMENT
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"
        if bullet_state == "fire":
            fireBullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Collision

        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()


mainloop()
