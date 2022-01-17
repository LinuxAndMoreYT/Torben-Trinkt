#!/usr/bin/python3
import pygame
import os
import random
import sys
import pickle
import time

pygame.init()
pygame.display.set_caption("Torben Trinkt")
programIcon = pygame.image.load("data/icon.jpg")
pygame.display.set_icon(programIcon)
clock=pygame.time.Clock()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((1100, 600))

RUNNING         =   [pygame.image.load(os.path.join("data", "run1.png")),
                    pygame.image.load(os.path.join("data", "run2.png")).convert_alpha()]
JUMPING         =   pygame.image.load(os.path.join("data", "jump.png"))
DUCKING         =   [pygame.image.load(os.path.join("data", "milch.png")),
                    pygame.image.load(os.path.join("data", "korn.png")).convert_alpha()]

SMALL_CACTUS    =   [pygame.image.load(os.path.join("data", "korn.png")),
                    pygame.image.load(os.path.join("data", "tost.png")),
                    pygame.image.load(os.path.join("data", "milch.png")).convert_alpha()]
LARGE_CACTUS    =   [pygame.image.load(os.path.join("data", "mett.png")),
                    pygame.image.load(os.path.join("data", "mate.png")),
                    pygame.image.load(os.path.join("data", "pizza.png")).convert_alpha()]

ANNE            =   [pygame.image.load(os.path.join("data", "anne.png"))]
RITTER            =   [pygame.image.load(os.path.join("data", "ritter.png"))]

BG              =   pygame.image.load(os.path.join("data", "Track.jpeg")).convert_alpha()
Blur            =   pygame.image.load(os.path.join("data", "Track-Blur.jpeg")).convert_alpha()

if os.path.isfile("first") == True:
    Best        =   "0"
    pickle.dump(Best, open("Best.dat", "wb"))
    os.remove("first")

Best            =   pickle.load(open("Best.dat", "rb"))

death_count = 0
points = 0
start = True
ussr = False
jam = False

pygame.mixer.music.load("data/start.wav")
pygame.mixer.music.play(-1)

def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        pygame.time.delay(5)

fade(1100,600)        
font = pygame.font.Font('freesansbold.ttf', 30)
intro = font.render(("MacAndMore Präsentiert Torben-Trinkt"), True, (255, 255, 255))
pygame.draw.rect(SCREEN, (255, 255, 255), pygame.Rect(225, 273, 650, 50), 2)
introRect = intro.get_rect()
introRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SCREEN.blit(intro, introRect)
pygame.display.update()
pygame.time.wait(7500)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    userInput = pygame.key.get_pressed()

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):

        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        if userInput[pygame.K_ESCAPE]:
            GUI(-1)

    def duck(self):
        self.image = self.duck_img[self.step_inuserInput[pygame.K_UP] and not self.dino_jumpdex // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        global cheat
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
        if self.dino_rect.y < 90:
            GUI(1)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 320


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 320

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, points, BG, Blur, death_count, start, jam, ussr
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    if death_count > 0 and jam == False and ussr == False:
        points = 0
        jam == False
        pygame.mixer.music.load("data/foo.wav")    
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
    if ussr == True:
        pygame.mixer.music.load("data/ussr.wav")
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
    if jam == True:
        pygame.mixer.music.load("data/jam.wav")
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
    if start == True and jam == False and ussr == False:
        pygame.mixer.music.load("data/foo.wav")    
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)
    death_count = 0

    def score():
        global points, game_speed, death_count
        points += 1
        if points % 100 == 0:
            game_speed += 1
        if (points) == 100:
            death_count = -2
            GUI(-2)
        if (points) == 5000:
            death_count -3
            GUI(-3)
        text = font.render("Kohlsuppen: " + str(points), True, (255, 0, 0)) 
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(910, 18, 180, 40))
        pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(910, 18, 180, 40), 2)
        SCREEN.blit(text, textRect)
        pygame.display.flip() 

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed                    

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        background()
        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(200)
                death_count += 1
                GUI(death_count)

        score()

        clock.tick(30)
        pygame.display.update()

def GUI(death_count):
    global points, Best, Blur, BG, jam, ussr
    run = True
    if death_count > 0:
        pygame.mixer.music.load("data/fail.wav")    
        pygame.mixer.music.stop()
        pygame.mixer.music.play(0)

    if death_count < 0:
        pygame.mixer.music.load("data/lvl.wav")    
        pygame.mixer.music.stop()
        pygame.mixer.music.play(0)
    while run:
        SCREEN.fill((0, 0, 0))
        font = pygame.font.Font('freesansbold.ttf', 30)
        if death_count == -1:
            SCREEN.blit(Blur, (0, 0)) 
            text = font.render("Spiel Pausiert - Weiter mit Enter", True, (255, 255, 255))
            score = font.render("Kohlsuppen: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(RITTER[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 160))
            SCREEN.blit(score, scoreRect,)
        if death_count == -2:
            BG              =   pygame.image.load(os.path.join("data", "ussr.jpeg")).convert_alpha()
            Blur            =   pygame.image.load(os.path.join("data", "ussr-Blur.jpeg")).convert_alpha()
            SCREEN.blit(Blur, (0, 0)) 
            text = font.render("Level 2 - Kommunismus - Freigeschalten", True, (255, 255, 255))
            score = font.render("Weiter mit Enter", True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(RITTER[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 160))
            SCREEN.blit(score, scoreRect,)
            jam = False
            ussr = True
        if death_count == -3:
            BG              =   pygame.image.load(os.path.join("data", "jam.jpeg")).convert_alpha()
            Blur            =   pygame.image.load(os.path.join("data", "jam-Blur.jpeg")).convert_alpha()
            SCREEN.blit(Blur, (0, 0)) 
            text = font.render("Level 3 - Kiff & Zierotten - Freigeschalten", True, (255, 255, 255))
            score = font.render("Weiter mit Enter", True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(RITTER[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 160))
            SCREEN.blit(score, scoreRect,)
            ussr = False
            jam = True
        if death_count == 0:
            SCREEN.blit(Blur, (0, 0))
            text = font.render(("High Score: ")+(Best), True, (255, 255, 255))
            high = font.render(("Drücke ENTER um die Reiterkarriere zu Starten "), True, (255, 255, 255))
            highRect = high.get_rect()
            highRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.7)
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 140))
            SCREEN.blit(high, highRect)
        elif death_count > 0:
            jam = False
            ussr = False
            BG              =   pygame.image.load(os.path.join("data", "Track.jpeg")).convert_alpha()
            Blur            =   pygame.image.load(os.path.join("data", "Track-Blur.jpeg")).convert_alpha()
            SCREEN.blit(Blur, (0, 0)) 
            text = font.render("Et wird Suppe gegessen!!!", True, (255, 255, 255))
            score = font.render("Kohlsuppen: " + str(points), True, (255, 255, 255))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(ANNE[0], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 140))
            SCREEN.blit(score, scoreRect,)
            if int(points) > int(Best):
                Best = str(points)
                pickle.dump(Best, open("Best.dat", "wb"))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        pygame.display.quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                sys.exit(0)
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()

        

GUI(death_count=0)
