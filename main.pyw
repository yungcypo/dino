import pygame, sys
import random
import json

pygame.init()
CLOCK = pygame.time.Clock()
FPS = 60
W, H = 900, 600
SCREEN = pygame.display.set_mode((W, H)) # make pygame window
TITLE = pygame.display.set_caption("Dino")
ICON = pygame.image.load("assets\images\icon.png")
pygame.display.set_icon(ICON)

colors = {
    "white" : (255, 255, 255),
    "gray" : (20, 20, 20),
    "black" : (0, 0, 0),
    "background" : (32, 33, 36)}

with open ("stats.json", "r") as json_file:
    game_stats = json.load(json_file)


class Text:
    def __init__(self, text, size, **kwargs):
        self.text = text
        self.size = size
        self.kwargs = kwargs
        self.make()
        
    def getfont(self):
        return pygame.font.Font("assets\\fonts\PressStart2P.ttf", self.size)
    
    def make(self):
        self.surf = self.getfont().render(str(self.text), True, colors["white"])
        self.rect = self.surf.get_rect(**self.kwargs)
        
    def draw(self):
        self.make()
        SCREEN.blit(self.surf, self.rect)

class Score:
    def __init__(self, str, size, **kwargs):
        self.str = str
        self.size = size
        self.kwargs = kwargs
        self.value = 0

    def getfont(self):
        return pygame.font.Font("assets\\fonts\PressStart2P.ttf", self.size)
    

    def draw(self):
        self.surf = self.getfont().render((str(self.str) + str(self.value)), True, colors["white"])
        self.rect = self.surf.get_rect(**self.kwargs)
        SCREEN.blit(self.surf, self.rect)
    
    def update(self):
        self.draw()

class Player(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.sprites = []
        self.sprites.append(pygame.image.load("assets\images\dino_walk1.png").convert_alpha())
        self.sprites.append(pygame.image.load("assets\images\dino_walk2.png").convert_alpha())
        self.sprites_crouch = []
        self.sprites_crouch.append(pygame.image.load("assets\images\dino_crouch1.png").convert_alpha())
        self.sprites_crouch.append(pygame.image.load("assets\images\dino_crouch2.png").convert_alpha())
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.surf = self.sprites[int(self.current_sprite)]
        self.rect = self.surf.get_rect(midbottom = (W/7, ground_level))
        self.death = False
        self.crouching = False
        self.jumping = False
        self.g = 1  # gravity
        self.h = 21  # jump height
        self.v = self.h  # speed of jump


    def jump(self):
        if self.jumping and not self.death:
            self.rect.y -= self.v
            self.v -= self.g
            if self.v < -self.h:
                self.jumping = False
                self.v = self.h

    def animate(self):
        if not (self.jumping and self.death):
            self.current_sprite = round(self.current_sprite + speed/60, 2)
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            if not self.crouching:
                self.image = self.sprites[int(self.current_sprite)] 
            else:
                self.image = self.sprites_crouch[int(self.current_sprite)] 
        if self.jumping:
            self.image = pygame.image.load("assets\images\dino_jump.png")
        if self.death:
            self.image = pygame.image.load("assets\images\dino_death1.png")
        self.surf = self.image
        self.mask = pygame.mask.from_surface(self.surf)

    def draw(self):
        SCREEN.blit(self.surf, self.rect)

    def update(self):
        self.animate()
        self.jump()
        self.draw()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == 1:
            self.cactus = []
            self.cactus.append(pygame.image.load("assets\images\cactus1.png").convert_alpha())
            self.cactus.append(pygame.image.load("assets\images\cactus2.png").convert_alpha())
            self.cactus.append(pygame.image.load("assets\images\cactus3.png").convert_alpha())
            self.cactus.append(pygame.image.load("assets\images\cactus4.png").convert_alpha())
            self.cactus.append(pygame.image.load("assets\images\cactus5.png").convert_alpha())
            self.cactus.append(pygame.image.load("assets\images\cactus6.png").convert_alpha())
            self.surf = self.cactus[random.randint(0, len(self.cactus) - 1)]
            self.rect = self.surf.get_rect(bottomleft = (random.randint(W, int(W * 1.5)), ground_level))
        if self.type == 2:
            self.cactus_big = []
            self.cactus_big.append(pygame.image.load("assets\images\cactus_big1.png").convert_alpha())
            self.cactus_big.append(pygame.image.load("assets\images\cactus_big2.png").convert_alpha())
            self.cactus_big.append(pygame.image.load("assets\images\cactus_big3.png").convert_alpha())
            self.cactus_big.append(pygame.image.load("assets\images\cactus_big4.png").convert_alpha())
            self.cactus_big.append(pygame.image.load("assets\images\cactus_big5.png").convert_alpha())
            self.surf = self.cactus_big[random.randint(0, len(self.cactus_big) - 1)]
            self.rect = self.surf.get_rect(bottomleft = (random.randint(W, int(W * 1.5)), ground_level))
        if self.type == 3:
            self.birds = []
            self.birds.append(pygame.image.load("assets\images\\bird1.png").convert_alpha())
            self.birds.append(pygame.image.load("assets\images\\bird2.png").convert_alpha())
            self.current_bird = 0
            self.surf = self.birds[self.current_bird]
            self.rect = self.surf.get_rect(bottomleft = (random.randint(W, int(W * 1.5)), random.randint(ground_level - 100, ground_level)))
        self.mask = pygame.mask.from_surface(self.surf)

    def animate(self):
        self.rect.x -= speed

    def draw(self):
        if self.type == 3:
            self.current_bird = round(self.current_bird + speed/100, 2)
            if self.current_bird >= len(self.birds):
                self.current_bird = 0
            self.image = self.birds[int(self.current_bird)]
            self.surf = self.image
            
            self.mask = pygame.mask.from_surface(self.surf)
        SCREEN.blit(self.surf, self.rect)

    def update(self):
        if not gameover:
            self.animate()
        self.draw()

class Ground:
    def __init__(self):
        self.image = "assets\images\ground.png"
        self.surf = pygame.image.load(self.image).convert_alpha()
        self.rect = self.surf.get_rect(midleft = (0, H/4*3))
        self.surf2 = pygame.image.load(self.image)
        self.rect2 = self.surf2.get_rect(midleft = self.rect.midright)

    def animate(self):
        self.rect.x -= speed
        self.rect2.x -= speed
        if self.rect.right <= 0:
            self.rect.left = self.rect2.right
        if self.rect2.right <= 0:
            self.rect2.left = self.rect.right

    def draw(self):
        SCREEN.blit(self.surf, self.rect)
        SCREEN.blit(self.surf2, self.rect2)
    
    def update(self):
        if not gameover:
            self.animate()
        self.draw()


original_speed = 5
speed = original_speed
ground = Ground()
ground_level = ground.rect.top + 10

current_score = Score("SCORE: ", 20, topright = (W - 32, 32))

#hiscore = Text("HISCORE: " + str(game_stats["hiscore"]), 20, topright = (W - 32, score.rect.bottom + 16))
gameover_text = Text("GAME OVER", 32, midbottom = (W/2, H/3))

player = Player(W/10)
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

enemy = Enemy(1)
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

def enemy_cycle():
    global enemy
    if enemy.rect.right < 0:
        enemy = Enemy(random.randint(1, 3))
        enemy_group.empty()
        enemy_group.add(enemy)

def colision():
    global gameover
    if pygame.sprite.spritecollide(player, enemy_group, False):
        if pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask):
            gameover = True

def save_stats():

    with open ("stats.json", "w") as json_file:
        json.dump(game_stats, json_file, indent=4)



gameover = False

def main():
    global speed, enemy, gameover
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jumping = True
                if event.key == pygame.K_DOWN:
                    player.crouching = True
                if event.key == pygame.K_RETURN:
                    if gameover:
                        speed = original_speed
                        enemy.rect.right = W
                        player.rect.bottom = ground_level
                        player.v = player.h
                        player.rect.bottom = ground_level
                        player.death = False
                        gameover = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.crouching = False

        SCREEN.fill(colors["background"])

        ground.update()
        enemy_group.update()
        player.update()

        current_score.update()
        #hiscore.draw()


        enemy_cycle()
        colision()

        if gameover: 
            player.death = True
            speed = 0
            gameover_text.draw()

        if not gameover:
            speed = round(speed + 1/900, 3)
            current_score.value = round((speed - original_speed) * 10)


        CLOCK.tick(FPS)
        pygame.display.update()

main()
