import pygame
from pygame.locals import *
import sys
 
pygame.init()
vec = pygame.math.Vector2 

class WindowInfo:
    def __init__(self):
        self.Dimension = vec(600,300)                               

Acceleration = 0.50
Friction = -0.10
FPS = 60
 
FramePerSec = pygame.time.Clock()
Window = WindowInfo()
window = pygame.display.set_mode((Window.Dimension.x, Window.Dimension.y))
pygame.display.set_caption("Jump Test")
 
class PlayerInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = vec(30,30)
        self.Surface = pygame.Surface((self.Dimension.y, self.Dimension.x))
        self.Surface.fill((128,255,40))
        self.rect = self.Surface.get_rect()
   
        self.Position = vec((10, 360))
        self.Velocity = vec(0,0)
        self.Acceleration = vec(0,0)
 
    def move(self):
        self.Acceleration = vec(0,0.3)
    
        pressed_keys = pygame.key.get_pressed()
        if self.Velocity.y > 10:
            self.Velocity.y = 10
        if pressed_keys[K_LEFT]:
            self.Acceleration.x = -Acceleration
        if pressed_keys[K_RIGHT]:
            self.Acceleration.x = Acceleration
                 
        self.Acceleration.x += self.Velocity.x * Friction
        self.Velocity += self.Acceleration
        self.Position += self.Velocity + 0.3 * self.Acceleration

        if self.Position.x > Window.Dimension.x + self.Dimension.x:
            self.Position.x = 0
        if self.Position.x < 0 - self.Dimension.x:
            self.Position.x = Window.Dimension.x
             
        self.rect.midbottom = self.Position
 
    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
           self.Velocity.y = -6
 
 
    def update(self):
        hits = pygame.sprite.spritecollide(Player ,platforms, False)
        if Player.Velocity.y > 0:        
            if hits:
                self.Position.y = hits[0].rect.top + 1

        if Player.Position.y > Window.Dimension.y + self.Dimension.x:
            Player.Position.y = Player.Dimension.x * (-1) 
 
 
class PlatformInfo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Dimension = vec(100, 30)
        self.Surface = pygame.Surface((self.Dimension.x, self.Dimension.y))
        self.Surface.fill((255,0,0))
        self.rect = self.Surface.get_rect(center = (Window.Dimension.x/2, Window.Dimension.y - 30))
 
    def move(self):
        pass
 
Platform = PlatformInfo()
Player = PlayerInfo()
 
all_sprites = pygame.sprite.Group()
all_sprites.add(Platform)
all_sprites.add(Player)
 
platforms = pygame.sprite.Group()
platforms.add(Platform)
 
 
while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE:
                Player.jump()
         
    window.fill((0,0,0))
    Player.update()
 
    for entity in all_sprites:
        window.blit(entity.Surface, entity.rect)
        entity.move()
 
    pygame.display.update()
    FramePerSec.tick(FPS)
