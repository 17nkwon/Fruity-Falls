# Template: KidsCanCode (http://kidscancode.org/blog/2016/08/pygame_1-1_getting-started/)
import pygame
import random
from os import path

# Path to the 'images' folder
img_dir = path.join(path.dirname(__file__), 'images')

WIDTH = 700
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame and Create Window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruity Falls")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def new_coconut():
    c = Coconut()
    all_sprites.add(c)
    coconuts.add(c)


def new_starfruit():
    s = Starfruit()
    all_sprites.add(s)
    starfruits.add(s)


def draw_shield(surface, x, y, percentage):
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100
    BAR_LENGTH = 200
    BAR_HEIGHT = 40
    fill = (percentage/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 30
        # Create a mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = 0
        self.shield = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        # Move player to the left
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        # Move player to the right
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        # Keeps the player from going off the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Coconut(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = coconut_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # Spawn coconuts randomly above the screen horizontally
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Spawn coconuts randomly above the screen vertically
        self.rect.y = random.randrange(-100, -40)
        # Speed of the coconuts ranging from 1-7
        self.speedy = random.randrange(1, 6)
        # Change the rotation of the coconuts
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        # Return ticks since the game started
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # Makes sure we don't go over 360 degrees
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            # Creates a rectangle around the image that changes size to fit the image as it rotates
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        # Move coconuts downwards
        self.rect.y += self.speedy
        # When coconuts reach the bottom, they move to the top again randomly
        if self.rect.top > HEIGHT - 80:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)


class Starfruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = starfruit_img
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        # Spawns starfruit randomly above the screen horizontally
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # Spawns starfruit randomly above the screen vertically
        self.rect.y = random.randrange(-100, -40)
        # Speed of the starfruit ranging from 1-7
        self.speedy = random.randrange(3, 6)
        # Change the rotation of the starfruit
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        # Return ticks since the game started
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            # Makes sure we don't go over 360 degrees
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            # Creates a rectangle around the image that changes size to fit the image as it rotates
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        # Move starfruit downwards
        self.rect.y += self.speedy
        # When starfruit reach the bottom, they move to the top again randomly
        if self.rect.top > HEIGHT - 80:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-1000, -40)
            self.speedy = random.randrange(3, 6)


# Load images
background = pygame.image.load(path.join(img_dir, "jungle.png")).convert_alpha()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "char.png")).convert_alpha()
coconut_img = pygame.image.load(path.join(img_dir, "coconut.png")).convert_alpha()
starfruit_img = pygame.image.load(path.join(img_dir, "starfruit.png")).convert_alpha()

# Grouping the sprites
all_sprites = pygame.sprite.Group()
starfruits = pygame.sprite.Group()
coconuts = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# Spawning 6 coconuts
for i in range(8):
    new_coconut()

for i in range(2):
    new_starfruit()

# Initialize score variable
score = 0

# Game Loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # Check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Check if a coconut hit the player
    # Returns a list called hits of the coconuts that hit the player
    coconut_hit = pygame.sprite.spritecollide(player, coconuts, True, pygame.sprite.collide_mask)
    # Game over if the player is hit
    for hit in coconut_hit:
        player.shield -= 25
        new_coconut()
        if player.shield <= 0:
            running = False

    starfruit_hit = pygame.sprite.spritecollide(player, starfruits, True, pygame.sprite.collide_mask)
    for hit in starfruit_hit:
        if player.shield != 100:
            player.shield += 25
        new_starfruit()

    # Update
    all_sprites.update()

    # Draw/Render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 40, 30, 10)
    score += 1
    draw_shield(screen, WIDTH-220, 20, player.shield)
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
