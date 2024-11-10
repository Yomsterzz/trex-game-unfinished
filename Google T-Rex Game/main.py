import pygame
import random
from pygame.locals import *
pygame.init()

WIDTH = 800
HEIGHT = 400

clock = pygame.time.Clock()
fps = 60
ground_x = 0
scroll_speed = 4
initial_scroll_speed = 4
score = 0
score_increment = 1
font = pygame.font.Font(None, 32)
running = True
game_over = False
cactus_frequency = 2000
last_cactus = pygame.time.get_ticks() - 1500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-rex Game") 

bg = pygame.image.load("./images/bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))  # Scale the background to fit the screen

class Trex(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.counter = 0
        self.trex_left = pygame.image.load("./images/trex-left-foot.png")
        self.trex_right = pygame.image.load("./images/trex-right-foot.png")
        self.trex_left_duck = pygame.image.load("./images/trex-left-duck.png")
        self.trex_right_duck = pygame.image.load("./images/trex-right-duck.png")
        self.image = self.trex_right
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.animation_delay = 5
        self.animation_counter = 0
        self.velocity = 0    
        self.clicked = False
        self.in_the_air = True
        self.hitbox = (self.rect.x + 5, self.rect.y + 10, 20, 40)
        self.ducking = False

    def update(self):
        if not game_over:

            if not self.in_the_air:
                self.animation_counter += 1
            else:
                self.animation_counter = 0

            keys = pygame.key.get_pressed()
            if (keys[K_SPACE] or keys[K_UP] or keys[K_w]) and not self.in_the_air:
                self.velocity = -15
                self.in_the_air = True

            if keys[K_DOWN] or keys[K_s]:
                self.ducking = True
            else: 
                self.ducking = False

            if self.ducking:
                self.image = self.trex_left_duck
                self.hitbox = (self.rect.x + 5, self.rect.y + 10, 20, 40)
                self.velocity += 5
                if self.animation_counter > self.animation_delay:
                    self.animation_counter = 0  
                    if self.image == self.trex_left_duck:
                        self.image = self.trex_right_duck
                    else:
                        self.image = self.trex_left_duck

            if not self.ducking:
                self.ducking = False
                self.image = self.trex_left
                self.hitbox = (self.rect.x + 5, self.rect.y + 10, 20, 40)
                if self.animation_counter > self.animation_delay:
                    self.animation_counter = 0  
                    if self.image == self.trex_left:
                        self.image = self.trex_right
                    else:
                        self.image = self.trex_left

            if self.in_the_air:
                self.velocity += 0.5
                if self.velocity > 8:
                    self.velocity = 8
                self.rect.y += int(self.velocity)

            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.velocity = 0
                self.in_the_air = False

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        if pos == 1:
            self.image = pygame.image.load("./images/cactus.png")
        elif pos == 2:
            self.image = pygame.image.load("./images/cacti.png")

        self.rect = self.image.get_rect()
        self.rect.topleft = [x, HEIGHT - self.rect.height]

    def update(self):
        global scroll_speed
        if not game_over:
            self.rect.x -= scroll_speed
            scroll_speed *= 1.001 
        if self.rect.right < 0:
            self.kill()

cactus_group = pygame.sprite.Group()
trex_group = pygame.sprite.Group()
trex1 = Trex(int(WIDTH / 4), HEIGHT)
trex_group.add(trex1)

def reset_game():
    global score, scroll_speed, game_over, last_cactus
    score = 0
    scroll_speed = initial_scroll_speed
    game_over = False
    last_cactus = pygame.time.get_ticks() - cactus_frequency
    cactus_group.empty()
    trex_group.empty()
    trex1 = Trex(int(WIDTH / 4), HEIGHT)
    trex_group.add(trex1)

while running:
    if game_over: 
        score_increment = 1
        scroll_speed = 0
        game_over_text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(game_over_text, game_over_rect)

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            reset_game()

    clock.tick(fps)

    # Update background position
    ground_x -= scroll_speed
    if ground_x <= -WIDTH:
        ground_x = 0

    # Draw background
    screen.blit(bg, (ground_x, 0))
    screen.blit(bg, (ground_x + WIDTH, 0))

    trex_group.draw(screen)
    trex_group.update()

    cactus_group.draw(screen)
    cactus_group.update()

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH / 2, 50))
    screen.blit(score_text, score_rect)
    score += score_increment

    if pygame.sprite.groupcollide(trex_group, cactus_group, False, False):
        game_over = True
        score_increment = 0

    time_now = pygame.time.get_ticks()
    if time_now - last_cactus >= cactus_frequency and not game_over:
        cactus = Cactus(WIDTH, HEIGHT, random.randint(1, 2))
        cactus_group.add(cactus)
        last_cactus = time_now
        cactus_frequency = random.randint(1500, 2500)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
