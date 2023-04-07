import pygame, sys, time
from settings import *
from sprites import background, ground, bird, obstacle   

pygame.init()

class Game:
    def __init__(self):

        #Settings the last obstacle passed to none
        self.last_obstacle = None
        
        #Creating a surface
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        #Setting game window name to flappy bird
        pygame.display.set_caption("Flappy Bird")

        #Creating a timer
        self.clock = pygame.time.Clock()
        self.active = False 

        #Sprite groups
        self.sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        
        #Calculating a scale factor to scale other images to the window size
        height = pygame.image.load("graphics/sky.png").get_height()
        self.scale_factor = WINDOW_HEIGHT/height

        #Initalizing the sprites 
        background(self.sprites, self.scale_factor)
        ground([self.sprites, self.collision_sprites])
        self.bird = bird(self.sprites, self.scale_factor/15)
        # self.obstacle = obstacle([self.sprites, self.collision_sprites])
        

        #timer to spawn obstacles 
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        #Loading in comicsans font
        self.font = pygame.font.SysFont("comicsansms", 50)
        self.score = 0 
        
        #
        self.menu_surf = pygame.image.load("graphics/menu.png").convert_alpha()
        self.menu_surf = pygame.transform.scale(self.menu_surf, (650,125))
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, 350))

        self.gameovertext_surf = pygame.image.load("graphics/gameovertext.png").convert_alpha()
        self.gameovertext_surf = pygame.transform.scale(self.gameovertext_surf, (700,400))
        self.gameovertext_rect = self.gameovertext_surf.get_rect(center = (WINDOW_WIDTH/2, 150))

        self.startscreenimg = pygame.image.load("graphics/startscreen.png").convert_alpha()
        self.startscreenimg_rect = self.startscreenimg.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        self.startbirdimg = pygame.image.load("graphics/flap2.png").convert_alpha()
        self.startbirdimg = pygame.transform.scale(self.startbirdimg, (295.125, 261.875))
        self.startbirdimg_rect = self.startbirdimg.get_rect(center = ((WINDOW_WIDTH/2)-25, 450)) 

        self.screentitle = pygame.image.load("graphics/flappybirdtitle.png").convert_alpha()
        self.screentitle_rect = self.screentitle.get_rect(center = (WINDOW_WIDTH/2, 100)) 

        self.spacetostart = pygame.image.load("graphics/spacestart.png").convert_alpha()
        self.spacetostart = pygame.transform.scale(self.spacetostart, (500,150))
        self.spacetostart_rect = self.spacetostart.get_rect(center= (WINDOW_WIDTH/2, 250))

        self.music = pygame.mixer.Sound("sounds/sounds_music.wav")
        self.music.set_volume(0.03)
        self.music.play(loops = -1)

    #Creating a method for when the bird collides into an obstacle (ground or firehydrant)
    def start_screen(self):
        while not self.active:
            self.spawn_start = False
            self.display_surface.fill((255,255,255))
            self.display_surface.blit(self.startscreenimg, self.startscreenimg_rect)
            self.screen_surf = self.font.render("Press SPACE to Play", True, "black")
            self.screen_surf_rect = self.screen_surf.get_rect(center = (WINDOW_WIDTH/2, 250))
            # self.display_surface.blit(self.screen_surf, self.screen_surf_rect)
            self.display_surface.blit(self.spacetostart, self.spacetostart_rect)
            self.display_surface.blit(self.startbirdimg, self.startbirdimg_rect)
            self.display_surface.blit(self.screentitle, self.screentitle_rect)

            self.infile = open("flappyhighscore.txt", "r")
            self.line = self.infile.readline()
            self.scorelist = []
            while self.line != "":
                self.scorelist.append(self.line)
                self.oldhighscore = self.scorelist
                self.line = self.infile.readline()
            self.infile.close()
            if self.score > int(self.oldhighscore[0]):
                self.highscores = open("flappyhighscore.txt", "w")
                self.highscores.write(str(self.score))

            self.highscore_surf = self.font.render(f"High Score: {self.scorelist[0]}", True, "black")
            self.highscore_rect = self.highscore_surf.get_rect(center = (WINDOW_WIDTH/2, 700))
            self.display_surface.blit(self.highscore_surf, self.highscore_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.active = True
                        self.spawn_start = True
                        self.bird.jump()
            pygame.display.update()
            self.clock.tick(FPS)

    def high_score(self):
        self.infile = open("flappyhighscore.txt", "r")
        self.line = self.infile.readline()
        self.scorelist = []
        while self.line != "":
            self.scorelist.append(self.line)
            self.oldhighscore = self.scorelist
            self.line = self.infile.readline()
        self.infile.close()
        if self.score > int(self.oldhighscore[0]):
            self.highscores = open("flappyhighscore.txt", "w")
            self.highscores.write(str(self.score))
            

    def collision(self):
        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask) or self.bird.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == "obstacle":
                    sprite.kill()
            self.active = False
            self.bird.kill()
    
    def display_score(self):
        if self.active:
            y = WINDOW_HEIGHT/10
            for obstacle in self.collision_sprites.sprites():
                if obstacle.rect.right <= self.bird.rect.right and obstacle != self.last_obstacle:
                    self.score += 1
                    self.last_obstacle = obstacle
        else:
            y = 500
            
        score_surf = self.font.render(f"Score: {self.score}", True, "black")
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH/2,y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        game.start_screen()
        last_time = time.time()
        while True:
            
            #Calculating the change in time
            dt = time.time() - last_time
            last_time = time.time()

            #Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.active == True: 
                            self.bird.jump()
                        elif self.active == False: 
                            self.score = 0
                            self.bird = bird(self.sprites, self.scale_factor/15)
                            self.active = True
                if event.type == self.obstacle_timer and self.active == True and self.spawn_start == True:
                    obstacle([self.sprites, self.collision_sprites])
                    

            self.sprites.update(dt)
           
            self.sprites.draw(self.display_surface) 
            self.display_score()
            self.high_score()

            if self.active == True: 
                self.collision()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)
                self.display_surface.blit(self.gameovertext_surf, self.gameovertext_rect) 

            #Updating the screen every 60 frames
            pygame.display.update()
            self.clock.tick(FPS)


#Running the game
if __name__ == "__main__":
    game = Game()
    game.run()


