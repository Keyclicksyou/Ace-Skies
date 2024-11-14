import pygame
pygame.init()
import random # for random number generation


# variable for games running state
run = True

gamestate = "playing"

#gamescore holder
gamescore = 0

#player1 lives
lives = 3

#text colours
white = (255, 255, 255)
red = (255, 0, 0)

#game font
gamefont = pygame.font.SysFont('comicsans', 40)

#game window
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Ace Skies")

#icon
invaderIcon = pygame.image.load('invader.ico')
pygame.display.set_icon(invaderIcon)

#images for all the objects
playerimage = pygame.image.load('player.png')
mothershipimage = pygame.image.load('mothership.png')
redbulletimage = pygame.image.load('redbullet.png')
bluebulletimage = pygame.image.load('bluebullet.png')

#bg images
bg1 = pygame.image.load('spacebackground.png')

#game clock
gameclock = pygame.time.Clock()

#invader list
invaderslist = []

#start direction
invaderdirection = "left"

# other invader variable
invaderspeed = 1
invadercount = 0
invadersfiring = False

#create the player class
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.isfiring = False
        self.hitbox = pygame.Rect(self.x, self.y, 100, 60)

    def draw(self, window):
        window.blit(playerimage, (self.x, self.y))


# invader class
class invader(object):
    def __init__(self,x,y,width,height,colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.dead = False
        self.hitbox = pygame.Rect(self.x, self.y, 30, 30)

    def draw(self, window):
        if self.colour== "red":
            invaderimage = pygame.image.load('redinvader.png')
        elif self.colour== "green":
            invaderimage = pygame.image.load('greeninvader.png')
        elif self.colour== "blue":
            invaderimage = pygame.image.load('blueinvader.png')

        window.blit(invaderimage, (self.x, self.y))


# create base class
class base(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.damage = 0
        self.destroyed = False
        self.hitbox = pygame.Rect(self.x, self.y, 100, 50)
        self.baseimage = pygame.image.load('basegreen.png')

    def draw(self, window):
        # check damage levels and update colour
        if self.damage == 0:
            self.baseimage = pygame.image.load('basegreen.png')
        elif self.damage == 2:
            self.baseimage = pygame.image.load('baseorange.png')
        elif self.damage == 4:
            self.baseimage = pygame.image.load('basered.png')

        window.blit(self.baseimage, (self.x, self.y))


#mother ship class
class mothership(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.ismoving = False
        self.hitbox = pygame.Rect(self.x, self.y, 90, 30)

    def draw(self, window):
        window.blit(mothershipimage, (self.x, self.y))


# bullet class
class bullet(object):
    def __init__(self,x,y,width,height,colour,speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed
        self.hitbox = pygame.Rect(self.x, self.y, 20, 50)

    def draw(self, window):
        if self.colour == "red":
            bulletimage = redbulletimage
        elif self.colour == "blue":
            bulletimage = bluebulletimage
        window.blit(bulletimage, (self.x, self.y))

# function to create invader instances
def makeinvaders():
    global invaderslist
    global invadercount
    lastinvaderX = 380
    lastinvaderY = 100
    rowstartX = lastinvaderX
    colour = "red"
    for i in range(1, 19):
        if i == 7:
            lastinvaderY+=60
            lastinvaderX = rowstartX
            colour = "blue"
        elif i == 13:
            lastinvaderY+=60
            lastinvaderX = rowstartX
            colour = "green"
        sinvader = invader(lastinvaderX+60,lastinvaderY,30,30,colour)
        lastinvaderX = sinvader.x
        invaderslist.append(sinvader)
    invadercount = 18

# invader left right function
def moveinvaders():
    global invaderslist
    global invaderspeed
    global invaderdirection
    global gamestate

    if invaderdirection == "left":

        for sinvader in invaderslist:
            sinvader.x -= invaderspeed
            sinvader.hitbox.x = sinvader.x

            #play sound effect
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("invadermoved.wav"), maxtime=1000)

            if sinvader.x == 10:
                invadersdown()
                invaderdirection = "right"

    elif invaderdirection == "right":

        for sinvader in invaderslist:
            sinvader.x += invaderspeed
            sinvader.hitbox.x = sinvader.x
            #play sound
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("invadermoved.wav"), maxtime=1000)

            if sinvader.x == 750:
                invadersdown()
                invaderdirection = "left"

            if sinvader.y >570:
                gamestate = "gameover"

           

# function for invader shots
def makeinvadersshoot():
    global invaderslist
    global invadercount
    global invadersfiring

    if invadersfiring == False:
        choseninvader = random.randint(0, invadercount)

        count = 0
        for sinvader in invaderslist:
            if count == choseninvader:
                bullet2.x = sinvader.x+5
                bullet2.y = sinvader.y+sinvader.height
                invadersfiring = True
            count +=1


#function to move invaders down at each end
def invadersdown():
    global invaderslist
    for sinvader in invaderslist:
        sinvader.y+=20
        sinvader.hitbox.y = sinvader.y


# function to randomly launch mothership
def launchmothership():
    launch = random.randint(1, 150)

    if launch == 75:
        mothership1.ismoving = True

    if mothership1.ismoving == True:
        mothership1.x -= mothership1.speed
        mothership1.hitbox.x = mothership1.x

        #play sound effect
        pygame.mixer.Channel(4).play(pygame.mixer.Sound("mothership.wav"), maxtime=2000)

    if mothership1.x == -90:
        mothership1.x = 800
        mothership1.hitbox.x = mothership1.x
        mothership1.ismoving = False

#create function to move player bullets
def moveplayerbullet():
    if player1.isfiring == True:
        bullet1.y -= bullet1.speed
        bullet1.hitbox.y = bullet1.y

    elif player1.isfiring == False:
        bullet1.x = player1.x+40
        bullet1.hitbox.x = player1.x+40

    if bullet1.y<-100:
        bullet1.x = player1.x+40
        bullet1.y = player1.y
        bullet1.hitbox.x = bullet1.x
        bullet1.hitbox.y = bullet1.y
        player1.isfiring = False

# create function to move invader bullets
def moveinvaderbullet():
    global invadersfiring
    if invadersfiring == True:
        bullet2.y+=bullet2.speed
        bullet2.hitbox.x = bullet2.x
        bullet2.hitbox.y = bullet2.y
    if bullet2.y>650:
        invadersfiring = False

# check collision function
def checkplayerbulletcollision():
    global invadercount
    count = 0

    for sinvader in invaderslist:

        collide = pygame.Rect.colliderect(bullet1.hitbox, sinvader.hitbox)

        if collide:
            #play the scream sound effect
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("invaderkilled.wav"), maxtime=1000)
            del invaderslist[count]
            global gamescore
            gamescore+=10
            bullet1.x = player1.x+40
            bullet1.y = player1.y
            bullet1.hitbox.x = bullet1.x
            bullet1.hitbox.y = bullet1.y
            player1.isfiring = False
            invadercount-=1
            count+=1

        collide = pygame.Rect.colliderect(bullet1.hitbox, mothership1.hitbox)

        if collide:
            #play scream sound
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("invaderkilled.wav"), maxtime=1000)
            gamescore+=40

            bullet1.x = player1.x+40
            bullet1.y = player1.y
            bullet1.hitbox.x = bullet1.x
            bullet1.hitbox.y = bullet1.y

            mothership1.x = 800
            mothership1.y = 10
            mothership1.hitbox.x = mothership1.x
            mothership1.hitbox.y = mothership1.y
            mothership1.ismoving = False
            player1.isfiring = False

# check invader collision
def checkinvaderbulletcollision():
    global invadersfiring

    if base1.destroyed == False:
        collide = pygame.Rect.colliderect(bullet2.hitbox, base1.hitbox)
        if collide:
            #play sound effect
            pygame.mixer.Channel(5).play(pygame.mixer.Sound("explosion.wav"), maxtime=2000)
            base1.damage+=1
            invadersfiring = False
            if base1.damage == 7:
                base1.destroyed = True

    if base2.destroyed == False:
        collide = pygame.Rect.colliderect(bullet2.hitbox, base2.hitbox)
        if collide:
            #play the sound
             pygame.mixer.Channel(5).play(pygame.mixer.Sound("explosion.wav"), maxtime=2000)
             base2.damage+=1
             invadersfiring = False
             if base2.damage == 7:
                 base2.destroyed = True

    if base3.destroyed == False:
        collide = pygame.Rect.colliderect(bullet2.hitbox, base3.hitbox)
        if collide:
            #play the sound
            pygame.mixer.Channel(5).play(pygame.mixer.Sound("explosion.wav"), maxtime=2000)
            base3.damage+=1
            invadersfiring = False
            if base3.damage == 7:
                base3.destroyed = True

    collide = pygame.Rect.colliderect(bullet2.hitbox, player1.hitbox)
    if collide:
        #play the sound effect
        pygame.mixer.Channel(5).play(pygame.mixer.Sound("explosion.wav"), maxtime=2000)
        global lives
        if lives >0:
            lives-=1
            invadersfiring = False
        else:
            global gamestate
            gamestate = "gameover"
    

#check collision between invader the player and the bases
def checkinvadercollision():
    if base1.destroyed == False:
        for sinvader in invaderslist:
            collide = pygame.Rect.colliderect(base1.hitbox, sinvader.hitbox)

            if collide:
                base1.destroyed = True

    if base2.destroyed == False:
        for sinvader in invaderslist:
            collide = pygame.Rect.colliderect(base2.hitbox, sinvader.hitbox)

            if collide:
                base2.destroyed = True

    if base3.destroyed == False:
        for sinvader in invaderslist:
            collide = pygame.Rect.colliderect(base3.hitbox, sinvader.hitbox)

            if collide:
                base3.destroyed = True

# check invader count function
def checkinvadercount():
    global invadercount
    global gamestate
    if invadercount == 0:
        levelreset()

#function to reset game
def gamereset():
    global gamescore
    global lives
    global invadercount
    global invaderslist
    global invadersfiring
    global gamestate

    gamescore = 0
    lives = 3

    base1.destroyed = False
    base1.damage = 0

    base2.destroyed = False
    base2.damage = 0

    base3.destroyed = False
    base3.damage = 0

    player1.x = 0
    player1.y = 520
    player1.hitbox.x = player1.x
    player1.hitbox.y = player1.y
    player1.isfiring = False

    invadercount = 0
    invadersfiring = False
    invaderslist = []

    bullet1.x = player1.x+40
    bullet1.y = player1.y
    bullet1.hitbox.x = bullet1.x
    bullet1.hitbox.y = bullet1.y

    bullet2.x = 0
    bullet2.y = -50
    bullet2.hitbox.x = bullet2.x
    bullet2.hitbox.y = bullet2.y

    mothership1.x = 800
    mothership1.y = 10
    mothership1.ismoving = False

    makeinvaders()

    gamestate = "playing"

def levelreset():
    global invadercount
    global invadersfiring

    player1.isfiring = False

    invadercount = 0
    invadersfiring = False
    invaderslist = []

    bullet1.x = player1.x+40
    bullet1.y = player1.y
    bullet1.hitbox.x = bullet1.x
    bullet1.hitbox.y = bullet1.y

    bullet2.x = 0
    bullet2.y = -50
    bullet2.hitbox.x = bullet2.x
    bullet2.hitbox.y = bullet2.y

    mothership1.x = 800
    mothership1.y = 10
    mothership1.ismoving = False

    makeinvaders()

    gamestate = "playing"

#redraw function
def redrawGameWindow():
    if gamestate == "playing":
      window.blit(bg1, (0,0))
      player1.draw(window)
      bullet1.draw(window)
      bullet2.draw(window)
      for invader in invaderslist:
        invader.draw(window)
      mothership1.draw(window)

      if base1.destroyed == False:
          base1.draw(window)
      if base2.destroyed == False:
          base2.draw(window)
      if base3.destroyed == False:
          base3.draw(window)

      score_text = gamefont.render("Score: " + str(gamescore), 1, white)
      window.blit(score_text, (10, 10))

      lives_text = gamefont.render("Lives: " + str(lives), 1, red)
      window.blit(lives_text, (680, 10))
    elif gamestate == "gameover":
        gameover_text = gamefont.render("Game over - Press Enter to restart", 1, white)
        window.blit(gameover_text, (150, 300))
    pygame.display.update()

     
#create instances and setup function running to start game
player1 = player(0,520, 100,60)
bullet1 = bullet(player1.x+40, player1.y, 20,50,"red",5)
mothership1 = mothership(800,10, 90,30)
base1 = base(80,450, 100,50)
base2 = base(350,450, 100,50)
base3 = base(620,450, 100,50)
bullet2 = bullet(0,-50, 20,50,"blue",5)
makeinvaders()

# main game loop
while run:
    gameclock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if gamestate == "playing":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            player1.isfiring = True
            #play sound
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("shoot.wav"), maxtime=100)

        if keys[pygame.K_LEFT] and player1.x >0:
            player1.x -= player1.speed
            player1.hitbox.x = player1.x

        elif keys[pygame.K_RIGHT] and player1.x < 8000 - player1.width:
            player1.x += player1.speed
            player1.hitbox.x = player1.x

        moveinvaders()
        launchmothership()
        moveplayerbullet()
        checkplayerbulletcollision()
        makeinvadersshoot()
        moveinvaderbullet()
        checkinvaderbulletcollision()
        checkinvadercollision()
        checkinvadercount()

    elif gamestate == "gameover":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            gamereset()

    redrawGameWindow()

pygame.quit()
