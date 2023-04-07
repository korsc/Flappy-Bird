import pygame
from settings import *
import random

class background(pygame.sprite.Sprite):
    def __init__(self,groups, scale_factor):
        super().__init__(groups)
        background_image = pygame.image.load("graphics/sky.png").convert()

        full_height = scale_factor * background_image.get_height() 
        full_width = scale_factor * background_image.get_width()
        full_image = pygame.transform.scale(background_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_image, (0,0))
        self.image.blit(full_image, (full_width,0)) 

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        self.pos.x -= 300 *dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class ground(pygame.sprite.Sprite):                      
    def __init__(self,groups):
        super().__init__(groups)

        self.sprite_type = "ground"

        ground_surf = pygame.image.load("graphics/ground.png").convert_alpha()
        self.image = pygame.transform.scale(ground_surf, (1000000,300))



        #position of ground
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #Mask to create better hitbox 
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 360*dt
        if self.rect.centerx <= 0:
            self.pos.x = 0

        self.rect.x = round(self.pos.x)

class bird(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        #rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20, WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #Mask to create better hitbox 
        self.mask = pygame.mask.from_surface(self.image)

        self.sound = pygame.mixer.Sound("sounds/sounds_jump.wav")
        self.sound.set_volume(0.05)

        #gravity
        self.gravity = 800
        self.direction = 0 

    def import_frames(self,scale_factor):
        self.frames = []
        for x in range(1,3):
            bird_surf = pygame.image.load(f"graphics/flap{x}.png").convert_alpha()
            scaled_surf = pygame.transform.scale(bird_surf, pygame.math.Vector2(bird_surf.get_size())*scale_factor)
            self.frames.append(scaled_surf)

    def apply_gravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.sound.play()
        self.direction -= 300

    def animate(self,dt):
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
            

    def update(self,dt):
        self.apply_gravity(dt)
        self.animate(dt)
        
class obstacle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.sprite_type = "obstacle"

        orientation = random.choice(("up", "down"))
        obstacle_surf = pygame.image.load(f"graphics/firehydrant{random.choice((1,2))}.png").convert_alpha()
        self.image = pygame.transform.scale(obstacle_surf, (225,500))
        
        if orientation == "up":
            obstacle_surf = pygame.transform.scale(obstacle_surf, (200,350))
            self.rect = self.image.get_rect(midbottom= (WINDOW_WIDTH +random.randint(50,100), random.randint(800,850)))
        else:
            obstacle_surf = pygame.transform.scale(obstacle_surf, (200,350))
            self.image = pygame.transform.flip(obstacle_surf, False, True)
            self.rect = self.image.get_rect(midtop = ((WINDOW_WIDTH +random.randint(50,100)), random.randint(-50, -10)))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        #Mask to create better hitbox 
        self.mask = pygame.mask.from_surface(self.image)


    def update(self,dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)

        #Deleting fire hydrants that have already been passed so game doesnt lag/so too much memory isnt used
        if self.rect.right <= -100:
            self.kill()