import pygame
pygame.init()

WIDTH = 1024 #32 tiles wide
HEIGHT = 768 #24 tile high
TILESIZE = 32
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

map = [[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

class Player(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos,xvel,yvel):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.xvel = xvel
        self.yvel = yvel
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((255,0,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.xpos, self.ypos)
    
    def up(self):
        self.ypos -= self.yvel
        self.rect.topleft = (self.xpos, self.ypos)
    def left(self):
        self.xpos -= self.xvel
        self.rect.topleft = (self.xpos, self.ypos)
    def down(self):
        self.ypos += self.yvel
        self.rect.topleft = (self.xpos, self.ypos)
    def right(self):
        self.xpos += self.xvel
        self.rect.topleft = (self.xpos, self.ypos)

class Block(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos):
        pygame.sprite.Sprite.__init__(self)
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.xpos, self.ypos)

#All sprites group
all_sprites = pygame.sprite.Group()
#Player
player = Player(0,0,32,32)
all_sprites.add(player)

running = True
#Game loop
while running:
    #Loop runs at FPS specified
    clock.tick(FPS)
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.up()
            if event.key == pygame.K_a:
                player.left()
            if event.key == pygame.K_s:
                player.down()
            if event.key == pygame.K_d:
                player.right()
                
        
    #Walls
    for ypos, y in enumerate(map):
        for xpos, x in enumerate (y):
            if x == 0:
                wall = Block(xpos*TILESIZE,ypos*TILESIZE)
                all_sprites.add(wall)
        
    #Draw background
    screen.fill((0,0,0))

    #Draw Grid (---temporary---)
    for i in range (0, WIDTH, TILESIZE):
        pygame.draw.line(screen,(50,50,50), (i,0), (i,HEIGHT))
    for i in range (0, HEIGHT, TILESIZE):
        pygame.draw.line(screen,(50,50,50), (0,i), (WIDTH,i))

    #Update
    all_sprites.update()
    
    #Draw all sprites
    all_sprites.draw(screen)

    #Flip screen
    pygame.display.flip()
        



