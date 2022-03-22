import pygame
import os
from maps import *

class Game():
    def __init__(self): #Setup for game
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('UNTITLED NEA GAME')
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500,100)

        self.current_room = room_a
        
        
        
        
    def new(self): #Initialize all variables and do all the setup for a new game
        #Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        #New player
        self.player = Player(8*TILESIZE,6*TILESIZE)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        #New enemy
        #self.enemy = Player(10*TILESIZE,10*TILESIZE)
        #self.all_sprites.add(self.enemy)

        #New walls
        self.draw_tiles()

    def enemy_move():
        self.enemy.vx += 1

    def run(self): #Run the game
        self.running = True
        while self.running: #Main game loop
            self.dt = game.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()

    def events(self): #All events in game
        #Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def update(self): #Update sprites
        self.all_sprites.update(self.dt)

    def draw(self): #Draw graphics onto screen
        self.screen.fill((255,255,255)) #Draw BG

        self.floors.draw(self.screen)
        self.draw_grid() #Grid
        self.walls.draw(self.screen)
        self.players.draw(self.screen)
        
        pygame.display.flip()

    def draw_grid(self): #Draw grid (temp)
        #Draw Grid (---temporary---)
        for i in range (0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen,(50,50,50), (i,0), (i,HEIGHT))
        for i in range (0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen,(50,50,50), (0,i), (WIDTH,i))
    
    def draw_tiles(self): #Draw tiles
        #Wall placement
        self.floors.empty()
        self.walls.empty()
        for ypos, y in enumerate(game.current_room):
            for xpos, x in enumerate (y):

                if x == 0:
                    floor_lightgrey = Floor(xpos*TILESIZE,ypos*TILESIZE, 0)
                    self.floors.add(floor_lightgrey)
                if x == 1:
                    wall = Wall(xpos*TILESIZE,ypos*TILESIZE, 1)
                    self.all_sprites.add(wall)
                    self.walls.add(wall)
                if x == 2:
                    floor = Floor(xpos*TILESIZE,ypos*TILESIZE, 2)
                    self.floors.add(floor)

    def quit(self): #Quit
        pygame.quit()
        sys.exit()

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x 
        self.y = y 
        self.vx, self.vy = 0, 0 #Initialise player x and y velocity
        self.image = pygame.Surface((TILESIZE-1, TILESIZE-1)) #Size of 1 tile
        self.image.fill((255,0,255)) #Colour fill
        self.rect = self.image.get_rect() #Box
        self.vx, self.vy = 0, 0
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def get_keys(self):
        self.vx, self.vy = 0, 0 #0 vel by default
        #print(self.rect.x,self.rect.y)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED

        

    def wall_collision_check(self, direction):
        if direction == "x":
            hit = pygame.sprite.spritecollide(self, game.walls, False) #Player collides with walls x?
            if hit:
                if self.vx > 0: #If moving right (x incresing)
                    self.x = hit[0].rect.left - self.rect.width
                if self.vx < 0: #If moving left (x decreasing)
                    self.x = hit[0].rect.right
                self.vx = 0
                self.rect.x = self.x

        if direction == "y":
            hit = pygame.sprite.spritecollide(self, game.walls, False) #Player collides with walls y?
            if hit:
                if self.vy < 0: #If moving up (y incresing)
                    self.y = hit[0].rect.bottom
                if self.vy > 0: #If moving down (y decreasing)
                    self.y = hit[0].rect.top - self.rect.height
                self.vy = 0
                self.rect.y = self.y

    def update(self,dt):
        #4 Directional movement
        self.get_keys()
        self.x += self.vx * game.dt
        self.y += self.vy * game.dt

        #Diagonal movement
        if self.vx != 0 and self.vy != 0: #If moving diagonally
            self.vx *= 0.7071 #Constant (1 over sqr root of 2)
            self.vy *= 0.7071 #Makes diagonal vel stay the same as horizontal/vertical vel

        #Check for wall collisions
        self.rect.x = self.x #Update x pos
        self.wall_collision_check("x") #Is touching wall horizontally?
        self.rect.y = self.y #Update y pos
        self.wall_collision_check("y") #Is touching wall vertically?

        #Check if offscreen
        self.offscreen_check()

    def offscreen_check(self):
        #Check if bottom
        if self.y > HEIGHT - 5:
            game.current_room = room_b
            self.y = -TILESIZE + 6

        #Check if top
        if self.y <= -TILESIZE + 5:
            self.y = HEIGHT - 6

        #Check if right
        if self.x > WIDTH - 5:
            self.x = -TILESIZE + 6
        #Check if left
        if self.x <= -TILESIZE + 5:
            self.x = WIDTH - 6
        
        #temp code
        if game.current_room == room_a:
            print("a")
        if game.current_room == room_b:
            print("b")
        else:
            print("error")
    

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,blockid):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        if blockid == 1:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Floor(pygame.sprite.Sprite):
    def __init__(self,x,y,blockid):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        if blockid == 0: #block_id 1 = Light grey floor tile
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill((100,100,100))
        if blockid == 2: #block_id 2 = dark grey floor tile
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill((50,50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    
#CONSTANTS
WIDTH = 512 #32 tiles wide
HEIGHT = 384 #24 tile high
TILESIZE = 32
FPS = 60
PLAYER_SPEED = 128

#Create the game object
game = Game()
while True:
    game.new()
    game.run()
    
        



